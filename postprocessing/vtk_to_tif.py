import pyvista as pv
import numpy as np
import rasterio
from rasterio.transform import from_origin

# Load the unstructured VTK file
def load_vtk(vtk_file):
    mesh = pv.read(vtk_file)
    return mesh

# Convert the unstructured VTK to a structured grid (interpolation)
def interpolate_to_grid(mesh, resolution=(100, 100)):
    # Get bounds of the mesh
    bounds = mesh.bounds
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    
    # Generate grid points (structured grid) within the bounds
    x = np.linspace(xmin, xmax, resolution[0])
    y = np.linspace(ymin, ymax, resolution[1])
    z = np.zeros_like(x)
    
    # Create a 2D grid of x, y points
    xx, yy = np.meshgrid(x, y)
    
    # Interpolate data at these points using the mesh's interpolation method
    structured_grid = mesh.sample_over_line([xmin, ymin, zmin], [xmax, ymax, zmin], resolution[0] * resolution[1])
    
    # Reshape the grid into a 2D array
    grid_values = structured_grid['Water_Elev_m'].reshape(resolution)
    
    return xx, yy, grid_values

# Write the interpolated grid to a GeoTIFF
def write_geotiff(output_file, xx, yy, grid_values):
    # Get the top left corner coordinates
    x_min, y_max = xx.min(), yy.max()

    # Resolution (pixel size)
    pixel_size_x = (xx.max() - xx.min()) / xx.shape[1]
    pixel_size_y = (yy.max() - yy.min()) / yy.shape[0]
    
    # Define the GeoTIFF transform
    transform = from_origin(x_min, y_max, pixel_size_x, pixel_size_y)

    # Write to a GeoTIFF
    with rasterio.open(
        output_file,
        'w',
        driver='GTiff',
        height=grid_values.shape[0],
        width=grid_values.shape[1],
        count=1,
        dtype=grid_values.dtype,
        crs='EPSG:26913',  # Assuming WGS84, change as necessary
        transform=transform,
    ) as dst:
        dst.write(grid_values, 1)

# Main function to load VTK, interpolate, and save to GeoTIFF
def vtk_to_geotiff(vtk_file, output_file, resolution=(100, 100)):
    # Load the unstructured VTK file
    mesh = load_vtk(vtk_file)
    
    # Interpolate the VTK to a structured grid
    xx, yy, grid_values = interpolate_to_grid(mesh, resolution)
    
    # Write the structured grid to a GeoTIFF
    write_geotiff(output_file, xx, yy, grid_values)
    
# Example usage
if __name__ == "__main__":
    vtk_file = r"C:\Users\alextd\Documents\GitHub\pyHMT2D\RAS2D_p02_ME_Valley_0016.vtk"
    output_tif = r"C:\Users\alextd\Documents\GitHub\pyHMT2D\RAS2D_p02_ME_Valley_0016.tif"

    resolution = (1, 1)  # Define your desired resolution here
    
    vtk_to_geotiff(vtk_file, output_tif, resolution)
