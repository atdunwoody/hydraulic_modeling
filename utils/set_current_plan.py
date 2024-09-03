"""
This script updates the Current Plan in the project file to the specified plan.
Current Plan in HEC-RAS project must be set before it is opened. Once a new plan is set, it must be closed and reopened to take effect.
"""

import os

def set_current_plan(file_path, new_plan):
    #Check that there is an extension = new_plan in the file_path directory
    # eg is new_plan = p21, then check if there is a file with extension p21 in the file_path directory
    # if there is no file with extension = new_plan in the file_path directory, then raise an error
    # if there is a file with extension = new_plan in the file_path directory, then proceed to update the Current Plan in the project file
    # Open the project file
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Project file not found: {file_path}")
    file_dir = os.path.dirname(file_path)
    ext_exists = False
    for file in os.listdir(file_dir):
        if file.endswith(f".{new_plan}"):
            ext_exists = True
            break
    if not ext_exists:
        # Provide a warning that the plan does not exist in the project directory
        print(f"Warning: Plan {new_plan} does not exist in the project directory.")
        print("Current Plan not updated.")
        return ext_exists
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Replace the Current Plan line
    for i, line in enumerate(lines):
        if line.startswith("Current Plan="):
            lines[i] = f"Current Plan={new_plan}\n"
            break
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
    return ext_exists

if __name__ == "__main__":
    # Specify the path to the file and the new plan ID
    prj_path = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.prj"
    new_plan = "p22"  # Replace with your desired plan ID
    
    set_current_plan(prj_path, new_plan)
    print(f"Current Plan updated to {new_plan}")
