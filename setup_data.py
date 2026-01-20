import polars as pl
import os
import glob

# CONFIG
ENROL_PATH = "api_data_aadhar_enrolment"
UPDATE_PATH = "api_data_aadhar_demographic"

def safe_convert(source_folder, output_filename, is_update_data=False):
    print(f"🔄 Scanning {source_folder}...")
    files = glob.glob(os.path.join(source_folder, "**", "*.csv"), recursive=True)
    
    if not files:
        print(f"❌ No files in {source_folder}")
        return

    print(f"Found {len(files)} CSVs. Cleaning & Converting...")
    
    try:
        # 1. Scan the CSVs
        q = pl.scan_csv(files, ignore_errors=True, try_parse_dates=True)
        
        # 2. FORCE FIX THE DATE COLUMN (This prevents the crash!)
        # We explicitly cast 'date' to pl.Date (YYYY-MM-DD) so there are no time/precision errors.
        if is_update_data:
            q = q.with_columns(pl.col("date").cast(pl.Date, strict=False))
            
        # 3. Collect and Write
        df = q.collect()
        df.write_parquet(output_filename, compression="zstd")
        
        print(f"✅ Success! Saved safe file: {output_filename}")
        
    except Exception as e:
        print(f"❌ Conversion Failed: {e}")

# Run Conversion
if __name__ == "__main__":
    # Enrolment data usually doesn't have a date column, but we run it anyway
    safe_convert(ENROL_PATH, "enrolment_data.parquet", is_update_data=False)
    
    # Update data definitely has a date column, so we apply the fix
    safe_convert(UPDATE_PATH, "demographic_data.parquet", is_update_data=True)