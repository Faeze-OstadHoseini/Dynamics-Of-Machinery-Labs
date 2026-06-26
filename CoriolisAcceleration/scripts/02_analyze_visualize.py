import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ============================
# Get the directory where this script is located
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================
# Define relative paths (script is in scripts/ folder)
# ============================
data_file = os.path.join(script_dir, "..", "data", "coriolis_raw_data.xlsx")
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
# Calculate Additional Derived Parameters
# ============================
# Calculate theoretical angle using formula: theta = arctan(a_coriolis / (omega^2 * r))
# Since we don't have r directly, we use the relationship from the data
# The theoretical angle is already provided, but we can verify

# Calculate the ratio of experimental to theoretical
df["theta_ratio"] = df["theta_exp(rad)"] / df["theta_theo(rad)"]

# Calculate absolute error in radians
df["theta_abs_error(rad)"] = abs(df["theta_exp(rad)"] - df["theta_theo(rad)"])

# Calculate the difference between a_coriolis and theoretical relationship
# Coriolis acceleration: a_c = 2 * omega * v_rel
df["a_coriolis_theo"] = 2 * df["omega(rad/s)"] * df["v_rel(m/s)"]
df["a_coriolis_error(%)"] = abs(df["a_coriolis(m/s^2)"] - df["a_coriolis_theo"]) / df["a_coriolis_theo"] * 100

# ============================
# Round Values for Better Readability
# ============================
df_rounded = df.round({
    "omega(rad/s)": 6,
    "v_rel(m/s)": 6,
    "a_coriolis(m/s^2)": 6,
    "theta_exp(rad)": 6,
    "theta_theo(rad)": 6,
    "Error(%)": 3,
    "theta_ratio": 4,
    "theta_abs_error(rad)": 6,
    "a_coriolis_theo": 6,
    "a_coriolis_error(%)": 3
})

# ============================
# Save Results to Excel
# ============================
output_file = os.path.join(output_dir, "coriolis_results.xlsx")
df_rounded.to_excel(output_file, index=False)

print(f"✓ Results saved: {output_file}")

# ============================
# Plot 1: Experimental vs Theoretical Angle
# ============================
plt.figure(figsize=(10, 6))
plt.scatter(df["omega(rpm)"], df["theta_exp(rad)"], 
           color='blue', s=100, label='Experimental', alpha=0.7)
plt.scatter(df["omega(rpm)"], df["theta_theo(rad)"], 
           color='red', s=100, label='Theoretical', alpha=0.7, marker='s')
