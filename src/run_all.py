import subprocess
import shutil
import os


def run_script(script_name):
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

def main():
    print("Starting data processing pipeline...")
    # Remove 'output' and 'processed' directories if they exist
    if os.path.exists('output'):
        shutil.rmtree('output')
        print("Removed 'output' directory.")
    if os.path.exists('processed'):
        shutil.rmtree('processed')
        print("Removed 'processed' directory.")

    # Run data harmonization
    run_script("src/data_harmonization.py")

    # Run data evaluation
    run_script("src/evaluate_data.py")

    # Run clustering analysis
    run_script("src/cluster.py")

    print("Data processing pipeline completed successfully.")

if __name__ == "__main__":
    main()
