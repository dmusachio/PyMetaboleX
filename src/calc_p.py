"""
calc_p.py

This script performs statistical analysis (t-tests) on metabolic data to compare two groups.

The script includes the following steps:
1. Loads the dataset from a CSV file.
2. Separates the metabolic data from other columns.
3. Identifies the first two unique groups in the 'Subject Diagnosis' column.
4. Performs t-tests for each metabolite to compare the two groups.
5. Saves the p-values and plots for significant metabolites.

Some documentation is AI-generated but reviewed by humans.

Usage:
    Run the script directly to perform the analysis.
    Example: python calc_p.py <data_file> <output_dir>

Dependencies:
    - os
    - pandas
    - matplotlib
    - seaborn
    - scipy.stats (ttest_ind)
    - tqdm
    - re

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import sys
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import re
from tqdm import tqdm

# Read input parameters from command line arguments
if len(sys.argv) != 3:
    print("Usage: python calc_p.py <data_file> <output_dir>")
    exit()

data_file = sys.argv[1]
output_dir = sys.argv[2]

# Load the data
if os.path.isfile(data_file):
    data = pd.read_csv(data_file)
    print(f"Data loaded successfully from {data_file}")
else:
    print(f"The file {data_file} does not exist. Please check the file path.")
    exit()

# Assume the metabolic data starts from the second column
metabolic_data = data.iloc[:, 1:]

# Add the diagnosis column separately and strip any leading/trailing whitespace
diagnosis = data['Subject Diagnosis'].str.strip()

# Identify the first two unique groups in the 'Subject Diagnosis' column
unique_groups = diagnosis.unique()
if len(unique_groups) < 2:
    print("There are fewer than two unique groups in the 'Subject Diagnosis' column.")
    exit()

group1 = unique_groups[0]
group2 = unique_groups[1]

# Set up the output directory
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)

# Function to calculate p-values and save the results
def calculate_p_values(X, y, group1, group2, output_dir):
    output_path = os.path.join(output_dir)
    os.makedirs(output_path, exist_ok=True)
    
    p_values = {}
    for column in tqdm(X.columns, desc="Processing p-values"):
        group1_data = X[y == group1][column]
        group2_data = X[y == group2][column]
        t_stat, p_val = ttest_ind(group1_data, group2_data, nan_policy='omit')
        if not pd.isna(p_val):
            if p_val < 0.01:
                p_values[column] = round(p_val, 6)  # Round to 6 decimal places for small p-values
            else:
                p_values[column] = round(p_val, 2)
    
    # Filter p-values less than 0.05
    significant_p_values = {k: v for k, v in p_values.items() if float(v) < 0.05}
    
    # If fewer than 3 significant p-values, take the 10 lowest p-values
    if len(significant_p_values) < 3:
        significant_p_values = dict(sorted(p_values.items(), key=lambda item: float(item[1]))[:10])
    
    # Save the p-values to a text file
    with open(os.path.join(output_path, 'p_values.txt'), 'w') as f:
        for metabolite, p_val in significant_p_values.items():
            f.write(f"{metabolite}: {p_val}\n")
    
    # Generate and save the plots for the significant metabolites
    for metabolite, p_val in significant_p_values.items():
        sanitized_metabolite = sanitize_filename(metabolite)
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=y, y=X[metabolite], inner='point', density_norm='width')
        sns.boxplot(x=y, y=X[metabolite], showcaps=True, boxprops={'facecolor':'None'}, showfliers=False, whiskerprops={'linewidth':2})
        plt.title(f'{metabolite} (p-value: {p_val})')
        plt.xlabel('Diagnosis')
        plt.ylabel(metabolite)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f'{sanitized_metabolite}.png'))
        plt.close()

# Define the condition for the two groups
condition_1 = diagnosis == group1
condition_2 = diagnosis == group2
condition = condition_1 | condition_2

# Filter the data for the two groups
X = metabolic_data[condition]
y_combined = diagnosis[condition]

# Calculate and save p-values and plots
calculate_p_values(X, y_combined, group1, group2, output_dir)

print("P-value calculation and plotting completed.")
