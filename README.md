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
│   ├── data_harmonization.py
│   └── evaluate_data.py
├── processed/
│   ├── patients_summary.txt
│   ├── cleaned_data.csv
│   └── data_cleanup_stats.txt
├── output/
│   ├── explained_variance_ratio.png
│   ├── PCA_{i}_explained_variance.png    # for each principal component i
│   └── PC{i}_boxplot.png                  # for each principal component i
└── README.md

input/: Contains all raw Excel data files.
src/: Python scripts for data processing and evaluation.
processed/: Processed data outputs, summaries, and statistics.
output/: Visualizations such as variance explained and boxplots for each principal component

```

## Setup

### Prerequisites
- Access to NIH biowulf account.

### Installing Dependencies
All dependencies should be pre-installed on biowulf.

## Running the Scripts
1. Log in to biowulf.
2. Type 'sinteractive' and wait to be allocated a node.
3. Navigate to the project root directory.

Execute the scripts sequentially:

python3 src/data_harmonization.py
python3 src/evaluate_data.py

## Output
The scripts will generate files in the `processed` and `output` directories:
/processed
1. **patients_summary.txt**: A summary of patient data.
2. **cleaned_data.csv**: The cleaned and processed data.
3. **data_cleanup_stats.txt**: Statistics about the data cleaning process.
/output
4. **explained_variance_ratio.png**: Bar graph of the explained variance ratio by principal component.
5. **PCA_{i}_explained_variance.png**: Cumulative explained variance plots for each principal component.
6. **PC{i}_boxplot.png**: Box plots for each principal component across different phenotypes.

## Notes
- Ensure the input files are correctly named and placed in the `input` directory.
- The scripts dynamically set input and output paths relative to the script location, facilitating easy execution from any environment.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.
