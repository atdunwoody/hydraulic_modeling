import os
import re

"""
Write a script that extracts the plan, flow, and/opr geometry titles from the input HEC-RAS project folder. 
Loop through all files with the extensions .p##, .u##, and .g## in the project directory and extract the titles.
Print titles next to the file names.

Plan File example (ext = .p01, .p02...)
"C:\ATD\Hydraulic Models\Bennett_MC\MW_Valleys.p19"

Plan Title=MW_10cms
Program Version=6.10
Short Identifier=MW_10cms                                                        
Simulation Date=28AUG2024,0100,28AUG2024,0500
Geom File=g01
Flow File=u03
Subcritical Flow
K Sum by GR= 0 
Std Step Tol= 0.003 
Critical Tol= 0.003 
Num of Std Step Trials= 20 
Max Error Tol= 0.1 
Flow Tol Ratio= 0.001 
Split Flow NTrial= 30 

Unsteady Flow File example (ext = .u01, .u02...)
"C:\ATD\Hydraulic Models\Bennett_MC\MW_Valleys.u08"

Flow Title=UE_10cms
Program Version=6.10
Use Restart= 0 
Boundary Location=                ,                ,        ,        ,                ,MW_Valley       ,                ,BC Line Up                      
Interval=1HOUR
Flow Hydrograph= 6 
      .4      .8     1.5       3       3       3
Stage Hydrograph TW Check=0
Flow Hydrograph Slope= 0.1 
DSS Path=
Use DSS=False
Use Fixed Start Time=False
Fixed Start Date/Time=28AUG2024,0500
Is Critical Boundary=False

Geometry File Example (ext = .g01, .g02...)
"C:\ATD\Hydraulic Models\Bennett_MC\MW_Valleys.g03"
Geom Title=MM_valley
Program Version=6.10
Viewing Rectangle= 454138.350788632 , 454996.859145258 , 4500484.99527748 , 4499489.5183865 

Storage Area=MM_valley       ,454555.3780483,4500001.853238
Storage Area Surface Line= 22 
454229.0053793854499536.24252133                
454181.7994514914499561.32067053                
454177.3738957514499590.82437546                
454259.9109420834499702.11056828                
454312.6515467544499803.42804568                
454373.7196153214499889.47850593              


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
