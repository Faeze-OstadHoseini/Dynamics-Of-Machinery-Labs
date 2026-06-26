# Linear Vibration Experiment

## Overview
This laboratory experiment investigates the free vibration characteristics of a linear spring-mass-damper system. The natural frequency, damping ratio, and damped period are measured experimentally and compared with theoretical predictions. The experiment is conducted with different masses and displacement amplitudes.

## Theory

### Free Vibration of a Spring-Mass-Damper System
A linear spring-mass-damper system is governed by the differential equation:

m * x'' + c * x' + k * x = 0

Where:
- m = Mass (kg)
- c = Damping coefficient (Ns/m)
- k = Spring stiffness (N/m)
- x = Displacement (m)

### Natural Frequency
The undamped natural frequency is given by:

omega_n = sqrt(k / m)

### Damped Frequency
The damped natural frequency is given by:

omega_d = omega_n * sqrt(1 - zeta^2)

### Damping Ratio
The damping ratio is defined as:

zeta = c / (2 * m * omega_n)

### Logarithmic Decrement
The logarithmic decrement is related to the damping ratio by:

delta = ln(y1/y2) / sqrt((2*pi)^2 + ln(y1/y2)^2)

## Directory Structure
LinearVibrations/
├── README.md
├── data/
│   └── linear_vibration_raw_data.xlsx
├── scripts/
│   ├── 01_generate_data.py
│   └── 02_analyze_visualize.py
└── outputs/
    ├── linear_vibration_results.xlsx
    └── plots/
        ├── natural_frequency_comparison.png
        ├── error_analysis.png
        ├── damping_analysis.png
        ├── mass_vs_frequency.png
        ├── vibration_dashboard.png
        ├── zeta_vs_error.png
        ├── natural_frequency_vs_mass.png
        ├── omega_n_vs_mass_subplots.png
        └── omega_n_comparison_table.png

## Test Cases

The experiment includes 6 test cases with different masses and displacement amplitudes:

| State | Mass (kg) | y1 (mm) | y2 (mm) | x (mm) |
|-------|-----------|---------|---------|--------|
| a     | 0.940     | 33      | 23      | 11.0   |
| b     | 0.940     | 55      | 42      | 12.5   |
| c     | 1.144     | 29      | 15      | 12.3   |
| d     | 1.144     | 42      | 30      | 13.0   |
| e     | 1.348     | 15      | 5       | 18.0   |
| f     | 1.348     | 28      | 19      | 13.0   |

## Requirements

Install the required packages:

pip install pandas numpy matplotlib openpyxl scipy

## Usage

### Step 1: Generate Raw Data Files
python scripts/01_generate_data.py

This will create:
- data/linear_vibration_raw_data.xlsx

### Step 2: Analyze and Visualize
python scripts/02_analyze_visualize.py

This will create:
- outputs/linear_vibration_results.xlsx
- outputs/plots/natural_frequency_comparison.png
- outputs/plots/error_analysis.png
- outputs/plots/damping_analysis.png
- outputs/plots/mass_vs_frequency.png
- outputs/plots/vibration_dashboard.png
- outputs/plots/zeta_vs_error.png
- outputs/plots/natural_frequency_vs_mass.png
- outputs/plots/omega_n_vs_mass_subplots.png
- outputs/plots/omega_n_comparison_table.png

## Calculations Performed

The script performs the following calculations:

1. Damping ratio from logarithmic decrement:
   zeta = ln(y1/y2) / sqrt((2*pi)^2 + ln(y1/y2)^2)

2. Experimental damped frequency:
   omega_d_exp = 2 * pi / Td

3. Experimental natural frequency:
   omega_n_exp = omega_d_exp / sqrt(1 - zeta^2)

4. Theoretical natural frequency (from report):
   omega_n_theo = [14.700, 14.700, 13.326, 13.326, 12.277, 12.277]

5. Error percentage:
   Error = abs(omega_n_exp - omega_n_theo) / omega_n_theo * 100

6. Damping coefficient:
   c = 2 * zeta * m * omega_n_exp

7. Logarithmic decrement:
   delta = zeta * 2 * pi / sqrt(1 - zeta^2)

8. Calculated stiffness:
   k_calc = m * omega_n_exp^2

9. Theoretical damped frequency:
   omega_d_theo = omega_n_exp * sqrt(1 - zeta^2)

10. Error in damped frequency:
    omega_d_error = abs(omega_d_exp - omega_d_theo) / omega_d_theo * 100

## Plots Generated

### 1. Natural Frequency Comparison (natural_frequency_comparison.png)
- Bar chart comparing experimental and theoretical natural frequencies
- Blue bars: Experimental values
- Red bars: Theoretical values

### 2. Error Analysis (error_analysis.png)
- Two subplots:
  - Error in natural frequency measurement
  - Difference between theoretical and experimental frequencies

### 3. Damping Analysis (damping_analysis.png)
- Two subplots:
  - Damping ratio for each state
  - Damped period for each state

### 4. Mass vs Frequency (mass_vs_frequency.png)
- Scatter plot showing effect of mass on natural frequency
- Bubble size represents damping ratio
- Color represents error percentage

### 5. Complete Dashboard (vibration_dashboard.png)
- 4 subplots combining all analysis
- Natural frequency comparison
- Error analysis
- Damping parameters
- Mass vs frequency relationship

### 6. Zeta vs Error (zeta_vs_error.png)
- Scatter plot showing relationship between damping ratio and measurement error
- Color represents mass value

### 7. Natural Frequency vs Mass (natural_frequency_vs_mass.png)
- Combined plot showing both experimental and theoretical ωn vs mass
- Error bars showing difference between experimental and theoretical
- Second y-axis showing displacement
- Power law fit for theoretical data

### 8. Omega n vs Mass Subplots (omega_n_vs_mass_subplots.png)
- Two separate subplots:
  - Experimental ωn vs mass with linear fit
  - Theoretical ωn vs mass with linear fit

### 9. Comparison Table (omega_n_comparison_table.png)
- Table showing comparison of experimental and theoretical values
- Color-coded error column:
  - Green: Error < 10%
  - Yellow: Error 10-20%
  - Red: Error > 20%

## Results Summary

### Natural Frequency Statistics
- Mean experimental: ~11.68 rad/s
- Mean theoretical: ~13.42 rad/s
- Mean error: ~13.16%
- Error range: 4.99% to 30.48%

### Damping Statistics
- Mean damping ratio: 0.0816
- Mean damped period: 0.5685 s
- Mean damping coefficient: ~1.856 Ns/m

### Mass Effects
- Higher mass generally results in lower natural frequency
- Higher damping ratio correlates with higher mass
- Maximum error occurs at highest mass and displacement

## Key Observations

1. Error increases with mass and displacement amplitude
2. State e shows the highest error (30.48%) and highest damping ratio (0.1722)
3. State b has the lowest damping ratio (0.0429) but shows significant error
4. Experimental natural frequencies are consistently lower than theoretical values
5. Damping ratio affects both the natural frequency and measurement accuracy

## Important Notes

- State b has missing stiffness (k) and velocity (v) data
- All measurements are taken at room temperature
- Theoretical calculations assume ideal spring behavior
- Damping is assumed to be viscous (linear)

## Troubleshooting

### If you get "no module named scipy":
pip install scipy

### If using conda environment:
conda install scipy

### If you want to skip scipy installation:
Comment out lines 410-420 in 02_analyze_visualize.py (the curve_fit section)

## Contributing
Feel free to modify the code to:
- Add more test cases
- Change mass or stiffness values
- Customize plot styles
- Add additional analysis

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026