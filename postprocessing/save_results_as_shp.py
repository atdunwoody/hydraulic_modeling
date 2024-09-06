import os
from osgeo import gdal
import h5py
import numpy as np
from shapely.geometry import Point
import geopandas as gpd

def extract_plan_title_from_file(filepath):

    with open(filepath, 'r') as file:
        for line in file:
            if 'Plan Title=' in line:
                # Extract the text to the right of the equals sign
                plan_title = line.split('=')[1].strip()
                # remove extension from plan_title
                plan_title = os.path.splitext(plan_title)[0]
                break  # Stop after the first match is found
        return plan_title

def get_georeferencing_info(hdf_file):
    # Get the coordinates of the cells
    coords = hdf_file['Geometry/2D Flow Areas/ME_Valley/Cells Center Coordinate'][()]
    x_coords, y_coords = coords[:, 0], coords[:, 1]
    
    # Calculate the bounding box of the grid
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()
    
    return x_coords, y_coords, x_min, y_min, x_max, y_max

def export_as_points(x_coords, y_coords, data, output_dir, filename):
    # Convert the coordinates and data into a GeoDataFrame
    gdf = gpd.GeoDataFrame({
        'value': data,
        'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
    })
    
    # Save to a shapefile
    gdf.to_file(output_path)
    print(f"Saved point shapefile: {output_path}")


def extract_and_save_rasters(hdf_path, output_path):
    with h5py.File(hdf_path, 'r') as hdf_file:
        # Get georeferencing info
        x_coords, y_coords, x_min, y_min, x_max, y_max = get_georeferencing_info(hdf_file)
        
        # Navigate to the specific group containing potential raster data
        dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/ME_Valley/Water Surface']
        #dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/MW_Valley/Water Surface']
        
        # Check if it's 2D data
        if len(dataset.shape) == 2:
            print(f"Processing dataset: Water Surface, Shape: {dataset.shape}, Dtype: {dataset.dtype}")
            
            # Extract the maximum value across all time steps
            data = np.max(dataset, axis=0)  # Max over the time dimension (axis 0)
            
            # Export the data as points
            export_as_points(x_coords, y_coords, data, output_path, "Max_Water_Surface_All_TimeSteps")



if __name__ == "__main__":
    hdf_path_list = [r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p11.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p10.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p09.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p08.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p07.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p06.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p05.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p04.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p03.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p02.hdf",
                r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p01.hdf",]
    
    output_dir = r"C:\ATD\Hydraulic Models\Bennett_MC\ME\Output_HDF_Max"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for hdf_path in hdf_path_list:
        plan_number = hdf_path.split(".")[1][-2:]
        plan_file = hdf_path.split(".")[0] + "." +  hdf_path.split(".")[1]
        plan_title = extract_plan_title_from_file(plan_file)
        output_path = os.path.join(output_dir, plan_title + ".shp")
        extract_and_save_rasters(hdf_path, output_path)
