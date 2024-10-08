import os
import re
import numpy as np

def create_hydrograph(max_flow_value, ramp_steps=2, steady_steps=3):
    """
    Creates a hydrograph array that ramps up to the max flow value.
    
    Parameters:
        max_flow_value (float): The maximum flow value to be reached in the hydrograph.
        ramp_steps (int): Number of steps to ramp up to the max flow value.
        steady_steps (int): Number of steps to maintain the max flow value.
    
    Returns:
        list: The generated hydrograph array.
    """
    ramp = [max_flow_value * (i + 1) / (ramp_steps ** 3) for i in range(ramp_steps)]
    steady = [max_flow_value] * steady_steps
    # #round ramp to 1 decimal place if it is less than 1
    # if ramp[0] < 1:
    #     ramp = [round(x, 1) for x in ramp]
    # #round ramp to whole number if it is greater than 1
    # else:
    #     ramp = [round(x) for x in ramp]
    return ramp + steady


def update_flow_hydrograph(input_file, new_hydrograph, new_title, max_flow_value):
    """
    Updates the Flow Hydrograph and Flow Title in the unsteady flow file.

    Parameters:
        input_file (str): Path to the input file to be updated.
        new_hydrograph (list): The new hydrograph values.
        max_flow_value (float): The maximum flow value for the hydrograph.
    
    Returns:
        str: The path to the newly created file.
    """
    
    #If  max_flow value has a decimal with trailing 0s after, remove the trailing 0s
    max_flow_value = float(max_flow_value)
    max_flow_value = int(max_flow_value) if max_flow_value.is_integer() else max_flow_value
    # Read the content of the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Update Flow Hydrograph and Flow Title
    for i, line in enumerate(lines):
        if line.strip().startswith("Flow Hydrograph="):
            # Update the line to reflect the new array length
            lines[i] = f"Flow Hydrograph= {len(new_hydrograph)}\n"
            
            # Replace the subsequent line with the new hydrograph values
            formatted_hydrograph = ''.join(
                f'{x:8.3f}' if x >= 1 or x == 0 else f' {x:7.3f}'  # Ensures 8 characters for each number
                for x in new_hydrograph
            ).rstrip()  # Remove the trailing spaces after the last number
            
            lines[i + 1] = formatted_hydrograph + '\n'
        
        elif line.strip().startswith("Flow Title=") and new_title is not None:
            # Extract the base title and update it with the new max flow value
            base_title = re.match(r'Flow Title=(.*?)[0-9]*cms', line.strip()).group(1).strip()
            new_flow_title = f"Flow Title={base_title}{int(max_flow_value)}cms\n"
            lines[i] = new_flow_title
                
        elif line.strip().startswith("Flow Title=") and new_title is None:
            print(f"Flow Title not provided. Updating based on the max flow value: {max_flow_value}")
            old_title = re.search(r'Flow Title=(.*)', lines[0]).group(1)
            old_title_prefix = old_title.split('_')[0]
            print(f"Old Title Prefix: {old_title_prefix}")
            
            # Format the max flow value as a float with two decimal places, replacing '.' with 'o'
            if isinstance(max_flow_value, float):
                new_title = f"{old_title_prefix}_{max_flow_value:.2f}cms".replace('.', 'o')
            else:
                new_title = f"{old_title_prefix}_{max_flow_value}cms"
            lines[i] = f"Flow Title={new_title}\n"

    
    # Get directory
    dir_name = os.path.dirname(input_file)
    # Find all .p## files in the directory
    import glob
    p_files = glob.glob(os.path.join(dir_name, '*.p[0-9][0-9]'))
    # Find the highest number in p_files
    highest_number = 0
    for p_file in p_files:
        base_name, ext = os.path.splitext(p_file)
        ext_number = int(ext[2:])
        if ext_number > highest_number:
            highest_number = ext_number
    
    # Determine the new file extension
    base_name, ext = os.path.splitext(input_file)
    ext_number = int(re.search(r'\d+$', ext).group())
    new_ext_number = f"{highest_number + 1:02}"
    new_file = f"{base_name}.u{new_ext_number}"
    
    # Write the modified content to the new file
    with open(new_file, 'w') as file:
        file.writelines(lines)
    
    print(f"Updated file saved as {new_file}")
    return new_file

