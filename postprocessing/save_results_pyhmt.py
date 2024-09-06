"""
Test the HEC_RAS_Model class

It demonstrates how to use pyHMT2D to control the run of HEC-RAS model.
"""
import os
os.environ['USE_PATH_FOR_GDAL_PYTHON'] = 'YES'
import os
import sys
os.add_dll_directory(r"C:\OSGeo4W\bin")
from osgeo import gdal

import pyHMT2D


def convert_HEC_RAS_to_VTK(terrain_file, plan_file):
    """ Convert HEC-RAS result to VTK

    Returns
    -------

    """

    my_ras_2d_data = pyHMT2D.RAS_2D.RAS_2D_Data(plan_file, terrain_file)
    my_ras_2d_data.saveHEC_RAS2D_results_to_VTK(lastTimeStep=True)


if __name__ == "__main__":

    terrain = r"C:\ATD\Hydraulic Models\Bennett_Test\Terrain\Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif"
    plan = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.p01.hdf"
    convert_HEC_RAS_to_VTK(terrain, plan)

    print("All done!")