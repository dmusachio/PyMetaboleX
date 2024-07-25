import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
        """
        Initialize the MetaboliteQC class with parameters for various QC steps.

        Parameters:
        filter_column_constant (bool): Whether to filter out columns with constant values.
        filter_column_missing_rate_threshold (float): Threshold for filtering columns by missing data rate.
        filter_row_missing_rate_threshold (float): Threshold for filtering rows by missing data rate.
        filter_column_zero_rate_threshold (float): Threshold for filtering columns by zero rate.
        replace_outlier_method (str): Method to replace outliers ('median' or None).
        nSD (int): Number of standard deviations to define outliers.
        impute_method (str): Method to impute missing values ('half-min', 'median', 'mean', 'zero').
        verbose (bool): Whether to print log messages.
        """
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
        """
        Log a change message.

        Parameters:
        message (str): The message to log.
        """
        self.log.append(message)
        if self.verbose:
            print(message)

    def save_log(self, file_path):
        """
        Save the log to a file.

        Parameters:
        file_path (str): The path to the log file.
        """
        with open(file_path, 'w') as f:
            for entry in self.log:
                f.write(entry + "\n")

    def load_data(self, file_path):
        """
        Load data from a CSV file and split it into metadata and metabolite data.

        Parameters:
        file_path (str): The path to the CSV file.
        """
        self.data = pd.read_excel(file_path)
        self.meta_data = self.data.iloc[:, :8]
        self.metabolite_data = self.data.iloc[:, 8:]
        self.metabolite_data = self.metabolite_data.apply(pd.to_numeric, errors='coerce')
        self.log_change(f"Loaded data from {file_path}")
        self.verify_format()

    def verify_format(self):
        """
        Verify the format of the CSV file.
        """
        print("Verifying Excel format...")
        print("ID column values (This should be the ID values, if not, reformat):")
        print(self.data['ID'].head())
        print("SUBJECTID column values (This should be the SUBJECTID values, if not, reformat):")
        print(self.data['SUBJECTID'].head())
        print("Subject Diagnosis column values (This should be the Subject Diagnosis values, if not, reformat):")
        print(self.data['Subject Diagnosis'].head())

    def filter_constant_columns(self):
        """
        Filter out columns with constant values.
        """
        if self.filter_column_constant:
            initial_cols = self.metabolite_data.shape[1]
            self.metabolite_data = self.metabolite_data.loc[:, self.metabolite_data.nunique() > 1]
            filtered_cols = self.metabolite_data.shape[1]
            self.log_change(f"Filtered constant columns: {initial_cols - filtered_cols} columns removed")

    def filter_by_missing_rate(self):
        """
        Filter out columns and rows based on missing data rate.
        """
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
        """
        Filter out columns with a high rate of zero values.
        """
        if self.filter_column_zero_rate_threshold is not None:
            zero_threshold = self.metabolite_data.shape[0] * self.filter_column_zero_rate_threshold
            initial_cols = self.metabolite_data.shape[1]
            self.metabolite_data = self.metabolite_data.loc[:, (self.metabolite_data == 0).sum() < zero_threshold]
            filtered_cols = self.metabolite_data.shape[1]
            self.log_change(f"Filtered columns with zero rate above {self.filter_column_zero_rate_threshold}: {initial_cols - filtered_cols} columns removed")

    def replace_outliers(self):
        """
        Replace outliers in the data based on the specified method.
        """
        if self.replace_outlier_method:
            if self.replace_outlier_method == "median":
                median = self.metabolite_data.median()
                std_dev = self.metabolite_data.std()
                outliers = (np.abs(self.metabolite_data - median) > self.nSD * std_dev)
                self.metabolite_data = self.metabolite_data.mask(outliers, median, axis=1)
                self.log_change(f"Replaced outliers using median method with nSD={self.nSD}")

    def impute_missing_values(self):
        """
        Impute missing values in the data based on the specified method.
        """
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
        """
        Run the full QC pipeline on the data.

        Parameters:
        file_path (str): The path to the input file.
        """
        self.load_data(file_path)
        self.filter_constant_columns()
        self.filter_by_missing_rate()
        self.filter_by_zero_rate()
        self.replace_outliers()
        self.impute_missing_values()
        self.data = pd.concat([self.meta_data, self.metabolite_data], axis=1)
        self.log_change("QC pipeline completed")
        return self.data

