"""
cluster.py

This script performs clustering analysis on both ranked and normalized datasets using:
1. K-Means Clustering
2. Hierarchical Clustering (Dendrogram)

The script includes the following steps:
1. Loads the ranked and normalized datasets from CSV files.
2. Performs Principal Component Analysis (PCA) to reduce dimensionality.
3. Applies K-Means Clustering and plots the results.
4. Applies Hierarchical Clustering and plots the dendrogram.

Some documentation is AI-generated but reviewed by humans.

Usage:
    Run the script directly to perform clustering analysis.
    Example: python cluster.py

Dependencies:
    - os
    - pandas
    - matplotlib
    - seaborn
    - sklearn.cluster (KMeans)
    - scipy.cluster.hierarchy (dendrogram, linkage)
    - sklearn.decomposition (PCA)

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA

# Set up directories
output_dir = 'output/cluster'
ranked_dir = os.path.join(output_dir, 'ranked')
normalized_dir = os.path.join(output_dir, 'normalized')
os.makedirs(ranked_dir, exist_ok=True)
os.makedirs(normalized_dir, exist_ok=True)

# Load the data
ranked_data_path = 'processed/ranked_data.csv'
normalized_data_path = 'processed/normalized_data.csv'

df_ranked = pd.read_csv(ranked_data_path)
df_normalized = pd.read_csv(normalized_data_path)

# Replace 'marasmic kwashiorkor' and 'marasmus kwashiorkor' with 'kwashiorkor'
df_ranked['Subject Diagnosis'] = df_ranked['Subject Diagnosis'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')
df_normalized['Subject Diagnosis'] = df_normalized['Subject Diagnosis'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')

# Map phenotypes to 3-letter abbreviations for readability
phenotype_map = {
    'control': 'CTR',
    'kwashiorkor': 'KWA',
    'mam': 'MAM',
    'marasmus': 'MAR'
}

df_ranked['Phenotype_Abbr'] = df_ranked['Subject Diagnosis'].map(phenotype_map)
df_normalized['Phenotype_Abbr'] = df_normalized['Subject Diagnosis'].map(phenotype_map)

def perform_pca(data, n_components=3):
    """
    Perform PCA on the data.

    Parameters:
    data (DataFrame): The data to perform PCA on.
    n_components (int): The number of principal components to compute.

    Returns:
    principal_components (ndarray): The principal components of the data.
    """
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(data)
    return principal_components

def kmeans_clustering(data, phenotypes, output_dir, output_suffix):
    """
    Perform K-Means clustering and plot the results.

    Parameters:
    data (ndarray): The data to cluster.
    phenotypes (Series): The phenotypes associated with the data.
    output_dir (str): The directory to save the output files.
    output_suffix (str): The suffix to add to the output file names.
    """
    kmeans = KMeans(n_clusters=4, n_init=10)
    clusters = kmeans.fit_predict(data)
    
    # Plotting the clusters
    plt.figure(figsize=(10, 7))
    plt.scatter(data[:, 0], data[:, 1], c=clusters, cmap='viridis', label='Cluster')
    plt.scatter(data[:, 0], data[:, 1], c=phenotypes.map({'CTR': 0, 'KWA': 1, 'MAM': 2, 'MAR': 3}), alpha=0.5, label='Subject Diagnosis')
    plt.title(f'K-Means Clustering vs Phenotypes ({output_suffix})')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(loc='best')
    plt.savefig(os.path.join(output_dir, f'kmeans_clustering_{output_suffix}.png'))
    plt.close()
    print(f"K-Means clustering plot saved to {output_dir}/kmeans_clustering_{output_suffix}.png")

def hierarchical_clustering(data, phenotypes, patient_ids, output_dir, output_suffix):
    """
    Perform Hierarchical clustering and plot the dendrogram.

    Parameters:
    data (ndarray): The data to cluster.
    phenotypes (Series): The phenotypes associated with the data.
    patient_ids (Series): The patient IDs associated with the data.
    output_dir (str): The directory to save the output files.
    output_suffix (str): The suffix to add to the output file names.
    """
    linked = linkage(data, 'single')
    
    plt.figure(figsize=(10, 7))
    dendrogram(
        linked,
        labels=[f'{pid} ({phen})' for pid, phen in zip(patient_ids, phenotypes)],
        leaf_rotation=90,
        leaf_font_size=10
    )
    plt.title(f'Hierarchical Clustering Dendrogram ({output_suffix})')
    plt.xlabel('Patient ID (Phenotype)')
    plt.ylabel('Distance')
    plt.savefig(os.path.join(output_dir, f'hierarchical_clustering_{output_suffix}.png'))
    plt.close()
    print(f"Hierarchical clustering dendrogram saved to {output_dir}/hierarchical_clustering_{output_suffix}.png")

# Perform PCA on both datasets
pca_ranked = perform_pca(df_ranked.drop(columns=['Subject Diagnosis', 'Phenotype_Abbr', 'ID']))
pca_normalized = perform_pca(df_normalized.drop(columns=['Subject Diagnosis', 'Phenotype_Abbr', 'ID']))

# K-Means Clustering
kmeans_clustering(pca_ranked, df_ranked['Phenotype_Abbr'], ranked_dir, 'ranked')
kmeans_clustering(pca_normalized, df_normalized['Phenotype_Abbr'], normalized_dir, 'normalized')

# Hierarchical Clustering
hierarchical_clustering(pca_ranked, df_ranked['Phenotype_Abbr'], df_ranked['ID'], ranked_dir, 'ranked')
hierarchical_clustering(pca_normalized, df_normalized['Phenotype_Abbr'], df_normalized['ID'], normalized_dir, 'normalized')
