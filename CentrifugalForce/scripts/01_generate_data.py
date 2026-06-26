# ============================
# 01_generate_data.py
# Raw Data Generation for Centrifugal Force Experiment
# ============================

import pandas as pd
import os

# ============================
# Raw Experimental Data (Input Parameters Only)
# ============================
raw_data = {
    "ma_g(N)": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    "mb_g(N)": [0.3, 0.6, 0.3, 0.6, 0.3, 0.6, 0.3, 0.6, 0.3, 0.6, 0.3, 0.6],
    "r(m)": [0.1, 0.1, 0.1, 0.1, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18],
    "a(m)": [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    "b(m)": [0.07, 0.07, 0.05, 0.05, 0.07, 0.07, 0.05, 0.05, 0.07, 0.07, 0.05, 0.05],
    "omega1_exp(rpm)": [167, 238, 135, 170, 98, 130, 78, 102, 119, 162, 90, 126],
    "omega2_exp(rpm)": [48, 110, None, 53, 40, 63, None, 45, 30, 65, None, 38]
}

# ============================
# Convert to DataFrame
# ============================
df_raw = pd.DataFrame(raw_data)

# ============================
# Create data directory (relative to script location)
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# ============================
# Save to Excel in data folder
# ============================
output_file = os.path.join(data_dir, "centrifugal_force_raw_data.xlsx")
df_raw.to_excel(output_file, index=False)

# ============================
# Print Summary
# ============================
print("=" * 70)
print("Raw Data File Created Successfully")
print("=" * 70)
print(f"\nFile saved: {output_file}")
print(f"Total data points: {len(df_raw)}")
print("\nInput parameters included:")
print("  - ma_g(N): Mass A weight")
print("  - mb_g(N): Mass B weight")
print("  - r(m): Radius of rotation")
print("  - a(m): Distance from center to mass A")
print("  - b(m): Distance from center to mass B")
print("  - omega1_exp(rpm): Experimental speed (case 1)")
print("  - omega2_exp(rpm): Experimental speed (case 2)")
print("\nFirst 5 rows:")
print(df_raw.head().to_string(index=False))
print("\n" + "=" * 70)

# ============================
# Data Statistics
# ============================
print("\nData Statistics:")
print("-" * 50)
print(f"ma_g(N): {df_raw['ma_g(N)'].unique()} (constant)")
print(f"mb_g(N): {df_raw['mb_g(N)'].unique()} (variable)")
print(f"r(m): {df_raw['r(m)'].unique()} (variable)")
print(f"b(m): {df_raw['b(m)'].unique()} (variable)")
print(f"\nMissing values in omega2_exp: {df_raw['omega2_exp(rpm)'].isna().sum()} rows")
print("=" * 70)