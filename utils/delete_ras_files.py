import os
import glob

def delete_p_files(folder_path):
    # Use glob to find all files in the folder starting with .p
    files_to_delete = glob.glob(os.path.join(folder_path, '*.p*'))
    
    # Delete each file found
    print(f"Deleting # of files: {len(files_to_delete)}")   
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    # Replace with your folder path
    folder_path = r"C:\ATD\Hydraulic Models\Bennett\MW"
    
    delete_p_files(folder_path)
