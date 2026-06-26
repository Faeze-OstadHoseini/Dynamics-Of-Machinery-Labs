import pandas as pd
import os

# ============================
# Raw Experimental Data (Input Parameters Only - No Calculations)
# ============================
raw_data = {
    "state": ["a", "b", "c", "d", "e", "f"],
    "m(Kg)": [0.94, 0.94, 1.143873598, 1.143873598, 1.347747197, 1.347747197],
    "y1(mm)": [33, 55, 29, 42, 15, 28],
    "y2(mm)": [23, 42, 15, 30, 5, 19],
    "x(mm)": [11, 12.5, 12.3, 13, 18, 13],
    "Td(sec)": [0.456705489, 0.51898351, 0.510679774, 0.53974285, 0.747336255, 0.53974285],
    "k": [203.125, None, None, None, None, None],
    "v(mm/s)": [24.08554368, None, None, None, None, None]
}

# ============================
# Note: The following parameters are CALCULATED in the analysis script:
# - zeta (damping ratio)
# - omega_d_exp (experimental damped frequency)
# - omega_n_exp (experimental natural frequency)
# - omega_n_theo (theoretical natural frequency)
# - Error(%)
# ============================

# ============================
# Convert to DataFrame
# ============================
df_raw = pd.DataFrame(raw_data)

# ============================
# Get the directory where this script is located
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================
# Create data directory (relative to script location)
# ============================
data_dir = os.path.join(script_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# ============================
# Save to Excel in data folder
# ============================
output_file = os.path.join(data_dir, "linear_vibration_raw_data.xlsx")
df_raw.to_excel(output_file, index=False)

# ============================
# Print Summary
# ============================
print("=" * 70)
print("Raw Data File Created Successfully")
print("=" * 70)
print(f"\nFile saved: {output_file}")
print(f"Total data points: {len(df_raw)}")
print("\nRAW INPUT PARAMETERS (No calculations included):")
print("  - state: Test condition label")
print("  - m(Kg): Mass of the system")
print("  - y1(mm): Initial displacement")
print("  - y2(mm): Final displacement")
print("  - x(mm): Displacement amplitude")
print("  - Td(sec): Damped period (measured)")
print("  - k: Spring stiffness (only for state a)")
print("  - v(mm/s): Velocity (only for state a)")
print("\nThe following parameters will be CALCULATED in 02_analyze_visualize.py:")
print("  - zeta: Damping ratio")
print("  - omega_d_exp: Experimental damped frequency")
print("  - omega_n_exp: Experimental natural frequency")
print("  - omega_n_theo: Theoretical natural frequency")
print("  - Error(%): Percentage error")
print("\nFirst 5 rows (RAW DATA):")
print(df_raw.head().to_string(index=False))
print("\n" + "=" * 70)

# ============================
# Data Statistics (Raw Data Only)
# ============================
print("\nRaw Data Statistics:")
print("-" * 50)
print(f"Mass range: {df_raw['m(Kg)'].min()} to {df_raw['m(Kg)'].max()} kg")
print(f"Displacement range: {df_raw['x(mm)'].min()} to {df_raw['x(mm)'].max()} mm")
print(f"Damped period range: {df_raw['Td(sec)'].min():.4f} to {df_raw['Td(sec)'].max():.4f} s")
print(f"Missing k data: {df_raw['k'].isna().sum()} states")
print(f"Missing v data: {df_raw['v(mm/s)'].isna().sum()} states")
print("=" * 70)