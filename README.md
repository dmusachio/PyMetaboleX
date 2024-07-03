# Data Harmonization and Analysis Scripts

## Overview
The project includes scripts that process, harmonize, and analyze data from three input Excel files. These scripts perform data cleaning, patient ID matching, phenotype harmonization, and statistical analysis using PCA and MANOVA.

## Directory Structure
```plaintext
your_project_folder/
├── input/
│   ├── metabolite_data.xlsx
│   ├── meta_data.xlsx
│   └── master_data.xlsx
├── src/
│   ├── bile_acid.py
│   ├── data_harmonization.py
│   ├── evaluate_data.py
│   ├── run_all.py
│   └── cluster.py
├── processed/
│   ├── patients_summary.txt
│   ├── cleaned_data.csv
│   ├── data_cleanup_stats.txt
│   ├── ranked_data.csv
│   └── normalized_data.csv
├── output/
│   ├── bile_acid/
│   │   ├── combined_sam_control_boxplot.png
│   │   ├── combined_sam_control_p_values.txt
│   │   ├── p_values.txt
│   │   ├── Cholic_acid/
│   │   │   └── Cholic_acid_boxplot.png
│   │   ├── Deoxycholic_acid/
│   │   │   └── Deoxycholic_acid_boxplot.png
│   │   ├── Glycodeoxycholic_acid/
│   │   │   └── Glycodeoxycholic_acid_boxplot.png
│   │   ├── Glycolitocholic_acid/
│   │   │   └── Glycolitocholic_acid_boxplot.png
│   ├── cluster/
│   │   ├── ranked/
│   │   │   ├── kmeans_clustering_ranked.png
│   │   │   ├── hierarchical_clustering_ranked.png
│   │   ├── normalized/
│   │   │   ├── kmeans_clustering_normalized.png
│   │   │   └── hierarchical_clustering_normalized.png
│   ├── data_info/
│   │   ├── ranked/
│   │   │   ├── explained_variance_ratio_ranked.png
│   │   │   ├── maov_test_results_ranked.txt
│   │   │   └── 3d_pca_plot_ranked.png
│   │   ├── normalized/
│   │   │   ├── explained_variance_ratio_normalized.png
│   │   │   ├── maov_test_results_normalized.txt
│   │   │   └── 3d_pca_plot_normalized.png
│   │   ├── variance_summary.txt
│   │   └── shapiro_test_results.txt
└── README.md

input/: Contains all raw Excel data files.
src/: Python scripts for data processing and evaluation.
processed/: Processed data outputs, summaries, and statistics.
output/: Visualizations such as variance explained and boxplots for each principal component.

```
### Prerequisites
- Access to an NIH Biowulf account.

### Installing Dependencies
All dependencies should be pre-installed on Biowulf.

## Setup

### Generating Personal Access Token and Cloning Repository

1. **Generate a Personal Access Token (PAT)**:
   - Log in to GitHub with an account that has been added to the repo.
   - Navigate to `Settings` > `Developer settings` > `Personal access tokens`.
   - Click on `Generate new token`.
   - Select the scopes or permissions you'd like to grant this token (at minimum, `repo` scope for private repositories).
   - Click `Generate token`.
   - Copy the token now. You won’t be able to see it again!

2. **Clone the Repository Using HTTPS**:
   - Log into Biowulf and navigate to the root directory where you want to clone the code.
   - Use the HTTPS URL for cloning.
   - Run the following command in the terminal:
     ```bash
     git clone https://github.com/dmusachio/Malnutrition_Metabolite_Project.git
     ```
   - When prompted for a username and password:
     - Enter your GitHub username.
     - Enter the personal access token as the password.

## Running the Scripts
1. Log in to Biowulf and navigate to the root directory.
2. Optionally, type `rm -r output` and `rm -r processed` so that new output and processed folders can be generated.
3. Type `sinteractive` and wait to be allocated a node.

Execute the scripts sequentially:

```bash
python3 src/data_harmonization.py
python3 src/evaluate_data.py
python3 src/cluster.py
python3 src/bile_acid.py
```

Alternatively, run all scripts at once (CURRENTLY DOES NOT RUN bile_acid.py):

```bash
python3 src/run_all.py
```

## Output Details

The scripts will generate files in the `processed` and `output` directories as described below:

### Processed Directory
- **`patients_summary.txt`**: A summary of patient data.
- **`cleaned_data.csv`**: The cleaned and processed data.
- **`data_cleanup_stats.txt`**: Statistics about the data cleaning process.
- **`ranked_data.csv`**: The ranked data used for analysis.
- **`normalized_data.csv`**: The normalized data used for analysis.

### Output Directory

- **`bile_acid`**:
  - **`combined_sam_control_boxplot.png`**: Box plot comparing combined SAM (Marasmus and Kwashiorkor) versus Control for total bile acids, glycine-conjugated, taurine-conjugated, and unconjugated bile acids.
  - **`combined_sam_control_p_values.txt`**: P-values from the Mann-Whitney U test comparing combined SAM (Marasmus and Kwashiorkor) versus Control.
  - **`p_values.txt`**: P-values for individual bile acids from t-tests.
  - **`Cholic_acid`**:
    - **`Cholic_acid_boxplot.png`**: Box plot for Cholic acid levels by subject diagnosis.
  - **`Deoxycholic_acid`**:
    - **`Deoxycholic_acid_boxplot.png`**: Box plot for Deoxycholic acid levels by subject diagnosis.
  - **`Glycodeoxycholic_acid`**:
    - **`Glycodeoxycholic_acid_boxplot.png`**: Box plot for Glycodeoxycholic acid levels by subject diagnosis.
  - **`Glycolitocholic_acid`**:
    - **`Glycolitocholic_acid_boxplot.png`**: Box plot for Glycolitocholic acid levels by subject diagnosis.

- **`data_info`**:
  - **`ranked`**:
    - **`explained_variance_ratio_ranked.png`**: Bar graph of the explained variance ratio by principal component.
    - **`maov_test_results_ranked.txt`**: MANOVA test results for ranked data.
    - **`3d_pca_plot_ranked.png`**: 3D PCA plot for ranked data.
  - **`normalized`**:
    - **`explained_variance_ratio_normalized.png`**: Bar graph of the explained variance ratio by principal component.
    - **`maov_test_results_normalized.txt`**: MANOVA test results for normalized data.
    - **`3d_pca_plot_normalized.png`**: 3D PCA plot for normalized data.
  - **`variance_summary.txt`**: Summary of the explained variance for each principal component.
  - **`shapiro_test_results.txt`**: Shapiro-Wilk test results for normality testing.

- **`cluster`**:
  - **`ranked`**:
    - **`kmeans_clustering_ranked.png`**: K-means clustering plot for ranked data.
    - **`hierarchical_clustering_ranked.png`**: Hierarchical clustering dendrogram for ranked data.
  - **`normalized`**:
    - **`kmeans_clustering_normalized.png`**: K-means clustering plot for normalized data.
    - **`hierarchical_clustering_normalized.png`**: Hierarchical clustering dendrogram for normalized data.

## Notes
- Ensure the input files are correctly named and placed in the `input` directory.
- The scripts dynamically set input and output paths relative to the script location, facilitating easy execution from any environment.

## Next Steps
- Fix cluster graphs to display more meaningful information
- Run regression analysis

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.




