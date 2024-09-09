import vtk
import numpy as np
import rasterio
from rasterio.transform import from_origin
from vtk.util import numpy_support

def vtk_to_tiff(vtk_file_path, tiff_file_path, pixel_size=(1.0, 1.0), origin=(0.0, 0.0)):
    """
    Convert a VTK Unstructured Grid file to a TIFF file.
    
    :param vtk_file_path: Path to the input VTK file
    :param tiff_file_path: Path to the output TIFF file
    :param pixel_size: Size of each pixel in the output TIFF (default is (1.0, 1.0))
    :param origin: Origin of the raster (default is (0.0, 0.0))
    """
    # Read the VTK file (Unstructured Grid)
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(vtk_file_path)
    reader.Update()

    # Get the unstructured grid data from the VTK file
    vtk_data = reader.GetOutput()

    # Extract scalar values from the VTK file (assuming scalar field exists)
    scalars = vtk_data.GetPointData().GetScalars()

    if scalars is None:
        raise ValueError("No scalars found in the VTK file.")

    # Convert VTK scalars to a numpy array
    array = numpy_support.vtk_to_numpy(scalars)

    # Define the transform (georeferencing)
    transform = from_origin(origin[0], origin[1], pixel_size[0], pixel_size[1])

    # Reshape the array into a 2D grid based on some known dimensions (requires assumption)
    # You may need to adjust these dimensions depending on your data structure
    num_points = vtk_data.GetNumberOfPoints()
    grid_size = int(np.sqrt(num_points))  # Assuming a square grid for demonstration
    array_2d = array.reshape((grid_size, grid_size))

    # Write to a TIFF file using rasterio
    with rasterio.open(
        tiff_file_path, 'w',
        driver='GTiff',
        height=array_2d.shape[0],
        width=array_2d.shape[1],
        count=1,  # Number of bands
        dtype=array_2d.dtype,
        crs='+proj=latlong',
        transform=transform
    ) as dst:
        dst.write(array_2d, 1)

vtk_file = r"C:\Users\alextd\Documents\GitHub\pyHMT2D\RAS2D_p02_ME_Valley_0016.vtk"
output_tif = r"C:\Users\alextd\Documents\GitHub\pyHMT2D\RAS2D_p02_ME_Valley_0016.tif"
vtk_to_tiff(vtk_file, output_tif, pixel_size=(1, 1), origin=(0, 0))
