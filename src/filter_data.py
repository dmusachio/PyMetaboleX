import pandas as pd
import numpy as np
import sys

class MetaboliteQC:
    def __init__(self, 
                 filter_column_constant=True,
                 filter_column_missing_rate_threshold=0.5,
                 filter_row_missing_rate_threshold=None,
                 filter_column_zero_rate_threshold=0.25,
                 replace_outlier_method=None,
                 nSD=5,
                 impute_method="half-min",
                 verbose=True):
        
        self.filter_column_constant = filter_column_constant
        self.filter_column_missing_rate_threshold = filter_column_missing_rate_threshold
        self.filter_row_missing_rate_threshold = filter_row_missing_rate_threshold
        self.filter_column_zero_rate_threshold = filter_column_zero_rate_threshold
        self.replace_outlier_method = replace_outlier_method
        self.nSD = nSD
        self.impute_method = impute_method
        self.verbose = verbose
        self.log = []

    def log_change(self, message):
        self.log.append(message)
        if self.verbose:
            print(message)

    def save_log(self, file_path):
        with open(file_path, 'w') as f:
            for entry in self.log:
                f.write(entry + "\n")

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        self.meta_data = self.data.iloc[:, :8]
        self.metabolite_data = self.data.iloc[:, 8:]
        self.metabolite_data = self.metabolite_data.apply(pd.to_numeric, errors='coerce')
        self.log_change(f"Loaded data from {file_path}")
        self.verify_format()

    def verify_format(self):
        print("Verifying CSV format...")
        print("ID column values (This should be the ID values, if not, reformat):")
        print(self.data['ID'].head())
        print("SUBJECTID column values (This should be the SUBJECTID values, if not, reformat):")
        print(self.data['SUBJECTID'].head())
        print("Subject Diagnosis column values (This should be the Subject Diagnosis values, if not, reformat):")
        print(self.data['Subject Diagnosis'].head())

    def filter_constant_columns(self):
        if self.filter_column_constant:
            initial_cols = self.metabolite_data.shape[1]
            self.metabolite_data = self.metabolite_data.loc[:, self.metabolite_data.nunique() > 1]
            filtered_cols = self.metabolite_data.shape[1]
            self.log_change(f"Filtered constant columns: {initial_cols - filtered_cols} columns removed")

    def filter_by_missing_rate(self):
        if self.filter_column_missing_rate_threshold is not None:
            col_threshold = self.metabolite_data.shape[0] * self.filter_column_missing_rate_threshold
            initial_cols = self.metabolite_data.shape[1]
            self.metabolite_data = self.metabolite_data.loc[:, self.metabolite_data.isna().sum() < col_threshold]
            filtered_cols = self.metabolite_data.shape[1]
            self.log_change(f"Filtered columns with missing rate above {self.filter_column_missing_rate_threshold}: {initial_cols - filtered_cols} columns removed")

        if self.filter_row_missing_rate_threshold is not None:
            row_threshold = self.metabolite_data.shape[1] * self.filter_row_missing_rate_threshold
            initial_rows = self.metabolite_data.shape[0]
            self.metabolite_data = self.metabolite_data.loc[self.metabolite_data.isna().sum(axis=1) < row_threshold, :]
            filtered_rows = self.metabolite_data.shape[0]
            self.log_change(f"Filtered rows with missing rate above {self.filter_row_missing_rate_threshold}: {initial_rows - filtered_rows} rows removed")

    def filter_by_zero_rate(self):
        if self.filter_column_zero_rate_threshold is not None:
            zero_threshold = self.metabolite_data.shape[0] * self.filter_column_zero_rate_threshold
            initial_cols = self.metabolite_data.shape[1]
            self.metabolite_data = self.metabolite_data.loc[:, (self.metabolite_data == 0).sum() < zero_threshold]
            filtered_cols = self.metabolite_data.shape[1]
            self.log_change(f"Filtered columns with zero rate above {self.filter_column_zero_rate_threshold}: {initial_cols - filtered_cols} columns removed")

    def replace_outliers(self):
        if self.replace_outlier_method:
            if self.replace_outlier_method == "median":
                median = self.metabolite_data.median()
                std_dev = self.metabolite_data.std()
                outliers = (np.abs(self.metabolite_data - median) > self.nSD * std_dev)
                self.metabolite_data = self.metabolite_data.mask(outliers, median, axis=1)
                self.log_change(f"Replaced outliers using median method with nSD={self.nSD}")

    def impute_missing_values(self):
        if self.impute_method == "half-min":
            min_values = self.metabolite_data.min() / 2
            self.metabolite_data = self.metabolite_data.apply(lambda x: x.fillna(min_values))
        elif self.impute_method == "median":
            self.metabolite_data = self.metabolite_data.apply(lambda x: x.fillna(x.median()))
        elif self.impute_method == "mean":
            self.metabolite_data = self.metabolite_data.apply(lambda x: x.fillna(x.mean()))
        elif self.impute_method == "zero":
            self.metabolite_data = self.metabolite_data.fillna(0)
        self.log_change(f"Imputed missing values using {self.impute_method} method")

    def run_QC_pipeline(self, file_path):
        self.load_data(file_path)
        self.filter_constant_columns()
        self.filter_by_missing_rate()
        self.filter_by_zero_rate()
        self.replace_outliers()
        self.impute_missing_values()
        self.data = pd.concat([self.meta_data, self.metabolite_data], axis=1)
        self.log_change("QC pipeline completed")
        return self.data

