# unzips a bunch of exported sheets and merges them all into one big csv file
import os  # Provides functions for interacting with the operating system
import zipfile  # Allows us to work with ZIP files
import pandas as pd  # Used for data manipulation and analysis
# Step 1: Prompt the user to enter the directory containing the ZIP files
zip_dir = input("Enter the path to the directory containing ZIP files: ")

# Step 2: Prompt the user to enter the directory where files should be extracted
extracted_dir = input("Enter the path to the directory where files should be extracted: ")

# Create the extraction directory if it doesn't exist
if not os.path.exists(extracted_dir):
    os.makedirs(extracted_dir)  # Make the directory so we can extract files into it

# Step 3: Unzip all ZIP files in the specified directory
for filename in os.listdir(zip_dir):  # List all files in the ZIP directory
    if filename.endswith('.zip'):  # Only process files that end with '.zip'
        zip_path = os.path.join(zip_dir, filename)  # Get the full path to the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:  # Open the ZIP file
            zip_ref.extractall(extracted_dir)  # Extract all contents to the extraction directory

# Step 4: Combine all CSV files found in the extracted directory into one DataFrame
combined_df = pd.DataFrame()  # Create an empty DataFrame to hold all data

# Walk through the extracted directory to find CSV files
for root, dirs, files in os.walk(extracted_dir):  # Traverse all folders and files
    for file in files:
        if file.endswith('.csv'):  # Only process files that end with '.csv'
            csv_path = os.path.join(root, file)  # Get the full path to the CSV file
            df = pd.read_csv(csv_path, low_memory=False)  # Read the CSV file into a DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)  # Append to the combined DataFrame

# Step 5: Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_output.csv', index=False)  # Save the combined data to a CSV file

# Print a message indicating completion
print("All CSV files have been combined into 'combined_output.csv', which is located where this script was run.")
