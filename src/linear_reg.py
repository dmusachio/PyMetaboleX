import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os
import re
from tqdm import tqdm
import warnings

# Create output directory if it doesn't exist
output_dir = "output/linear_reg"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the data
file_path = 'processed/processed_cleaned_data.csv'
data = pd.read_csv(file_path)

# Split the data into two groups: Case (Kwashiorkor and Marasmus) and Control (including MAM)
case_conditions = ['Kwashiorkor', 'Marasmic Kwashiorkor', 'Marasmus']
control_conditions = ['Control', 'MAM']

case_data = data[data['Subject Diagnosis'].isin(case_conditions)].copy()
control_data = data[data['Subject Diagnosis'].isin(control_conditions)].copy()

# Assign 'Phenotype' column
case_data.loc[:, 'Phenotype'] = 1  # 1 for Case
control_data.loc[:, 'Phenotype'] = 0  # 0 for Control

# Select metabolite columns (from the 9th column onwards)
metabolite_columns = data.columns[8:]

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

# Function to perform linear regression and save results
def perform_linear_regression(group1_data, group2_data, group1_name, group2_name):
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
            plt.xticks([0, 1], [group1_name, group2_name])
            plt.legend()
            plt.savefig(f"{output_dir}/{sanitize_filename(metabolite)}_regression.png")
            plt.close()

    # Save all summaries to a single text file
    with open(f"{output_dir}/{group1_name}_vs_{group2_name}_regression_summaries.txt", "w") as f:
        f.writelines(all_summaries)

# Perform linear regression comparing Control and Case
perform_linear_regression(control_data, case_data, 'Control', 'Case')

print("Linear regression analysis and plots saved to output/linear_reg")
