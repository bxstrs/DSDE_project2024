import pandas as pd
import os

# Step 1: Specify the folder where your CSV files are located
folder_path = r'C:\desktop\workspace\university\dsde\DSDE_project2024\DE\merge_csv'  # Replace with the path to your folder

# Step 2: List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Step 3: Read and merge all CSV files
merged_df = pd.concat([pd.read_csv(os.path.join(folder_path, file)) for file in csv_files], ignore_index=True)

# Step 4: Optionally, save the merged data to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)

# Step 5: Print a confirmation message
print("CSV files merged successfully!")
