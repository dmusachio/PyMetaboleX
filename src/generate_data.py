import pandas as pd
import numpy as np
import os

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

def filter_by_rsd(data, qc_data, threshold):
    log = []
    qc_rsd = qc_data.std() / qc_data.mean()
    high_rsd_columns = qc_rsd[qc_rsd > threshold / 100.0].index
    removed_columns = []
    for col in high_rsd_columns:
        if col in data.columns:
            data = data.drop(columns=[col])
            removed_columns.append(col)
    log.append(f"Number of metabolites removed based on RSD threshold ({threshold}%): {len(removed_columns)}")
    log.extend(removed_columns)
    return data, log

def filter_by_iqr(data, iqr_threshold):
    log = []
    iqr = data.quantile(0.75) - data.quantile(0.25)
    low_iqr_columns = iqr[iqr < iqr_threshold].index
    removed_columns = []
    for col in low_iqr_columns:
        if col in data.columns:
            data = data.drop(columns=[col])
            removed_columns.append(col)
    log.append(f"Number of metabolites removed with low IQR: {len(removed_columns)}")
    log.extend(removed_columns)
    return data, log

def filter_by_baseline(data, baseline_threshold):
    log = []
    low_mean_columns = data.columns[data.mean() < baseline_threshold]
    removed_columns = []
    for col in low_mean_columns:
        if col in data.columns:
            data = data.drop(columns=[col])
            removed_columns.append(col)
    log.append(f"Number of metabolites removed close to baseline or detection limit: {len(removed_columns)}")
    log.extend(removed_columns)
    return data, log

def normalize_data(data):
    return (data - data.mean()) / data.std()

def perform_normality_test(data):
    from scipy.stats import shapiro
    log = []
    non_normal_columns = []
    for column in data.columns:
        stat, p = shapiro(data[column].dropna())
        if p < 0.05:
            data = data.drop(columns=[column])
            non_normal_columns.append(column)
    log.append(f"Number of non-normal metabolites removed: {len(non_normal_columns)}")
    log.extend(non_normal_columns)
    return data, log

def main():
    config = read_config('src/config.txt')

    input_file = config.get('input_file')
    qc_file = config.get('qc_file')
    perform_qc = config.get('perform_qc', 'no').lower() == 'yes'
    rsd_threshold = float(config.get('rsd_threshold', 20))
    filter_iqr = config.get('filter_iqr', 'no').lower() == 'yes'
    iqr_threshold = float(config.get('iqr_threshold', 0.1))
    filter_baseline = config.get('filter_baseline', 'no').lower() == 'yes'
    baseline_threshold = float(config.get('baseline_threshold', 0.1))
    normalize = config.get('normalize', 'no').lower() == 'yes'
    perform_normality = config.get('perform_normality', 'no').lower() == 'yes'

    data = pd.read_excel(input_file, index_col=0)
    if perform_qc:
        qc_data = pd.read_excel(qc_file, index_col=0)

    # Ensure all values except the first column are numeric
    data.iloc[:, 1:] = data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    if perform_qc:
        qc_data.iloc[:, 1:] = qc_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    log = []
    original_count = data.shape[1] - 1  # Exclude the first column

    if perform_qc:
        data, qc_log = filter_by_rsd(data, qc_data, rsd_threshold)
        log.extend(qc_log)

    if filter_iqr:
        data, iqr_log = filter_by_iqr(data, iqr_threshold)
        log.extend(iqr_log)

    if filter_baseline:
        data, baseline_log = filter_by_baseline(data, baseline_threshold)
        log.extend(baseline_log)

    if normalize:
        data.iloc[:, 1:] = normalize_data(data.iloc[:, 1:])
        log.append("Normalized the data.")

    if perform_normality:
        data, normality_log = perform_normality_test(data)
        log.extend(normality_log)

    final_count = data.shape[1] - 1  # Exclude the first column

    os.makedirs('data', exist_ok=True)
    data.to_csv('data/final_data.csv')

    with open('data/filter_log.txt', 'w') as log_file:
        log_file.write(f"Original number of metabolites: {original_count}\n\n")
        step = 1
        for entry in log:
            if 'Number of' in entry:
                log_file.write(f"\nStep {step}: {entry}\n")
                step += 1
            else:
                log_file.write(entry + '\n')
        log_file.write(f"\nFinal number of metabolites: {final_count}\n")

    ranked_data = data.rank(axis=0)
    ranked_data.to_csv('data/ranked_data.csv')

if __name__ == "__main__":
    main()
