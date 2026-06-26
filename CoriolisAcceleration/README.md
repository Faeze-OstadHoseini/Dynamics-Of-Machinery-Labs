# Coriolis Acceleration Experiment

## Overview
This laboratory experiment investigates the Coriolis acceleration effect on a rotating system. The Coriolis force is a fictitious force that acts on objects in motion within a rotating reference frame. The angle of deflection is measured experimentally and compared with theoretical predictions.

## Theory

### Coriolis Acceleration
When an object moves with velocity v_rel in a rotating frame with angular velocity omega, it experiences a Coriolis acceleration:

a_c = 2 * omega * v_rel

Where:
- a_c = Coriolis acceleration (m/s^2)
- omega = Angular velocity (rad/s)
- v_rel = Relative velocity (m/s)

### Deflection Angle
The deflection angle due to Coriolis acceleration is given by:

theta = arctan(a_c / (omega^2 * r))

Where:
- theta = Deflection angle (rad)
- r = Radius of rotation (m)

## Directory Structure
coriolis_acceleration/
├── README.md
├── data/
│   └── coriolis_raw_data.xlsx
├── scripts/
│   ├── 01_generate_data.py
│   └── 02_analyze_visualize.py
└── outputs/
    ├── coriolis_results.xlsx
    └── plots/
        ├── coriolis_angle_comparison.png
        ├── coriolis_error.png
        ├── coriolis_acceleration.png
        ├── coriolis_relationship.png
        └── coriolis_dashboard.png

## Test Cases

The experiment includes 5 test cases at different rotational speeds:

| Test | Omega (rpm) | Delta_x (m) | v_rel (m/s) | a_coriolis (m/s^2) |
|------|-------------|-------------|-------------|-------------------|
| 1    | 20          | 0.050       | 2.356       | 9.870             |
| 2    | 24          | 0.062       | 2.280       | 11.461            |
| 3    | 28          | 0.075       | 2.199       | 12.896            |
| 4    | 33          | 0.095       | 2.046       | 14.142            |
| 5    | 35          | 0.100       | 2.062       | 15.113            |

## Requirements

pip install pandas numpy matplotlib openpyxl

## Usage

### Step 1: Generate Raw Data Files
python scripts/01_generate_data.py

This will create:
- data/coriolis_raw_data.xlsx

### Step 2: Analyze and Visualize
python scripts/02_analyze_visualize.py

This will create:
- outputs/coriolis_results.xlsx
- outputs/plots/coriolis_angle_comparison.png
- outputs/plots/coriolis_error.png
- outputs/plots/coriolis_acceleration.png
- outputs/plots/coriolis_relationship.png
- outputs/plots/coriolis_dashboard.png

## Calculations Performed

The script performs the following calculations:

1. Convert RPM to rad/s:
   omega_rad = omega_rpm * (2 * pi / 60)

2. Theoretical Coriolis acceleration:
   a_c_theo = 2 * omega * v_rel

3. Error in angle measurement:
   Error = (abs(theta_exp - theta_theo) / theta_theo) * 100

4. Error in Coriolis acceleration:
   Error = (abs(a_c_exp - a_c_theo) / a_c_theo) * 100

5. Ratio of experimental to theoretical angle:
   Ratio = theta_exp / theta_theo

## Plots Generated

### 1. Angle Comparison (coriolis_angle_comparison.png)
- Scatter plot comparing experimental and theoretical angles
- Blue circles: Experimental angles
- Red squares: Theoretical angles

### 2. Error Analysis (coriolis_error.png)
- Bar chart showing percentage error for each test
- Blue dashed line: Mean error

### 3. Coriolis Acceleration (coriolis_acceleration.png)
- Two subplots:
  - Measured vs theoretical acceleration
  - Error analysis for acceleration

### 4. Relationship Analysis (coriolis_relationship.png)
- Two subplots:
  - Angle vs rotational speed (experimental and theoretical)
  - Experimental to theoretical ratio

### 5. Complete Dashboard (coriolis_dashboard.png)
- 4 subplots combining all analysis

## Results Summary

### Angle Statistics
- Mean experimental: ~0.30 rad
- Mean theoretical: ~0.27 rad
- Mean error: ~6.69%
- Error range: 1.11% to 12.76%

### Coriolis Acceleration Statistics
- Mean measured: ~12.70 m/s^2
- Mean theoretical: ~12.70 m/s^2
- Mean error: ~0.01%

### Ratio Analysis
- Mean Exp/Theo ratio: ~1.07
- Range: 0.99 to 1.13

## Key Observations

1. Experimental angles are slightly higher than theoretical at higher speeds
2. Error increases with rotational speed (from 1.1% at 20 rpm to 12.8% at 33 rpm)
3. Coriolis acceleration increases linearly with rotational speed
4. The experimental/theoretical ratio is close to 1 at low speeds
5. Higher speeds show more deviation due to increased measurement uncertainty

## Important Notes

- All measurements are taken at room temperature
- System friction is assumed negligible
- The theoretical model assumes ideal conditions
- Delta_x is the displacement of the mass along the rotating arm

## Contributing
Feel free to modify the code to:
- Add more test cases
- Change speed ranges
- Customize plot styles
- Add additional analysis

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026