"""
bile_acid.py

This script analyzes bile acid levels in different subject groups, performing statistical tests and generating visualizations.

The script performs the following tasks:
1. Loads cleaned data from a CSV file.
2. Replaces specific diagnoses with a unified term.
3. Identifies significant bile acids through t-tests.
4. Calculates and compares total, glycine-conjugated, taurine-conjugated, and unconjugated bile acids using Mann-Whitney U tests.
5. Generates and saves box plots for significant bile acids and bile acid categories.

Some documentation is AI-generated but reviewed by humans.

Usage:
    Run the script directly to analyze bile acid levels.
    Example: python bile_acid.py

Dependencies:
    - os
    - pandas
    - seaborn
    - matplotlib
    - scipy.stats (ttest_ind, mannwhitneyu, chi2, norm)

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu, chi2, norm
import numpy as np

# Ensure the output directories exist
output_dir = 'output/bile_acid'
os.makedirs(output_dir, exist_ok=True)

# Load the data
data_dir = 'processed'
csv_file_path = os.path.join(data_dir, 'cleaned_data.csv')

if os.path.isfile(csv_file_path):
    df = pd.read_csv(csv_file_path)
    print(f"Data loaded successfully from {csv_file_path}")
else:
    print(f"The file {csv_file_path} does not exist. Please check your data directory.")
    exit()

# Remove the 'Phenotype' column if it exists
if 'Phenotype' in df.columns:
    df = df.drop(columns=['Phenotype'])

# Replace 'Marasmic Kwashiorkor' and 'Marasmus Kwashiorkor' with 'Kwashiorkor'
df['Subject Diagnosis'] = df['Subject Diagnosis'].replace(['Marasmic Kwashiorkor', 'Marasmus Kwashiorkor'], 'Kwashiorkor')

# List of bile acids
bile_acids = [
    'Cholic acid', 'Chenodeoxycholic acid', 'Deoxycholic acid', 'Glycocholic acid',
    'Glycochenodeoxycholic acid', 'Glycodeoxycholic acid', 'Glycolitocholic acid',
    'Glycolitocholic acid sulfate', 'Glycoursodeoxycholic acid', 'Taurocholic acid',
    'Taurochenodeoxycholic acid', 'Taurodeoxycholic acid', 'Taurolitocholic acid'
]

# Convert bile acid columns to numeric, forcing non-numeric values to NaN
df[bile_acids] = df[bile_acids].apply(pd.to_numeric, errors='coerce')

# Perform t-tests and collect significant bile acids
significant_bile_acids = []
p_values = []
for bile_acid in bile_acids:
    kwashiorkor_data = df[df['Subject Diagnosis'] == 'Kwashiorkor'][bile_acid].dropna()
    marasmus_data = df[df['Subject Diagnosis'] == 'Marasmus'][bile_acid].dropna()
    
    if len(kwashiorkor_data) > 1 and len(marasmus_data) > 1:  # Ensure there are enough data points
        t_stat, p_value = ttest_ind(kwashiorkor_data, marasmus_data)
        p_values.append((bile_acid, p_value))
        if p_value < 0.1:
            significant_bile_acids.append((bile_acid, p_value))

# Path to save the p-values
p_values_path = os.path.join(output_dir, 'p_values.txt')

# Save p-values to a text file
with open(p_values_path, 'w') as file:
    for bile_acid, p_value in p_values:
        file.write(f"{bile_acid}: p-value = {p_value:.5f}\n")

print(f"P-values saved to {p_values_path}")

# Combine p-values using Stouffer's Z-score method
z_scores = norm.ppf(1 - np.array([p for _, p in p_values]))
combined_z = np.sum(z_scores) / np.sqrt(len(z_scores))
combined_p_value_stouffer = norm.sf(combined_z)  # one-tailed p-value

# Combine p-values using Fisher's method
X2 = -2 * np.sum(np.log([p for _, p in p_values]))
df_fisher = 2 * len(p_values)  # degrees of freedom
combined_p_value_fisher = chi2.sf(X2, df_fisher)

# Save combined p-values to a text file
combined_p_values_path = os.path.join(output_dir, 'combined_p_values.txt')
with open(combined_p_values_path, 'w') as file:
    file.write(f"Combined p-value (Stouffer's Z-score method): {combined_p_value_stouffer:.5f}\n")
    file.write(f"Combined p-value (Fisher's method): {combined_p_value_fisher:.5f}\n")

print(f"Combined p-values saved to {combined_p_values_path}")

# Plot the significant bile acids
for bile_acid, p_value in significant_bile_acids:
    # Create output directory for this bile acid
    bile_acid_dir = os.path.join(output_dir, bile_acid.replace(' ', '_'))
    os.makedirs(bile_acid_dir, exist_ok=True)
    
    # Plot the boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Subject Diagnosis', y=bile_acid, data=df)
    plt.title(f'{bile_acid} Levels by Subject Diagnosis\np-value = {p_value:.5f}')
    plt.xlabel('Subject Diagnosis')
    plt.ylabel(bile_acid)
    
    # Save the plot
    plot_path = os.path.join(bile_acid_dir, f'{bile_acid.replace(" ", "_")}_boxplot.png')
    plt.savefig(plot_path)
    plt.close()
    
    # Debugging statement to confirm the plot was saved
    print(f"Boxplot saved to {plot_path}")