def update_plan_file(file_path, new_flow_file, new_title, max_flow_value):
    """
    Updates the Flow File and Short Identifier in the specified HEC-RAS plan file,
    and saves a copy of the file with the extension updated by one number.

    Parameters:
        file_path (str): The path to the text file to be updated.
        new_flow_file (str): The new Flow File string to replace the existing one.
        new_title (str): The new identifier string to replace the existing Short Identifier.
    """
    # Rename the title, using the format "{Area Name}_{Max Flow}cms"

    #If  max_flow value has a decimal with trailing 0s after, remove the trailing 0s
    max_flow_value = float(max_flow_value)
    max_flow_value = int(max_flow_value) if max_flow_value.is_integer() else max_flow_value
    
    
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the relevant lines
    for i, line in enumerate(lines):
        if line.startswith("Flow File"):
            lines[i] = f"Flow File={new_flow_file}\n"
        elif line.startswith("Short Identifier") and new_title is not None:
            # Preserve any whitespace after the identifier to maintain the format
            title_padding = len(line) - len(line.lstrip()) + len(line.split('=')[0]) + 1
            lines[i] = f"Short Identifier={new_title:<{title_padding}}\n"
        elif line.startswith("Plan Title") and new_title is not None:
            # Preserve any whitespace after the title to maintain the format
            title_padding = len(line) - len(line.lstrip()) + len(line.split('=')[0]) + 1
            lines[i] = f"Plan Title={new_title:<{title_padding}}\n"
        elif line.startswith("Plan Title") and new_title is None:
            old_title = re.search(r'Plan Title=(.*)', lines[0]).group(1)
            old_title_prefix = old_title.split('_')[0]
            #check if max_flow_value is a float
            if isinstance(max_flow_value, float):
                new_title = f"{old_title_prefix}_{max_flow_value:.2f}cms".replace('.', 'o')
            else:
                new_title = f"{old_title_prefix}_{max_flow_value}cms"
                
            lines[i] = f"Plan Title={new_title}\n"
            print(f"Plan Title not provided. Updating based on the max flow value: {max_flow_value}")
        elif line.startswith("Short Identifier") and new_title is None:
            old_title = re.search(r'Short Identifier=(.*)', lines[0]).group(1)
            old_title_prefix = old_title.split('_')[0]
            if isinstance(max_flow_value, float):
                new_title = f"{old_title_prefix}_{max_flow_value:.2f}cms".replace('.', 'o')
            else:
                new_title = f"{old_title_prefix}_{max_flow_value}cms"
            lines[i] = f"Short Identifier={new_title}\n"
    # Increment the extension number
    #get directory
    dir_name = os.path.dirname(file_path)
    #find all .p## files in the directory
    import glob
    p_files = glob.glob(os.path.join(dir_name, '*.p[0-9][0-9]'))
    #find the highest number in p_files
    highest_number = 0
    for p_file in p_files:
        base_name, ext = os.path.splitext(p_file)
        ext_number = int(ext[2:])
        if ext_number > highest_number:
            highest_number = ext_number
    base_name, ext = os.path.splitext(file_path)
    if ext.startswith('.p') and ext[2:].isdigit():
        new_ext_number = highest_number + 1
        new_ext = f"p{new_ext_number:02d}"
    else:
        raise ValueError(f"Unexpected file extension format: {ext}")


    # Create new file path
    new_file_path = f"{base_name}.{new_ext}"

    # Write the updated content to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(lines)

    print(f"Updated file saved as: {new_file_path}")
    return new_file_path

