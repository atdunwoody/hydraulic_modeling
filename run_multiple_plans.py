import pyHMT2D
from utils.get_plan_names import extract_plan_titles
import os

def run_HEC_RAS(project_file, terrain_file):
    # Create a HEC-RAS model instance
    my_hec_ras_model = pyHMT2D.RAS_2D.HEC_RAS_Model(version="6.1.0", faceless=False)

    # Initialize the HEC-RAS model
    my_hec_ras_model.init_model()

    print("Hydraulic model name:", my_hec_ras_model.getName())
    print("Hydraulic model version:", my_hec_ras_model.getVersion())

    # Open a HEC-RAS project
    my_hec_ras_model.open_project(project_file, terrain_file)

    # Get the ras_controller instance
    ras = my_hec_ras_model._RASController
    print("RAS Controller:", ras)
    # Attempt to list plan names with fewer parameters
    plans = extract_plan_titles(os.path.dirname(project_file))
    
    print("Plans in the project:", plans)

    for file, plan in plans.items():
        try:
            print("Running plan:", plan)
            if plan == 'MW_1cms_1s':
                continue
            # Set the current plan
            successful = ras.Plan_SetCurrent(plan)
            print(f"Plan Changed Successfully: {successful}")
            # Run the model for the current plan
            #my_hec_ras_model.run_model()
            ras.Plan_New()
            print("Current plan file:", plan)


        except Exception as e:
            print(f"Error occurred while running plan {plan}: {e}")

    # Close the HEC-RAS project
    my_hec_ras_model.close_project()

    # Quit HEC-RAS
    my_hec_ras_model.exit_model()

if __name__ == "__main__":
    project_file = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.prj"
    terrain_file = r"C:\ATD\Hydraulic Models\Bennett_Valleys\Terrain\Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif"
    run_HEC_RAS(project_file, terrain_file)

    print("All done!")
