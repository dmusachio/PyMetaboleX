"""
run_all.py

This script orchestrates the data processing pipeline by running a series of Python scripts in sequence:
1. Optionally runs the data harmonization script.
2. Runs the data evaluation script.
3. Runs the clustering analysis script.
4. Runs the bile acid analysis script.

The script logs the output and errors from each script and ensures that any errors encountered will stop the pipeline.

Some documentation is AI-generated but reviewed by humans.

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

def run_script(script_name):
    """
    Run a given Python script and capture its output and errors.

    Parameters:
    script_name (str): The name of the script to run.

    Returns:
    None
    """
    print(f"Running {script_name}...")
    process = subprocess.Popen(["python3", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        err = process.stderr.readline()
        if err:
            print(err.strip())
        if output == '' and err == '' and process.poll() is not None:
            break

    return_code = process.poll()
    if return_code == 0:
        print(f"{script_name} completed successfully.")
    else:
        print(f"Error running {script_name}.")
        exit(1)

def run_interactive_script(script_name):
    """
    Run a given Python script that requires interactive user input.

    Parameters:
    script_name (str): The name of the script to run.

    Returns:
    None
    """
    print(f"Running {script_name} interactively...")
    return_code = subprocess.call(["python3", script_name])

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
    print("Starting data processing pipeline...")
    # Remove 'output' and 'processed' directories if they exist
    if os.path.exists('output'):
        shutil.rmtree('output')
        print("Removed 'output' directory.")
    if os.path.exists('processed'):
        shutil.rmtree('processed')
        print("Removed 'processed' directory.")

    # Ask user if they want to run data harmonization
    run_harmonization = input("Do you want to run the data harmonization script? (yes/no): ").strip().lower()
    if run_harmonization == 'yes':
        # Run data harmonization
        run_script("src/data_harmonization.py")

    run_script("src/qc.py")

    # Run the interactive script for data evaluation
    run_interactive_script("src/filter_data.py")

    # Run data evaluation
    run_script("src/evaluate_data.py")

    # Run clustering analysis
    run_script("src/cluster.py")

    # Run bile acid analysis
    run_script("src/bile_acid.py")

    print("Data processing pipeline completed successfully.")

if __name__ == "__main__":
    main()
