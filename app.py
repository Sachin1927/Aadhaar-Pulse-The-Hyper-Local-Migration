import streamlit as st
import polars as pl
import plotly.express as px
import plotly.figure_factory as ff
import os
import glob
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np

# =========================================================
# 0. CONFIGURATION & STYLING
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@dataclass(frozen=True)
class ProjectConfig:
    # PATHS
    ENROLMENT_ROOT: str = os.path.join(BASE_DIR, "api_data_aadhar_enrolment")
    UPDATE_ROOT: str    = os.path.join(BASE_DIR, "api_data_aadhar_demographic")
    
    # COLUMNS
    COL_STATE: str = "state"
    COL_DISTRICT: str = "district"
    COL_DATE: str = "date"
    COL_BIRTH_PROXY: str = "age_0_5"
    COL_UPDATE_MAIN: str = "demo_age"
    COL_UPDATE_ALT: str  = "demo_age_5_17"
    COL_UPDATE_ADULT: str = "demo_age_17_"
    
    COLOR_SCALE: str = "Reds"

def inject_custom_css():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; }
        .descriptive-box {
            background-color: #e3f2fd; border-left: 5px solid #2196f3;
            padding: 15px; border-radius: 5px; color: #0d47a1; margin-bottom: 20px;
        }
        .prescriptive-box {
            background-color: #f3e5f5; border-left: 5px solid #8e24aa;
            padding: 15px; border-radius: 5px; color: #4a148c; margin-bottom: 20px;
            animation: fadeIn 1s;
        }
        @keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
        </style>
    """, unsafe_allow_html=True)

# =========================================================
# 1. DATA LOADER (FIXED: AGGREGATION ON PARQUET)
# =========================================================
class DataLoader:
    def __init__(self, config: ProjectConfig):
        self.config = config

    def _get_csv_files(self, root: str) -> List[str]:
        if not os.path.exists(root): return []
        return glob.glob(os.path.join(root, "**", "*.csv"), recursive=True)

    @st.cache_data(show_spinner=False)
    def load_enrolment(_self) -> pl.DataFrame:
        # OPTION A: Try Parquet
        if os.path.exists("enrolment_data.parquet"):
            try:
                df = pl.read_parquet("enrolment_data.parquet")
                
                # --- THE FIX IS HERE ---
                # We must aggregate the raw parquet data just like we did for CSVs
                return (
                    df.group_by([_self.config.COL_STATE, _self.config.COL_DISTRICT])
                    .agg(pl.col(_self.config.COL_BIRTH_PROXY).sum().alias("new_births"))
                )
            except Exception:
                st.warning("⚠️ Parquet file failed. Falling back to CSVs...")

        # OPTION B: Fallback to CSV
        files = _self._get_csv_files(_self.config.ENROLMENT_ROOT)
        if not files: return pl.DataFrame()
        return (
            pl.scan_csv(files, ignore_errors=True)
            .group_by([_self.config.COL_STATE, _self.config.COL_DISTRICT])
            .agg(pl.col(_self.config.COL_BIRTH_PROXY).sum().alias("new_births"))
            .collect()
        )

    @st.cache_data(show_spinner=False)
    def load_demographic_time_series(_self) -> pl.DataFrame:
        # OPTION A: Try Parquet
        if os.path.exists("demographic_data.parquet"):
            try:
                df = pl.read_parquet("demographic_data.parquet")
                # Force Date Format again just to be safe
                df = df.with_columns(pl.col("date").cast(pl.Date, strict=False))
                
                cols = df.columns
                if _self.config.COL_UPDATE_MAIN in cols: target = _self.config.COL_UPDATE_MAIN
                elif _self.config.COL_UPDATE_ALT in cols: target = _self.config.COL_UPDATE_ALT
                else: return pl.DataFrame()
                
                return (
                    df.with_columns(pl.col(target).alias("base_update"))
                    .select([_self.config.COL_STATE, _self.config.COL_DISTRICT, _self.config.COL_DATE, "base_update", _self.config.COL_UPDATE_ADULT])
                    .with_columns((pl.col("base_update") + pl.col(_self.config.COL_UPDATE_ADULT)).alias("migrant_inflow"))
                )
            except Exception:
                st.warning("⚠️ Parquet file failed. Falling back to CSVs...")

        # OPTION B: Fallback to CSV
        files = _self._get_csv_files(_self.config.UPDATE_ROOT)
        if not files: return pl.DataFrame()
        
        q = pl.scan_csv(files, ignore_errors=True, try_parse_dates=True)
        q = q.with_columns(pl.col("date").cast(pl.Date, strict=False))
        
        cols = q.collect_schema().names()
        if _self.config.COL_UPDATE_MAIN in cols: target = _self.config.COL_UPDATE_MAIN
        elif _self.config.COL_UPDATE_ALT in cols: target = _self.config.COL_UPDATE_ALT
        else: return pl.DataFrame()
        
        return (
            q.with_columns(pl.col(target).alias("base_update"))
            .select([_self.config.COL_STATE, _self.config.COL_DISTRICT, _self.config.COL_DATE, "base_update", _self.config.COL_UPDATE_ADULT])
            .with_columns((pl.col("base_update") + pl.col(_self.config.COL_UPDATE_ADULT)).alias("migrant_inflow"))
            .collect()
        )

# =========================================================
# 2. ANALYTICS ENGINE
# =========================================================
class AnalyticsEngine:
    @staticmethod
    def calculate_mli(births: pl.DataFrame, updates: pl.DataFrame) -> pl.DataFrame:
        births = births.with_columns(pl.col("state").str.strip_chars().str.to_titlecase())
        
        # Aggregate static view
        updates_static = updates.group_by(["state", "district"]).agg([
            pl.col("migrant_inflow").sum(),
            pl.col("base_update").sum().alias("child_updates"), 
            pl.col("demo_age_17_").sum().alias("adult_updates") 
        ])
        updates_static = updates_static.with_columns(pl.col("state").str.strip_chars().str.to_titlecase())
        
        df = births.join(updates_static, on=["state", "district"], how="inner")
        
        THRESHOLD = 500 # Adding threshold to define migration pressure
        df = df.with_columns(
            pl.when(pl.col("migrant_inflow") < THRESHOLD).then(0.0)
            .otherwise(pl.col("migrant_inflow") / (pl.col("new_births") + 1)).alias("MLI")
        )
        return df

    @staticmethod
    def generate_descriptive_summary(df: pl.DataFrame, region_name: str, is_district: bool = False) -> str:
        total_inflow = df['migrant_inflow'].sum()
        avg_pressure = df['MLI'].mean()
        
        if is_district:
            # District Specific Text
            status = "CRITICAL" if avg_pressure > 3.0 else ("WARNING" if avg_pressure > 1.5 else "STABLE")
            return (f"**District Report:** {region_name} has received **{total_inflow:,.0f}** updates. "
                    f"The local infrastructure pressure score is **{avg_pressure:.2f}** ({status}).")
        else:
            # State Specific Text
            high_risk = df.filter(pl.col('MLI') > 3.0).height
            return (f"**State Report:** {region_name} has recorded **{total_inflow:,.0f}** total updates. "
                    f"Currently, **{high_risk} districts** are flagged as high-stress zones.")

    @staticmethod
    def generate_prescriptive_advice(df: pl.DataFrame, region_name: str, forecast_vol: int, is_district: bool = False) -> str:
        advice = f"**Strategic Plan ({region_name}):** Predicted influx: +{forecast_vol:,.0f} migrants.\n\n"
        
        if is_district:
            # Advice for a District Collector
            mli = df['MLI'][0]
            if mli > 3.0:
                advice += (f"1.  **Action:** Open 2 temporary Aadhaar Seva Kendras near industrial zones.\n"
                           f"2.  **Resource:** Alert Municipal Corporation to increase water tanker frequency by 15%.\n")
            elif mli > 1.5:
                 advice += "1.  **Action:** Conduct spot-checks at rental housing clusters.\n"
            else:
                 advice += "1.  **Action:** Routine monitoring. No specific intervention needed.\n"
        else:
            # Advice for a State Minister
            critical = df.filter(pl.col("MLI") > 3.0).height
            advice += (f"1.  **Supply Chain:** Increase Ration allocations for the {critical} critical districts.\n"
                       f"2.  **Long Term:** Review urban expansion budget for Q3.")
            
        return advice

class ForecastingEngine:
    @staticmethod
    def generate_forecast(df: pl.DataFrame, state: str, district: Optional[str] = None) -> pl.DataFrame:
        # Filter State
        data = df.filter(pl.col("state").str.strip_chars().str.to_titlecase() == state)
        
        # If District selected, filter further
        if district and district != "All Districts":
            data = data.filter(pl.col("district") == district)
            
        if data.is_empty(): return pl.DataFrame()
        
        ts_data = (
            data.group_by(pl.col("date").dt.truncate("1mo"))
            .agg(pl.col("migrant_inflow").sum())
            .sort("date")
        )
        
        if ts_data.height < 2: return pl.DataFrame()

        pdf = ts_data.to_pandas()
        pdf['type'] = 'Historical'
        
        last_val = pdf['migrant_inflow'].iloc[-1]
        avg_growth = pdf['migrant_inflow'].pct_change().mean()
        last_date = pdf['date'].iloc[-1]
        
        future_data = []
        current_val = last_val
        growth_factor = max(min(avg_growth, 0.2), -0.2) 
        
        for i in range(1, 4):
            next_date = last_date + timedelta(days=30*i)
            current_val = current_val * (1 + growth_factor)
            future_data.append({
                "date": next_date,
                "migrant_inflow": int(current_val),
                "type": "Predicted"
            })
            
        hist_pl = pl.from_pandas(pdf).with_columns(pl.col("date").cast(pl.Date))
        future_pl = pl.from_dicts(future_data).with_columns(pl.col("date").cast(pl.Date))
        return pl.concat([hist_pl, future_pl])

# =========================================================
# 3. UI DASHBOARD
# =========================================================
def run_app():
    st.set_page_config(page_title="Aadhaar-Pulse", layout="wide", page_icon="📈")
    inject_custom_css()

    c1, c2 = st.columns([4, 1])
    with c1:
        st.title("🇮🇳 Aadhaar-Pulse: Migration Observatory")
        st.markdown("**System Status:** Online | **Mode:** District-Level Drilldown")

    cfg = ProjectConfig()
    loader = DataLoader(cfg)
    
    with st.spinner("Loading Data..."):
        try:
            births = loader.load_enrolment()
            updates_ts = loader.load_demographic_time_series()
        except Exception as e:
            st.error(f"Data Load Error: {e}")
            st.stop()
            
    if births.is_empty() or updates_ts.is_empty():
        st.warning("⚠️ Data missing.")
        st.stop()
    
    # Run Static Analysis (Full State Data)
    df_full = AnalyticsEngine.calculate_mli(births, updates_ts)

    # --- SIDEBAR CONTROLS ---
    st.sidebar.title("🎛️ Control Panel")
    
    # --- NEW: SYSTEM MONITOR ---
    if os.path.exists("enrolment_data.parquet"):
        st.sidebar.success("⚡ System: High-Performance (Parquet)")
    else:
        st.sidebar.warning("🐢 System: Legacy Mode (CSV Fallback)")
    
    # 1. Select State
    states = sorted(df_full["state"].unique().to_list())
    selected_state = st.sidebar.selectbox("Select State", states)
    
    # Filter to State
    state_df = df_full.filter(pl.col("state") == selected_state)
    
    # 2. Select District
    districts = sorted(state_df["district"].unique().to_list())
    selected_district = st.sidebar.selectbox("Select District", ["All Districts"] + districts)
    
    # Decide which DataFrame to show (State vs District)
    if selected_district != "All Districts":
        view_df = state_df.filter(pl.col("district") == selected_district)
        is_district_view = True
        region_label = selected_district
    else:
        view_df = state_df
        is_district_view = False
        region_label = selected_state

# --- PART 1: DESCRIPTIVE ANALYTICS ---
    st.subheader(f" Descriptive Analytics ({region_label})")
    
    # CALCULATE BASELINES (The Fix)
    state_avg_mli = state_df['MLI'].mean()
    current_mli = view_df['MLI'].mean() # For district, this is just the value
    
    # Calculate the "Multiplier" (e.g., 3.2x higher)
    if state_avg_mli > 0:
        multiplier = current_mli / state_avg_mli
        comparison_text = f"{multiplier:.1f}x vs State Avg"
    else:
        comparison_text = "N/A"

    # Dynamic Summary Text
    summary_text = AnalyticsEngine.generate_descriptive_summary(view_df, region_label, is_district_view)
    st.markdown(f'<div class="descriptive-box">{summary_text}</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Inflow", f"{int(view_df['migrant_inflow'].sum()):,}")
    m2.metric("Natural Growth", f"{int(view_df['new_births'].sum()):,}")
    
    # UPDATED METRIC: Shows the comparison
    m3.metric(
        "Avg MLI Score", 
        f"{current_mli:.2f}",
        delta=comparison_text, 
        delta_color="inverse" # Red if higher (bad), Green if lower (good)
    )
    
    if is_district_view:
        status = "CRITICAL" if current_mli > 3 else "STABLE"
        m4.metric("Risk Status", status, help="Based on threshold > 3.0")
    else:
        m4.metric("Critical Districts", f"{view_df.filter(pl.col('MLI') > 3.0).height}", delta="Alerts")
    # --- VISUALIZATIONS ---
    col_viz1, col_viz2 = st.columns(2)
    
    # VIZ 1: Smart Context Aware Chart
    with col_viz1:
        if is_district_view:
            # Show "Where do I stand?" on State Bell Curve
            st.markdown(f"##### 📍 Where does {region_label} stand?")
            try:
                state_scores = state_df['MLI'].to_numpy()
                my_score = view_df['MLI'][0]
                state_scores = [float(x) for x in state_scores if x > 0.1]
                
                if len(state_scores) > 1:
                    fig_dist = ff.create_distplot([state_scores], ['State Distribution'], bin_size=0.2, show_rug=False, show_hist=False, colors=['#cfd8dc'])
                    # Add Red Line for THIS District
                    fig_dist.add_vline(x=my_score, line_width=3, line_dash="dash", line_color="red", annotation_text="YOU", annotation_position="top right")
                    fig_dist.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig_dist, use_container_width=True)
            except:
                st.info("Not enough data for distribution.")
        else:
            # Show State Heatmap
            st.markdown("##### 🗺️ District Pressure Heatmap")
            chart_df = view_df.filter(pl.col("MLI") > 0).sort("MLI", descending=True).head(15).to_pandas()
            if not chart_df.empty:
                fig = px.bar(chart_df, x="district", y="MLI", color="MLI", color_continuous_scale=cfg.COLOR_SCALE)
                st.plotly_chart(fig, use_container_width=True)

    # VIZ 2: Demographics
    with col_viz2:
        st.markdown(f"##### 👥 Demographics of {region_label}")
        # For district view, simple pie chart is better. For State, stacked bar.
        if is_district_view:
            c_up = view_df['child_updates'][0]
            a_up = view_df['adult_updates'][0]
            fig_pie = px.pie(names=['Children (5-17)', 'Adults (18+)'], values=[c_up, a_up], hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            stack_df = view_df.sort("migrant_inflow", descending=True).head(10).to_pandas()
            fig_stack = px.bar(stack_df, x="district", y=["child_updates", "adult_updates"], labels={"value":"Updates"})
            st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown("---")

    # --- PART 2: PRESCRIPTIVE ANALYTICS ---
    st.subheader(f" Prescriptive Analytics ({region_label})")
    
    show_forecast = st.toggle(" Activate AI Prescriptive Model", value=False)
    
    if show_forecast:
        with st.spinner("Running Predictive Models..."):
            # Pass district to forecast engine if selected
            dist_filter = region_label if is_district_view else "All Districts"
            forecast_df = ForecastingEngine.generate_forecast(updates_ts, selected_state, dist_filter)
            
            if not forecast_df.is_empty():
                pred_vol = forecast_df.filter(pl.col("type")=="Predicted")['migrant_inflow'].sum()
                
                # Context-Aware Advice
                advice = AnalyticsEngine.generate_prescriptive_advice(view_df, region_label, pred_vol, is_district_view)
                st.markdown(f'<div class="prescriptive-box">{advice}</div>', unsafe_allow_html=True)
                
                st.markdown("##### 3-Month Trajectory")
                fig = px.line(
                    forecast_df.to_pandas(), x="date", y="migrant_inflow", color="type",
                    markers=True, line_dash="type",
                    color_discrete_map={"Historical": "#1f77b4", "Predicted": "#ff7f0e"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Insufficient historical data for prediction.")

if __name__ == "__main__":
    run_app()