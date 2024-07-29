"""
linear_reg.py

This script performs linear regression analysis on metabolite data comparing two groups.

It loads metabolite data from a CSV file, preprocesses the data by assigning a 'Phenotype' column,
performs linear regression using statsmodels, and saves regression summaries and plots for key metabolites.

Usage:
    Run the script using Python 3.
    Example: python3 linear_reg.py <data_file> <output_dir>

Dependencies:
    - pandas
    - statsmodels.api
    - matplotlib.pyplot
    - os
    - re
    - tqdm
    - warnings

Author:
    Daniel Musachio

Date:
    July 2024
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os
import re
from tqdm import tqdm
import warnings
import sys

# Read input parameters from command line arguments
if len(sys.argv) != 3:
    print("Usage: python linear_reg.py <data_file> <output_dir>")
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

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Add the diagnosis column separately and strip any leading/trailing whitespace
diagnosis = data['Subject Diagnosis'].str.strip()

# Identify the first two unique groups in the 'Subject Diagnosis' column
unique_groups = diagnosis.unique()
if len(unique_groups) < 2:
    print("There are fewer than two unique groups in the 'Subject Diagnosis' column.")
    exit()

group1 = unique_groups[0]
group2 = unique_groups[1]

# Split the data into two groups
group1_data = data[data['Subject Diagnosis'] == group1].copy()
group2_data = data[data['Subject Diagnosis'] == group2].copy()

# Assign 'Phenotype' column
group1_data.loc[:, 'Phenotype'] = 1  # 1 for group1
group2_data.loc[:, 'Phenotype'] = 0  # 0 for group2

# Select metabolite columns (from the 2nd column onwards)
metabolite_columns = data.columns[1:]

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

# Function to perform linear regression and save results
def perform_linear_regression(group1_data, group2_data, group1_name, group2_name):
    """
    Performs linear regression for each metabolite comparing two groups.
    
    Args:
    - group1_data: DataFrame, data for group 1
    - group2_data: DataFrame, data for group 2
    - group1_name: str, name of group 1 for labeling
    - group2_name: str, name of group 2 for labeling
    """
    # Combine the two groups into one DataFrame
    combined_data = pd.concat([group1_data, group2_data])
    
    all_summaries = []
    key_metabolites = ['Carnitine', 'Acetylcarnitine', 'Propionylcarnitine']  # Example key metabolites
    
    for metabolite in tqdm(metabolite_columns, desc="Processing metabolites"):
        X = sm.add_constant(combined_data['Phenotype'])  # Independent variable
        Y = combined_data[metabolite]  # Dependent variable
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            model = sm.OLS(Y, X).fit()
        summary = model.summary()
        all_summaries.append(f"{metabolite}:\n{summary}\n\n")
        
        if metabolite in key_metabolites:
            # Plot the regression for key metabolites
            plt.figure()
            plt.scatter(combined_data['Phenotype'], Y, label='Data')
            plt.plot(combined_data['Phenotype'], model.predict(X), color='red', label='OLS fit')
            plt.title(f'{metabolite} vs Phenotype ({group1_name} vs {group2_name})')
            plt.xlabel('Phenotype')
            plt.ylabel(metabolite)
            plt.xticks([0, 1], [group2_name, group1_name])
            plt.legend()
            plt.savefig(f"{output_dir}/{sanitize_filename(metabolite)}_regression.png")
            plt.close()

    # Save all summaries to a single text file
    with open(f"{output_dir}/{group1_name}_vs_{group2_name}_regression_summaries.txt", "w") as f:
        f.writelines(all_summaries)

# Perform linear regression comparing the two groups
perform_linear_regression(group1_data, group2_data, group1, group2)

print(f"Linear regression analysis and plots saved to {output_dir}")
