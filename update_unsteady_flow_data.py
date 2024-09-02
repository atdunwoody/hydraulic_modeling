import os
import re

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


input_file_path = r"C:\ATD\Hydraulic Models\Bennett_Valleys\MW_Valleys.u01"  # Path to your input file
new_hydrograph = [0.5, 0.9 , 2, 2, 2, 2]  # Your new hydrograph array

update_flow_hydrograph(input_file_path, new_hydrograph)
