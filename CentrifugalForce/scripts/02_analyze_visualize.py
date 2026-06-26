# ============================
# 02_analyze_visualize.py
# Analysis and Visualization for Centrifugal Force Experiment
# ============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ============================
# Constants
# ============================
g = 9.81  # Gravitational acceleration (m/s^2)

# ============================
# Get the directory where this script is located
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================
# Define relative paths (script is in scripts/ folder)
# ============================
data_file = os.path.join(script_dir, "..", "data", "centrifugal_force_raw_data.xlsx")
output_dir = os.path.join(script_dir, "..", "outputs")
plots_dir = os.path.join(output_dir, "plots")

# ============================
# Create output directories
# ============================
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# ============================
# Load Raw Data
# ============================
df = pd.read_excel(data_file)

# ============================
# Calculate Derived Parameters
# ============================
# Convert RPM to rad/s for omega1
df["omega1_exp(rad/s)"] = df["omega1_exp(rpm)"] * (2 * np.pi / 60)

# Convert RPM to rad/s for omega2 (handle None values)
df["omega2_exp(rad/s)"] = df["omega2_exp(rpm)"].apply(
    lambda x: x * (2 * np.pi / 60) if pd.notna(x) else None
)

# Calculate (b/a)*mb
df["(b/a)mb"] = (df["b(m)"] / df["a(m)"]) * df["mb_g(N)"]

# Calculate 1/r
df["1/r"] = 1 / df["r(m)"]

# Calculate 1/ma
df["1/ma"] = 1 / df["ma_g(N)"]

# ============================
# Calculate Theoretical Values
# ============================
# Theoretical omega1: sqrt(((b/a)*mb*g) / (r*ma*g)) = sqrt((b/a)*mb / (r*ma))
df["omega1_theo(rad/s)"] = np.sqrt(
    (df["b(m)"] / df["a(m)"]) * df["mb_g(N)"] / 
    (df["r(m)"] * df["ma_g(N)"])
)

# Theoretical omega2: sqrt((ma*g) / (r*mb*g)) = sqrt(ma / (r*mb))
df["omega2_theo(rad/s)"] = np.sqrt(
    df["ma_g(N)"] / (df["r(m)"] * df["mb_g(N)"])
)

# Handle None values for omega2 theoretical
df.loc[df["omega2_exp(rpm)"].isna(), "omega2_theo(rad/s)"] = None

# ============================
# Calculate Error Percentages
# ============================
# Error for omega1
df["omega1_Error(%)"] = (
    abs(df["omega1_theo(rad/s)"] - df["omega1_exp(rad/s)"]) / 
    df["omega1_theo(rad/s)"] * 100
)

# Error for omega2 (handle None values)
df["omega2_Error(%)"] = np.where(
    df["omega2_theo(rad/s)"].notna(),
    abs(df["omega2_theo(rad/s)"] - df["omega2_exp(rad/s)"]) / 
    df["omega2_theo(rad/s)"] * 100,
    None
)

# ============================
# Round Values for Better Readability
# ============================
df_rounded = df.round({
    "omega1_exp(rad/s)": 6,
    "omega1_theo(rad/s)": 6,
    "omega1_Error(%)": 3,
    "omega2_exp(rad/s)": 6,
    "omega2_theo(rad/s)": 6,
    "omega2_Error(%)": 3,
    "(b/a)mb": 6,
    "1/r": 6,
    "1/ma": 1
})

# ============================
# Reorder Columns
# ============================
column_order = [
    "ma_g(N)", "mb_g(N)", "r(m)", "a(m)", "b(m)",
    "omega1_exp(rpm)", "omega1_exp(rad/s)", "omega1_theo(rad/s)", "omega1_Error(%)",
    "omega2_exp(rpm)", "omega2_exp(rad/s)", "omega2_theo(rad/s)", "omega2_Error(%)",
    "(b/a)mb", "1/r", "1/ma"
]

df_final = df_rounded[column_order]

# ============================
# Save Results to Excel
# ============================
output_file = os.path.join(output_dir, "centrifugal_force_results.xlsx")
df_final.to_excel(output_file, index=False)

print(f"✓ Results saved: {output_file}")

