"""
cluster.py

This script performs clustering analysis on a dataset using:
1. K-Means Clustering
2. Hierarchical Clustering (Dendrogram)

The script includes the following steps:
1. Loads the dataset from a CSV file.
2. Performs Principal Component Analysis (PCA) to reduce dimensionality.
3. Applies K-Means Clustering and plots the results with a mesh coloring background.
4. Applies Hierarchical Clustering and plots the dendrogram with 'Subject Diagnosis' as labels.

Some documentation is AI-generated but reviewed by humans.

Usage:
    Run the script directly to perform clustering analysis.
    Example: python cluster.py <data_file> <output_dir>

Dependencies:
    - os
    - pandas
    - matplotlib
    - seaborn
    - sklearn.cluster (KMeans)
    - scipy.cluster.hierarchy (dendrogram, linkage)
    - sklearn.decomposition (PCA)
    - numpy

Author:
    Daniel Musachio

Date:
    July 2024
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import numpy as np
import seaborn as sns

# Read input files and output directory from command line arguments
if len(sys.argv) != 3:
    print("Usage: python cluster.py <data_file> <output_dir>")
    exit()

data_file = sys.argv[1]
output_dir = sys.argv[2]

# Set up the output directory
os.makedirs(output_dir, exist_ok=True)

# Load the data
if os.path.isfile(data_file):
    df = pd.read_csv(data_file)
    print(f"Data loaded successfully from {data_file}")
else:
    print(f"The file {data_file} does not exist. Please check the file path.")
    exit()

# Perform PCA on the dataset
def perform_pca(data, n_components=2):
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

# K-Means Clustering
def kmeans_clustering(data, labels, output_dir):
    """
    Perform K-Means clustering and plot the results with a mesh coloring background.

    Parameters:
    data (ndarray): The data to cluster.
    labels (Series): The labels for the data points.
    output_dir (str): The directory to save the output files.
    """
    kmeans = KMeans(n_clusters=8, n_init=10)
    clusters = kmeans.fit_predict(data)
    
    # Create a mesh grid
    h = .02
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(10, 7))
    plt.imshow(Z, interpolation='nearest', extent=(xx.min(), xx.max(), yy.min(), yy.max()), 
               cmap=plt.cm.Paired, aspect='auto', origin='lower')
    
    # Plotting the clusters with the actual labels
    sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels, palette='deep', edgecolor='k', s=50)
    plt.title('K-Means Clustering with Subject Diagnosis')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(loc='best')
    plt.savefig(os.path.join(output_dir, 'kmeans_clustering.png'))
    plt.close()
    print(f"K-Means clustering plot saved to {output_dir}/kmeans_clustering.png")

# Hierarchical Clustering
def hierarchical_clustering(data, labels, output_dir):
    """
    Perform Hierarchical clustering and plot the dendrogram.

    Parameters:
    data (ndarray): The data to cluster.
    labels (Series): The labels for the data points.
    output_dir (str): The directory to save the output files.
    """
    linked = linkage(data, 'single')
    
    plt.figure(figsize=(10, 7))
    dendrogram(
        linked,
        labels=labels.tolist(),
        leaf_rotation=90,
        leaf_font_size=10
    )
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Subject Diagnosis')
    plt.ylabel('Distance')
    plt.savefig(os.path.join(output_dir, 'hierarchical_clustering.png'))
    plt.close()
    print(f"Hierarchical clustering dendrogram saved to {output_dir}/hierarchical_clustering.png")

# Drop non-numeric columns if any
numeric_df = df.select_dtypes(include=[np.number])

# Perform PCA
pca_result = perform_pca(numeric_df)

# Perform clustering analyses
kmeans_clustering(pca_result, df['Subject Diagnosis'], output_dir)
hierarchical_clustering(pca_result, df['Subject Diagnosis'], output_dir)

print("Clustering analysis completed.")