def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default: {default}): ")
    return user_input if user_input else default

def main():
    print("Please provide input for the following parameters. Press Enter to use the default value.")
    sys.stdout.flush()

    file_path = get_user_input("Path to the input CSV file", 'processed/cleaned_data.csv')

    # Load and verify the format of the CSV file
    print("Loading and verifying CSV format...")
    qc_pipeline = MetaboliteQC()
    qc_pipeline.load_data(file_path)
    
    filter_column_constant = get_user_input("Filter columns with constant value [True, False]", 'True') == 'True'
    print(f"Filter columns with constant value chosen: {filter_column_constant}")
    
    filter_column_missing_rate_threshold = float(get_user_input("Threshold to filter columns by missing rate (e.g., 0.5)", 0.5))
    print(f"Threshold to filter columns by missing rate chosen: {filter_column_missing_rate_threshold}")
    
    filter_row_missing_rate_threshold = get_user_input("Threshold to filter rows by missing rate (e.g., 0.25) or 'None'", 'None')
    filter_row_missing_rate_threshold = float(filter_row_missing_rate_threshold) if filter_row_missing_rate_threshold != 'None' else None
    print(f"Threshold to filter rows by missing rate chosen: {filter_row_missing_rate_threshold}")
    
    filter_column_zero_rate_threshold = float(get_user_input("Threshold to filter columns by zero rate (e.g., 0.25)", 0.25))
    print(f"Threshold to filter columns by zero rate chosen: {filter_column_zero_rate_threshold}")
    
    replace_outlier_method = get_user_input("Method to replace outliers [None, median]", 'None')
    replace_outlier_method = replace_outlier_method if replace_outlier_method != 'None' else None
    print(f"Method to replace outliers chosen: {replace_outlier_method}")
    
    nSD = int(get_user_input("Number of standard deviations to define outliers (e.g., 5)", 5))
    print(f"Number of standard deviations to define outliers chosen: {nSD}")
    
    impute_method = get_user_input("Method to impute missing values [half-min, median, mean, zero]", 'half-min')
    print(f"Method to impute missing values chosen: {impute_method}")
    
    verbose = get_user_input("Print log information [True, False]", 'True') == 'True'
    print(f"Print log information chosen: {verbose}")

    # Update the qc_pipeline instance with the chosen parameters
    qc_pipeline.filter_column_constant = filter_column_constant
    qc_pipeline.filter_column_missing_rate_threshold = filter_column_missing_rate_threshold
    qc_pipeline.filter_row_missing_rate_threshold = filter_row_missing_rate_threshold
    qc_pipeline.filter_column_zero_rate_threshold = filter_column_zero_rate_threshold
    qc_pipeline.replace_outlier_method = replace_outlier_method
    qc_pipeline.nSD = nSD
    qc_pipeline.impute_method = impute_method
    qc_pipeline.verbose = verbose

    processed_data = qc_pipeline.run_QC_pipeline(file_path)
    output_file_path = 'processed/processed_cleaned_data.csv'
    log_file_path = 'processed/changes_log.txt'
    processed_data.to_csv(output_file_path, index=False)
    qc_pipeline.save_log(log_file_path)
    print(f"QC pipeline completed and data saved to '{output_file_path}'")
    print(f"Log of changes saved to '{log_file_path}'")

if __name__ == "__main__":
    main()
