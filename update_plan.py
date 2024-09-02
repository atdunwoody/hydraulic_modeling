import os

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

# Example usage:
file_path = r"C:\ATD\Hydraulic Models\Bennett_Valleys\MW_Valleys.p01"
new_flow_file = 'u02'
new_identifier = 'MW_2cms_1s'
update_plan_file(file_path, new_flow_file, new_identifier)
