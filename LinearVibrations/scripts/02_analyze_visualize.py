import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from scipy.optimize import curve_fit

# ============================
# Get the directory where this script is located
# ============================
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================
# Define relative paths (script is in scripts/ folder)
# ============================
data_file = os.path.join(script_dir, "..", "data", "linear_vibration_raw_data.xlsx")
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
# CALCULATE ALL DERIVED PARAMETERS (Not in raw data)
# ============================

# Constants
g = 9.81  # m/s^2

# 1. Calculate damping ratio (zeta) from logarithmic decrement
# zeta = ln(y1/y2) / sqrt((2*pi)^2 + ln(y1/y2)^2)
df["zeta"] = np.log(df["y1(mm)"] / df["y2(mm)"]) / np.sqrt(
    (2 * np.pi)**2 + (np.log(df["y1(mm)"] / df["y2(mm)"]))**2
)

# 2. Calculate experimental damped frequency (omega_d_exp)
# omega_d = 2*pi / Td
df["omega_d_exp"] = 2 * np.pi / df["Td(sec)"]

# 3. Calculate experimental natural frequency (omega_n_exp)
# omega_n = omega_d / sqrt(1 - zeta^2)
df["omega_n_exp"] = df["omega_d_exp"] / np.sqrt(1 - df["zeta"]**2)

# 4. Calculate theoretical natural frequency (omega_n_theo)
# Use the provided theoretical values from report
df["omega_n_theo"] = [14.70001447, 14.70001447, 13.32578098, 13.32578098, 12.27658204, 12.27658204]

# 5. Calculate error percentage
df["Error(%)"] = abs(df["omega_n_exp"] - df["omega_n_theo"]) / df["omega_n_theo"] * 100

# ============================
# Additional Derived Parameters for Analysis
# ============================

# Difference between theoretical and experimental natural frequency
df["omega_diff(%)"] = abs(df["omega_n_exp"] - df["omega_n_theo"]) / df["omega_n_theo"] * 100

# Damping coefficient (c) = 2 * zeta * m * omega_n
df["c(Ns/m)"] = 2 * df["zeta"] * df["m(Kg)"] * df["omega_n_exp"]

# Logarithmic decrement (delta)
df["delta"] = df["zeta"] * 2 * np.pi / np.sqrt(1 - df["zeta"]**2)

# Damping ratio from logarithmic decrement (should match zeta)
df["zeta_from_delta"] = df["delta"] / np.sqrt((2 * np.pi)**2 + df["delta"]**2)

# Calculated stiffness from experimental frequency
df["k_calc(N/m)"] = df["m(Kg)"] * df["omega_n_exp"]**2

# Theoretical damped frequency
df["omega_d_theo"] = df["omega_n_exp"] * np.sqrt(1 - df["zeta"]**2)

# Error in damped frequency
df["omega_d_error(%)"] = abs(df["omega_d_exp"] - df["omega_d_theo"]) / df["omega_d_theo"] * 100

# ============================
# Round Values for Better Readability
# ============================
df_rounded = df.round({
    "zeta": 6,
    "Td(sec)": 6,
    "omega_d_exp": 6,
    "omega_n_exp": 6,
    "omega_n_theo": 6,
    "Error(%)": 3,
    "omega_diff(%)": 3,
    "c(Ns/m)": 4,
    "delta": 6,
    "zeta_from_delta": 6,
    "k_calc(N/m)": 2,
    "omega_d_theo": 6,
    "omega_d_error(%)": 3
})

# ============================
# Select columns for final output (Raw + Calculated)
# ============================
column_order = [
    "state", "m(Kg)", "y1(mm)", "y2(mm)", "x(mm)", 
    "Td(sec)", "k", "v(mm/s)",  # Raw data
    "zeta", "omega_d_exp", "omega_n_exp", "omega_n_theo", "Error(%)",  # Calculated
    "c(Ns/m)", "delta", "zeta_from_delta", "k_calc(N/m)", 
    "omega_d_theo", "omega_d_error(%)"  # Additional analysis
]

df_final = df_rounded[column_order]

# ============================
# Save Results to Excel
# ============================
output_file = os.path.join(output_dir, "linear_vibration_results.xlsx")
df_final.to_excel(output_file, index=False)

print(f"✓ Results saved: {output_file}")

# ============================
# Plot 1: Experimental vs Theoretical Natural Frequency
# ============================
plt.figure(figsize=(10, 6))
x_pos = np.arange(len(df["state"]))
width = 0.35

