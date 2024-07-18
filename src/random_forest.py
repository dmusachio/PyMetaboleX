"""
random_forest.py

This script performs random forest classification on metabolite data to classify subjects into different diagnostic groups:
- Marasmus vs. Kwashiorkor
- All 4 groups (Marasmus, Kwashiorkor, Control, MAM)
- Combined Marasmus + Kwashiorkor vs. Control
- Combined Marasmus + Kwashiorkor vs. MAM

It loads metabolite data from a CSV file, preprocesses the data, runs random forest classification using sklearn,
saves classification reports, plots feature importances, and outputs top feature lists for each comparison.

Usage:
    Run the script using Python 3.
    Example: python3 random_forest.py

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

# Load the data
file_path = 'processed/processed_cleaned_data.csv'
data = pd.read_csv(file_path)

# Assume the first 8 columns are non-metabolic data
metabolic_data = data.iloc[:, 8:]

# Add the diagnosis column separately, replacing 'Marasmic Kwashiorkor' with 'Kwashiorkor'
diagnosis = data['Subject Diagnosis'].replace('Marasmic Kwashiorkor', 'Kwashiorkor')

# Define the output directory
output_dir = 'output/random_forest'
os.makedirs(output_dir, exist_ok=True)

# Function to run random forest and save the results
def run_random_forest(X, y, output_subdir):
    """
    Runs random forest classification on given data and saves results.

    Args:
    - X: DataFrame, features (metabolic data)
    - y: Series, target variable (diagnosis)
    - output_subdir: str, name of subdirectory for saving results
    """
    output_path = os.path.join(output_dir, output_subdir)
    os.makedirs(output_path, exist_ok=True)
    
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
    report_df.to_csv(os.path.join(output_path, 'classification_report.csv'), index=True)
    
    # Plot top 10 feature importances
    feature_importances = clf.feature_importances_
    sorted_indices = feature_importances.argsort()[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(10), feature_importances[sorted_indices[:10]], align='center')
    plt.xticks(range(10), [X.columns[i] for i in sorted_indices[:10]], rotation=90)
    plt.title('Top 10 Feature Importances')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'feature_importances.png'))
    plt.close()
    
    # Print the top 10 features with their importance scores to a text file
    top_features = [(X.columns[i], feature_importances[i]) for i in sorted_indices[:10]]
    with open(os.path.join(output_path, 'top_features.txt'), 'w') as f:
        for feature, importance in top_features:
            f.write(f"{feature}: {importance}\n")

# Run 1: Marasmus vs. Kwashiorkor
condition_1 = diagnosis.isin(['Marasmus', 'Kwashiorkor'])
X_1 = metabolic_data[condition_1]
y_1 = diagnosis[condition_1]
run_random_forest(X_1, y_1, 'marasmus_vs_kwashiorkor')

# Run 2: All 4 groups (Marasmus, Kwashiorkor, Control, MAM)
condition_2 = diagnosis.isin(['Marasmus', 'Kwashiorkor', 'Control', 'MAM'])
X_2 = metabolic_data[condition_2]
y_2 = diagnosis[condition_2]
run_random_forest(X_2, y_2, 'all_groups')

# Run 3: Marasmus + Kwashiorkor combined vs. Control
diagnosis_combined = diagnosis.replace(['Marasmus', 'Kwashiorkor'], 'Combined')
condition_3 = diagnosis_combined.isin(['Combined', 'Control'])
X_3 = metabolic_data[condition_3]
y_3 = diagnosis_combined[condition_3]
run_random_forest(X_3, y_3, 'combined_vs_control')

# Run 4: Marasmus + Kwashiorkor combined vs. MAM
condition_4 = diagnosis_combined.isin(['Combined', 'MAM'])
X_4 = metabolic_data[condition_4]
y_4 = diagnosis_combined[condition_4]
run_random_forest(X_4, y_4, 'combined_vs_mam')

print("Random forest classification analysis completed. Results saved in output/random_forest.")
