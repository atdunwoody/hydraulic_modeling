import os
import h5py
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.features import dataset_features
from shapely.geometry import Point
import geopandas as gpd

def get_georeferencing_info(hdf_file):
    # Get the coordinates of the cells
    coords = hdf_file['Geometry/2D Flow Areas/MW_Valley/Cells Center Coordinate'][()]
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
    output_path = f"{output_dir}/{filename}.shp"
    gdf.to_file(output_path)
    print(f"Saved point shapefile: {output_path}")

def extract_and_save_rasters(hdf_path, output_dir):
    with h5py.File(hdf_path, 'r') as hdf_file:
        # Get georeferencing info
        x_coords, y_coords, x_min, y_min, x_max, y_max = get_georeferencing_info(hdf_file)
        
        # Navigate to the specific group containing potential raster data
        dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas/MW_Valley/Maximum Water Surface']
        #dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/MW_Valley/Water Surface']
        
        # Check if it's 2D data
        if len(dataset.shape) == 2:
            print(f"Processing dataset: Water Surface, Shape: {dataset.shape}, Dtype: {dataset.dtype}")
            
            # Extract a single time step (e.g., the first one)
            data = dataset[-1, :]  # Assuming the first dimension is time
            
            # Export the data as points
            export_as_points(x_coords, y_coords, data, output_dir, "Max_Water_Surface_TimeStep_Last")
            

def print_hdf_structure(hdf_path):
    with h5py.File(hdf_path, 'r') as hdf_file:
        def print_structure(name, obj):
            print(name)
        hdf_file.visititems(print_structure)


if __name__ == "__main__":
    hdf_path = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.p01.hdf"
    output_dir = r"C:\ATD\Hydraulic Models\Bennett_Test\Output_HDF"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    extract_and_save_rasters(hdf_path, output_dir)
    #print_hdf_structure(hdf_path)

