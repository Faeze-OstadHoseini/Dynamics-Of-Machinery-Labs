# Dynamics of Machinery Labs

## Overview
This repository contains a comprehensive collection of laboratory experiments and analyses for the Dynamics of Machinery course. Each experiment is organized in its own directory with consistent structure, including raw data, analysis scripts, and visual outputs.

## Repository Structure
Dynamics_Of_Machinery_Labs/
├── README.md
├── .gitignore
├── Governor/
│   ├── README.md
│   ├── data/
│   ├── scripts/
│   └── outputs/
├── Gyroscope/
│   ├── README.md
│   ├── data/
│   ├── scripts/
│   └── outputs/
├── CamAndFollower/
│   ├── README.md
│   ├── data/
│   ├── scripts/
│   └── outputs/
├── CentrifugalForce/
│   ├── README.md
│   ├── data/
│   ├── scripts/
│   └── outputs/
├── CoriolisAcceleration/
│   ├── README.md
│   ├── data/
│   ├── scripts/
│   └── outputs/
└── LinearVibration/
    ├── README.md
    ├── data/
    ├── scripts/
    └── outputs/

## Standard Directory Structure

Each experiment follows this standardized structure:

experiment_name/
├── README.md
├── data/
│   └── experiment_raw_data.xlsx
├── scripts/
│   ├── 01_generate_data.py
│   └── 02_analyze_visualize.py
└── outputs/
    ├── experiment_results.xlsx
    └── plots/
        ├── plot1.png
        ├── plot2.png
        └── ...

## List of Experiments

### 1. Governor Test (Governor/)
Analysis of Porter and Proell governors including sensitivity, insensitiveness, and theoretical vs experimental speed comparison.

Key Topics:
- Centrifugal governor operation
- Sensitivity and insensitiveness analysis
- Forward and return stroke characteristics
- Porter vs Proell governor comparison

### 2. Gyroscope Precession (Gyroscope/)
Investigation of gyroscopic precession with different masses and rotor speeds.

Key Topics:
- Gyroscopic precession theory
- Theoretical vs experimental precession speed
- Effect of mass on precession
- Torque and angular velocity relationships

### 3. Cam and Follower Kinematics (CamAndFollower/)
Analysis of four different cam profiles (Cam1-Cam4) including displacement, velocity, and acceleration.

Key Topics:
- Cam follower kinematics
- Numerical differentiation
- Theoretical cam profiles
- Comparative analysis of cam types

### 4. Centrifugal Force (CentrifugalForce/)
Experimental investigation of centrifugal force with varying masses and radii.

Key Topics:
- Centrifugal force theory
- Rotational speed effects
- Mass and radius parameter study
- Experimental vs theoretical comparison

### 5. Coriolis Acceleration (CoriolisAcceleration/)
Study of Coriolis acceleration effects on rotating systems.

Key Topics:
- Coriolis acceleration theory
- Deflection angle measurement
- Experimental vs theoretical analysis
- Parameter effects study

### 6. Linear Vibration (LinearVibration/)
Free vibration analysis of spring-mass-damper systems.

Key Topics:
- Natural frequency analysis
- Damping ratio measurement
- Logarithmic decrement method
- Mass effects on vibration characteristics

## Common Requirements

All experiments require the following Python packages:

pip install pandas numpy matplotlib seaborn openpyxl scipy

Package Details:
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- matplotlib: Plotting and visualization
- seaborn: Statistical data visualization
- openpyxl: Excel file handling
- scipy: Scientific computing (curve fitting, etc.)

## Getting Started

### 1. Clone the Repository
git clone https://github.com/Dynamics-Of-Machinery-Labs/Dynamics_Of_Machinery_Labs.git
cd Dynamics_Of_Machinery_Labs

### 2. Set Up Python Environment
conda create -n dynamics python=3.9
conda activate dynamics
pip install pandas numpy matplotlib seaborn openpyxl scipy

### 3. Run an Experiment
Navigate to the desired experiment directory and run the scripts:

cd Governor/
python scripts/01_generate_data.py
python scripts/02_analyze_visualize.py

## Experiment Workflow

### Step 1: Generate Raw Data
Each experiment has a 01_generate_data.py script that creates the raw data file in the data/ directory.

### Step 2: Analyze and Visualize
The 02_analyze_visualize.py script performs all calculations and generates:
- Processed results in Excel format
- Professional plots in the outputs/plots/ directory

### Step 3: Review Results
- Check outputs/experiment_results.xlsx for detailed calculations
- View plots in outputs/plots/ for visual analysis

## Output Summary

### Excel Files
- Raw Data: Contains original experimental measurements
- Results: Includes all calculations, theoretical values, and error analysis

### Plots
Each experiment generates multiple plot variations:
- Comparison Plots: Experimental vs theoretical
- Error Analysis: Percentage errors and deviations
- Dashboard: Multiple plots in a single figure
- Parameter Effects: Relationships between variables

## Best Practices

### Data Management
- Raw data is never modified; calculations are performed on copies
- All inputs and outputs are clearly labeled
- Missing data is handled appropriately (NaN)

### Code Quality
- English comments for code readability
- Modular functions for reusability
- Consistent naming conventions
- Error handling and validation

### Documentation
- Each experiment has a detailed README
- Results include statistical summaries
- Plots are professionally styled

## Contributing

### Adding a New Experiment
1. Create a new directory following the standard structure
2. Add raw data and scripts
3. Write comprehensive README
4. Generate and include outputs
5. Update this main README

### Code Improvements
- Add new analysis methods
- Improve visualization styles
- Optimize calculations
- Add unit tests

## Common Issues and Solutions

### Missing Data
- Some experiments have missing values (None/NaN)
- Scripts handle missing data appropriately
- Check README for data availability

### Path Issues
- All paths are relative to the script location
- Use os.path.join() for cross-platform compatibility
- Ensure directories exist before saving

### Package Installation
- Use pip install -r requirements.txt if available
- Check environment compatibility
- For scipy issues: conda install scipy

## License
This repository is for educational and research purposes in mechanical engineering laboratory experiments. All code and data are provided as-is for academic use.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026
Maintainer: [Faeze OstadHoseini]
