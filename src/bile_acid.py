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
    - scipy.stats (ttest_ind, mannwhitneyu)

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu

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

# List of bile acids by categories
total_ba = ['Cholic acid', 'Chenodeoxycholic acid', 'Deoxycholic acid', 'Glycocholic acid',
            'Glycochenodeoxycholic acid', 'Glycodeoxycholic acid', 'Glycolitocholic acid',
            'Glycolitocholic acid sulfate', 'Glycoursodeoxycholic acid', 'Taurocholic acid',
            'Taurochenodeoxycholic acid', 'Taurodeoxycholic acid', 'Taurolitocholic acid']

glycine_conjugated = ['Glycocholic acid', 'Glycochenodeoxycholic acid', 'Glycodeoxycholic acid', 'Glycoursodeoxycholic acid']
taurine_conjugated = ['Taurocholic acid', 'Taurochenodeoxycholic acid', 'Taurodeoxycholic acid', 'Taurolitocholic acid']
unconjugated = ['Cholic acid', 'Chenodeoxycholic acid', 'Deoxycholic acid']

# Function to calculate total, conjugated, and unconjugated bile acids
def calculate_bile_acids(df, category):
    """
    Calculate the sum of bile acids in a specific category.

    Parameters:
    df (DataFrame): The data frame containing bile acid levels.
    category (list): List of bile acids in the category.

    Returns:
    Series: Sum of bile acids in the specified category for each row.
    """
    return df[category].sum(axis=1)

# Combine Marasmus and Kwashiorkor into a single group 'SAM'
df['Group'] = df['Subject Diagnosis'].apply(lambda x: 'Control' if x == 'Control' else 'SAM')

# Filter out the 'MAM' group if it exists
df_filtered = df[df['Group'].isin(['Control', 'SAM'])]

# Calculate total, glycine-conjugated, taurine-conjugated, and unconjugated bile acids
df_filtered['Total_BA'] = calculate_bile_acids(df_filtered, total_ba)
df_filtered['Total_Glycine_Conjugated'] = calculate_bile_acids(df_filtered, glycine_conjugated)
df_filtered['Total_Taurine_Conjugated'] = calculate_bile_acids(df_filtered, taurine_conjugated)
df_filtered['Total_Unconjugated'] = calculate_bile_acids(df_filtered, unconjugated)

# Categories to analyze
categories = ['Total_BA', 'Total_Glycine_Conjugated', 'Total_Taurine_Conjugated', 'Total_Unconjugated']
category_names = ['Total BA', 'Glycine Conjugated', 'Taurine Conjugated', 'Unconjugated BA']

# Perform Mann-Whitney U tests and store p-values
p_values = {}
for category in categories:
    control_data = df_filtered[df_filtered['Group'] == 'Control'][category].dropna()
    sam_data = df_filtered[df_filtered['Group'] == 'SAM'][category].dropna()
    
    if len(control_data) > 1 and len(sam_data) > 1:  # Ensure there are enough data points
        stat, p_value = mannwhitneyu(control_data, sam_data, alternative='two-sided')
        p_values[category] = p_value

# Save p-values to a text file
p_values_path = os.path.join(output_dir, 'combined_sam_control_p_values.txt')
with open(p_values_path, 'w') as file:
    for category, p_value in p_values.items():
        file.write(f"{category}: p-value = {p_value:.5f}\n")

print(f"P-values saved to {p_values_path}")

# Create box plots for bile acid categories
plt.figure(figsize=(18, 6))

for i, category in enumerate(categories):
    plt.subplot(1, 4, i+1)
    data = [df_filtered[df_filtered['Group'] == 'Control'][category], df_filtered[df_filtered['Group'] == 'SAM'][category]]
    plt.boxplot(data, tick_labels=['Control', 'SAM'])
    plt.title(f'{category_names[i]}\n(p-value = {p_values[category]:.5f})')
    plt.ylabel('Bile Acids (µmol/L)')
    if i > 0:
        plt.yticks([])

# Save the box plot
box_plot_path = os.path.join(output_dir, 'combined_sam_control_boxplot.png')
plt.tight_layout()
plt.savefig(box_plot_path)
plt.close()

print(f"Box plot saved to {box_plot_path}")
