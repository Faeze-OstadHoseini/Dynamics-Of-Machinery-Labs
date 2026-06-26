import pandas as pd
import numpy as np


# (Forward)
forward_data = {
    "Height_mm": [5, 10, 15, 20, 25, 30, 35, 40],
    "Porter_2N_RPM": [160, 175, 190, 205, 220, None, None, None],
    "Porter_4N_RPM": [170, 185, 200, 215, 230, None, None, None],
    "Proell_2N_RPM": [80, 95, 110, 125, 140, None, None, None],
    "Proell_4N_RPM": [100, 115, 130, 145, 160, None, None, None]
}

# (Return)
return_data = {
    "Height_mm": [40, 35, 30, 25, 20, 15, 10, 5],
    "Porter_2N_RPM": [None, None, None, None, 220, 205, 190, 175],
    "Porter_4N_RPM": [None, None, None, None, 230, 215, 200, 185],
    "Proell_2N_RPM": [None, None, None, None, 140, 125, 110, 95],
    "Proell_4N_RPM": [None, None, None, None, 160, 145, 130, 115]
}

# ============================================
# DataFrame
# ============================================

df_forward = pd.DataFrame(forward_data)
df_return = pd.DataFrame(return_data)

# Forward and Return Complete data
complete_data = {
    "Height_mm": [],
    "Stroke_Type": [],
    "Porter_2N_RPM": [],
    "Porter_4N_RPM": [],
    "Proell_2N_RPM": [],
    "Proell_4N_RPM": []
}

# add Forward data
for i in range(len(df_forward)):
    if not pd.isna(df_forward.loc[i, "Porter_2N_RPM"]):
        complete_data["Height_mm"].append(df_forward.loc[i, "Height_mm"])
        complete_data["Stroke_Type"].append("Forward")
        complete_data["Porter_2N_RPM"].append(df_forward.loc[i, "Porter_2N_RPM"])
        complete_data["Porter_4N_RPM"].append(df_forward.loc[i, "Porter_4N_RPM"])
        complete_data["Proell_2N_RPM"].append(df_forward.loc[i, "Proell_2N_RPM"])
        complete_data["Proell_4N_RPM"].append(df_forward.loc[i, "Proell_4N_RPM"])

# add Return data
for i in range(len(df_return)):
    if not pd.isna(df_return.loc[i, "Porter_2N_RPM"]):
        complete_data["Height_mm"].append(df_return.loc[i, "Height_mm"])
        complete_data["Stroke_Type"].append("Return")
        complete_data["Porter_2N_RPM"].append(df_return.loc[i, "Porter_2N_RPM"])
        complete_data["Porter_4N_RPM"].append(df_return.loc[i, "Porter_4N_RPM"])
        complete_data["Proell_2N_RPM"].append(df_return.loc[i, "Proell_2N_RPM"])
        complete_data["Proell_4N_RPM"].append(df_return.loc[i, "Proell_4N_RPM"])

df_complete = pd.DataFrame(complete_data)

# ============================================
# Save in multiple sheets
# ============================================

file_name = "Governor_Test_Data.xlsx"

with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    
    # sheet1: Forward Stroke
    df_forward.to_excel(writer, sheet_name='Forward_Stroke', index=False)
    
    # sheet2: Return Stroke
    df_return.to_excel(writer, sheet_name='Return_Stroke', index=False)

    # sheet3: Complete Data
    df_complete.to_excel(writer, sheet_name='Complete_Data', index=False)
    
    # adjust width of columns
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            worksheet.column_dimensions[column_letter].width = adjusted_width

# ============================================
# Represent Output
# ============================================

print("=" * 70)
print("✅ فایل Excel با موفقیت ایجاد شد!")
print(f"📁 نام فایل: {file_name}")
print("=" * 70)

print("\n📊 داده‌های مرحله رفت (Forward):")
print(df_forward.to_string(index=False))

print("\n📊 داده‌های مرحله برگشت (Return):")
print(df_return.to_string(index=False))

print("\n📊 داده‌های کامل ترکیبی:")
print(df_complete.to_string(index=False))

print("\n" + "=" * 70)
print(f"📈 تعداد کل داده‌ها: {len(df_complete)}")
print(f"   - مرحله رفت: {len(df_forward[df_forward['Porter_2N_RPM'].notna()])} نقطه")
print(f"   - مرحله برگشت: {len(df_return[df_return['Porter_2N_RPM'].notna()])} نقطه")
print("=" * 70)