# ============================
# Plot 1: Experimental vs Theoretical omega1
# ============================
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df["omega1_exp(rad/s)"], 
           color='blue', s=80, label='Experimental', alpha=0.7)
plt.scatter(df.index, df["omega1_theo(rad/s)"], 
           color='red', s=80, label='Theoretical', alpha=0.7, marker='s')
plt.xlabel('Test Number', fontsize=12)
plt.ylabel('omega1 (rad/s)', fontsize=12)
plt.title('omega1: Experimental vs Theoretical Comparison', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega1_comparison.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega1_comparison.png')}")

# ============================
# Plot 2: Experimental vs Theoretical omega2
# ============================
df_omega2 = df[df["omega2_exp(rad/s)"].notna()]
plt.figure(figsize=(10, 6))
plt.scatter(df_omega2.index, df_omega2["omega2_exp(rad/s)"], 
           color='green', s=80, label='Experimental', alpha=0.7)
plt.scatter(df_omega2.index, df_omega2["omega2_theo(rad/s)"], 
           color='orange', s=80, label='Theoretical', alpha=0.7, marker='s')
plt.xlabel('Test Number', fontsize=12)
plt.ylabel('omega2 (rad/s)', fontsize=12)
plt.title('omega2: Experimental vs Theoretical Comparison', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega2_comparison.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega2_comparison.png')}")

# ============================
# Plot 3: Error Analysis - omega1
# ============================
plt.figure(figsize=(10, 6))
bars = plt.bar(df.index, df["omega1_Error(%)"], color='coral', alpha=0.7, edgecolor='darkred')
plt.xlabel('Test Number', fontsize=12)
plt.ylabel('Error (%)', fontsize=12)
plt.title('omega1: Percentage Error', fontsize=14, fontweight='bold')
plt.axhline(y=df["omega1_Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean Error: {df["omega1_Error(%)"].mean():.1f}%')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega1_error.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega1_error.png')}")

# ============================
# Plot 4: Error Analysis - omega2
# ============================
plt.figure(figsize=(10, 6))
bars = plt.bar(df_omega2.index, df_omega2["omega2_Error(%)"], 
               color='lightgreen', alpha=0.7, edgecolor='darkgreen')
plt.xlabel('Test Number', fontsize=12)
plt.ylabel('Error (%)', fontsize=12)
plt.title('omega2: Percentage Error', fontsize=14, fontweight='bold')
plt.axhline(y=df_omega2["omega2_Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean Error: {df_omega2["omega2_Error(%)"].mean():.1f}%')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega2_error.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega2_error.png')}")

# ============================
# Plot 5: Combined Dashboard (4 Subplots)
# ============================
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Subplot 1: omega1 comparison
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(df.index, df["omega1_exp(rad/s)"], color='blue', s=60, label='Experimental', alpha=0.7)
ax1.scatter(df.index, df["omega1_theo(rad/s)"], color='red', s=60, label='Theoretical', alpha=0.7, marker='s')
ax1.set_xlabel('Test Number')
ax1.set_ylabel('omega1 (rad/s)')
ax1.set_title('omega1 Comparison')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Subplot 2: omega2 comparison
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(df_omega2.index, df_omega2["omega2_exp(rad/s)"], color='green', s=60, label='Experimental', alpha=0.7)
ax2.scatter(df_omega2.index, df_omega2["omega2_theo(rad/s)"], color='orange', s=60, label='Theoretical', alpha=0.7, marker='s')
ax2.set_xlabel('Test Number')
ax2.set_ylabel('omega2 (rad/s)')
ax2.set_title('omega2 Comparison')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Subplot 3: omega1 error
ax3 = fig.add_subplot(gs[1, 0])
ax3.bar(df.index, df["omega1_Error(%)"], color='coral', alpha=0.7, edgecolor='darkred')
ax3.axhline(y=df["omega1_Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean: {df["omega1_Error(%)"].mean():.1f}%')
ax3.set_xlabel('Test Number')
ax3.set_ylabel('Error (%)')
ax3.set_title('omega1 Error Analysis')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Subplot 4: omega2 error
ax4 = fig.add_subplot(gs[1, 1])
ax4.bar(df_omega2.index, df_omega2["omega2_Error(%)"], color='lightgreen', alpha=0.7, edgecolor='darkgreen')
ax4.axhline(y=df_omega2["omega2_Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean: {df_omega2["omega2_Error(%)"].mean():.1f}%')
ax4.set_xlabel('Test Number')
ax4.set_ylabel('Error (%)')
ax4.set_title('omega2 Error Analysis')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

fig.suptitle('Centrifugal Force Experiment - Complete Analysis Dashboard', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'centrifugal_dashboard.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'centrifugal_dashboard.png')}")

# ============================
# Plot 6: Effect of Parameters on omega1
# ============================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Effect of r on omega1
ax1 = axes[0, 0]
for r_val in df["r(m)"].unique():
    subset = df[df["r(m)"] == r_val]
    ax1.scatter(subset["(b/a)mb"], subset["omega1_exp(rad/s)"], 
               label=f'r = {r_val}m', s=80, alpha=0.7)
ax1.set_xlabel('(b/a)*mb')
ax1.set_ylabel('omega1_exp (rad/s)')
ax1.set_title('Effect of (b/a)*mb on omega1')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Effect of mb on omega1
ax2 = axes[0, 1]
for mb_val in df["mb_g(N)"].unique():
    subset = df[df["mb_g(N)"] == mb_val]
    ax2.scatter(subset["1/r"], subset["omega1_exp(rad/s)"], 
               label=f'mb = {mb_val}N', s=80, alpha=0.7)
ax2.set_xlabel('1/r')
ax2.set_ylabel('omega1_exp (rad/s)')
ax2.set_title('Effect of 1/r on omega1')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Effect of r on omega2
ax3 = axes[1, 0]
for r_val in df["r(m)"].unique():
    subset = df_omega2[df_omega2["r(m)"] == r_val]
    ax3.scatter(subset["ma_g(N)"], subset["omega2_exp(rad/s)"], 
               label=f'r = {r_val}m', s=80, alpha=0.7)
ax3.set_xlabel('ma (N)')
ax3.set_ylabel('omega2_exp (rad/s)')
ax3.set_title('Effect of ma on omega2')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Effect of mb on omega2
ax4 = axes[1, 1]
for mb_val in df["mb_g(N)"].unique():
    subset = df_omega2[df_omega2["mb_g(N)"] == mb_val]
    ax4.scatter(subset["1/r"], subset["omega2_exp(rad/s)"], 
               label=f'mb = {mb_val}N', s=80, alpha=0.7)
ax4.set_xlabel('1/r')
ax4.set_ylabel('omega2_exp (rad/s)')
ax4.set_title('Effect of 1/r on omega2')
ax4.legend()
ax4.grid(True, alpha=0.3)

fig.suptitle('Parameter Effects Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'parameter_effects.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'parameter_effects.png')}")

# ============================
# Print Summary Report
# ============================
print("\n" + "=" * 70)
print("SUMMARY REPORT")
print("=" * 70)
print(f"\nTotal data points: {len(df)}")
print(f"Tests with omega2 data: {len(df_omega2)}")
print(f"\nomega1 Statistics:")
print(f"  Mean experimental: {df['omega1_exp(rad/s)'].mean():.3f} rad/s")
print(f"  Mean theoretical: {df['omega1_theo(rad/s)'].mean():.3f} rad/s")
print(f"  Mean error: {df['omega1_Error(%)'].mean():.1f}%")
print(f"  Max error: {df['omega1_Error(%)'].max():.1f}%")
print(f"  Min error: {df['omega1_Error(%)'].min():.1f}%")
print(f"\nomega2 Statistics:")
print(f"  Mean experimental: {df_omega2['omega2_exp(rad/s)'].mean():.3f} rad/s")
print(f"  Mean theoretical: {df_omega2['omega2_theo(rad/s)'].mean():.3f} rad/s")
print(f"  Mean error: {df_omega2['omega2_Error(%)'].mean():.1f}%")
print(f"  Max error: {df_omega2['omega2_Error(%)'].max():.1f}%")
print(f"  Min error: {df_omega2['omega2_Error(%)'].min():.1f}%")
print("\n" + "=" * 70)
print(f"\n✅ Results saved in: {output_file}")
print(f"✅ All plots saved in: {plots_dir}/")
print("=" * 70)