import pandas as pd
import os
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import re
from tqdm import tqdm

# Load the data
file_path = 'processed/processed_cleaned_data.csv'
data = pd.read_csv(file_path)

# Assume the first 8 columns are non-metabolic data
metabolic_data = data.iloc[:, 8:]

# Add the diagnosis column separately and strip any leading/trailing whitespace
diagnosis = data['Subject Diagnosis'].str.strip()

# Define the output directory
output_dir = 'output/p_values'
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)

# Function to calculate p-values and save the results
def calculate_p_values(X, y, output_subdir, group1, group2):
    output_path = os.path.join(output_dir, output_subdir)
    os.makedirs(output_path, exist_ok=True)
    
    p_values = {}
    for column in tqdm(X.columns, desc=f"Processing {output_subdir}"):
        group1_data = X[y == group1][column]
        group2_data = X[y == group2][column]
        t_stat, p_val = ttest_ind(group1_data, group2_data, nan_policy='omit')
        if not pd.isna(p_val):
            if p_val < 0.01:
                p_values[column] = round(p_val, 6)  # Round to 6 decimal places for small p-values
            else:
                p_values[column] = round(p_val, 2)
    
    # Filter p-values less than 0.01
    significant_p_values = {k: v for k, v in p_values.items() if float(v) < 0.01}
    
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
        sns.violinplot(x=y, y=X[metabolite], inner='point', scale='width')
        sns.boxplot(x=y, y=X[metabolite], showcaps=True, boxprops={'facecolor':'None'}, showfliers=False, whiskerprops={'linewidth':2})
        plt.title(f'{metabolite} (p-value: {p_val})')
        plt.xlabel('Diagnosis')
        plt.ylabel(metabolite)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f'{sanitized_metabolite}.png'))
        plt.close()

# Group comparisons
comparisons = [
    (['Marasmus Kwashiorkor', 'Kwashiorkor'], 'Marasmus', 'edematous_vs_non_edematous'),
    ('Marasmus Kwashiorkor', 'Marasmus', 'mk_vs_m'),
    ('Marasmus Kwashiorkor', ['Marasmus', 'Kwashiorkor'], 'mk_vs_non_mk'),
    ('Marasmus', 'Kwashiorkor', 'marasmus_vs_kwashiorkor')
]

# Run comparisons
for group1, group2, output_subdir in comparisons:
    print(f"Comparing {group1} to {group2}...")  # Debug info
    if isinstance(group1, list):
        condition_1 = diagnosis.isin(group1)
        label1 = "_".join(group1)
        y_combined = diagnosis.copy()
        y_combined[y_combined.isin(group1)] = label1
    else:
        condition_1 = diagnosis == group1
        label1 = group1
        y_combined = diagnosis.copy()

    if isinstance(group2, list):
        condition_2 = diagnosis.isin(group2)
        label2 = "_".join(group2)
        y_combined[y_combined.isin(group2)] = label2
    else:
        condition_2 = diagnosis == group2
        label2 = group2

    condition = condition_1 | condition_2
    X = metabolic_data[condition]
    y_combined = y_combined[condition]
    
    print(f"Group 1: {label1}, count: {condition_1.sum()}")  # Debug info
    print(f"Group 2: {label2}, count: {condition_2.sum()}")  # Debug info
    print(f"Combined condition count: {condition.sum()}")  # Debug info
    
    calculate_p_values(X, y_combined, output_subdir, label1, label2)
