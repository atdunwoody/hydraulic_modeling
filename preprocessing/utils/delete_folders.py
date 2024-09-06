import shutil
import os

# List of folders to delete
prefixes = ["ME", "MM", "MW", "UE", "UM", "UW"]
source_folder = r"C:\ATD\Hydraulic Models\Bennett"
folder_names = [
    "1", "4_max", "40_max", "ME_1cms_max_5s", "ME_3_Max_5s", "wide_1_max", "wide_4_max_1s", "wide_10_cms_max_1s_comp"
]
folders_to_delete = []
for prefix in prefixes:
    for folder_name in folder_names:
        folder = os.path.join(source_folder, prefix, f"{folder_name}")
        folders_to_delete.append(folder)
# Delete each folder
for folder in folders_to_delete:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Deleted: {folder}")
    else:
        print(f"Folder not found: {folder}")
