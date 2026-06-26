import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Constants ---
g = 9.81
R = 0.094
I = 8.55e-5

files = ["case1.xlsx", "case2.xlsx", "case3.xlsx"]

# Set modern style
plt.style.use('seaborn-v0_8-darkgrid')
# Or use: plt.style.use('ggplot') for another nice style


def process_gyro_data(file_name, case_num):
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found!")
        return

    df = pd.read_excel(file_name)

    df["F"] = df["m"] * g
    df["T"] = df["F"] * R

    ws_rad = df["ws"] * (2 * np.pi / 60)

    wp_theo_rad = df["T"] / (I * ws_rad)
    df["wp_theo"] = wp_theo_rad * (60 / (2 * np.pi))

    df["Error_Pct"] = (abs(df["wp_theo"] - df["wp_exp"]) / df["wp_theo"]) * 100

    df_rounded = df.round(2)

    print(f"\n================ Results for Case {case_num} ================")
    print(df_rounded[["ws", "wp_exp", "wp_theo", "Error_Pct"]].to_string(index=False))

    df.to_excel(f"calculated_case{case_num}.xlsx", index=False)

    # --- Modern and beautiful plot ---
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Set background color
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    # Plot with beautiful colors and markers
    line1, = ax.plot(df["ws"], df["wp_theo"], 
                     marker='o', 
                     markersize=8,
                     markerfacecolor='white',
                     markeredgewidth=2,
                     linestyle='-', 
                     linewidth=2.5,
                     color='#2E86AB',  # Beautiful blue
                     label='Theoretical $\omega_p$',
                     zorder=3)
    
    line2, = ax.plot(df["ws"], df["wp_exp"], 
                     marker='s', 
                     markersize=8,
                     markerfacecolor='white',
                     markeredgewidth=2,
                     linestyle='--', 
                     linewidth=2,
                     color='#D64933',  # Beautiful red
                     label='Experimental $\omega_p$',
                     zorder=3)
    
    # Add grid with style
    ax.grid(True, linestyle='--', alpha=0.3, color='gray', linewidth=0.8)
    ax.set_axisbelow(True)  # Grid behind the data
    
    # Set labels with larger font
    ax.set_xlabel('Rotor Speed $\omega_s$ (rpm)', fontsize=12, fontweight='medium', labelpad=10)
    ax.set_ylabel('Precession Speed $\omega_p$ (rpm)', fontsize=12, fontweight='medium', labelpad=10)
    
    # Title with better formatting
    ax.set_title(f'Gyroscopic Precession Analysis - Case {case_num}', 
                 fontsize=14, 
                 fontweight='bold', 
                 pad=15,
                 color='#1a1a1a')
    
    # Smart axis limits
    ax.set_xlim(df["ws"].min() - 200, df["ws"].max() + 200)
    max_val = max(df["wp_theo"].max(), df["wp_exp"].max())
    ax.set_ylim(0, max_val + max_val * 0.1)
    
    # Beautiful legend
    legend = ax.legend(loc='upper left', 
                       frameon=True, 
                       fancybox=True, 
                       shadow=True, 
                       fontsize=10,
                       edgecolor='#cccccc',
                       facecolor='white')
    legend.get_frame().set_alpha(0.9)
    
    # Add value labels on points
    for i, (x, y_theo, y_exp) in enumerate(zip(df["ws"], df["wp_theo"], df["wp_exp"])):
        ax.annotate(f'{y_theo:.0f}', 
                   (x, y_theo), 
                   textcoords="offset points", 
                   xytext=(0, 10), 
                   ha='center',
                   fontsize=8,
                   color='#2E86AB',
                   fontweight='bold')
        
        ax.annotate(f'{y_exp:.0f}', 
                   (x, y_exp), 
                   textcoords="offset points", 
                   xytext=(0, -15), 
                   ha='center',
                   fontsize=8,
                   color='#D64933',
                   fontweight='bold')
    
    # Add a subtle spine color
    for spine in ax.spines.values():
        spine.set_color('#666666')
        spine.set_linewidth(0.8)
    
    # Tight layout
    plt.tight_layout()
    
    # Save with high quality
    plt.savefig(f"gyro_chart_case{case_num}.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"-> Successfully saved: gyro_chart_case{case_num}.png")


for idx, file in enumerate(files, start=1):
    process_gyro_data(file, idx)