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
df_ranked['Phenotype'] = df_ranked['Phenotype'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')
df_normalized['Phenotype'] = df_normalized['Phenotype'].replace(['marasmic kwashiorkor', 'marasmus kwashiorkor'], 'kwashiorkor')

# Map phenotypes to 3-letter abbreviations for readability
phenotype_map = {
    'control': 'CTR',
    'kwashiorkor': 'KWA',
    'mam': 'MAM',
    'marasmus': 'MAR'
}

df_ranked['Phenotype_Abbr'] = df_ranked['Phenotype'].map(phenotype_map)
df_normalized['Phenotype_Abbr'] = df_normalized['Phenotype'].map(phenotype_map)

def perform_pca(data, n_components=3):
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(data)
    return principal_components

def kmeans_clustering(data, phenotypes, output_dir, output_suffix):
    kmeans = KMeans(n_clusters=4, n_init=10)
    clusters = kmeans.fit_predict(data)
    
    # Plotting the clusters
    plt.figure(figsize=(10, 7))
    plt.scatter(data[:, 0], data[:, 1], c=clusters, cmap='viridis', label='Cluster')
    plt.scatter(data[:, 0], data[:, 1], c=phenotypes.map({'CTR': 0, 'KWA': 1, 'MAM': 2, 'MAR': 3}), alpha=0.5, label='Phenotype')
    plt.title(f'K-Means Clustering vs Phenotypes ({output_suffix})')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(loc='best')
    plt.savefig(os.path.join(output_dir, f'kmeans_clustering_{output_suffix}.png'))
    plt.close()
    print(f"K-Means clustering plot saved to {output_dir}/kmeans_clustering_{output_suffix}.png")

def hierarchical_clustering(data, phenotypes, patient_ids, output_dir, output_suffix):
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
pca_ranked = perform_pca(df_ranked.drop(columns=['Phenotype', 'Phenotype_Abbr', 'ID']))
pca_normalized = perform_pca(df_normalized.drop(columns=['Phenotype', 'Phenotype_Abbr', 'ID']))

# K-Means Clustering
kmeans_clustering(pca_ranked, df_ranked['Phenotype_Abbr'], ranked_dir, 'ranked')
kmeans_clustering(pca_normalized, df_normalized['Phenotype_Abbr'], normalized_dir, 'normalized')

# Hierarchical Clustering
hierarchical_clustering(pca_ranked, df_ranked['Phenotype_Abbr'], df_ranked['ID'], ranked_dir, 'ranked')
hierarchical_clustering(pca_normalized, df_normalized['Phenotype_Abbr'], df_normalized['ID'], normalized_dir, 'normalized')
