import os
import re

"""
Extracts the plan, flow, and/opr geometry titles from the input HEC-RAS project folder. 
Loops through all files with the extensions .p##, .u##, and .g## in the project directory and extract the titles.
Print titles next to the file names.

"""

import os
import re

# Function to extract title from file content
def extract_title(file_path):
    title_patterns = {
        '.p': r'Plan Title=(.*)',
        '.u': r'Flow Title=(.*)',
        '.g': r'Geom Title=(.*)'
    }
    
    ext = os.path.splitext(file_path)[1][:2]  # Get the extension prefix like .p, .u, .g
    
    with open(file_path, 'r') as file:
        content = file.read()
        pattern = title_patterns.get(ext)
        if pattern:
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()  # Return the first match as the title
    return None

# Directory containing the HEC-RAS project files
project_directory = r"C:\ATD\Hydraulic Models\Bennett_MC"

# Loop through the directory and process relevant files
for file_name in os.listdir(project_directory):
    if re.match(r'.*\.(p\d+|u\d+|g\d+)$', file_name):  # Match files with .p##, .u##, .g## extensions
        file_path = os.path.join(project_directory, file_name)
        title = extract_title(file_path)
        if title:
            print(f"{file_name}: {title}")
        else:
            print(f"{file_name}: Title not found")
