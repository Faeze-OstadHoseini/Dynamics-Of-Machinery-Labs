# Centrifugal Force Experiment

## Overview
This laboratory experiment investigates the relationship between centrifugal force and rotational speed using a centrifugal force apparatus. Two different experimental configurations (omega1 and omega2) are tested with varying masses, radii, and distances. Theoretical values are calculated and compared with experimental measurements.

## Directory Structure
centrifugal_force/
├── README.md
├── data/
│   └── centrifugal_force_raw_data.xlsx
├── scripts/
│   ├── 01_generate_data.py
│   └── 02_analyze_visualize.py
└── outputs/
    ├── centrifugal_force_results.xlsx
    └── plots/
        ├── omega1_comparison.png
        ├── omega2_comparison.png
        ├── omega1_error.png
        ├── omega2_error.png
        ├── centrifugal_dashboard.png
        └── parameter_effects.png

## Theory

### Centrifugal Force
When a mass rotates around a central axis, it experiences a centrifugal force directed outward. The relationship between rotational speed and centrifugal force is:

F_c = m * r * omega^2

Where:
- F_c = Centrifugal force (N)
- m = Mass (kg)
- r = Radius of rotation (m)
- omega = Angular velocity (rad/s)

### Experimental Configurations

#### Case 1 (omega1)
The system is configured such that:
omega1 = sqrt(((b/a) * mb * g) / (r * ma * g))

Simplifying:
omega1 = sqrt((b/a) * mb / (r * ma))

#### Case 2 (omega2)
The system is configured such that:
omega2 = sqrt((ma * g) / (r * mb * g))

Simplifying:
omega2 = sqrt(ma / (r * mb))

### Parameters
| Parameter | Description | Units |
|-----------|-------------|-------|
| ma | Mass A | N |
| mb | Mass B | N |
| r | Radius of rotation | m |
| a | Distance from center to mass A | m |
| b | Distance from center to mass B | m |
| omega1 | Angular velocity (Case 1) | rad/s |
| omega2 | Angular velocity (Case 2) | rad/s |

## Test Cases

The experiment includes 12 test cases with varying parameters:

| Test | ma (N) | mb (N) | r (m) | a (m) | b (m) |
|------|--------|--------|-------|-------|-------|
| 1    | 0.3    | 0.3    | 0.1   | 0.05  | 0.07  |
| 2    | 0.3    | 0.6    | 0.1   | 0.05  | 0.07  |
| 3    | 0.3    | 0.3    | 0.1   | 0.05  | 0.05  |
| 4    | 0.3    | 0.6    | 0.1   | 0.05  | 0.05  |
| 5    | 0.3    | 0.3    | 0.18  | 0.05  | 0.07  |
| 6    | 0.3    | 0.6    | 0.18  | 0.05  | 0.07  |
| 7    | 0.3    | 0.3    | 0.18  | 0.05  | 0.05  |
| 8    | 0.3    | 0.6    | 0.18  | 0.05  | 0.05  |
| 9    | 0.3    | 0.3    | 0.18  | 0.05  | 0.07  |
| 10   | 0.3    | 0.6    | 0.18  | 0.05  | 0.07  |
| 11   | 0.3    | 0.3    | 0.18  | 0.05  | 0.05  |
| 12   | 0.3    | 0.6    | 0.18  | 0.05  | 0.05  |

## Requirements

Install the required packages:

pip install pandas numpy matplotlib openpyxl

## Usage

### Step 1: Generate Raw Data Files
Run the first script to create the initial Excel files:

python scripts/01_generate_data.py

This will create:
- data/centrifugal_force_raw_data.xlsx

### Step 2: Analyze and Visualize
Run the second script to process data and generate plots:

python scripts/02_analyze_visualize.py

This will create:
- outputs/centrifugal_force_results.xlsx (Calculated results)
- outputs/plots/omega1_comparison.png
- outputs/plots/omega2_comparison.png
- outputs/plots/omega1_error.png
- outputs/plots/omega2_error.png
- outputs/plots/centrifugal_dashboard.png
- outputs/plots/parameter_effects.png

## Calculations Performed

The script performs the following calculations:

1. Convert RPM to rad/s:
   omega_rad = omega_rpm * (2 * pi / 60)

2. Calculate (b/a)*mb:
   (b/a)*mb = (b / a) * mb

3. Calculate 1/r and 1/ma

4. Theoretical omega1:
   omega1_theo = sqrt((b/a) * mb / (r * ma))

5. Theoretical omega2:
   omega2_theo = sqrt(ma / (r * mb))

6. Error Percentage:
   Error = (abs(theoretical - experimental) / theoretical) * 100

## Plots Generated

### 1. Omega1 Comparison (omega1_comparison.png)
- Scatter plot comparing experimental and theoretical omega1 values
- Blue circles: Experimental values
- Red squares: Theoretical values

### 2. Omega2 Comparison (omega2_comparison.png)
- Scatter plot comparing experimental and theoretical omega2 values
- Green circles: Experimental values
- Orange squares: Theoretical values

### 3. Omega1 Error Analysis (omega1_error.png)
- Bar chart showing percentage error for each test
- Blue dashed line: Mean error

### 4. Omega2 Error Analysis (omega2_error.png)
- Bar chart showing percentage error for each test (only available tests)
- Blue dashed line: Mean error

### 5. Complete Dashboard (centrifugal_dashboard.png)
- 4 subplots combining all analysis:
  - omega1 comparison
  - omega2 comparison
  - omega1 error analysis
  - omega2 error analysis

### 6. Parameter Effects (parameter_effects.png)
- 4 subplots showing effect of parameters:
  - Effect of (b/a)*mb on omega1
  - Effect of 1/r on omega1
  - Effect of ma on omega2
  - Effect of 1/r on omega2

## Results Summary

### Omega1 Statistics
- Mean experimental: ~13.5 rad/s
- Mean theoretical: ~3.2 rad/s
- Mean error: ~300%
- Error range: 220% to 371%

### Omega2 Statistics
- Mean experimental: ~5.0 rad/s
- Mean theoretical: ~1.9 rad/s
- Mean error: ~185%
- Error range: 124% to 282%

## Key Observations

1. Theoretical values are significantly lower than experimental values
2. Higher mass (mb) results in higher rotational speeds
3. Larger radius (r) results in lower rotational speeds
4. Error percentages are consistent across similar configurations
5. Some tests (3, 7, 11) have missing omega2 data

## Notes

- Omega2 data is not available for tests with ma = mb (tests 3, 7, 11)
- All experimental speeds are measured in RPM and converted to rad/s
- Theoretical calculations assume ideal conditions (no friction, perfect geometry)

## Contributing
Feel free to modify the code to:
- Add more test cases
- Change mass or geometry parameters
- Customize plot styles
- Add additional analysis

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026