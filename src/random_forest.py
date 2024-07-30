"""
random_forest.py

This script performs random forest classification on metabolite data to classify subjects into two diagnostic groups.

It loads metabolite data from a CSV file, preprocesses the data, runs random forest classification using sklearn,
saves classification reports, plots feature importances, and outputs top feature lists for the comparison.

Usage:
    Run the script using Python 3.
    Example: python3 random_forest.py <data_file> <output_dir>

Dependencies:
    - pandas
    - sklearn.ensemble.RandomForestClassifier
    - sklearn.metrics.classification_report
    - sklearn.model_selection.train_test_split
    - matplotlib.pyplot
    - os

Author:
    Daniel Musachio

Date:
    July 2024
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import sys

# Read input parameters from command line arguments
if len(sys.argv) != 3:
    print("Usage: python random_forest.py <data_file> <output_dir>")
    exit()

data_file = sys.argv[1]
output_dir = sys.argv[2]

# Load the data
if os.path.isfile(data_file):
    data = pd.read_csv(data_file)
    print(f"Data loaded successfully from {data_file}")
else:
    print(f"The file {data_file} does not exist. Please check the file path.")
    exit()

# Assume the metabolic data starts from the second column
metabolic_data = data.iloc[:, 1:]

# Add the diagnosis column separately, replacing 'Marasmic Kwashiorkor' with 'Kwashiorkor'
diagnosis = data['Subject Diagnosis'].replace('Marasmic Kwashiorkor', 'Kwashiorkor')

# Identify the first two unique groups in the 'Subject Diagnosis' column
unique_groups = diagnosis.unique()
if len(unique_groups) < 2:
    print("There are fewer than two unique groups in the 'Subject Diagnosis' column.")
    exit()

group1 = unique_groups[0]
group2 = unique_groups[1]

# Define the output directory
os.makedirs(output_dir, exist_ok=True)

# Function to run random forest and save the results
def run_random_forest(X, y, output_dir):
    """
    Runs random forest classification on given data and saves results.

    Args:
    - X: DataFrame, features (metabolic data)
    - y: Series, target variable (diagnosis)
    - output_dir: str, directory for saving results
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Initialize and train the random forest classifier
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = clf.predict(X_test)
    
    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv(os.path.join(output_dir, 'classification_report.csv'), index=True)
    
    # Plot top 10 feature importances
    feature_importances = clf.feature_importances_
    sorted_indices = feature_importances.argsort()[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(10), feature_importances[sorted_indices[:10]], align='center')
    plt.xticks(range(10), [X.columns[i] for i in sorted_indices[:10]], rotation=90)
    plt.title('Top 10 Feature Importances')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importances.png'))
    plt.close()
    
    # Print the top 10 features with their importance scores to a text file
    top_features = [(X.columns[i], feature_importances[i]) for i in sorted_indices[:10]]
    with open(os.path.join(output_dir, 'top_features.txt'), 'w') as f:
        for feature, importance in top_features:
            f.write(f"{feature}: {importance}\n")

# Define the condition for the two groups
condition = diagnosis.isin([group1, group2])

# Filter the data for the two groups
X = metabolic_data[condition]
y = diagnosis[condition]

# Run random forest classification
run_random_forest(X, y, output_dir)

print(f"Random forest classification analysis completed. Results saved to {output_dir}")
