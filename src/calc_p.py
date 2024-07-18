"""
calc_p.py

This script performs statistical analysis on metabolic data to calculate p-values between different subject groups based on their diagnosis. It loads cleaned data from a CSV file, processes the data to select metabolic columns, replaces specific diagnoses, calculates t-tests for each metabolic column, saves p-values less than 0.01 to text files, and generates box plots for significant metabolites.

Usage:
    Run the script using Python 3.
    Example: python3 calc_p.py

Dependencies:
    - pandas
    - scipy.stats (ttest_ind)
    - matplotlib.pyplot
    - seaborn
    - re
    - tqdm

Author:
    Daniel Musachio

Date:
    July 2024
"""

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

# Add the diagnosis column separately
diagnosis = data['Subject Diagnosis'].replace('Marasmic Kwashiorkor', 'Kwashiorkor')

# Define the output directory
output_dir = 'output/p_values'
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize file names
def sanitize_filename(filename):
    """
    Sanitizes a filename by replacing non-alphanumeric characters with underscores.
    
    Parameters:
    filename (str): The filename to sanitize.
    
    Returns:
    str: Sanitized filename.
    """
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)

# Function to calculate p-values and save the results
def calculate_p_values(X, y, output_subdir, group1, group2):
    """
    Calculates t-tests for each metabolic column between two groups and saves results.
    Generates box plots for metabolites with p-values less than 0.01.
    
    Parameters:
    X (DataFrame): Metabolic data columns.
    y (Series): Diagnoses corresponding to the metabolic data.
    output_subdir (str): Subdirectory name for output files.
    group1 (str): Label for the first group.
    group2 (str): Label for the second group.
    """
    output_path = os.path.join(output_dir, output_subdir)
    os.makedirs(output_path, exist_ok=True)
    
    p_values = {}
    for column in tqdm(X.columns, desc=f"Processing {output_subdir}"):
        group1_data = X[y == group1][column]
        group2_data = X[y == group2][column]
        t_stat, p_val = ttest_ind(group1_data, group2_data, nan_policy='omit')
        if p_val < 0.01:
            p_values[column] = p_val
    
    # Save the p-values less than 0.01 to a text file
    with open(os.path.join(output_path, 'p_values_less_than_0.01.txt'), 'w') as f:
        for metabolite, p_val in p_values.items():
            f.write(f"{metabolite}: {p_val}\n")
    
    # Generate and save the plots for the metabolites with p-values less than 0.01
    for metabolite, p_val in p_values.items():
        sanitized_metabolite = sanitize_filename(metabolite)
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=y, y=X[metabolite])
        plt.title(f'{metabolite} (p-value: {p_val:.3e})')
        plt.xlabel('Diagnosis')
        plt.ylabel(metabolite)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f'{sanitized_metabolite}.png'))
        plt.close()

# Group comparisons
comparisons = [
    ('Marasmus', 'Kwashiorkor', 'marasmus_vs_kwash'),
    (['Control', 'MAM'], ['Kwashiorkor', 'Marasmus'], 'control_mam_vs_kwash_marasmus'),
    ('Control', ['Kwashiorkor', 'Marasmus'], 'control_vs_kwash_marasmus'),
    ('Control', 'Kwashiorkor', 'control_vs_kwash'),
    ('Control', 'Marasmus', 'control_vs_marasmus'),
    ('MAM', 'Kwashiorkor', 'mam_vs_kwash'),
    ('MAM', 'Marasmus', 'mam_vs_marasmus')
]

# Run comparisons
for group1, group2, output_subdir in comparisons:
    if isinstance(group1, list):
        condition_1 = diagnosis.isin(group1)
        label1 = "_".join(group1)
    else:
        condition_1 = diagnosis == group1
        label1 = group1

    if isinstance(group2, list):
        condition_2 = diagnosis.isin(group2)
        label2 = "_".join(group2)
    else:
        condition_2 = diagnosis == group2
        label2 = group2

    condition = condition_1 | condition_2
    X = metabolic_data[condition]
    y = diagnosis[condition]
    
    calculate_p_values(X, y, output_subdir, label1, label2)