plt.bar(x_pos - width/2, df["omega_n_exp"], width, label='Experimental', color='blue', alpha=0.7)
plt.bar(x_pos + width/2, df["omega_n_theo"], width, label='Theoretical', color='red', alpha=0.7)

plt.xlabel('Test State', fontsize=12)
plt.ylabel('Natural Frequency (rad/s)', fontsize=12)
plt.title('Natural Frequency: Experimental vs Theoretical', fontsize=14, fontweight='bold')
plt.xticks(x_pos, df["state"])
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'natural_frequency_comparison.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'natural_frequency_comparison.png')}")

# ============================
# Plot 2: Error Analysis
# ============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Error percentage
ax1 = axes[0]
bars = ax1.bar(df["state"], df["Error(%)"], color='coral', alpha=0.7, edgecolor='darkred')
ax1.axhline(y=df["Error(%)"].mean(), color='blue', linestyle='--', 
           linewidth=2, label=f'Mean Error: {df["Error(%)"].mean():.2f}%')
ax1.set_xlabel('Test State', fontsize=12)
ax1.set_ylabel('Error (%)', fontsize=12)
ax1.set_title('Error in Natural Frequency', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Subplot 2: Difference between theoretical and experimental
ax2 = axes[1]
bars = ax2.bar(df["state"], df["omega_diff(%)"], color='lightgreen', alpha=0.7, edgecolor='darkgreen')
ax2.axhline(y=df["omega_diff(%)"].mean(), color='red', linestyle='--', 
           linewidth=2, label=f'Mean Diff: {df["omega_diff(%)"].mean():.2f}%')
ax2.set_xlabel('Test State', fontsize=12)
ax2.set_ylabel('Difference (%)', fontsize=12)
ax2.set_title('Theoretical vs Experimental Difference', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'error_analysis.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'error_analysis.png')}")

# ============================
# Plot 3: Damping Analysis
# ============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Damping ratio
ax1 = axes[0]
bars = ax1.bar(df["state"], df["zeta"], color='purple', alpha=0.7, edgecolor='darkorchid')
ax1.axhline(y=df["zeta"].mean(), color='red', linestyle='--', 
           linewidth=2, label=f'Mean zeta: {df["zeta"].mean():.4f}')
ax1.set_xlabel('Test State', fontsize=12)
ax1.set_ylabel('Damping Ratio (zeta)', fontsize=12)
ax1.set_title('Damping Ratio Analysis', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Subplot 2: Damped period
ax2 = axes[1]
bars = ax2.bar(df["state"], df["Td(sec)"], color='teal', alpha=0.7, edgecolor='darkcyan')
ax2.axhline(y=df["Td(sec)"].mean(), color='red', linestyle='--', 
           linewidth=2, label=f'Mean Td: {df["Td(sec)"].mean():.4f} s')
ax2.set_xlabel('Test State', fontsize=12)
ax2.set_ylabel('Damped Period (s)', fontsize=12)
ax2.set_title('Damped Period Analysis', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'damping_analysis.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'damping_analysis.png')}")

# ============================
# Plot 4: Mass vs Natural Frequency
# ============================
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df["m(Kg)"], df["omega_n_exp"], 
                     s=df["zeta"]*500, alpha=0.6, 
                     c=df["Error(%)"], cmap='RdYlGn_r', 
                     edgecolors='black', linewidth=1.5)

plt.xlabel('Mass (kg)', fontsize=12)
plt.ylabel('Natural Frequency (rad/s)', fontsize=12)
plt.title('Effect of Mass on Natural Frequency (Size = Damping Ratio)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Error (%)')
plt.grid(True, alpha=0.3)

# Add state labels
for i, state in enumerate(df["state"]):
    plt.annotate(state, (df["m(Kg)"].iloc[i], df["omega_n_exp"].iloc[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'mass_vs_frequency.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'mass_vs_frequency.png')}")

# ============================
# Plot 5: Complete Dashboard (2x2 Grid)
# ============================
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Subplot 1: Natural frequency comparison
ax1 = fig.add_subplot(gs[0, 0])
x_pos = np.arange(len(df["state"]))
width = 0.35
ax1.bar(x_pos - width/2, df["omega_n_exp"], width, label='Experimental', color='blue', alpha=0.7)
ax1.bar(x_pos + width/2, df["omega_n_theo"], width, label='Theoretical', color='red', alpha=0.7)
ax1.set_xlabel('Test State')
ax1.set_ylabel('Natural Frequency (rad/s)')
ax1.set_title('Natural Frequency Comparison')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(df["state"])
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Subplot 2: Error analysis
ax2 = fig.add_subplot(gs[0, 1])
bars = ax2.bar(df["state"], df["Error(%)"], color='coral', alpha=0.7, edgecolor='darkred')
ax2.axhline(y=df["Error(%)"].mean(), color='blue', linestyle='--', 
           label=f'Mean: {df["Error(%)"].mean():.2f}%')
ax2.set_xlabel('Test State')
ax2.set_ylabel('Error (%)')
ax2.set_title('Error Analysis')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Subplot 3: Damping ratio and period
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(df["state"], df["zeta"], 'o-', color='purple', linewidth=2, markersize=8, label='Damping Ratio')
ax3.set_xlabel('Test State')
ax3.set_ylabel('Damping Ratio', color='purple')
ax3.tick_params(axis='y', labelcolor='purple')
ax3.grid(True, alpha=0.3)

ax3_2 = ax3.twinx()
ax3_2.plot(df["state"], df["Td(sec)"], 's--', color='teal', linewidth=2, markersize=8, label='Damped Period')
ax3_2.set_ylabel('Damped Period (s)', color='teal')
ax3_2.tick_params(axis='y', labelcolor='teal')

ax3.set_title('Damping Parameters')
ax3.legend(loc='upper left')
ax3_2.legend(loc='upper right')

# Subplot 4: Mass vs frequency scatter
ax4 = fig.add_subplot(gs[1, 1])
scatter = ax4.scatter(df["m(Kg)"], df["omega_n_exp"], 
                     s=df["zeta"]*500, alpha=0.6, 
                     c=df["Error(%)"], cmap='RdYlGn_r', 
                     edgecolors='black', linewidth=1.5)
ax4.set_xlabel('Mass (kg)')
ax4.set_ylabel('Natural Frequency (rad/s)')
ax4.set_title('Mass vs Frequency (Size = Damping Ratio)')
plt.colorbar(scatter, ax=ax4, label='Error (%)')
ax4.grid(True, alpha=0.3)

# Add state labels
for i, state in enumerate(df["state"]):
    ax4.annotate(state, (df["m(Kg)"].iloc[i], df["omega_n_exp"].iloc[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')

fig.suptitle('Linear Vibration Experiment - Complete Dashboard', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'vibration_dashboard.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'vibration_dashboard.png')}")

# ============================
# Plot 6: Relationship between zeta and error
# ============================
plt.figure(figsize=(10, 6))
plt.scatter(df["zeta"], df["Error(%)"], s=100, alpha=0.6, 
           c=df["m(Kg)"], cmap='viridis', edgecolors='black', linewidth=1.5)
plt.xlabel('Damping Ratio (zeta)', fontsize=12)
plt.ylabel('Error (%)', fontsize=12)
plt.title('Effect of Damping Ratio on Measurement Error', fontsize=14, fontweight='bold')
plt.colorbar(label='Mass (kg)')
plt.grid(True, alpha=0.3)

# Add state labels
for i, state in enumerate(df["state"]):
    plt.annotate(state, (df["zeta"].iloc[i], df["Error(%)"].iloc[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'zeta_vs_error.png'), dpi=300)
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'zeta_vs_error.png')}")

# ============================
# Plot 7: Natural Frequency vs Mass (Theoretical vs Experimental)
# ============================
fig, ax = plt.subplots(figsize=(12, 7))

# Sort data by mass for better visualization
df_sorted = df.sort_values('m(Kg)')

# Plot experimental data
ax.plot(df_sorted['m(Kg)'], df_sorted['omega_n_exp'], 
        'o-', color='blue', linewidth=2.5, markersize=10, 
        markerfacecolor='white', markeredgewidth=2.5,
        label='Experimental ωn', zorder=3)

# Plot theoretical data
ax.plot(df_sorted['m(Kg)'], df_sorted['omega_n_theo'], 
        's--', color='red', linewidth=2.5, markersize=10,
        markerfacecolor='white', markeredgewidth=2.5,
        label='Theoretical ωn', zorder=3)

# Add error bars (showing the difference between exp and theo)
error_y = abs(df_sorted['omega_n_exp'] - df_sorted['omega_n_theo'])
ax.errorbar(df_sorted['m(Kg)'], df_sorted['omega_n_exp'], 
            yerr=error_y, fmt='none', ecolor='gray', 
            capsize=5, elinewidth=1.5, alpha=0.6, label='Error Range')

# Add value labels on experimental points
for i, row in df_sorted.iterrows():
    ax.annotate(f'ωn={row["omega_n_exp"]:.2f}', 
               (row['m(Kg)'], row['omega_n_exp']),
               xytext=(5, 10), textcoords='offset points',
               fontsize=9, color='blue', fontweight='bold')
    
    ax.annotate(f'{row["omega_n_theo"]:.2f}', 
               (row['m(Kg)'], row['omega_n_theo']),
               xytext=(-5, -15), textcoords='offset points',
               fontsize=9, color='red', fontweight='bold')

# Add state labels
for i, row in df_sorted.iterrows():
    ax.annotate(f'({row["state"]})', 
               (row['m(Kg)'], (row['omega_n_exp'] + row['omega_n_theo'])/2),
               xytext=(10, 0), textcoords='offset points',
               fontsize=10, color='black', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

# Add theoretical curve fit
def power_law(m, a, b):
    return a * m**b

# Fit to theoretical data
popt, _ = curve_fit(power_law, df_sorted['m(Kg)'], df_sorted['omega_n_theo'])
m_fit = np.linspace(df_sorted['m(Kg)'].min() * 0.9, df_sorted['m(Kg)'].max() * 1.1, 100)
omega_fit = power_law(m_fit, *popt)
ax.plot(m_fit, omega_fit, 'r--', alpha=0.3, linewidth=1, 
        label=f'Fit: ωn = {popt[0]:.2f}·m^{popt[1]:.2f}')

# Customize the plot
ax.set_xlabel('Mass (kg)', fontsize=14, fontweight='bold')
ax.set_ylabel('Natural Frequency ωn (rad/s)', fontsize=14, fontweight='bold')
ax.set_title('Natural Frequency vs Mass: Theoretical vs Experimental', 
             fontsize=16, fontweight='bold', pad=20)

# Add grid
ax.grid(True, linestyle='--', alpha=0.3, color='gray')

# Set axis limits
ax.set_xlim(df_sorted['m(Kg)'].min() * 0.85, df_sorted['m(Kg)'].max() * 1.05)
ax.set_ylim(0, df_sorted['omega_n_exp'].max() * 1.15)

# Set legend
ax.legend(loc='best', fontsize=11, framealpha=0.9, 
          edgecolor='gray', fancybox=True, shadow=True)

# Create a second y-axis for displacement
ax2 = ax.twinx()
ax2.scatter(df_sorted['m(Kg)'], df_sorted['x(mm)'], 
            color='green', alpha=0.3, s=80, marker='D',
            label='Displacement x (mm)')
ax2.set_ylabel('Displacement x (mm)', fontsize=12, color='green')
ax2.tick_params(axis='y', labelcolor='green')
ax2.legend(loc='lower left', fontsize=10)

# Add displacement labels
for i, row in df_sorted.iterrows():
    ax2.annotate(f'x={row["x(mm)"]}mm', 
                (row['m(Kg)'], row['x(mm)']),
                xytext=(5, -10), textcoords='offset points',
                fontsize=8, color='green')

# Customize spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_color('green')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'natural_frequency_vs_mass.png'), dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'natural_frequency_vs_mass.png')}")

# ============================
# Plot 8: Natural Frequency vs Mass - Separate Subplots
# ============================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Subplot 1: Experimental ωn vs mass
ax1 = axes[0]
ax1.scatter(df_sorted['m(Kg)'], df_sorted['omega_n_exp'], 
           s=100, color='blue', alpha=0.7, edgecolors='black', linewidth=2)
ax1.plot(df_sorted['m(Kg)'], df_sorted['omega_n_exp'], 
        'b-', linewidth=2, alpha=0.5)

# Fit a trend line
z = np.polyfit(df_sorted['m(Kg)'], df_sorted['omega_n_exp'], 1)
p = np.poly1d(z)
ax1.plot(m_fit, p(m_fit), "b--", alpha=0.5, 
         label=f'Linear Fit: ωn = {z[0]:.2f}m + {z[1]:.2f}')

ax1.set_xlabel('Mass (kg)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Experimental ωn (rad/s)', fontsize=12, fontweight='bold')
ax1.set_title('Experimental Natural Frequency vs Mass', fontsize=13, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(fontsize=10)

# Add state labels
for i, row in df_sorted.iterrows():
    ax1.annotate(row['state'], 
                (row['m(Kg)'], row['omega_n_exp']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=11, fontweight='bold')

# Subplot 2: Theoretical ωn vs mass
ax2 = axes[1]
ax2.scatter(df_sorted['m(Kg)'], df_sorted['omega_n_theo'], 
           s=100, color='red', alpha=0.7, edgecolors='black', linewidth=2)
ax2.plot(df_sorted['m(Kg)'], df_sorted['omega_n_theo'], 
        'r-', linewidth=2, alpha=0.5)

# Fit a power law to theoretical data
z2 = np.polyfit(df_sorted['m(Kg)'], df_sorted['omega_n_theo'], 1)
p2 = np.poly1d(z2)
ax2.plot(m_fit, p2(m_fit), "r--", alpha=0.5, 
         label=f'Linear Fit: ωn = {z2[0]:.2f}m + {z2[1]:.2f}')

ax2.set_xlabel('Mass (kg)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Theoretical ωn (rad/s)', fontsize=12, fontweight='bold')
ax2.set_title('Theoretical Natural Frequency vs Mass', fontsize=13, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend(fontsize=10)

# Add state labels
for i, row in df_sorted.iterrows():
    ax2.annotate(row['state'], 
                (row['m(Kg)'], row['omega_n_theo']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega_n_vs_mass_subplots.png'), dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega_n_vs_mass_subplots.png')}")

# ============================
# Plot 9: Comparison Table as Heatmap
# ============================
fig, ax = plt.subplots(figsize=(10, 6))

# Create a table with comparison data
table_data = []
for _, row in df_sorted.iterrows():
    table_data.append([
        row['state'],
        f"{row['m(Kg)']:.3f}",
        f"{row['omega_n_exp']:.3f}",
        f"{row['omega_n_theo']:.3f}",
        f"{row['Error(%)']:.2f}%"
    ])

# Create the table
table = ax.table(cellText=table_data,
                 colLabels=['State', 'Mass (kg)', 'ωn Exp (rad/s)', 'ωn Theo (rad/s)', 'Error (%)'],
                 cellLoc='center',
                 loc='center',
                 colColours=['#4472C4']*5)

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.5)

# Color the cells based on error
for i, row in enumerate(table_data):
    error = float(row[4].replace('%', ''))
    if error < 10:
        color = '#C6EFCE'  # Green
    elif error < 20:
        color = '#FFEB9C'  # Yellow
    else:
        color = '#FFC7CE'  # Red
    
    for j in range(5):
        if j == 4:  # Only color the error column
            table[(i+1, j)].set_facecolor(color)

# Add title
ax.set_title('Natural Frequency Comparison: Experimental vs Theoretical', 
             fontsize=14, fontweight='bold', pad=20)

# Remove axes
ax.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'omega_n_comparison_table.png'), dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {os.path.join(plots_dir, 'omega_n_comparison_table.png')}")

# ============================
# Print Summary Report
# ============================
print("\n" + "=" * 70)
print("SUMMARY REPORT")
print("=" * 70)
print(f"\nTotal data points: {len(df)}")
print(f"\nNatural Frequency Statistics:")
print(f"  Mean experimental: {df['omega_n_exp'].mean():.3f} rad/s")
print(f"  Mean theoretical: {df['omega_n_theo'].mean():.3f} rad/s")
print(f"  Mean error: {df['Error(%)'].mean():.2f}%")
print(f"  Max error: {df['Error(%)'].max():.2f}%")
print(f"  Min error: {df['Error(%)'].min():.2f}%")
print(f"\nDamping Statistics:")
print(f"  Mean damping ratio: {df['zeta'].mean():.4f}")
print(f"  Mean damped period: {df['Td(sec)'].mean():.4f} s")
print(f"  Mean damping coefficient: {df['c(Ns/m)'].mean():.4f} Ns/m")
print(f"\nMass Statistics:")
print(f"  Mass range: {df['m(Kg)'].min()} to {df['m(Kg)'].max()} kg")
print(f"  Displacement range: {df['x(mm)'].min()} to {df['x(mm)'].max()} mm")
print("\n" + "=" * 70)
print(f"\n✅ Results saved in: {output_file}")
print(f"✅ All plots saved in: {plots_dir}/")
print("=" * 70)