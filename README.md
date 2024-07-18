# Malnutrition Metabolite Data Harmonization and Analysis

## Overview
This project involves a comprehensive data processing pipeline that harmonizes and analyzes metabolite data from multiple Excel input files. The scripts in this project perform a series of tasks including data cleaning, patient ID matching, phenotype harmonization, and extensive statistical analysis. The analysis includes methods such as Principal Component Analysis (PCA) and Multivariate Analysis of Variance (MANOVA). Additionally, the pipeline includes steps for quality control, clustering analysis, bile acid analysis, linear regression, and random forest classification. The aim is to ensure data integrity and provide meaningful insights into metabolite levels across different subject groups, specifically focusing on conditions such as Kwashiorkor, Marasmus, and other related phenotypes.


## Directory Structure
```plaintext
├── input
│   ├── master_data.xlsx
│   ├── metabolite_data.xlsx
│   ├── meta_data.xlsx
│   └── qc.xlsx
├── output
│   ├── bile_acid
│   │   ├── Cholic_acid
│   │   │   └── Cholic_acid_boxplot.png
│   │   ├── combined_p_values.txt
│   │   ├── combined_sam_control_boxplot.png
│   │   ├── combined_sam_control_p_values.txt
│   │   ├── Deoxycholic_acid
│   │   │   └── Deoxycholic_acid_boxplot.png
│   │   ├── Glycodeoxycholic_acid
│   │   │   └── Glycodeoxycholic_acid_boxplot.png
│   │   ├── Glycolitocholic_acid
│   │   │   └── Glycolitocholic_acid_boxplot.png
│   │   └── p_values.txt
│   ├── cluster
│   │   ├── normalized
│   │   │   ├── hierarchical_clustering_normalized.png
│   │   │   └── kmeans_clustering_normalized.png
│   │   └── ranked
│   │       ├── hierarchical_clustering_ranked.png
│   │       └── kmeans_clustering_ranked.png
│   ├── data_info
│   │   ├── normalized
│   │   │   ├── 3d_pca_plot_normalized.png
│   │   │   ├── explained_variance_ratio_normalized.png
│   │   │   └── maov_test_results_normalized.txt
│   │   ├── ranked
│   │   │   ├── 3d_pca_plot_ranked.png
│   │   │   ├── explained_variance_ratio_ranked.png
│   │   │   └── maov_test_results_ranked.txt
│   │   ├── shapiro_test_results.txt
│   │   └── variance_summary.txt
│   ├── linear_reg
│   │   ├── Acetylcarnitine_regression.png
│   │   ├── Carnitine_regression.png
│   │   ├── Control_vs_Case_regression_summaries.txt
│   │   └── Propionylcarnitine_regression.png
│   ├── p_values
│   │   ├── control_mam_vs_kwash_marasmus
│   │   │   └── p_values_less_than_0.01.txt
│   │   ├── control_vs_kwash
│   │   │   ├── Deoxycholic_acid.png
│   │   │   ├── Hippuric_acid.png
│   │   │   └── p_values_less_than_0.01.txt
│   │   ├── control_vs_kwash_marasmus
│   │   │   └── p_values_less_than_0.01.txt
│   │   ├── control_vs_marasmus
│   │   │   ├── Alanine_.png
│   │   │   ├── LPE_18_1.png
│   │   │   ├── LPE_18_2.png
│   │   │   ├── LPG_16_1.png
│   │   │   ├── Lysophosphatidylcholine_a_C18_2.png
│   │   │   ├── Methionine_sulfoxide.png
│   │   │   ├── PA_16_0_18_1.png
│   │   │   ├── PA_18_1_18_3.png
│   │   │   ├── PE_P-18_0_20_4.png
│   │   │   ├── PE_P-18_1_20_4.png
│   │   │   ├── Phosphatidylcholine_ae_C40_1.png
│   │   │   ├── p_values_less_than_0.01.txt
│   │   │   └── Serine.png
│   │   ├── mam_vs_kwash
│   │   │   ├── Chenodeoxycholic_acid.png
│   │   │   ├── Cholic_acid.png
│   │   │   ├── LPA_22_3.png
│   │   │   ├── LPI_19_0.png
│   │   │   ├── PA_17_0_18_3.png
│   │   │   ├── PG_16_0_22_2.png
│   │   │   └── p_values_less_than_0.01.txt
│   │   ├── mam_vs_marasmus
│   │   │   ├── Alanine_.png
│   │   │   ├── Diacylglyceride__16_1_18_1_.png
│   │   │   ├── LPE_20_0.png
│   │   │   ├── LPG_16_1.png
│   │   │   ├── LPG_18_1.png
│   │   │   ├── LPI_16_0.png
│   │   │   ├── PA_16_0_18_1.png
│   │   │   ├── PA_16_2_18_1.png
│   │   │   ├── PA_17_0_18_1.png
│   │   │   ├── PA_17_1_18_1.png
│   │   │   ├── PA_17_2_18_1.png
│   │   │   ├── PA_18_1_18_1.png
│   │   │   ├── PA_18_1_18_3.png
│   │   │   ├── PA_18_1_20_2.png
│   │   │   ├── PA_18_1_20_3.png
│   │   │   ├── PA_18_1_22_1.png
│   │   │   ├── PA_18_1_22_2.png
│   │   │   ├── PA_18_1_22_3.png
│   │   │   ├── PG_15_0_18_1.png
│   │   │   ├── PG_16_0_16_0.png
│   │   │   ├── PG_16_0_22_2.png
│   │   │   ├── PG_17_0_18_1.png
│   │   │   ├── PG_17_1_18_1.png
│   │   │   ├── PG_18_1_18_1.png
│   │   │   ├── PG_18_1_18_3.png
│   │   │   ├── PG_18_1_20_5.png
│   │   │   ├── PG_18_1_22_0.png
│   │   │   ├── PI_14_0_18_1.png
│   │   │   ├── PI_18_0_20_4.png
│   │   │   ├── PI_18_1_22_2.png
│   │   │   ├── Proline.png
│   │   │   ├── p_values_less_than_0.01.txt
│   │   │   ├── Sarcosine.png
│   │   │   └── Triacylglyceride__18_3_38_5_.png
│   │   └── marasmus_vs_kwash
│   │       ├── Alanine_.png
│   │       ├── Ceramide__d18_2_24_0_.png
│   │       ├── Decanoylcarnitine.png
│   │       ├── Deoxycholic_acid.png
│   │       ├── PA_18_1_18_3.png
│   │       └── p_values_less_than_0.01.txt
│   └── random_forest
│       ├── all_groups
│       │   ├── classification_report.csv
│       │   ├── feature_importances.png
│       │   └── top_features.txt
│       ├── combined_vs_control
│       │   ├── classification_report.csv
│       │   ├── feature_importances.png
│       │   └── top_features.txt
│       ├── combined_vs_mam
│       │   ├── classification_report.csv
│       │   ├── feature_importances.png
│       │   └── top_features.txt
│       └── marasmus_vs_kwashiorkor
│           ├── classification_report.csv
│           ├── feature_importances.png
│           └── top_features.txt
├── processed
│   ├── changes_log.txt
│   ├── cleaned_data.csv
│   ├── data_cleanup_stats.txt
│   ├── normalized_data.csv
│   ├── patients_summary.txt
│   ├── processed_cleaned_data.csv
│   ├── ranked_data.csv
│   ├── rsd_plot.png
│   ├── rsd_results.txt
│   └── sorted_rsd.csv
├── README.md
├── ref
│   └── Impaired Bile Acid Homeostasis in Children with Severe Acute Malnutrition.pdf
└── src
    ├── bile_acid.py
    ├── calc_p.py
    ├── cluster.py
    ├── config.txt
    ├── data_harmonization.py
    ├── evaluate_data.py
    ├── linear_reg.py
    ├── qc.py
    ├── random_forest.py
    └── run_all.py

31 directories, 127 files
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
4. Update the config.txt file as neccesary.
5. Execute the script:

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

- **`cluster (CURRENTLY UNDER CONSTRUCTION: ERRORS WITH DISPLAY OF PHENOTYPES)`**:
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
- Fix cluster graphs to display more meaningful information.
- Run regression analysis.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.
