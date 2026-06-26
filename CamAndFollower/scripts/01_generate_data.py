import pandas as pd
import numpy as np

# 1. Define angles from 0 to 360 degrees (step 10)
theta = np.arange(0, 361, 10)

# Constant angular velocity w = 0.523 rad/s
omega = np.full_like(theta, 0.523, dtype=float)

# 2. Exact displacement x (mm) extracted from the experimental PDF report
x_cam1 = [0, -0.28, -0.60, -1.36, -2.33, -3.56, -4.88, -6.35, -7.87, -9.58, -11.45, -13.18, -14.54, -15.78, -16.95, -17.9, -18.74, -19.36, -19.51, -19.34, -18.88, -18.14, -17.19, -15.91, -14.49, -12.79, -10.88, -9.19, -7.04, -5.17, -3.71, -2.3, -1.17, -0.34, 0.36, 0.77, 0.86]

x_cam2 = [0, -0.73, -1.53, -2.75, -4.22, -5.67, -7.17, -8.37, -9.14, -9.52, -9.34, -8.70, -7.86, -6.57, -5.19, -3.58, -2.06, -0.54, 0.16, -0.13, -1.39, -2.79, -4.22, -5.75, -7, -8.39, -8.86, -9.11, -8.88, -8.29, -7.26, -6.02, -4.33, -2.75, -1.03, -0.12, 0.39]

x_cam3 = [0, -1.51, -4.90, -11.56, -14.93, -16.64, -17.33, -17.10, -16.20, -15.27, -14.48, -13.49, -12.66, -11.87, -11.18, -10.62, -10.07, -9.83, -9.80, -9.91, -10.21, -10.66, -11.31, -11.98, -12.85, -13.78, -14.69, -15.38, -16.23, -16.91, -17.23, -16.62, -15.04, -12.48, -8.12, -2.19, 0]

x_cam4 = [0, -0.21, -0.95, -2.20, -4.10, -6.45, -8.49, -11.57, -13.33, -13.54, -12.71, -10, -6.84, -2.95, 0.92, 3.33, 5.79, 7.16, 7.49, 6.85, 5.66, 3.69, 0.13, -3.2, -6.72, -10.27, -12.78, -13.32, -12.79, -10.91, -8.52, -6.16, -3.87, -2.41, -0.80, -0.22, 0]

# Dictionary to hold data for iteration
cams_data = {
    "Cam1": x_cam1,
    "Cam2": x_cam2,
    "Cam3": x_cam3,
    "Cam4": x_cam4
}

# 3. Create and save 4 separate Excel files
for cam_name, x_values in cams_data.items():

    # Create a structured DataFrame
    df = pd.DataFrame({
        "Angle (deg)": theta,
        "Displacement x (mm)": x_values,
        "Angular Velocity w (rad/s)": omega
    })

    # Generate file name and save
    file_name = f"{cam_name}_RawData.xlsx"
    df.to_excel(file_name, index=False)

    print(f"Successfully created: {file_name}")

print("All 4 Excel files have been generated!")