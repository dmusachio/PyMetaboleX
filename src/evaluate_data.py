"""
evaluate_data.py

This script performs various data evaluation and analysis tasks including:
1. Loading cleaned and normalized data from a CSV file.
2. Performing Principal Component Analysis (PCA) on the data.
3. Conducting MANOVA tests on PCA results.
4. Plotting 3D PCA results.
5. Saving the results including variance summaries, MANOVA test results, and PCA plots.

Assumptions:
    The data is already normalized.

Usage:
    Run the script directly to evaluate the data.
    Example: python evaluate_data.py <input_file> <output_dir>

Dependencies:
    - os
    - pandas
    - seaborn
    - matplotlib
    - sklearn.decomposition (PCA)
    - numpy
    - sklearn.preprocessing (LabelEncoder)
    - statsmodels.api
    - statsmodels.multivariate.manova (MANOVA)

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

# Read input file and output directory from command line arguments
if len(sys.argv) != 3:
    print("Usage: python evaluate_data.py <input_file> <output_dir>")
    exit()

input_file = sys.argv[1]
output_dir = sys.argv[2]

# Set up directories
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")

# Define the path to the output files
variance_output_file_path = os.path.join(output_dir, 'variance_summary.txt')
manova_test_results_path = os.path.join(output_dir, 'manova_test_results.txt')
pca_plot_path = os.path.join(output_dir, '3d_pca_plot.png')

# Load and process the data
if input_file and os.path.isfile(input_file):
    df = pd.read_csv(input_file)
    print(f"Data loaded successfully from {input_file}")
else:
    print(f"The file {input_file} does not exist. Please check your data directory.")
    exit()

# Assuming the first column is 'Subject Diagnosis' and the rest are metabolic data
df.rename(columns={'Subject Diagnosis': 'Subject_Diagnosis'}, inplace=True)
phenotypes = df['Subject_Diagnosis'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')
metabolic_data = df.iloc[:, 1:]

def perform_pca_and_save_results(data, output_dir):
    """
    Perform PCA on the data and save the explained variance ratio and PCA plots.
    
    Parameters:
    data (DataFrame): The data to perform PCA on.
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
    plt.title('Explained Variance Ratio by Principal Component')
    plt.grid(True)
    plot_path = os.path.join(output_dir, 'explained_variance_ratio.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Explained Variance Ratio plot saved to {plot_path}")

    # Write explained variance to a file
    with open(variance_output_file_path, 'a') as file:
        file.write(f"\nExplained Variance Ratio for Each Principal Component:\n")
        for i, variance in enumerate(explained_variance_ratio, 1):
            file.write(f"PC{i}: {variance:.4f} ({variance * 100:.2f}% of total variance)\n")
    print(f"Variance summary saved to {variance_output_file_path}")

    return principal_components

def perform_manova_and_save_results(principal_components, phenotypes, output_dir):
    """
    Perform MANOVA on the principal components and save the results.
    
    Parameters:
    principal_components (ndarray): The principal components of the data.
    phenotypes (Series): The phenotypes associated with the data.
    output_dir (str): The directory to save the output files.
    """
    df_pca = pd.DataFrame(principal_components, columns=[f'PC{i}' for i in range(1, 4)])
    df_pca['Subject_Diagnosis'] = phenotypes
    maov = MANOVA.from_formula('PC1 + PC2 + PC3 ~ C(Subject_Diagnosis)', data=df_pca)
    maov_results = maov.mv_test()
    with open(manova_test_results_path, 'w') as file:
        file.write(str(maov_results))
    print(f"MANOVA test results saved to {manova_test_results_path}")

def plot_3d_pca(principal_components, phenotypes, output_dir):
    """
    Plot a 3D scatter plot of the PCA results.
    
    Parameters:
    principal_components (ndarray): The principal components of the data.
    phenotypes (Series): The phenotypes associated with the data.
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
    ax.set_title('3D PCA Plot')

    legend = ax.legend(*scatter.legend_elements(), title="Phenotypes")
    legend_labels = [text.get_text().replace('$\\mathdefault{', '').replace('}$', '') for text in legend.get_texts()]
    legend_texts = [label_encoder.inverse_transform([int(label)])[0] for label in legend_labels]
    for text, label in zip(legend.get_texts(), legend_texts):
        text.set_text(label)
    ax.add_artist(legend)

    plot_path = os.path.join(output_dir, '3d_pca_plot.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"3D PCA plot saved to {plot_path}")

# Perform PCA and save results
principal_components = perform_pca_and_save_results(metabolic_data, output_dir)
perform_manova_and_save_results(principal_components, phenotypes, output_dir)
plot_3d_pca(principal_components, phenotypes, output_dir)

print("Data evaluation and analysis completed.")
