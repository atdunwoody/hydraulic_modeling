import shutil
import os

def save_hec_ras_project(src_project_folder, dest_folders):
    """
    Saves the contents of a HEC-RAS project folder to multiple destination folders.

    Parameters:
    src_project_folder (str): The path to the source HEC-RAS project folder.
    dest_folders (list of str): A list of destination folders where the project contents should be copied.
    """
    if not os.path.exists(src_project_folder):
        raise ValueError(f"Source project folder '{src_project_folder}' does not exist.")

    for dest_folder in dest_folders:
        # Ensure the destination directory exists, if not, create it
        os.makedirs(dest_folder, exist_ok=True)

        # Copy all files and subdirectories from the source folder to the destination
        for item in os.listdir(src_project_folder):
            src_item = os.path.join(src_project_folder, item)
            dest_item = os.path.join(dest_folder, item)

            if os.path.isdir(src_item):
                # Copy directory
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                # Copy file
                shutil.copy2(src_item, dest_item)

        print(f"Project contents saved to: {dest_folder}")

src_project_folder = r"C:\ATD\Hydraulic Models\UM_Valleys"
dest_folders = [
    r"C:\ATD\Hydraulic Models\Bennett\ME",
r"C:\ATD\Hydraulic Models\Bennett\MM",
r"C:\ATD\Hydraulic Models\Bennett\MW",
r"C:\ATD\Hydraulic Models\Bennett\UE",
r"C:\ATD\Hydraulic Models\Bennett\UM",
r"C:\ATD\Hydraulic Models\Bennett\UW",
]

save_hec_ras_project(src_project_folder, dest_folders)
