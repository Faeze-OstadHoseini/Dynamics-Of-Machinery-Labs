# Cam and Follower Kinematic Analysis

## Overview
This laboratory experiment analyzes the kinematic behavior of four different cam profiles (Cam1 to Cam4). The displacement, velocity, and acceleration of the cam follower are calculated both experimentally (using numerical differentiation) and theoretically (using analytical formulas). Results are visualized using multiple professional plot styles.

## Directory Structure
```text
├── CamAndFollower/
│   ├── README.md
│   ├── data/
│   │   ├── Cam1_RawData.xlsx
│   │   ├── Cam2_RawData.xlsx
│   │   ├── Cam3_RawData.xlsx
│   │   └── Cam4_RawData.xlsx
│   ├── scripts/
│   │   ├── 01_generate_data.py
│   │   └── 02_analyze_visualize.py
│   └── outputs/
│       ├── cam_experiment_processed_results.xlsx
│       └── plots/
│           ├── cam_dashboard_dark.png
│           ├── cam_minimalist_white.png
│           ├── cam_comparison_pro.png
│           └── cam_infographic_style.png
```

## Theory

### Cam-Follower Kinematics
For a cam mechanism with constant angular velocity (omega), the follower kinematics are defined by:

- Displacement: x(theta)
- Velocity: v = dx/dt = (dx/dtheta) * omega
- Acceleration: a = dv/dt = (d^2x/dtheta^2) * omega^2

### Numerical Differentiation
Experimental values are computed using numerical differentiation:
- v_approx = gradient(x, theta_rad) * omega
- a_approx = gradient(v_approx, theta_rad) * omega

### Theoretical Models

#### Cam1 (Cycloidal Motion)
x = -19.51 * sin(theta/2)^2

#### Cam2 (Sinusoidal Motion)
x = -9.52 * sin(theta)^2

#### Cam3 (Modified Trapezoidal)
- Rise: 0 to 60 degrees (cycloidal)
- Dwell: 60 to 300 degrees
- Return: 300 to 360 degrees (cycloidal)

#### Cam4 (Complex Harmonic)
x = -13.54 * sin(theta) + 7.49 * sin(theta/2)^2 * sin(theta) (0-180 deg)
x = 7.49 * (360-theta)/180 - 13.32 * sin(theta-180) (180-360 deg)

## Test Cases

| Case | Cam Name | Description |
|------|----------|-------------|
| 1    | Cam1     | Cycloidal motion profile |
| 2    | Cam2     | Sinusoidal motion profile |
| 3    | Cam3     | Modified trapezoidal with dwell |
| 4    | Cam4     | Complex harmonic profile |

## Requirements
pip install pandas numpy matplotlib openpyxl

## Usage

### Step 1: Generate Raw Data Files
python scripts/01_generate_data.py

This will create:
- data/Cam1_RawData.xlsx
- data/Cam2_RawData.xlsx
- data/Cam3_RawData.xlsx
- data/Cam4_RawData.xlsx

### Step 2: Analyze and Visualize
python scripts/02_analyze_visualize.py

This will create:
- outputs/cam_experiment_processed_results.xlsx (Excel with all calculated data)
- outputs/plots/cam_dashboard_dark.png (Dark theme dashboard)
- outputs/plots/cam_minimalist_white.png (Clean minimalist style)
- outputs/plots/cam_comparison_pro.png (Professional comparison)
- outputs/plots/cam_infographic_style.png (Infographic individual profiles)

## Excel Output Structure

Each sheet in the Excel file corresponds to one cam and contains:

| Column | Description | Units |
|--------|-------------|-------|
| Angle (deg) | Cam rotation angle | degrees |
| Theta (rad) | Cam rotation angle | radians |
| Displacement x Raw (mm) | Experimental displacement | mm |
| Displacement x Theoretical (mm) | Theoretical displacement | mm |
| Velocity V Exp Derivative (m/s) | Experimental velocity (numerical) | m/s |
| Velocity V Theoretical (m/s) | Theoretical velocity | m/s |
| Acceleration a Exp Derivative (m/s^2) | Experimental acceleration (numerical) | m/s^2 |
| Acceleration a Theoretical (m/s^2) | Theoretical acceleration | m/s^2 |

## Plot Styles Generated

### 1. Dark Dashboard (cam_dashboard_dark.png)
- Dark theme with 2x2 grid
- All cams compared per kinematic parameter
- Professional dashboard style
- File: cam_dashboard_dark.png

### 2. Minimalist White (cam_minimalist_white.png)
- Clean white background
- 3 stacked plots (displacement, velocity, acceleration)
- Minimal styling with accent colors
- File: cam_minimalist_white.png

### 3. Professional Comparison (cam_comparison_pro.png)
- All cams overlaid on same axes
- Different line styles and markers
- Perfect for report presentations
- File: cam_comparison_pro.png

### 4. Infographic Style (cam_infographic_style.png)
- Individual profile for each cam
- Displacement with filled area
- Acceleration overlay on secondary axis
- Detailed annotations for maximum values
- File: cam_infographic_style.png

## Key Observations

1. Cam1 shows smooth cycloidal motion with symmetric velocity profile
2. Cam2 exhibits sinusoidal displacement with zero acceleration at extremes
3. Cam3 demonstrates constant velocity segments with smooth transitions
4. Cam4 shows complex harmonic motion with multiple inflection points

## Important Notes

- Angular velocity is constant at 0.523 rad/s (5 rad/s)
- All displacement values are in millimeters
- Data points are recorded every 10 degrees (0 to 360 degrees)
- Numerical differentiation uses central difference method

## Contributing
Feel free to modify the code to:
- Adjust angular velocity values
- Add new cam profiles
- Customize plot styles
- Change color schemes

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026
