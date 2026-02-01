# 🇮🇳 Aadhaar-Pulse: Inter-District Migration Observatory
### *Hyper-local Decision Support System (DSS) for Administrative Resource Allocation*

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Polars](https://img.shields.io/badge/Polars-⚡_Fast_Engine-fccb1c?style=for-the-badge&logo=polars&logoColor=black)](https://pola.rs)


---

## 📋 Abstract

**Aadhaar-Pulse** is a privacy-preserving data analytics platform designed for the UIDAI Hackathon. It addresses the critical information gap regarding real-time internal migration in India. By leveraging administrative footprints—specifically comparing natural demographic growth against high-frequency address updates—the system calculates a **Migrant Load Index (MLI)**. This enables District Administrators to proactively identify infrastructure stress points and optimize resource allocation (water, ration, housing) before crises occur.

---

## 🚨 The Problem Statement

Census data, collected decadally, is insufficient for tracking modern, dynamic migration patterns. This data lag creates a "blind spot" for administrators, leading to:

1.  **Reactive Governance:** Resources are allocated only after shortages (e.g., water scarcity in industrial hubs) become critical.
2.  **Infrastructure Strain:** Unexpected population surges overwhelm local services in specific districts.
3.  **Privacy Dilemma:** Tracking individual movement to understand migration flow violates the Aadhaar Act's privacy mandates.

---

## 💡 The Solution

Aadhaar-Pulse utilizes anonymized aggregate data to create live proxy indicators for migration pressure. It shifts the focus from *"Where did they come from?"* (which is privacy-intrusive) to ***"Where are they going, and what is the impact?"* (which is actionable governance).**

### Key Capabilities:
* **Descriptive Analytics:** Real-time assessment of current migration pressure at both State and District levels.
* **Prescriptive Analytics:** AI-driven actionable recommendations based on severity and forecasted trends.
* **Context-Aware Visualization:** Dynamic charts that adapt based on the user's drill-down level (e.g., State Heatmaps vs. District Comparative Bell Curves).



</div>

<br />

<img width="1728" height="2464" alt="aadhaar_pulse_dashboard" src="https://github.com/user-attachments/assets/11ca1383-bcdb-4340-8c40-89407cef9aa8" />



  <p><em>Figure: Full Dashboard View demonstrating District-Level Drilldown, Descriptive Analytics, and AI-Driven Prescriptive Forecasting.</em></p>
</div>

---

## ⚙️ Methodology: The Migrant Load Index (MLI)

We quantify infrastructure pressure using a custom metric, the **Migrant Load Index (MLI)**. It is a ratio of administrative inward flow relative to organic natural growth.

<div align="center">

### $MLI = \frac{\text{Inward Administrative Flow (Updates)}}{\text{Natural Growth (Child Enrolments 0-5y)} + 1}$

</div>

* **Numerator (Inflow Signal):** Sum of demographic updates across age brackets (proxies for active migration).
* **Denominator (Base Signal):** New child enrolments (aged 0-5), representing natural organic population growth.
* **Noise Filtering:** A magnitude threshold applies; districts with insignificant absolute update volumes are filtered to prevent statistical skew.

| MLI Score | Risk Status | Interpretation |
| :--- | :--- | :--- |
| **< 1.5** | 🟢 STABLE | Organic growth. Maintain standard monitoring. |
| **1.5 - 3.0** | 🟠 WARNING | Elevated turnover. Monitor housing and labor sectors. |
| **> 3.0** | 🔴 CRITICAL | Influx significantly exceeds natural base. Immediate intervention required. |

---

## 🛠️ Technical Architecture & Stack

The application is built for performance and scalability, utilizing modern data engineering tools.

| Component | Technology | Key Rationale |
| :--- | :--- | :--- |
| **Data Processing Engine** | **Polars (Rust)** | Chosen over Pandas for its blazingly fast, multi-threaded performance on large datasets and lazy evaluation capabilities. |
| **Frontend Interface** | **Streamlit** | Enables rapid development of interactive, highly customized web applications with Python. |
| **Visualization Layer** | **Plotly Express / FF** | Provides interactive, publication-quality charts (Heatmaps, Bell Curves, Line Charts). |
| **Predictive Modeling** | **NumPy / SciPy** | Used for statistical analysis and time-series linear growth projections. |
| **Data Ingestion** | **Recursive Globbing** | Robust file handling that automatically scans complex, nested directory structures for partitioned data files. |

---

## 🚀 Installation & Setup Guide

Follow these steps to deploy the application locally.

### Prerequisites
* Python 3.9 or higher

### Step 1: Clone Repository

git clone [https://github.com/Sachin1927/aadhaar-pulse.git](https://github.com/Sachin1927/aadhaar-pulse.git)
cd aadhaar-pulse

### Step 2: Install Dependencies
It is recommended to use a virtual environment.
pip install -r requirements.txt

### Step 3: Data Configuration
Ensure the raw data folders are present in the project root directory. The system will automatically scan them recursively.

/api_data_aadhaar_enrolment/

/api_data_aadhaar_demographic/

### Step 4: Launch Application
streamlit run app.py

The dashboard will open automatically in your default web browser at http://localhost:8501.

### 🔮 Future Roadmap
```bash
Geospatial Integration: Mapping ward-level data onto GIS layers using Mapbox for precise hotspot localization.

GenAI Reporting: Integrating LLMs (e.g., Llama-2) to auto-generate comprehensive PDF policy briefs for ministerial review.

Inter-Departmental API: Exposing live MLI scores via REST endpoints for integration with PDS (Ration) and Urban Planning systems.
