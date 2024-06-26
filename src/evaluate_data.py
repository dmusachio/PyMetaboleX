import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

# Set up directories
data_dir = 'processed'
output_dir = 'output/data_info'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the path to the CSV file and output file
csv_file_path = os.path.join(data_dir, 'cleaned_data.csv')
variance_output_file_path = os.path.join(output_dir, 'variance_summary.txt')

# Load and process the data
if os.path.isfile(csv_file_path):
    df = pd.read_csv(csv_file_path)
    print(f"Data loaded successfully from {csv_file_path}")
else:
    print(f"The file {csv_file_path} does not exist. Please check your data directory. Are you sure you already ran python3 src/data_harmonization.py?")
    exit()

# Perform PCA
pca = PCA(n_components=6)
principal_components = pca.fit_transform(df.iloc[:, 3:])  # Adjust as per your dataset slicing. Currently factors meta data (like weight)
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_explained_variance = np.cumsum(explained_variance_ratio)

# Plot and save the explained variance ratio
plt.figure(figsize=(8, 5))
plt.bar(range(1, 7), explained_variance_ratio, alpha=0.6)
plt.xlabel('Principal Components')
plt.ylabel('Explained Variance Ratio')
plt.title('Explained Variance Ratio by Principal Component')
plt.grid(True)
plot_path = os.path.join(output_dir, 'explained_variance_ratio.png')
plt.savefig(plot_path)
plt.close()
print(f"Explained Variance Ratio plot saved to {plot_path}")

# Write explained variance to a file
with open(variance_output_file_path, 'w') as file:
    file.write("Explained Variance Ratio for Each Principal Component:\n")
    for i, variance in enumerate(explained_variance_ratio, 1):
        file.write(f"PC{i}: {variance:.4f} ({variance * 100:.2f}% of total variance)\n")
print(f"Variance summary saved to {variance_output_file_path}")

# Perform MANOVA and save results
df_pca = pd.DataFrame(principal_components, columns=[f'PC{i}' for i in range(1, 7)])
df_pca['Phenotype'] = df['Subject Diagnosis']  # Adjust based on your column name
maov = MANOVA.from_formula('PC1 + PC2 + PC3 + PC4 + PC5 + PC6 ~ C(Phenotype)', data=df_pca)
maov_results = maov.mv_test()
maov_results_path = os.path.join(output_dir, 'maov_test_results.txt')
with open(maov_results_path, 'w') as file:
    file.write(str(maov_results))
print(f"MANOVA test results saved to {maov_results_path}")

# Create and save box plots for each PC across Phenotype
for i in range(1, 7):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Phenotype', y=f'PC{i}', data=df_pca)
    plt.title(f'Box Plot of PC{i} by Phenotype')
    plt.xlabel('Phenotype')
    plt.ylabel(f'PC{i} Scores')
    box_plot_path = os.path.join(output_dir, f'PC{i}_boxplot.png')
    plt.savefig(box_plot_path)
    plt.close()
    print(f"Box plot for PC{i} saved to {box_plot_path}")
