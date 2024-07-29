import pandas as pd
import os

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        lines = file.readlines()
        current_group = None
        for line in lines:
            key, value = line.strip().split('=')
            key, value = key.strip(), value.strip()
            if key == 'group_input_file':
                config[key] = value
            elif key.endswith('_name'):
                current_group = key[:-5]  # remove '_name'
                config[current_group] = {'name': value, 'diagnoses': []}
            elif current_group and key.startswith('group'):
                config[current_group]['diagnoses'].append(value)
    return config

def create_combined_grouped_data(input_file, config):
    data = pd.read_csv(input_file)
    data.columns = data.columns.str.strip()  # Remove leading/trailing spaces from column names
    
    # Ensure all index values are stripped of leading/trailing spaces
    data['Subject Diagnosis'] = data['Subject Diagnosis'].str.strip()

    # Create a new column to store group names
    data['Group'] = None

    # Assign group names based on Subject Diagnosis
    for group_key, group_info in config.items():
        if isinstance(group_info, dict) and group_key.startswith('group') and 'name' in group_info:
            group_name = group_info['name']
            diagnoses = group_info['diagnoses']
            data.loc[data['Subject Diagnosis'].isin(diagnoses), 'Group'] = group_name

    # Drop rows that don't belong to any group
    data = data.dropna(subset=['Group'])

    # Reset the index to make 'Subject Diagnosis' the first column
    data = data.drop(columns=['Subject Diagnosis'])
    data = data.rename(columns={'Group': 'Subject Diagnosis'})
    data.reset_index(drop=True, inplace=True)

    # Reorder columns to make 'Subject Diagnosis' the first column
    columns = ['Subject Diagnosis'] + [col for col in data.columns if col != 'Subject Diagnosis']
    data = data[columns]

    os.makedirs('data', exist_ok=True)

    # Create the combined file name based on group names
    group_names = "_and_".join([group_info['name'].lower().replace(' ', '_') for group_key, group_info in config.items() if isinstance(group_info, dict) and group_key.startswith('group')])
    combined_file_path = os.path.join('data', f"{group_names}.csv")

    # Save the combined grouped data to a single CSV file
    data.to_csv(combined_file_path, index=False)
    print(f"Combined grouped data has been written to '{combined_file_path}'.")

    # Rank the data
    ranked_data = data.copy()
    ranked_data.iloc[:, 1:] = ranked_data.iloc[:, 1:].rank()
    ranked_file_path = os.path.join('data', f"{group_names}_ranked.csv")

    # Save the ranked data to a single CSV file
    ranked_data.to_csv(ranked_file_path, index=False)
    print(f"Ranked data has been written to '{ranked_file_path}'.")

def main():
    config_file = 'src/group_config.txt'
    config = read_config(config_file)

    input_file = config.get('group_input_file')
    create_combined_grouped_data(input_file, config)

if __name__ == "__main__":
    main()
