from osgeo import gdal
import h5py

def print_hdf_structure(hdf_path):
    with h5py.File(hdf_path, 'r') as hdf_file:
        def print_structure(name, obj):
            print(name)
        hdf_file.visititems(print_structure)

if __name__ == "__main__":
    hdf_path = r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.p01.hdf"
    print_hdf_structure(hdf_path)