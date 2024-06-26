import os
import pandas as pd
import re
import csv

script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the input and output directories relative to the script location
input_path = os.path.join(script_directory, '../input')
output_path = os.path.join(script_directory, '../processed')

# Check and create the processed directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Load data from Excel files
metabolite_data_excel = pd.read_excel(f'{input_path}/metabolite_data.xlsx')
meta_data_excel = pd.read_excel(f'{input_path}/meta_data.xlsx')
master_data_excel = pd.read_excel(f'{input_path}/master_data.xlsx')

# Number of patients based on the data
NUM_PATIENTS_METABOLITE_DATA = metabolite_data_excel.shape[0] - 5
NUM_PATIENTS_META_DATA = meta_data_excel.shape[0] - 1
NUM_PATIENTS_MASTER_DATA = master_data_excel.shape[0]

# Processing data
patient_ids = []
for i in range(NUM_PATIENTS_METABOLITE_DATA):
    patient_id = metabolite_data_excel.iloc[i + 5, 1]
    if isinstance(patient_id, (int, float)) and patient_id < 10000:
        patient_id = int(patient_id)
        patient_ids.append(patient_id)

meta_pheno_dict = {}
vial_id_to_patient_id = {}
patients_with_two_vials = []

for i in range(NUM_PATIENTS_META_DATA):
    patient_id = meta_data_excel.iloc[i + 1, 2]
    if patient_id in patient_ids:
        meta_pheno_dict[patient_id] = meta_data_excel.iloc[i + 1, 7].lower()
        vial_id = int(re.sub(r'[^0-9]', '', meta_data_excel.iloc[i + 1, 0]))
        if vial_id in vial_id_to_patient_id:
            patient_1 = vial_id_to_patient_id[vial_id]
            patients_with_two_vials.append(int(patient_id))
            patients_with_two_vials.append(int(patient_1))
            del vial_id_to_patient_id[vial_id]
        else:
            vial_id_to_patient_id[vial_id] = int(patient_id)

valid_everything = []

for i in range(NUM_PATIENTS_MASTER_DATA):
    vial_id = int(master_data_excel.iloc[i, 0])
    if vial_id in vial_id_to_patient_id:
        patient_id = vial_id_to_patient_id[vial_id]
        phenotype = master_data_excel.iloc[i, 1].lower()
        if phenotype == "mam":
            phenotype = "moderate acute malnutrition"
        elif phenotype == "marasmic kwashiorkor":
            phenotype = "marasmus kwashiorkor"
        if meta_pheno_dict[patient_id] == phenotype:
            valid_everything.append(patient_id)

not_in_master = [id for id in vial_id_to_patient_id.values() if id not in valid_everything]

# Writing summary file
file_path = f'{output_path}/patients_summary.txt'
with open(file_path, 'w') as file:
    file.write("Patients in master with one vial and matching phenotypes\n")
    for id in valid_everything:
        file.write(str(id) + '\n')
    file.write("\nPatients with two vials\n")
    for id in patients_with_two_vials:
        file.write(str(id) + '\n')
    file.write("\nPatients not in master\n")
    for id in not_in_master:
        file.write(str(id) + '\n')

print(f"File has been saved as {file_path}")

# Process and clean data
final_data = []
data_descriptors = list(metabolite_data_excel.iloc[0, 7:])
meta_descriptors = list(master_data_excel.columns[:7])
header_row = ["ID"] + meta_descriptors + data_descriptors
final_data.append(header_row)

for i in range(NUM_PATIENTS_MASTER_DATA):
    data_list = []
    vial_id = int(master_data_excel.iloc[i, 0])
    if vial_id in vial_id_to_patient_id:
        patient_id = vial_id_to_patient_id[vial_id]
        data_list.append(patient_id)
        data_list += [vial_id] + list(master_data_excel.iloc[i, 1:7])
        for j in range(NUM_PATIENTS_METABOLITE_DATA):
            if metabolite_data_excel.iloc[j + 5, 1] == patient_id:
                data_list += list(metabolite_data_excel.iloc[j + 5, 7:])
                final_data.append(data_list)
                break

# Save to DataFrame and CSV
df = pd.DataFrame(final_data[1:], columns=final_data[0])

# Initialize counters for corrections
non_numeric_corrections = 0
outlier_corrections = 0

# Perform data cleaning
for column in df.columns[9:]:
    df.loc[:, column] = pd.to_numeric(df[column], errors='coerce')
    original_non_numeric_count = df[column].isna().sum()
    column_mean = df[column].mean(skipna=True)
    current_non_numeric_count = df[column].isna().sum()
    non_numeric_corrections += (original_non_numeric_count - current_non_numeric_count)

    # Detect and replace outliers
    mean, std = df[column].mean(), df[column].std()
    outliers = (df[column] < (mean - 3 * std)) | (df[column] > (mean + 3 * std))
    original_outlier_count = outliers.sum()
    df.loc[outliers, column] = column_mean
    outlier_corrections += original_outlier_count

# Log total changes to a text file
total_data_points_examined = df.iloc[:, 9:].count().sum()
stats_file_path = os.path.join(output_path, 'data_cleanup_stats.txt')
with open(stats_file_path, 'w') as file:
    file.write(f"Total number of data points examined: {total_data_points_examined}\n")
    file.write(f"Total non-numeric entries corrected: {non_numeric_corrections}\n")
    file.write(f"Total outliers corrected: {outlier_corrections}\n")

print(f"Data change stats saved to {stats_file_path}")

# Output the cleaned CSV
cleaned_csv_path = f'{output_path}/cleaned_data.csv'
df.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned data saved to {cleaned_csv_path}")
