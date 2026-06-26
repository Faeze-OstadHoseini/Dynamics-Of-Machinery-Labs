import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
import os

# ============================
# Plot Style Settings
# ============================
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = (10, 6)

# ============================
# Experimental Data (from report)
# ============================
# Porter 2N
porter_2N_forward_RPM = [182, 190, 196, 203, 208, 215, 223, 226]
porter_2N_return_RPM = [216, 210, 199, 195, 191, 184, 179, 168]

# Porter 4N
porter_4N_forward_RPM = [151, 156, 159, 165, 168, 174, 181, 187]
porter_4N_return_RPM = [187, 181, 174, 169, 163, 158, 153, 150]

# Proell 4N
proell_4N_forward_RPM = [94, 96, 99, 103, 106, 108, 110, 115]
proell_4N_return_RPM = [114, 111, 107, 105, 102, 98, 94, 91]

# Sleeve displacements (mm)
heights = [5, 10, 15, 20, 25, 30, 35, 40]

# Physical constants
g = 9.81  # gravity (m/s^2)

# ============================
# Utility Functions
# ============================

def rpm_to_rad_per_s(rpm):
    """Convert RPM to angular velocity (rad/s)"""
    return rpm * 2 * np.pi / 60

def sensitivity(N1, N2):
    """Sensitivity based on RPM values"""
    return (N2 - N1) / ((N2 + N1) / 2)

def insensitiveness(omega_up, omega_down):
    """Insensitiveness coefficient based on angular velocity"""
    return abs(omega_up - omega_down) / ((omega_up + omega_down) / 2)

# ============================
# Porter Governor Theory
# ============================
def porter_theory(disp_mm, weight_N, M_g_N=0.93, c_mm=28, L2_mm=85, L3_mm=25, tan_phi=1.12):
    """
    Calculate theoretical angular velocity for Porter governor
    disp_mm: sleeve displacement (X) in mm
    weight_N: weight of each ball (N)
    M_g_N: sleeve weight (N)
    Returns: omega (rad/s), RPM
    """
    h_mm = L3_mm + disp_mm
    h = h_mm / 1000  # convert to meters
    tan_theta = np.sqrt(L2_mm**2 - h_mm**2) / h_mm
    m = weight_N / g
    M = M_g_N / g
    c = c_mm / 1000
    bracket = 1 + (1 / (2 * m)) * (1 + (tan_phi / tan_theta))
    denominator = (h * tan_theta) + c
    omega2 = (g * tan_theta) / denominator * bracket
    if omega2 < 0:
        omega2 = 0
    omega = np.sqrt(omega2)
    rpm = omega * 60 / (2 * np.pi)
    return omega, rpm

# ============================
# Proell Governor Theory
# ============================
def proell_theory(disp_mm, weight_N, M_g_N=1.9, b_mm=25, L1_mm=85, L2_mm=65, L3_mm=50, L0_mm=135, theta4_deg=4):
    """
    Calculate theoretical angular velocity for Proell governor
    disp_mm: sleeve displacement (X) in mm
    weight_N: weight of each ball (N)
    M_g_N: sleeve weight (N)
    Returns: omega (rad/s), RPM
    """
    L = L0_mm - disp_mm
    cos_theta5 = (L1_mm**2 + L2_mm**2 - L**2) / (2 * L1_mm * L2_mm)
    cos_theta5 = np.clip(cos_theta5, -1.0, 1.0)
    theta5 = np.arccos(cos_theta5)
    sin_theta1 = (L2_mm / L) * np.sin(theta5)
    sin_theta1 = np.clip(sin_theta1, -1.0, 1.0)
    theta1 = np.arcsin(sin_theta1)
    theta2 = np.pi - theta1 - theta5
    alpha = theta1 + theta2
    theta3 = alpha - np.deg2rad(theta4_deg)
    beta = np.pi/2 - theta2
    x_mm = L2_mm * np.sin(alpha) / np.sin(beta)
    psi = np.pi - (np.pi/2 - theta1 + theta3)
    r_mm = L1_mm * np.sin(theta1) + L3_mm * np.cos(psi)
    y_mm = L2_mm * np.cos(theta2) + L3_mm * np.sin(psi)
    r = r_mm / 1000
    y = y_mm / 1000
    x = x_mm / 1000
    b = b_mm / 1000
    m = weight_N / g
    M = M_g_N / g
    term1 = (x - r)
    term2 = 0.5 * (M / m) * (x - b)
    omega2 = (g / (r * y)) * (term1 + term2)
    if omega2 < 0:
        omega2 = 0
    omega = np.sqrt(omega2)
    rpm = omega * 60 / (2 * np.pi)
    return omega, rpm

# ============================
# Process All Test Cases
# ============================

