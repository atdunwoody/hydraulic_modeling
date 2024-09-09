import os
import shutil

# List of folders containing the .tif files exported from HEC-RAS
# Output tif files are named as "MM_0o25cms.tif", "MM_0o75cms.tif", etc.
folders = [
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_0o5cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_0o25cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_0o75cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_1cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_1o50cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_2cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_3cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_4cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_5cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_6cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_7cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_8cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_9cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\UM\UM_10cms",
]

# Output folder to store renamed files
output_folder = r"C:\ATD\Hydraulic Models\Bennett_MC\UM\Results"

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each folder
for folder in folders:
    # Get the name of the parent folder (which will be used as the new file name)
    parent_folder_name = os.path.basename(folder)
    
    # List all the files in the current folder
    for file in os.listdir(folder):
        # Check if the file is a .tif file
        if file.endswith('.tif'):
            # Full path to the original file
            old_file_path = os.path.join(folder, file)
            
            # New file name based on the parent folder name
            new_file_name = f"{parent_folder_name}.tif"
            
            # Full path to the new location in the output folder
            new_file_path = os.path.join(output_folder, new_file_name)
            
            # Copy the file to the new location and rename it
            shutil.copyfile(old_file_path, new_file_path)
            print(f"Copied and renamed: {old_file_path} -> {new_file_path}")

print("All files processed.")
