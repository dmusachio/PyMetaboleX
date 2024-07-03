"""
evaluate_data.py

This script performs various data evaluation and analysis tasks including:
1. Loading cleaned data from a CSV file.
2. Performing Principal Component Analysis (PCA) on ranked and normalized data.
3. Conducting MANOVA tests on PCA results.
4. Plotting 3D PCA results.
5. Normalizing data and applying transformations for normality.
6. Saving the results including variance summaries, MANOVA test results, and PCA plots.

Some documentation is AI-generated but reviewed by humans.

Usage:
    Run the script directly to evaluate the data.
    Example: python evaluate_data.py

Dependencies:
    - os
    - pandas
    - seaborn
    - matplotlib
    - sklearn.decomposition (PCA)
    - numpy
    - scipy.stats (shapiro)
    - sklearn.preprocessing (LabelEncoder)
    - statsmodels.api
    - statsmodels.multivariate.manova (MANOVA)

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from scipy.stats import shapiro
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

# Set up directories
data_dir = 'processed'
output_dir = 'output/data_info'
ranked_dir = os.path.join(output_dir, 'ranked')
normalized_dir = os.path.join(output_dir, 'normalized')
processed_dir = 'processed'

# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(ranked_dir, exist_ok=True)
os.makedirs(normalized_dir, exist_ok=True)

# Define the path to the CSV file and output file
csv_file_path = os.path.join(data_dir, 'cleaned_data.csv')
variance_output_file_path = os.path.join(output_dir, 'variance_summary.txt')
shapiro_test_results_path = os.path.join(output_dir, 'shapiro_test_results.txt')

# Load and process the data
if os.path.isfile(csv_file_path):
    df = pd.read_csv(csv_file_path)
    print(f"Data loaded successfully from {csv_file_path}")
else:
    print(f"The file {csv_file_path} does not exist. Please check your data directory. Are you sure you already ran python3 data_harmonization.py?")
    exit()

phenotypes = df['Phenotype'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')

def perform_pca_and_save_results(data, output_suffix, output_dir):
    """
    Perform PCA on the data and save the explained variance ratio and PCA plots.
    
    Parameters:
    data (DataFrame): The data to perform PCA on.
    output_suffix (str): The suffix to add to the output file names.
    output_dir (str): The directory to save the output files.
    
    Returns:
    principal_components (ndarray): The principal components of the data.
    """
    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(data)
    explained_variance_ratio = pca.explained_variance_ratio_
    cumulative_explained_variance = np.cumsum(explained_variance_ratio)

    # Plot and save the explained variance ratio
    plt.figure(figsize=(8, 5))
    plt.bar(range(1, 4), explained_variance_ratio, alpha=0.6)
    plt.xlabel('Principal Components')
    plt.ylabel('Explained Variance Ratio')
    plt.title(f'Explained Variance Ratio by Principal Component ({output_suffix})')
    plt.grid(True)
    plot_path = os.path.join(output_dir, f'explained_variance_ratio_{output_suffix}.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Explained Variance Ratio plot saved to {plot_path}")

    # Write explained variance to a file
    with open(variance_output_file_path, 'a') as file:
        file.write(f"\nExplained Variance Ratio for Each Principal Component ({output_suffix}):\n")
        for i, variance in enumerate(explained_variance_ratio, 1):
            file.write(f"PC{i}: {variance:.4f} ({variance * 100:.2f}% of total variance)\n")
    print(f"Variance summary saved to {variance_output_file_path}")

    return principal_components

def perform_manova_and_save_results(principal_components, phenotypes, output_suffix, output_dir):
    """
    Perform MANOVA on the principal components and save the results.
    
    Parameters:
    principal_components (ndarray): The principal components of the data.
    phenotypes (Series): The phenotypes associated with the data.
    output_suffix (str): The suffix to add to the output file names.
    output_dir (str): The directory to save the output files.
    """
    df_pca = pd.DataFrame(principal_components, columns=[f'PC{i}' for i in range(1, 4)])
    df_pca['Phenotype'] = phenotypes
    maov = MANOVA.from_formula('PC1 + PC2 + PC3 ~ C(Phenotype)', data=df_pca)
    maov_results = maov.mv_test()
    maov_results_path = os.path.join(output_dir, f'maov_test_results_{output_suffix}.txt')
    with open(maov_results_path, 'w') as file:
        file.write(str(maov_results))
    print(f"MANOVA test results saved to {maov_results_path}")

def plot_3d_pca(principal_components, phenotypes, output_suffix, output_dir):
    """
    Plot a 3D scatter plot of the PCA results.
    
    Parameters:
    principal_components (ndarray): The principal components of the data.
    phenotypes (Series): The phenotypes associated with the data.
    output_suffix (str): The suffix to add to the output file names.
    output_dir (str): The directory to save the output files.
    """
    label_encoder = LabelEncoder()
    phenotypes_encoded = label_encoder.fit_transform(phenotypes)
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(principal_components[:, 0], principal_components[:, 1], principal_components[:, 2], 
                         c=phenotypes_encoded, cmap='viridis')

    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.set_title(f'3D PCA Plot ({output_suffix})')

    legend = ax.legend(*scatter.legend_elements(), title="Phenotypes")
    legend_labels = [text.get_text().replace('$\\mathdefault{', '').replace('}$', '') for text in legend.get_texts()]
    legend_texts = [label_encoder.inverse_transform([int(label)])[0] for label in legend_labels]
    for text, label in zip(legend.get_texts(), legend_texts):
        text.set_text(label)
    ax.add_artist(legend)

    plot_path = os.path.join(output_dir, f'3d_pca_plot_{output_suffix}.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"3D PCA plot saved to {plot_path}")

# Convert data to ranks
numeric_df = df.select_dtypes(include=[np.number])
df_ranked = numeric_df.rank(axis=1, method='average')
df_ranked = pd.concat([df[['ID', 'Phenotype']], df_ranked], axis=1)
ranked_principal_components = perform_pca_and_save_results(df_ranked.drop(columns=['ID', 'Phenotype']), 'ranked', ranked_dir)
perform_manova_and_save_results(ranked_principal_components, phenotypes, 'ranked', ranked_dir)
plot_3d_pca(ranked_principal_components, phenotypes, 'ranked', ranked_dir)

# Normalize data
df_normalized = numeric_df.copy()
failed_shapiro_count = 0

numeric_columns = df_normalized.columns

for column in numeric_columns:
    stat, p = shapiro(df_normalized[column].dropna())
    if p <= 0.03:
        failed_shapiro_count += 1
        df_normalized[column] = np.log1p(df_normalized[column] - df_normalized[column].min())

post_log_failed_shapiro_count = 0
total_columns = len(numeric_columns)
for column in numeric_columns:
    stat, p = shapiro(df_normalized[column].dropna())
    if p <= 0.03:
        post_log_failed_shapiro_count += 1

with open(shapiro_test_results_path, 'w') as file:
    file.write(f"Number of columns that failed the Shapiro-Wilk test and were log transformed: {failed_shapiro_count}\n")
    file.write(f"Number of columns that failed the Shapiro-Wilk test after log transformation: {post_log_failed_shapiro_count}\n")
    file.write(f"Total columns: {total_columns}\n")
    file.write(f"Percentage passing after log transformation: {100 * (total_columns - post_log_failed_shapiro_count) / total_columns:.2f}%\n")
print(f"Shapiro-Wilk test results saved to {shapiro_test_results_path}")

df_normalized = pd.concat([df[['ID', 'Phenotype']], df_normalized], axis=1)
normalized_principal_components = perform_pca_and_save_results(df_normalized.drop(columns=['ID', 'Phenotype']), 'normalized', normalized_dir)
perform_manova_and_save_results(normalized_principal_components, phenotypes, 'normalized', normalized_dir)
plot_3d_pca(normalized_principal_components, phenotypes, 'normalized', normalized_dir)

# Save ranked and normalized dataframes to CSV
df_ranked = pd.concat([df_ranked.drop(columns=['Phenotype']), phenotypes], axis=1)
df_normalized = pd.concat([df_normalized.drop(columns=['Phenotype']), phenotypes], axis=1)
df_ranked.to_csv(os.path.join(processed_dir, 'ranked_data.csv'), index=False)
df_normalized.to_csv(os.path.join(processed_dir, 'normalized_data.csv'), index=False)
print(f"Ranked and normalized data saved to {processed_dir}")