cases = [
    {'name': 'Porter_2N', 'forward': porter_2N_forward_RPM, 'return': porter_2N_return_RPM,
     'weight_N': 2, 'M_g_N': 0.93, 'type': 'porter'},
    {'name': 'Porter_4N', 'forward': porter_4N_forward_RPM, 'return': porter_4N_return_RPM,
     'weight_N': 4, 'M_g_N': 0.93, 'type': 'porter'},
    {'name': 'Proell_4N', 'forward': proell_4N_forward_RPM, 'return': proell_4N_return_RPM,
     'weight_N': 4, 'M_g_N': 1.9, 'type': 'proell'}
]

results = {}

for case in cases:
    name = case['name']
    fwd = case['forward']
    ret = case['return']
    weight = case['weight_N']
    Mg = case['M_g_N']
    typ = case['type']
    
    # Experimental angular velocities
    omega_fwd = [rpm_to_rad_per_s(r) for r in fwd]
    omega_ret = [rpm_to_rad_per_s(r) for r in ret]
    
    # Theoretical calculations
    if typ == 'porter':
        omega_theory = [porter_theory(h, weight, Mg)[0] for h in heights]
        rpm_theory = [porter_theory(h, weight, Mg)[1] for h in heights]
    else:  # proell
        omega_theory = [proell_theory(h, weight, Mg)[0] for h in heights]
        rpm_theory = [proell_theory(h, weight, Mg)[1] for h in heights]
    
    # Sensitivity (using first and last points)
    sens_fwd = sensitivity(fwd[0], fwd[-1])
    sens_ret_correct = sensitivity(ret[-1], ret[0])
    
    # Insensitiveness for each displacement
    insens = []
    for i in range(len(heights)):
        h = heights[i]
        idx_ret = heights[::-1].index(h)
        omega_up = omega_fwd[i]
        omega_down = omega_ret[idx_ret]
        insens.append(insensitiveness(omega_up, omega_down))
    
    results[name] = {
        'heights': heights,
        'fwd_RPM': fwd,
        'ret_RPM': ret,
        'omega_fwd': omega_fwd,
        'omega_ret': omega_ret,
        'omega_theory': omega_theory,
        'rpm_theory': rpm_theory,
        'sens_fwd': sens_fwd,
        'sens_ret': sens_ret_correct,
        'insens': insens
    }

# ============================
# Export to Excel
# ============================

output_excel = "Governor_Results.xlsx"
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    # Sheet 1: Experimental RPM data
    df_exp = pd.DataFrame({
        'Height_mm': heights,
        'Porter_2N_Fwd_RPM': porter_2N_forward_RPM,
        'Porter_2N_Ret_RPM': porter_2N_return_RPM,
        'Porter_4N_Fwd_RPM': porter_4N_forward_RPM,
        'Porter_4N_Ret_RPM': porter_4N_return_RPM,
        'Proell_4N_Fwd_RPM': proell_4N_forward_RPM,
        'Proell_4N_Ret_RPM': proell_4N_return_RPM
    })
    df_exp.to_excel(writer, sheet_name='Experimental_Data', index=False)
    
    # Sheet 2: Experimental angular velocities
    df_omega = pd.DataFrame({
        'Height_mm': heights,
        'Porter_2N_omega_fwd': results['Porter_2N']['omega_fwd'],
        'Porter_2N_omega_ret': results['Porter_2N']['omega_ret'],
        'Porter_4N_omega_fwd': results['Porter_4N']['omega_fwd'],
        'Porter_4N_omega_ret': results['Porter_4N']['omega_ret'],
        'Proell_4N_omega_fwd': results['Proell_4N']['omega_fwd'],
        'Proell_4N_omega_ret': results['Proell_4N']['omega_ret']
    })
    df_omega.to_excel(writer, sheet_name='Omega_Experimental', index=False)
    
    # Sheet 3: Theoretical data
    df_theory = pd.DataFrame({
        'Height_mm': heights,
        'Porter_2N_RPM_theory': results['Porter_2N']['rpm_theory'],
        'Porter_2N_omega_theory': results['Porter_2N']['omega_theory'],
        'Porter_4N_RPM_theory': results['Porter_4N']['rpm_theory'],
        'Porter_4N_omega_theory': results['Porter_4N']['omega_theory'],
        'Proell_4N_RPM_theory': results['Proell_4N']['rpm_theory'],
        'Proell_4N_omega_theory': results['Proell_4N']['omega_theory']
    })
    df_theory.to_excel(writer, sheet_name='Theoretical_Data', index=False)
    
    # Sheet 4: Sensitivity values
    df_sens = pd.DataFrame({
        'Case': ['Porter_2N', 'Porter_4N', 'Proell_4N'],
        'Sensitivity_Forward': [results['Porter_2N']['sens_fwd'], results['Porter_4N']['sens_fwd'], results['Proell_4N']['sens_fwd']],
        'Sensitivity_Return': [results['Porter_2N']['sens_ret'], results['Porter_4N']['sens_ret'], results['Proell_4N']['sens_ret']]
    })
    df_sens.to_excel(writer, sheet_name='Sensitivity', index=False)
    
    # Sheet 5: Insensitiveness coefficients
    df_insens = pd.DataFrame({
        'Height_mm': heights,
        'Porter_2N_Insens': results['Porter_2N']['insens'],
        'Porter_4N_Insens': results['Porter_4N']['insens'],
        'Proell_4N_Insens': results['Proell_4N']['insens']
    })
    df_insens.to_excel(writer, sheet_name='Insensitiveness', index=False)

