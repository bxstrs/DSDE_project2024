import os
import magic

# Path to your folder
source_folder = r'C:/Desktop Shortcut/workspace/university/dsde/DSDE_project2024/Data_2018-2023/Project/2023'

# Initialize the magic detector
file_magic = magic.Magic()

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Detect file type
    file_type = file_magic.from_file(file_path)
    print(f"{filename}: {file_type}")

    # Map common file types to extensions

    new_name = filename + ".json"


    # Rename the file
    new_file_path = os.path.join(source_folder, new_name)
    os.rename(file_path, new_file_path)
    print(f"Renamed {filename} to {new_name}")
