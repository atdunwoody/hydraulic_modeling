import pyHMT2D
from preprocessing.get_plan_names import extract_plan_titles
from preprocessing.set_current_plan import set_current_plan
import os

def run_multiple_HEC_RAS_plans(project_file, terrain_file, plan_array = []):
    # Get the list of all plans in the project
    if not plan_array:
        plans = extract_plan_titles(os.path.dirname(project_file))
        #get just the plan names from dictionary {file: plan}
        plan_array = {file for file, plan in plans.items()}
        print("Plans in the project:", plans)
        
    for plan in plan_array:
        # Create a HEC-RAS model instance
        print(f"Running plan {plan}")
        plan_set_suceessfully = set_current_plan(project_file, plan)
        if not plan_set_suceessfully:
            continue
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

        try:
            print(f"Running plan {plan}")
            my_hec_ras_model.run_model()
            
        except Exception as e:
            print(f"Error occurred while running plan {plan}: {e}")

        # Close the HEC-RAS project
        my_hec_ras_model.close_project()

        # Quit HEC-RAS
        my_hec_ras_model.exit_model()

if __name__ == "__main__":
    project_file = r"C:\ATD\Hydraulic Models\Bennett_MC\ME\ME_Valleys.prj"
    terrain_file = r"C:\ATD\Hydraulic Models\Bennett_MC Backup\Terrain\Terrain.Terrain (1).dem_2021_bennett_clip_filtered.tif"
    plan_array =[]
    run_multiple_HEC_RAS_plans(project_file, terrain_file, plan_array)

    print("All done!")