plt.xlabel('Rotational Speed (rpm)', fontsize=12)
plt.ylabel('Angle (rad)', fontsize=12)
plt.title('Coriolis Angle: Experimental vs Theoretical', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'coriolis_angle_comparison.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'coriolis_angle_comparison.png')}")

# ============================
# Plot 2: Error Analysis
# ============================
plt.figure(figsize=(10, 6))
bars = plt.bar(df["omega(rpm)"], df["Error(%)"], 
               color='coral', alpha=0.7, edgecolor='darkred', width=2)
plt.xlabel('Rotational Speed (rpm)', fontsize=12)
plt.ylabel('Error (%)', fontsize=12)
plt.title('Percentage Error in Angle Measurement', fontsize=14, fontweight='bold')
plt.axhline(y=df["Error(%)"].mean(), color='blue', linestyle='--', 
           linewidth=2, label=f'Mean Error: {df["Error(%)"].mean():.2f}%')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'coriolis_error.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'coriolis_error.png')}")

# ============================
# Plot 3: Coriolis Acceleration Analysis
# ============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Coriolis acceleration vs omega
ax1 = axes[0]
ax1.plot(df["omega(rpm)"], df["a_coriolis(m/s^2)"], 
         'o-', color='green', linewidth=2, markersize=8, label='Measured')
ax1.plot(df["omega(rpm)"], df["a_coriolis_theo"], 
         's--', color='purple', linewidth=2, markersize=8, label='Theoretical')
ax1.set_xlabel('Rotational Speed (rpm)', fontsize=12)
ax1.set_ylabel('Coriolis Acceleration (m/s^2)', fontsize=12)
ax1.set_title('Coriolis Acceleration: Measured vs Theoretical', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Subplot 2: Error in Coriolis acceleration
ax2 = axes[1]
bars = ax2.bar(df["omega(rpm)"], df["a_coriolis_error(%)"], 
               color='lightblue', alpha=0.7, edgecolor='darkblue', width=2)
ax2.axhline(y=df["a_coriolis_error(%)"].mean(), color='red', linestyle='--', 
           linewidth=2, label=f'Mean Error: {df["a_coriolis_error(%)"].mean():.2f}%')
ax2.set_xlabel('Rotational Speed (rpm)', fontsize=12)
ax2.set_ylabel('Error (%)', fontsize=12)
ax2.set_title('Coriolis Acceleration Error Analysis', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'coriolis_acceleration.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'coriolis_acceleration.png')}")

# ============================
# Plot 4: Relationship between omega and angle
# ============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Angle vs omega
ax1 = axes[0]
ax1.plot(df["omega(rpm)"], df["theta_exp(rad)"], 
         'o-', color='blue', linewidth=2, markersize=8, label='Experimental')
ax1.plot(df["omega(rpm)"], df["theta_theo(rad)"], 
         's--', color='red', linewidth=2, markersize=8, label='Theoretical')
ax1.set_xlabel('Rotational Speed (rpm)', fontsize=12)
ax1.set_ylabel('Angle (rad)', fontsize=12)
ax1.set_title('Angle vs Rotational Speed', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Subplot 2: Angle ratio vs omega
ax2 = axes[1]
ax2.plot(df["omega(rpm)"], df["theta_ratio"], 
         'D-', color='orange', linewidth=2, markersize=8)
ax2.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
ax2.set_xlabel('Rotational Speed (rpm)', fontsize=12)
ax2.set_ylabel('Ratio (Exp/Theo)', fontsize=12)
ax2.set_title('Experimental to Theoretical Ratio', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'coriolis_relationship.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'coriolis_relationship.png')}")

# ============================
# Plot 5: Complete Dashboard (2x2 Grid)
# ============================
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Subplot 1: Angle comparison
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(df["omega(rpm)"], df["theta_exp(rad)"], 
           color='blue', s=80, label='Experimental', alpha=0.7)
ax1.scatter(df["omega(rpm)"], df["theta_theo(rad)"], 
           color='red', s=80, label='Theoretical', alpha=0.7, marker='s')
ax1.set_xlabel('Omega (rpm)')
ax1.set_ylabel('Angle (rad)')
ax1.set_title('Angle Comparison')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Subplot 2: Error percentage
ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(df["omega(rpm)"], df["Error(%)"], color='coral', alpha=0.7, edgecolor='darkred', width=2)
ax2.axhline(y=df["Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean: {df["Error(%)"].mean():.2f}%')
ax2.set_xlabel('Omega (rpm)')
ax2.set_ylabel('Error (%)')
ax2.set_title('Angle Error Analysis')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Subplot 3: Coriolis acceleration
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(df["omega(rpm)"], df["a_coriolis(m/s^2)"], 
        'o-', color='green', linewidth=2, markersize=8, label='Measured')
ax3.plot(df["omega(rpm)"], df["a_coriolis_theo"], 
        's--', color='purple', linewidth=2, markersize=8, label='Theoretical')
ax3.set_xlabel('Omega (rpm)')
ax3.set_ylabel('Acceleration (m/s^2)')
ax3.set_title('Coriolis Acceleration')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Subplot 4: Ratio analysis
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(df["omega(rpm)"], df["theta_ratio"], 
        'D-', color='orange', linewidth=2, markersize=8)
ax4.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
ax4.set_xlabel('Omega (rpm)')
ax4.set_ylabel('Ratio (Exp/Theo)')
ax4.set_title('Experimental/Theoretical Ratio')
ax4.grid(True, alpha=0.3)

fig.suptitle('Coriolis Acceleration Experiment - Complete Dashboard', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'coriolis_dashboard.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'coriolis_dashboard.png')}")

# ============================
# Print Summary Report
# ============================
print("\n" + "=" * 70)
print("SUMMARY REPORT")
print("=" * 70)
print(f"\nTotal data points: {len(df)}")
print(f"\nAngle Statistics:")
print(f"  Mean experimental angle: {df['theta_exp(rad)'].mean():.4f} rad")
print(f"  Mean theoretical angle: {df['theta_theo(rad)'].mean():.4f} rad")
print(f"  Mean error: {df['Error(%)'].mean():.2f}%")
print(f"  Max error: {df['Error(%)'].max():.2f}%")
print(f"  Min error: {df['Error(%)'].min():.2f}%")
print(f"\nCoriolis Acceleration Statistics:")
print(f"  Mean measured: {df['a_coriolis(m/s^2)'].mean():.3f} m/s^2")
print(f"  Mean theoretical: {df['a_coriolis_theo'].mean():.3f} m/s^2")
print(f"  Mean error: {df['a_coriolis_error(%)'].mean():.2f}%")
print(f"\nRatio (Exp/Theo) Statistics:")
print(f"  Mean ratio: {df['theta_ratio'].mean():.4f}")
print(f"  Min ratio: {df['theta_ratio'].min():.4f}")
print(f"  Max ratio: {df['theta_ratio'].max():.4f}")
print("\n" + "=" * 70)
print(f"\n✅ Results saved in: {output_file}")
print(f"✅ All plots saved in: {plots_dir}/")
print("=" * 70)