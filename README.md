# MetabolomicsAnalyzer

## Demo Video
TBD

## Overview
This project involves a comprehensive data processing pipeline thatanalyzes metabolite data from an Excel input file (and an optional QC Excel file). The scripts in this project perform a series of tasks including data cleaning, csv generation, and extensive statistical analysis. The analysis includes methods such as Principal Component Analysis (PCA) and Multivariate Analysis of Variance (MANOVA). Additionally, the pipeline includes steps for quality control, clustering analysis, linear regression, and random forest classification. The aim is to ensure data integrity and provide meaningful insights into metabolite levels across different subject groups. While the data pipeline can be run on any metabolic data, the input data is 'fake' data that is a demo for users. The output directory is also 'fake' demo results. The 'output malnutrition' are the actual results comparing metabolic differences across Edematous and Non-Edematous (both forms of Severe Acute Malntrition) children from a cohort in Malawi.


## Directory Structure
```plaintext
├── output
│   ├── cluster
│   │   ├── hierarchical_clustering.png
│   │   └── kmeans_clustering.png
│   ├── cluster_r
│   │   ├── hierarchical_clustering.png
│   │   └── kmeans_clustering.png
│   ├── evaluate_data
│   │   ├── 3d_pca_plot.png
│   │   ├── explained_variance_ratio.png
│   │   ├── manova_test_results.txt
│   │   └── variance_summary.txt
│   ├── evaluate_data_r
│   │   ├── 3d_pca_plot.png
│   │   ├── explained_variance_ratio.png
│   │   ├── manova_test_results.txt
│   │   └── variance_summary.txt
│   ├── linear_reg
│   │   └── Cancer_vs_Control_regression_summaries.txt
│   ├── linear_reg_r
│   │   └── Cancer_vs_Control_regression_summaries.txt
│   ├── p_values
│   │   ├── Metabolite_10.png
│   │   ├── Metabolite_1.png
│   │   ├── Metabolite_2.png
│   │   ├── Metabolite_4.png
│   │   ├── Metabolite_5.png
│   │   ├── Metabolite_6.png
│   │   ├── Metabolite_7.png
│   │   ├── Metabolite_9.png
│   │   └── p_values.txt
│   ├── p_values_r
│   │   ├── Metabolite_10.png
│   │   ├── Metabolite_1.png
│   │   ├── Metabolite_2.png
│   │   ├── Metabolite_4.png
│   │   ├── Metabolite_5.png
│   │   ├── Metabolite_6.png
│   │   ├── Metabolite_7.png
│   │   ├── Metabolite_9.png
│   │   └── p_values.txt
│   ├── random_forest
│   │   └── classification_report.csv
│   └── random_forest_r
│       └── classification_report.csv
├── output malnutrition
│   ├── cluster
│   │   ├── hierarchical_clustering.png
│   │   └── kmeans_clustering.png
│   ├── evaluate_data
│   │   ├── 3d_pca_plot.png
│   │   ├── explained_variance_ratio.png
│   │   ├── manova_test_results.txt
│   │   └── variance_summary.txt
│   ├── linear_reg
│   │   ├── Acetylcarnitine_regression.png
│   │   ├── Carnitine_regression.png
│   │   ├── Edematous_vs_Non Edematous_regression_summaries.txt
│   │   └── Propionylcarnitine_regression.png
│   ├── p_values
│   │   ├── 3-Indolepropionic_acid.png
│   │   ├── Ceramide__d18_1_16_0_.png
│   │   ├── Deoxycholic_acid.png
│   │   ├── Hexosylceramide__d18_1_20_0_.png
│   │   ├── Hippuric_acid.png
│   │   ├── LPI_18_1.png
│   │   ├── PE_33_1.png
│   │   ├── PE_33_2.png
│   │   ├── PE_34_1.png
│   │   ├── PE_34_2.png
│   │   ├── PE_35_1.png
│   │   ├── PE_35_2.png
│   │   ├── PE_35_3.png
│   │   ├── PE_36_1.png
│   │   ├── PE_36_2.png
│   │   ├── PE_36_3.png
│   │   ├── PE_36_4.png
│   │   ├── PE_36_5.png
│   │   ├── PE_38_4.png
│   │   ├── PE_38_5.png
│   │   ├── PE_38_7.png
│   │   ├── PE_40_4.png
│   │   ├── PE_40_8.png
│   │   ├── PG_16_1_18_2.png
│   │   ├── PG_16_2_18_2.png
│   │   ├── PG_18_2_20_3.png
│   │   ├── PG_18_2_22_3.png
│   │   ├── Phosphatidylcholine_aa_C40_2.png
│   │   ├── PI_14_0_18_2.png
│   │   ├── PI_15_0_16_0.png
│   │   ├── PI_15_1_16_0.png
│   │   ├── PI_16_0_18_1.png
│   │   ├── PI_16_0_18_2.png
│   │   ├── PI_17_1_18_2.png
│   │   ├── PI_18_0_18_2.png
│   │   ├── PI_18_1_18_1.png
│   │   ├── PI_18_2_22_1.png
│   │   ├── PI_18_2_22_6.png
│   │   ├── PS_36_5.png
│   │   ├── PS_38_5.png
│   │   ├── p_values.txt
│   │   ├── Triacylglyceride__14_0_36_1_.png
│   │   ├── Triacylglyceride__16_0_28_2_.png
│   │   ├── Triacylglyceride__16_0_32_3_.png
│   │   ├── Triacylglyceride__16_0_34_2_.png
│   │   ├── Triacylglyceride__17_2_36_3_.png
│   │   ├── Triacylglyceride__18_0_32_1_.png
│   │   ├── Triacylglyceride__18_0_32_2_.png
│   │   ├── Triacylglyceride__18_0_34_2_.png
│   │   ├── Triacylglyceride__18_0_34_3_.png
│   │   ├── Triacylglyceride__18_1_32_0_.png
│   │   ├── Triacylglyceride__18_2_32_0_.png
│   │   ├── Triacylglyceride__18_2_34_0_.png
│   │   ├── Triacylglyceride__18_3_34_0_.png
│   │   └── Triacylglyceride__20_1_32_2_.png
│   └── random_forest
│       ├── classification_report.csv
│       ├── feature_importances.png
│       └── top_features.txt
├── README.md
├── ref
│   ├── Impaired Bile Acid Homeostasis in Children with Severe Acute Malnutrition.pdf
│   └── MUSACHIO_POSTER_FINAL.pptx
└── src
    ├── calc_p.py
    ├── cluster.py
    ├── config.txt
    ├── evaluate_data.py
    ├── generate_data.py
    ├── group_config.txt
    ├── group.py
    ├── job_info.txt
    ├── linear_reg.py
    ├── random_forest.py
    └── run_jobs.py

19 directories, 116 files

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
2. Optionally, type `rm -r output` so that new output folder can be generated.
3. Type `sinteractive` and wait to be allocated a node.
4. Update the config.txt, group_config.txt and job_info.txt file as neccesary (refer to YouTube demo for more information)
5. Execute the script:

```bash
python3 src/generate_data.py
python3 src/group.py
python3 src/run_jobs.py
```

## Output Details

The scripts will generate files in the directories you specify in job_info.txt

## Notes
- Ensure the input files are correctly named and placed in the `input` directory.
- The scripts dynamically set input and output paths relative to the script location, facilitating easy execution from any environment.


## Citation for MetabolomicsAnalyzer:
Daniel Musachio. 2024. *MetabolomicsAnalyzer: A Streamlined Workflow to Analyze Metabolomic Data in Python*. Unpublished tool. Available at https://github.com/dmusachio/MetabolomicsAnalyzer.

## Contributing and Contact
Contributions are welcome! If you have suggestions or improvements, please feel free to reach out to me at dmusachi@stanford.edu. Also, feel free to reach out for debuggining issues. I am very eager to have MetabolomicsAnalyzer help you in your research so please consider trying out this software and citing it if it produces something useful! Thank you very much!
