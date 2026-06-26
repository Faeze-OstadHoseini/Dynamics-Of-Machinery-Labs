import pandas as pd
import os

# ============================
# Raw Experimental Data (Input Parameters Only)
# ============================
raw_data = {
    "omega(rpm)": [20, 24, 28, 33, 35],
    "omega(rad/s)": [2.094395102, 2.513274123, 2.932153143, 3.455751919, 3.665191429],
    "Delta_x(m)": [0.05, 0.062, 0.075, 0.095, 0.1],
    "v_rel(m/s)": [2.35619449, 2.280188216, 2.199114858, 2.046168899, 2.061670179],
    "a_coriolis(m/s^2)": [9.869604401, 11.46147608, 12.89628308, 14.1421042, 15.11283174],
    "theta_exp(rad)": [0.193621993, 0.238509252, 0.286051442, 0.356620136, 0.37372682],
    "theta_theo(rad)": [0.195792037, 0.233652523, 0.270843093, 0.316264908, 0.334073369],
    "Error(%)": [1.108341409, 2.078611829, 5.615188068, 12.75994487, 11.86968334]
}

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
output_file = os.path.join(data_dir, "coriolis_raw_data.xlsx")
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
print("  - omega(rpm): Rotational speed")
print("  - omega(rad/s): Rotational speed (converted)")
print("  - Delta_x(m): Displacement of mass")
print("  - v_rel(m/s): Relative velocity")
print("  - a_coriolis(m/s^2): Coriolis acceleration")
print("  - theta_exp(rad): Experimental angle")
print("  - theta_theo(rad): Theoretical angle")
print("  - Error(%): Percentage error")
print("\nFirst 5 rows:")
print(df_raw.to_string(index=False))
print("\n" + "=" * 70)

# ============================
# Data Statistics
# ============================
print("\nData Statistics:")
print("-" * 50)
print(f"Omega range: {df_raw['omega(rpm)'].min()} to {df_raw['omega(rpm)'].max()} rpm")
print(f"Delta_x range: {df_raw['Delta_x(m)'].min()} to {df_raw['Delta_x(m)'].max()} m")
print(f"v_rel range: {df_raw['v_rel(m/s)'].min():.3f} to {df_raw['v_rel(m/s)'].max():.3f} m/s")
print(f"a_coriolis range: {df_raw['a_coriolis(m/s^2)'].min():.3f} to {df_raw['a_coriolis(m/s^2)'].max():.3f} m/s^2")
print(f"Error range: {df_raw['Error(%)'].min():.2f}% to {df_raw['Error(%)'].max():.2f}%")
print("=" * 70)