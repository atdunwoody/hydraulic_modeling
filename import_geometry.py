import pyHMT2D

# Initialize the HEC-RAS model
version = "6.1.0"  # Replace with your HEC-RAS version
faceless = True  # Run HEC-RAS without GUI

# Create a HEC-RAS model instance
hec_ras_model = pyHMT2D.RAS_2D.HEC_RAS_Model(version, faceless)

# Initialize the HEC-RAS model (start the HEC-RAS process)
hec_ras_model.init_model()

# Define paths
project_file = r"C:\ATD\Hydraulic Models\Bennett\MW\MW_valley.prj"  # Replace with your HEC-RAS project file path
terrain_file = r"C:\ATD\Hydraulic Models\UM_Valleys\Terrain\Terrain (1).dem_2021_bennett_clip_filtered.tif" # Replace with your terrain file path
gis_geometry_file = r"Y:\ATD\GIS\Bennett\Valley Widths\Testing\HEC_Import\MW_Valley.shp"  # Replace with your GIS geometry file path


# Open the HEC-RAS project
hec_ras_model.open_project(project_file, terrain_file)

# Use the RASController to import the GIS geometry and save it as a HEC-RAS geometry file
ras_controller = hec_ras_model._RASController

# Assuming ras_controller has a method to import GIS data and add it to the geometry
# This method may vary depending on your version and exact API, so adjust as needed


ras_controller.Geometry_GISImport("MW_Valley", gis_geometry_file)

# After importing, the geometry is added to the project
# need to associate this geometry with a specific plan

# Save the updated project
hec_ras_model.save_project()

# Close the project and exit the model
hec_ras_model.close_project()
hec_ras_model.exit_model()

print("GIS geometry file imported and added to HEC-RAS project successfully.")
