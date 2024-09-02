import os
from osgeo import gdal
gdal_dll = r"C:\ProgramData\miniconda3\envs\pyHMT2D_env\Library\bin"

# os.add_dll_directory(gdal_dll)
# os.environ['USE_PATH_FOR_GDAL_PYTHON'] = 'YES'


# def save_to_VTK(project_file, terrain_file):
#     # Create a HEC-RAS model instance
#     ras_2d_data = pyHMT2D.RAS_2D.RAS_2D_Data(project_file, terrain_file)

#     #ras_2d_data.saveHEC_RAS2D_results_to_VTK(lastTimeStep=True)
#     ras_2d_data.load2DAreaSolutions()
    
# if __name__ == "__main__":
#     plan_file = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.p01.hdf"
#     terrain_file = r"C:\ATD\Hydraulic Models\Bennett_Valleys\Terrain\Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif"
#     save_to_VTK(plan_file, terrain_file)

#     print("All done!")
    