print(f"✅ Excel file saved: {output_excel}")

# ============================
# Generate Plots
# ============================

output_dir = "Governor_Plots"
os.makedirs(output_dir, exist_ok=True)

# Plot 1: Experimental vs Theoretical comparison
for name in ['Porter_2N', 'Porter_4N', 'Proell_4N']:
    res = results[name]
    heights = res['heights']
    fwd = res['fwd_RPM']
    ret = res['ret_RPM']
    rpm_th = res['rpm_theory']
    
    plt.figure(figsize=(10, 6))
    plt.plot(heights, fwd, 'o-', label='Experimental (Forward)', linewidth=2, markersize=8)
    plt.plot(heights, ret, 's-', label='Experimental (Return)', linewidth=2, markersize=8)
    plt.plot(heights, rpm_th, '^-', label='Theoretical', linewidth=2, markersize=8)
    plt.xlabel('Sleeve Displacement (mm)')
    plt.ylabel('Speed (RPM)')
    plt.title(f'{name} - Experimental vs Theoretical')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{name}_comparison.png'), dpi=300)
    plt.close()

# Plot 2: Sensitivity bar chart
cases_names = ['Porter 2N', 'Porter 4N', 'Proell 4N']
sens_fwd = [results['Porter_2N']['sens_fwd'], results['Porter_4N']['sens_fwd'], results['Proell_4N']['sens_fwd']]
sens_ret = [results['Porter_2N']['sens_ret'], results['Porter_4N']['sens_ret'], results['Proell_4N']['sens_ret']]

x = np.arange(len(cases_names))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, sens_fwd, width, label='Forward', color='royalblue')
bars2 = ax.bar(x + width/2, sens_ret, width, label='Return', color='tomato')
ax.set_xlabel('Governor Type')
ax.set_ylabel('Sensitivity')
ax.set_title('Sensitivity Comparison')
ax.set_xticks(x)
ax.set_xticklabels(cases_names)
ax.legend()
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height:.3f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.3f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Sensitivity_comparison.png'), dpi=300)
plt.close()

# Plot 3: Insensitiveness vs displacement
plt.figure(figsize=(10, 6))
for name in ['Porter_2N', 'Porter_4N', 'Proell_4N']:
    plt.plot(heights, results[name]['insens'], 'o-', label=name, linewidth=2, markersize=8)
plt.xlabel('Sleeve Displacement (mm)')
plt.ylabel('Insensitiveness Coefficient')
plt.title('Insensitiveness vs Displacement')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Insensitiveness.png'), dpi=300)
plt.close()

# Plot 4: Effect of weight on Porter (2N vs 4N)
plt.figure(figsize=(10, 6))
plt.plot(heights, porter_2N_forward_RPM, 'o-', label='Porter 2N (Forward)', linewidth=2)
plt.plot(heights, porter_4N_forward_RPM, 's-', label='Porter 4N (Forward)', linewidth=2)
plt.xlabel('Sleeve Displacement (mm)')
plt.ylabel('Speed (RPM)')
plt.title('Effect of Weight on Porter Governor (Forward)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Porter_weight_effect.png'), dpi=300)
plt.close()

# Plot 5: Porter vs Proell comparison (both 4N)
plt.figure(figsize=(10, 6))
plt.plot(heights, porter_4N_forward_RPM, 'o-', label='Porter 4N (Forward)', linewidth=2)
plt.plot(heights, proell_4N_forward_RPM, 's-', label='Proell 4N (Forward)', linewidth=2)
plt.xlabel('Sleeve Displacement (mm)')
plt.ylabel('Speed (RPM)')
plt.title('Comparison of Porter and Proell (4N)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Porter_vs_Proell_4N.png'), dpi=300)
plt.close()

print(f"✅ All plots saved in '{output_dir}' folder.")
print("="*50)
print("Summary of Results:")
print("-"*50)
for name in ['Porter_2N', 'Porter_4N', 'Proell_4N']:
    res = results[name]
    print(f"{name}:")
    print(f"  Sensitivity (Forward): {res['sens_fwd']:.4f}  ({res['sens_fwd']*100:.2f}%)")
    print(f"  Sensitivity (Return):  {res['sens_ret']:.4f}  ({res['sens_ret']*100:.2f}%)")
    print(f"  Avg Insensitiveness: {np.mean(res['insens']):.4f}")
    print()