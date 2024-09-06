import h5py
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.features import rasterize
from shapely.geometry import Point
import geopandas as gpd
import os

# Function to retrieve georeferencing information from the HDF5 file
def get_georeferencing_info(hdf_file):
    # Extract the coordinates of cell centers from the HDF5 file
    coords = hdf_file['Geometry/2D Flow Areas/MW_Valley/Cells Center Coordinate'][()]
    x_coords, y_coords = coords[:, 0], coords[:, 1]
    
    # Calculate the bounding box of the grid based on the min and max coordinates
    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()
    
    return x_coords, y_coords, x_min, y_min, x_max, y_max

# Function to rasterize point data and save it as a GeoTIFF file
def rasterize_points(x_coords, y_coords, data, x_min, y_min, x_max, y_max, resolution, output_dir, filename):
    # Create a GeoDataFrame from the x, y coordinates and corresponding data values
    gdf = gpd.GeoDataFrame({
        'value': data,
        'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
    })
    
    # Define the dimensions of the output raster based on the resolution and bounding box
    width = int((x_max - x_min) / resolution)
    height = int((y_max - y_min) / resolution)
    
    # Define the affine transform for the raster based on the bounding box and raster dimensions
    transform = from_bounds(x_min, y_min, x_max, y_max, width, height)
    
    # Rasterize the points into a 2D array, filling cells with the 'value' from the GeoDataFrame
    raster = rasterize(
        [(geom, value) for geom, value in zip(gdf.geometry, gdf['value'])],
        out_shape=(height, width),
        transform=transform,
        fill=0,  # Fill value for empty cells; can be changed to a nodata value if needed
        all_touched=True,  # Ensures that all pixels touched by geometries are rasterized
        dtype='float32'  # Data type for the raster; 'float32' to match typical DEM formats
    )
    
    # Define the path for the output raster file
    output_raster_path = f"{output_dir}/{filename}.tif"
    
    # Save the rasterized data to a GeoTIFF file
    with rasterio.open(
        output_raster_path, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,  # Number of bands in the raster; 1 for single-band raster
        dtype='float32',  # Data type for the raster
        crs='+proj=utm +zone=13 +datum=NAD83 +units=m +no_defs +ellps=GRS80 +towgs84=0,0,0',  # Coordinate reference system (CRS)
        transform=transform,
        nodata=0  # Define nodata value; this should match the fill value used in rasterize
    ) as dst:
        dst.write(raster, 1)  # Write the raster data to the file
    
    # Print confirmation message indicating the location of the saved raster
    print(f"Saved raster: {output_raster_path}")

# Main function to extract data from the HDF5 file and save it as rasters
def extract_and_save_rasters(hdf_path, output_dir, resolution):
    # Open the HDF5 file in read mode
    with h5py.File(hdf_path, 'r') as hdf_file:
        # Retrieve georeferencing information (coordinates and bounding box)
        x_coords, y_coords, x_min, y_min, x_max, y_max = get_georeferencing_info(hdf_file)
        
        # Navigate to the dataset containing the desired raster data
        dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas/MW_Valley/Maximum Water Surface']
        #dataset = hdf_file['Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/MW_Valley/Water Surface']
        
        # Check if the dataset contains 2D data (e.g., time x cells)
        if len(dataset.shape) == 2:
            print(f"Processing dataset: Water Surface, Shape: {dataset.shape}, Dtype: {dataset.dtype}")
            
            # Extract data for the last time step (assuming the first dimension is time)
            data = dataset[-1, :]  # '-1' accesses the last time step
            
            # Rasterize the extracted data and save it as a GeoTIFF
            rasterize_points(x_coords, y_coords, data, x_min, y_min, x_max, y_max, resolution, output_dir, "Max_Water_Surface_TimeStep_Last")


if __name__ == "__main__":
    # Define paths and resolution
    hdf_path = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.p01.hdf"
    output_dir = r"C:\ATD\Hydraulic Models\Bennett_Test\Output_HDF"
    resolution = 1

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Execute the extraction and rasterization process
    extract_and_save_rasters(hdf_path, output_dir, resolution)
