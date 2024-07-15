import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the file paths
qc_file_path = 'input/qc.xlsx'
cleaned_data_file_path = 'processed/cleaned_data.csv'

# Define the RSD threshold
rsd_threshold = 20 #LC is 20, GC is 30

# Step 1: Read the qc.xlsx file
qc_df = pd.read_excel(qc_file_path)

# Step 2: Extract the relevant metabolite data columns (assuming they start from the 8th column)
metabolite_data = qc_df.iloc[:, 7:]

# Ensure all values in metabolite data are numeric, converting non-numeric values to NaN
metabolite_data = metabolite_data.apply(pd.to_numeric, errors='coerce')

# Step 3: Calculate RSD for each column
rsd = metabolite_data.std() / metabolite_data.mean() * 100

# Step 4: Identify columns with an RSD above the threshold
high_rsd_columns = rsd[rsd > rsd_threshold].index

# Step 5: Read the cleaned_data.csv file
cleaned_df = pd.read_csv(cleaned_data_file_path)

# Step 6: Remove the 'Phenotype' column if it exists
if 'Phenotype' in cleaned_df.columns:
    cleaned_df = cleaned_df.drop(columns=['Phenotype'])

# Step 7: Remove columns with high RSD from cleaned_data.csv
filtered_df = cleaned_df.drop(columns=high_rsd_columns, errors='ignore')

# Save the filtered data back to cleaned_data.csv
filtered_df.to_csv(cleaned_data_file_path, index=False)

# Step 8: Plot the RSD values
sorted_rsd = rsd.sort_values()

plt.figure(figsize=(10, 6))
plt.scatter(range(len(sorted_rsd)), sorted_rsd, color='b')
plt.axhline(y=20, color='r', linestyle='--', label='20% Cut-off')
plt.axhline(y=30, color='g', linestyle='--', label='30% Cut-off')
plt.xlabel('Variable Index (Sorted by RSD)')
plt.ylabel('RSD (%)')
plt.title('RSD across all variables (Sorted in Ascending Order)')
plt.legend()
plt.grid(True)
os.makedirs('processed', exist_ok=True)
plt.savefig('processed/rsd_plot.png')
plt.show()

# Save the sorted RSD values to a CSV file
sorted_rsd.to_csv('processed/sorted_rsd.csv', header=True)

# Print the percentage of variables with RSD less than the thresholds and save to a text file
percentage_below_20 = (sorted_rsd < 20).sum() / len(sorted_rsd) * 100
percentage_below_30 = (sorted_rsd < 30).sum() / len(sorted_rsd) * 100

results = [
    f"Percentage of variables with RSD less than 20%: {percentage_below_20:.2f}%",
    f"Percentage of variables with RSD less than 30%: {percentage_below_30:.2f}%"
]

with open('processed/rsd_results.txt', 'w') as f:
    for line in results:
        print(line)
        f.write(line + "\n")