def update_prj_file(prj_file_path, new_unsteady_file, new_plan_file):
    """
    Updates the .prj file to include the new unsteady and plan file lines
    directly below the last pre-existing unsteady and plan file lines.

    Parameters:
        prj_file_path (str): Path to the .prj file to be updated.
        new_unsteady_file (str): The new Unsteady File entry to be added.
        new_plan_file (str): The new Plan File entry to be added.
    """
    # Read the content of the .prj file
    with open(prj_file_path, 'r') as file:
        lines = file.readlines()

    # Find the last Unsteady File and Plan File lines
    unsteady_exists = False
    plan_exists = False
    last_unsteady_index = -1
    last_plan_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("Unsteady File="):
            last_unsteady_index = i
        elif line.strip().startswith("Plan File="):
            last_plan_index = i
    #check if new_unsteady_file and new_plan_file are already in the file
    for line in lines:
        if line.strip().startswith("Unsteady File="):
            if line.strip() == f"Unsteady File={new_unsteady_file}":
                print(f"Unsteady File {new_unsteady_file} already in {prj_file_path}")
                unsteady_exists = True
        if line.strip().startswith("Plan File="):
            if line.strip() == f"Plan File={new_plan_file}":
                print(f"Plan File {new_plan_file} already in {prj_file_path}")
                plan_exists = True
    # Insert the new Unsteady File line after the last one
    if last_unsteady_index != -1 and not unsteady_exists:
        lines.insert(last_unsteady_index + 1, f"Unsteady File={new_unsteady_file}\n")
    
    # Insert the new Plan File line after the last one
    if last_plan_index != -1 and not plan_exists:
        lines.insert(last_plan_index + 1, f"Plan File={new_plan_file}\n")

    # Write the updated content back to the .prj file
    with open(prj_file_path, 'w') as file:
        file.writelines(lines)
    
    print(f"Updated .prj file saved as: {prj_file_path}")

def generate_hydrograph_and_update_plan(input_flow_file, input_plan_file, input_prj_file, max_flow_value, new_title = None):
    """
    Generates a hydrograph, updates the flow file, updates the plan file, and updates the .prj file with new entries.

    Parameters:
        input_flow_file (str): Path to the original flow file to be updated.
        input_plan_file (str): Path to the original plan file to be updated.
        input_prj_file (str): Path to the .prj file to be updated.
        max_flow_value (float): Maximum flow value for the hydrograph.
    """
    # Generate new hydrograph
    new_hydrograph = create_hydrograph(max_flow_value)
    
    # Update flow hydrograph file and flow title
    new_flow_file_path = update_flow_hydrograph(input_flow_file, new_hydrograph, new_title, max_flow_value)
    
    # Extract just the extension for the flow and plan files
    new_flow_file = os.path.splitext(os.path.basename(new_flow_file_path))[1][1:]
    
    # Update plan file
    new_plan_file_path = update_plan_file(input_plan_file, new_flow_file, new_title, max_flow_value)
    
    # Extract just the extension for the plan file
    new_plan_file = os.path.splitext(os.path.basename(new_plan_file_path))[1][1:]
    
    # Update the .prj file with the new unsteady and plan files
    update_prj_file(input_prj_file, new_flow_file, new_plan_file)

if __name__ == "__main__":

    prefix_list = ['UM', 'UE']
    base_folder = r"C:\ATD\Hydraulic Models\Bennett_MC"
    for prefix in prefix_list:
        subfolder_and_file = os.path.join(prefix, f"{prefix}_Valleys")
        input_plan_file_path = os.path.join(base_folder, subfolder_and_file + ".p01")
        input_prj_file_path = os.path.join(base_folder, subfolder_and_file + ".prj")
        input_flow_file_path = os.path.join(base_folder, subfolder_and_file + ".u01")
        # input_plan_file_path = r"C:\ATD\Hydraulic Models\Bennett_MC\MM\MM_Valleys.p01"
        # input_prj_file_path = r"C:\ATD\Hydraulic Models\Bennett_MC\MM\MM_Valleys.prj"
        # input_flow_file_path =r"C:\ATD\Hydraulic Models\Bennett_MC\MM\MM_Valleys.u01"

        max_flow_value_list = [0.25, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Set to a string to replace the Short Identifier and Plan Title and Flow Title
        new_title = None # If None, the title will be updated based on {Text before '_' in old plan title}_{the max flow value}cms
        for max_flow_value in max_flow_value_list:
            generate_hydrograph_and_update_plan(input_flow_file_path, input_plan_file_path, 
                                                input_prj_file_path, max_flow_value, new_title = new_title) 

