# Governor Test Data Analysis

## Overview
This project processes and organizes experimental data from governor testing (Porter and Proell governors) under different load conditions (2N and 4N). The data includes forward and return stroke measurements at various sleeve displacements.

## Project Structure
.
├── Governor_Test_Data.xlsx    # Output Excel file with all data
├── Governor_Results.xlsx      # Full analysis results (optional)
├── Governor_Plots/            # Generated plots (optional)
└── README.md                  # This file

## Features
- Data Processing: Organizes raw experimental data into structured DataFrames
- Multi-sheet Excel Export: Creates an Excel file with three organized sheets:
  - Forward_Stroke: Data collected during forward (increasing) stroke
  - Return_Stroke: Data collected during return (decreasing) stroke
  - Complete_Data: Combined dataset with stroke type identification
- Auto-formatting: Automatically adjusts column widths for better readability
- Data Validation: Handles missing values (None/NaN) appropriately

## Data Description

### Test Parameters
- Governor Types: Porter and Proell
- Load Conditions: 2N and 4N
- Sleeve Displacements: 5mm to 40mm (step: 5mm)
- Stroke Types: Forward (increasing speed) and Return (decreasing speed)

### Data Structure
| Column | Description |
|--------|-------------|
| Height_mm | Sleeve displacement in millimeters |
| Stroke_Type | "Forward" or "Return" (Complete_Data only) |
| Porter_2N_RPM | Porter governor speed at 2N load (RPM) |
| Porter_4N_RPM | Porter governor speed at 4N load (RPM) |
| Proell_2N_RPM | Proell governor speed at 2N load (RPM) |
| Proell_4N_RPM | Proell governor speed at 4N load (RPM) |

## Requirements
pip install pandas numpy openpyxl

## Usage

### 1. Run the Script
python governor_data_processor.py

### 2. Expected Output
======================================================================
Excel file created successfully!
File name: Governor_Test_Data.xlsx
======================================================================

Forward Stroke Data:
Height_mm  Porter_2N_RPM  Porter_4N_RPM  Proell_2N_RPM  Proell_4N_RPM
        5            160            170             80            100
       10            175            185             95            115
       15            190            200            110            130
       20            205            215            125            145
       25            220            230            140            160

Return Stroke Data:
Height_mm  Porter_2N_RPM  Porter_4N_RPM  Proell_2N_RPM  Proell_4N_RPM
       40            NaN            NaN            NaN            NaN
       35            NaN            NaN            NaN            NaN
       30            NaN            NaN            NaN            NaN
       25            NaN            NaN            NaN            NaN
       20            220            230            140            160
       15            205            215            125            145
       10            190            200            110            130
        5            175            185             95            115

### 3. Output Files
- Governor_Test_Data.xlsx: Excel workbook with all processed data
- Console Output: Summary statistics and data preview

## Sample Data Points

### Forward Stroke (Increasing Displacement)
| Height (mm) | Porter 2N (RPM) | Porter 4N (RPM) | Proell 2N (RPM) | Proell 4N (RPM) |
|-------------|-----------------|-----------------|-----------------|-----------------|
| 5           | 160             | 170             | 80              | 100             |
| 10          | 175             | 185             | 95              | 115             |
| 15          | 190             | 200             | 110             | 130             |
| 20          | 205             | 215             | 125             | 145             |
| 25          | 220             | 230             | 140             | 160             |

### Return Stroke (Decreasing Displacement)
| Height (mm) | Porter 2N (RPM) | Porter 4N (RPM) | Proell 2N (RPM) | Proell 4N (RPM) |
|-------------|-----------------|-----------------|-----------------|-----------------|
| 20          | 220             | 230             | 140             | 160             |
| 15          | 205             | 215             | 125             | 145             |
| 10          | 190             | 200             | 110             | 130             |
| 5           | 175             | 185             | 95              | 115             |

## Key Observations
1. Load Effect: Higher load (4N) results in lower operating speeds compared to 2N
2. Governor Type: Proell governors operate at significantly lower speeds than Porter governors
3. Hysteresis: Speed values differ between forward and return strokes at the same displacement
4. Missing Data: Return stroke data is available only for 20mm and below displacements

## Notes
- Missing data points are represented as None (NaN in Excel)
- The return stroke data is recorded in descending height order
- All speed measurements are in RPM (Revolutions Per Minute)

## Contributing
Feel free to modify the code to:
- Add more governor types or load conditions
- Include theoretical calculations
- Generate visualizations (plots)
- Implement sensitivity and insensitiveness analysis

## License
This project is for educational and research purposes in mechanical engineering laboratory experiments.

## Contact
For questions or improvements, please refer to the laboratory instructor or project supervisor.

---
Last Updated: June 2026