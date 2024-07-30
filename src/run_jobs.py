"""
run_jobs.py

This script reads job definitions from a job_info.txt file and executes each job sequentially.
Each job consists of a script path, an input file, and an output directory.

Usage:
    Run the script using Python 3.
    Example: python3 src/run_jobs.py

Dependencies:
    - subprocess
    - os

Author:
    Daniel Musachio

Date:
    July 2024
"""

import subprocess
import os

# Define the path to the job_info.txt file
job_info_path = 'src/job_info.txt'

# Read the job_info.txt file
if os.path.isfile(job_info_path):
    with open(job_info_path, 'r') as file:
        lines = file.readlines()
else:
    print(f"The file {job_info_path} does not exist. Please check the file path.")
    exit()

# Iterate over the lines and run each job
for i in range(0, len(lines), 3):
    if i + 2 < len(lines):
        script_path = lines[i].strip()
        input_file = lines[i + 1].strip()
        output_dir = lines[i + 2].strip()
        
        # Create the full path to the script
        full_script_path = os.path.join('src', script_path)
        
        # Check if the script file exists
        if not os.path.isfile(full_script_path):
            print(f"The script {full_script_path} does not exist. Skipping this job.")
            continue
        
        # Check if the input file exists
        if not os.path.isfile(input_file):
            print(f"The input file {input_file} does not exist. Skipping this job.")
            continue

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        
        # Run the script with the input file and output directory as arguments
        command = ['python3', full_script_path, input_file, output_dir]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully ran {script_path} with input {input_file} and output {output_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path} with input {input_file} and output {output_dir}. Error: {e}")
    else:
        print(f"Incomplete job definition in {job_info_path}. Each job should have three lines (script, input file, and output directory).")

print("All jobs completed.")
