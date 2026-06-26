# Governor Test Data Analysis

## Overview
This laboratory experiment processes and organizes experimental data from governor testing (Porter and Proell governors) under different load conditions (2N and 4N). The data includes forward and return stroke measurements at various sleeve displacements.

## Directory Structure
Governor/
├── README.md
├── data/
│   └── governor_Test_data.xlsx
├── scripts/
│   ├── 01_data_processor.py
│   └── 02_analysis_visualization.py
└── outputs/
    ├── Governor_Test_Data.xlsx
    ├── Governor_Results.xlsx
    └── plots/
        ├── Insensitiveness.png
        ├── Porter_2N_comparison.png
        ├── Porter_4N_comparison.png
        ├── Porter_vs_proell.png
        ├── Porter_weight_effect.png
        ├── Proell_4N_comparison.png
        └── Sensitivity_comparison.png

## Theory

### Governor Operation
A centrifugal governor is a device that uses rotating masses to regulate the speed of an engine. As the engine speed increases, the masses move outward, which adjusts the throttle or fuel supply to maintain a constant speed.

### Sensitivity
Sensitivity is a measure of how responsive the governor is to speed changes:

Sensitivity = (N2 - N1) / ((N2 + N1) / 2)

Where:
- N1 = Speed at minimum displacement (5mm)
- N2 = Speed at maximum displacement (40mm)

### Insensitiveness
Insensitiveness is the range of speed over which the governor does not respond due to friction:

Insensitiveness = (omega_up - omega_down) / ((omega_up + omega_down) / 2)

### Porter Governor
The Porter governor has a central sleeve weight that adds to the centrifugal force. The theoretical speed is calculated by:

omega^2 = (g * tan(theta)) / (h * tan(theta) + c) * (1 + (1/(2m)) * (1 + tan(phi)/tan(theta)))

### Proell Governor
The Proell governor has an additional linkage that modifies the effective mass distribution. The theoretical speed is calculated using the geometry of the linkage system.

## Test Cases

| Case | Governor Type | Load (N) | Description |
|------|---------------|----------|-------------|
| 1    | Porter        | 2N       | Porter governor with 2N load |
| 2    | Porter        | 4N       | Porter governor with 4N load |
| 3    | Proell        | 4N       | Proell governor with 4N load |

### Experimental Data
Sleeve displacements: 5, 10, 15, 20, 25, 30, 35, 40 mm

| Displacement (mm) | Porter 2N (RPM) | Porter 4N (RPM) | Proell 4N (RPM) |
|-------------------|-----------------|-----------------|-----------------|
| 5                 | 182             | 151             | 94              |
| 10                | 190             | 156             | 96              |
| 15                | 196             | 159             | 99              |
| 20                | 203             | 165             | 103             |
| 25                | 208             | 168             | 106             |
| 30                | 215             | 174             | 108             |
| 35                | 223             | 181             | 110             |
| 40                | 226             | 187             | 115             |

## Requirements

pip install pandas numpy matplotlib seaborn openpyxl

## Usage

### Step 1: Generate Raw Data Files
python scripts/01_data_processor.py

This will create:
- data/governor_Test_data.xlsx

### Step 2: Analyze and Visualize
python scripts/02_analysis_visualization.py

This will create:
- outputs/Governor_Test_Data.xlsx (Organized experimental data)
- outputs/Governor_Results.xlsx (Full analysis with calculations)
- outputs/plots/Insensitiveness.png
- outputs/plots/Porter_2N_comparison.png
- outputs/plots/Porter_4N_comparison.png
- outputs/plots/Porter_vs_proell.png
- outputs/plots/Porter_weight_effect.png
- outputs/plots/Proell_4N_comparison.png
- outputs/plots/Sensitivity_comparison.png

## Calculations Performed

The script performs the following calculations:

1. Convert RPM to rad/s:
   omega = RPM * (2 * pi / 60)

2. Sensitivity:
   Sensitivity = (N2 - N1) / ((N2 + N1) / 2)

3. Insensitiveness:
   Insensitiveness = abs(omega_up - omega_down) / ((omega_up + omega_down) / 2)

4. Theoretical speed for Porter governor:
   omega = sqrt((g * tan(theta)) / (h * tan(theta) + c) * (1 + (1/(2m)) * (1 + tan(phi)/tan(theta))))

5. Theoretical speed for Proell governor:
   Using geometric relationships of the linkage system

6. Error percentage:
   Error = abs(omega_theo - omega_exp) / omega_theo * 100

## Plots Generated

### 1. Porter 2N Comparison (Porter_2N_comparison.png)
- Comparison of experimental forward, return, and theoretical speeds for Porter 2N
- Blue circles: Experimental Forward
- Red squares: Experimental Return
- Green triangles: Theoretical

### 2. Porter 4N Comparison (Porter_4N_comparison.png)
- Comparison of experimental forward, return, and theoretical speeds for Porter 4N
- Blue circles: Experimental Forward
- Red squares: Experimental Return
- Green triangles: Theoretical

### 3. Proell 4N Comparison (Proell_4N_comparison.png)
- Comparison of experimental forward, return, and theoretical speeds for Proell 4N
- Blue circles: Experimental Forward
- Red squares: Experimental Return
- Green triangles: Theoretical

### 4. Sensitivity Comparison (Sensitivity_comparison.png)
- Bar chart comparing sensitivity for all cases
- Forward and return sensitivity side by side
- Values displayed on top of bars

### 5. Insensitiveness (Insensitiveness.png)
- Line plot showing insensitiveness coefficient vs displacement
- All three cases overlaid for comparison

### 6. Porter Weight Effect (Porter_weight_effect.png)
- Comparison of Porter 2N and 4N forward speeds
- Shows effect of increased load on governor performance

### 7. Porter vs Proell (Porter_vs_proell.png)
- Comparison of Porter and Proell governors (both 4N)
- Shows difference in operating characteristics

## Results Summary

### Sensitivity Analysis
| Case | Forward Sensitivity | Return Sensitivity |
|------|--------------------|--------------------|
| Porter 2N | ~21.6% | ~24.7% |
| Porter 4N | ~21.4% | ~22.0% |
| Proell 4N | ~20.1% | ~22.4% |

### Insensitiveness Analysis
| Case | Average Insensitiveness |
|------|------------------------|
| Porter 2N | ~0.022 |
| Porter 4N | ~0.025 |
| Proell 4N | ~0.019 |

## Key Observations

1. Higher load (4N) results in lower operating speeds compared to 2N
2. Proell governors operate at significantly lower speeds than Porter governors
3. Speed values differ between forward and return strokes (hysteresis effect)
4. Sensitivity decreases with increased load
5. Proell governor shows better sensitivity characteristics
6. Theoretical values closely match experimental results for most cases

## Important Notes

- All speed measurements are in RPM (Revolutions Per Minute)
- Theoretical calculations use the provided geometric parameters
- Return stroke data is recorded in descending displacement order
- Insensitiveness is calculated using angular velocities (rad/s)

## Contributing
Feel free to modify the code to:
- Add more governor types or load conditions
- Adjust geometric parameters
- Customize plot styles
- Add additional analysis

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026