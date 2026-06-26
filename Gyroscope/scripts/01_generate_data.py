import pandas as pd

# ============================
# Raw Data for Case 1 (Mass = 0.13245 kg)
# ============================
data_case1 = {
    "ws": [800, 1200, 2100, 2500],      # Rotor speed (rpm)
    "wp_exp": [60, 55, 40, 30],         # Experimental precession speed (rpm)
    "m": [0.13245, 0.13245, 0.13245, 0.13245],  # Mass (kg)
}

# ============================
# Raw Data for Case 2 (Mass = 0.15 kg)
# ============================
data_case2 = {
    "ws": [800, 1200, 2100, 2500],      # Rotor speed (rpm)
    "wp_exp": [85, 80, 60, 40],         # Experimental precession speed (rpm)
    "m": [0.15, 0.15, 0.15, 0.15],      # Mass (kg)
}

# ============================
# Raw Data for Case 3 (Mass = 0.17 kg)
# ============================
data_case3 = {
    "ws": [800, 1200, 2100, 2500],      # Rotor speed (rpm)
    "wp_exp": [70, 65, 50, 45],         # Experimental precession speed (rpm)
    "m": [0.17, 0.17, 0.17, 0.17],      # Mass (kg)
}

# ============================
# Convert to DataFrames and Save as Excel Files
# ============================
df1 = pd.DataFrame(data_case1)
df1.to_excel("case1.xlsx", index=False)

df2 = pd.DataFrame(data_case2)
df2.to_excel("case2.xlsx", index=False)

df3 = pd.DataFrame(data_case3)
df3.to_excel("case3.xlsx", index=False)

# ============================
# Confirmation Message
# ============================
print("All 3 raw Excel files created successfully:")
print("- case1.xlsx")
print("- case2.xlsx")
print("- case3.xlsx")