def main():
    """
    Main function to run the QC pipeline and RSD analysis.

    Parameters:
    None
    """
    # File paths
    input_file_path = 'processed/HOLY_DATA.xlsx'
    qc_file_path = 'processed/qc.xlsx'

    # Initialize and run QC pipeline
    qc_pipeline = MetaboliteQC(
        filter_column_constant=True,
        filter_column_missing_rate_threshold=0.5,
        filter_row_missing_rate_threshold=None,
        filter_column_zero_rate_threshold=0.25,
        replace_outlier_method=None,
        nSD=5,
        impute_method="half-min",
        verbose=True
    )

    processed_data = qc_pipeline.run_QC_pipeline(input_file_path)
    log_file_path = 'processed/changes_log.txt'
    processed_data.to_csv('processed/processed_cleaned_data.csv', index=False)
    qc_pipeline.save_log(log_file_path)
    print(f"QC pipeline completed and data saved to 'processed/processed_cleaned_data.csv'")
    print(f"Log of changes saved to '{log_file_path}'")

    # RSD analysis
    rsd_threshold = 20

    # Step 1: Read the qc.xlsx file
    qc_df = pd.read_excel(qc_file_path)

    # Step 2: Extract the relevant metabolite data columns (assuming they start from the 8th column)
    metabolite_data = qc_df.iloc[:, 8:]

    # Ensure all values in metabolite data are numeric, converting non-numeric values to NaN
    metabolite_data = metabolite_data.apply(pd.to_numeric, errors='coerce')

    # Step 3: Calculate RSD for each column
    rsd = metabolite_data.std() / metabolite_data.mean() * 100

    # Step 4: Identify columns with an RSD above the threshold
    high_rsd_columns = rsd[rsd > rsd_threshold].index

    # Step 5: Remove high RSD columns from the processed data
    final_data = processed_data.drop(columns=high_rsd_columns, errors='ignore')

    # Save the final data to a new CSV file in the output folder
    os.makedirs('output', exist_ok=True)
    final_data.to_csv('output/HOLY_DATA_filtered.csv', index=False)

    # Step 6: Plot the RSD values
    sorted_rsd = rsd.sort_values()

    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(sorted_rsd)), sorted_rsd, color='b')
    plt.axhline(y=20, color='r', linestyle='--', label='20% Cut-off')
    plt.axhline(y=30, color='g', linestyle='--', label='30% Cut-off')
    plt.xlabel('Variable Index (Sorted by RSD)')
    plt.ylabel('RSD (%)')
    plt.title('RSD across all variables (Sorted in Ascending Order)')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/rsd_plot.png')
    plt.show()

    # Save the sorted RSD values to a CSV file
    sorted_rsd.to_csv('output/sorted_rsd.csv', header=True)

    # Print the percentage of variables with RSD less than the thresholds and save to a text file
    percentage_below_20 = (sorted_rsd < 20).sum() / len(sorted_rsd) * 100
    percentage_below_30 = (sorted_rsd < 30).sum() / len(sorted_rsd) * 100

    results = [
        f"Percentage of variables with RSD less than 20%: {percentage_below_20:.2f}%",
        f"Percentage of variables with RSD less than 30%: {percentage_below_30:.2f}%"
    ]

    with open('output/rsd_results.txt', 'w') as f:
        for line in results:
            print(line)
            f.write(line + "\n")

if __name__ == "__main__":
    main()
