import os
import re

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
    ramp = [max_flow_value * (i + 1) / ramp_steps for i in range(ramp_steps)]
    steady = [max_flow_value] * steady_steps
    return ramp + steady

def update_flow_hydrograph(input_file, new_hydrograph):
    # Read the content of the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Find the line with "Flow Hydrograph ="
    for i, line in enumerate(lines):
        if line.strip().startswith("Flow Hydrograph="):
            # Update the line to reflect the new array length
            lines[i] = f"Flow Hydrograph= {len(new_hydrograph)}\n"
            
            # Replace the subsequent line with the new hydrograph values
            formatted_hydrograph = ''.join(
                (f'      {str(x).lstrip("0")}' if 0 < x < 1 else f'{x:.6g}').rjust(8)
                for x in new_hydrograph
            ).rstrip()  # Remove the trailing spaces after the last number
            lines[i + 1] = formatted_hydrograph + '\n'
            break
    
    # Determine the new file extension
    base_name, ext = os.path.splitext(input_file)
    ext_number = int(re.search(r'\d+$', ext).group())
    new_ext_number = f"{ext_number + 1:02}"
    new_file = f"{base_name}.u{new_ext_number}"
    
    # Write the modified content to the new file
    with open(new_file, 'w') as file:
        file.writelines(lines)
    
    print(f"Updated file saved as {new_file}")
    return new_file

def update_plan_file(file_path, new_flow_file, new_identifier):
    """
    Updates the Flow File and Short Identifier in the specified HEC-RAS plan file,
    and saves a copy of the file with the extension updated by one number.

    Parameters:
        file_path (str): The path to the text file to be updated.
        new_flow_file (str): The new Flow File string to replace the existing one.
        new_identifier (str): The new identifier string to replace the existing Short Identifier.
    """
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the relevant lines
    for i, line in enumerate(lines):
        if line.startswith("Flow File"):
            lines[i] = f"Flow File={new_flow_file}\n"
        elif line.startswith("Short Identifier"):
            # Preserve any whitespace after the identifier to maintain the format
            identifier_padding = len(line) - len(line.lstrip()) + len(line.split('=')[0]) + 1
            lines[i] = f"Short Identifier={new_identifier:<{identifier_padding}}\n"
        elif line.startswith("Plan Title"):
            # Preserve any whitespace after the title to maintain the format
            title_padding = len(line) - len(line.lstrip()) + len(line.split('=')[0]) + 1
            lines[i] = f"Plan Title={new_identifier:<{title_padding}}\n"
            
    # Increment the extension number
    base_name, ext = os.path.splitext(file_path)
    if ext.startswith('.p') and ext[2:].isdigit():
        new_ext_number = int(ext[2:]) + 1
        new_ext = f".p{new_ext_number:02d}"
    else:
        raise ValueError(f"Unexpected file extension format: {ext}")

    # Create new file path
    new_file_path = f"{base_name}{new_ext}"

    # Write the updated content to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(lines)

    print(f"Updated file saved as: {new_file_path}")
    return new_file_path

def generate_hydrograph_and_update_plan(input_flow_file, input_plan_file, max_flow_value):
    """
    Generates a hydrograph, updates the flow file, and updates the plan file with new titles.

    Parameters:
        input_flow_file (str): Path to the original flow file to be updated.
        input_plan_file (str): Path to the original plan file to be updated.
        max_flow_value (float): Maximum flow value for the hydrograph.
    """
    # Generate new hydrograph
    new_hydrograph = create_hydrograph(max_flow_value)
    
    # Update flow hydrograph file
    new_flow_file = update_flow_hydrograph(input_flow_file, new_hydrograph)
    
    # Create a new identifier for the plan
    new_identifier = f"MW_{max_flow_value:.0f}cms"
    
    # Update plan file
    update_plan_file(input_plan_file, os.path.basename(new_flow_file), new_identifier)

input_flow_file_path = r"C:\ATD\Hydraulic Models\Bennett_Test - Copy\MW_Valleys.u01"

input_plan_file_path = r"C:\ATD\Hydraulic Models\Bennett_Test - Copy\MW_Valleys.p01"
max_flow_value = 10

generate_hydrograph_and_update_plan(input_flow_file_path, input_plan_file_path, max_flow_value)
