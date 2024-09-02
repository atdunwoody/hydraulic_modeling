import os
import pyHMT2D


def save_to_VTK(project_file, terrain_file):
    # Create a HEC-RAS model instance
    #ras_2d_data = pyHMT2D.RAS_2D.RAS_2D_Data(project_file, terrain_file)
    my_hec_ras_model = pyHMT2D.RAS_2D.HEC_RAS_Model(version="6.1.0", faceless=False)

    # Initialize the HEC-RAS model
    my_hec_ras_model.init_model()

    print("Hydraulic model name:", my_hec_ras_model.getName())
    print("Hydraulic model version:", my_hec_ras_model.getVersion())

    # Get the ras_controller instance
    ras = my_hec_ras_model._RASController
    output_data = ras.OutputDSS_GetStageFlowSA("MW_valley")
    #ras_2d_data.saveHEC_RAS2D_results_to_VTK(lastTimeStep=True)
    print(f"Output data: {output_data}")

    
if __name__ == "__main__":
    plan_file = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.p01.hdf"
    terrain_file = r"C:\ATD\Hydraulic Models\Bennett_Valleys\Terrain\Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif"
    save_to_VTK(plan_file, terrain_file)

    print("All done!")
    
