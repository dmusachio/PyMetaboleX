"""
run_all.py

This script orchestrates the data processing pipeline by running a series of Python scripts in sequence:
1. Optionally runs the data harmonization script.
2. Runs the data evaluation script.
3. Runs the clustering analysis script.
4. Runs the bile acid analysis script.
5. Runs linear regression and random forest analysis.
6. Runs p-value calculation.

The script logs the output and errors from each script and ensures that any errors encountered will stop the pipeline.

Usage:
    Run the script directly to execute the data processing pipeline.
    Example: python run_all.py

Dependencies:
    - subprocess
    - shutil
    - os

Author:
    Daniel Musachio

Date:
    July 2024
"""

import subprocess
import shutil
import os

def read_config(config_file):
    """
    Read configuration settings from a text file.

    Parameters:
    config_file (str): Path to the configuration file.

    Returns:
    dict: Dictionary containing configuration settings.
    """
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            if value.lower() == 'none':
                config[key] = None
            elif value.lower() == 'true':
                config[key] = True
            elif value.lower() == 'false':
                config[key] = False
            else:
                try:
                    config[key] = float(value)
                except ValueError:
                    config[key] = value
    return config

def run_script(script_name, verbose=True):
    """
    Run a given Python script and capture its output and errors.

    Parameters:
    script_name (str): The name of the script to run.
    verbose (bool): Whether to print the output and errors.

    Returns:
    None
    """
    print(f"Running {script_name}...")
    process = subprocess.Popen(
        ["python3", script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        env=dict(os.environ, PYTHONUNBUFFERED="1")
    )

    while True:
        output = process.stdout.readline()
        if output and verbose:
            print(output, end='')
        err = process.stderr.readline()
        if err and verbose:
            print(err, end='')
        if output == '' and err == '' and process.poll() is not None:
            break

    return_code = process.poll()
    if return_code == 0:
        print(f"{script_name} completed successfully.")
    else:
        print(f"Error running {script_name}.")
        exit(1)

def main():
    """
    Main function to orchestrate the data processing pipeline.

    Parameters:
    None

    Returns:
    None
    """
    config = read_config('src/config.txt')
    
    print("Starting data processing pipeline...")

    # Remove 'output' directory if it exists
    if os.path.exists('output'):
        shutil.rmtree('output')
        print("Removed 'output' directory.")

    # Check if data harmonization should be run
    run_harmonization = config.get('run_harmonization', False)
    if run_harmonization:
        # Remove 'processed' directory if it exists
        if os.path.exists('processed'):
            shutil.rmtree('processed')
            print("Removed 'processed' directory.")
        # Run data harmonization
        run_script("src/data_harmonization.py")
    else:
        # Ensure 'processed' directory exists and contains specified data file
        processed_data_file = config.get('processed_data_file', 'processed/cleaned_data.csv')
        if not os.path.exists(processed_data_file):
            print(f"Error: Specified data file '{processed_data_file}' does not exist.")
            exit(1)
        os.environ['PROCESSED_DATA_FILE'] = processed_data_file

    # Run quality control script
    run_script("src/qc.py")

    # Run data evaluation script
    run_script("src/evaluate_data.py")

    # Run clustering analysis script
    run_script("src/cluster.py")

    # Run bile acid analysis script
    run_script("src/bile_acid.py")

    # Run linear regression script without printing output
    run_script("src/linear_reg.py", verbose=False)

    # Run random forest analysis script
    run_script("src/random_forest.py")

    # Run p-value calculation script without printing output
    run_script("src/calc_p.py", verbose=False)

    print("Data processing pipeline completed successfully.")

if __name__ == "__main__":
    main()
