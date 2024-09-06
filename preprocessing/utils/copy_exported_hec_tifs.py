import os
import shutil

# List of source folders
source_folders = [
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_10cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_09cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_08cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_07cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_06cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_05cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_04cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_03cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_02cms",
    r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_01cms"
]

# Output folder
output_folder = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Copy Depth(max).tif from each folder and rename it
for folder in source_folders:
    # Define the source raster path
    source_raster = os.path.join(folder, "Depth (Max).Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif")
    
    if os.path.exists(source_raster):
        # Extract the folder name (e.g., ME_10cms)
        folder_name = os.path.basename(folder)
        
        # Define the destination path with the new name
        destination_raster = os.path.join(output_folder, f"{folder_name}.tif")
        
        # Copy the file
        shutil.copy(source_raster, destination_raster)
        print(f"Copied: {source_raster} to {destination_raster}")
    else:
        print(f"File not found: {source_raster}")
