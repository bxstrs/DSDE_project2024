import pandas as pd

# File paths
existing_csv = r"C:/desktop/workspace/university/dsde/DSDE_project2024/json_data/information.csv"  # Path to your existing record file
new_scraped_csv = r"C:/desktop/workspace/university/dsde/DSDE_project2024/web_scraping/scopus_trend_2018-2023.csv"  # Path to the newly scraped file
output_csv = r"C:/desktop/workspace/university/dsde/DSDE_project2024/web_scraping/2018-2023_filtered.csv"  # Path to save filtered results

# Load existing and new scraped records
existing_records = pd.read_csv(existing_csv)
new_records = pd.read_csv(new_scraped_csv)

# Ensure the DOI field is consistent in both datasets (case-sensitive)
existing_records['DOI'] = existing_records['DOI'].str.strip().str.lower()
new_records['DOI'] = new_records['DOI'].str.strip().str.lower()

# Filter out new records that already exist in the existing records
filtered_new_records = new_records[~new_records['DOI'].isin(existing_records['DOI'])]

# Save the filtered results
filtered_new_records.to_csv(output_csv, index=False)

print(f"Filtered {len(new_records) - len(filtered_new_records)} duplicate records.")
print(f"Saved {len(filtered_new_records)} new unique records to '{output_csv}'.")
