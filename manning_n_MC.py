import numpy as np
import time
from pyHMT2D import RAS_2D

def monte_carlo_n_values(project_file, terrain_file, num_realizations=1000):
    """
    This function runs a Monte Carlo experiment by sampling n values from a normal distribution
    and applying them to the main channel of each cross section in a HEC-RAS project. The water
    surface elevations are stored after each realization and sorted to determine elevation exceedance
    probabilities.

    :param project_file: Path to the HEC-RAS project file
    :param terrain_file: Path to the terrain file
    :param num_realizations: Number of Monte Carlo realizations to run
    :return: Exceedance probability water surface elevations
    """

    # Initialize the HEC-RAS model
    my_hec_ras_model = RAS_2D.HEC_RAS_Model(version="6.1.0", faceless=False)
    my_hec_ras_model.init_model()
    ras_controller = my_hec_ras_model._RASController
    
    # Open the HEC-RAS project
    my_hec_ras_model.open_project(project_file, terrain_file)

    # Define the normal distribution parameters for Manning's n
    mean_n = 0.04
    stddev_n = 0.015

    # Store start time
    start_time = time.time()

    # Array to store water surface elevations for each realization
    wse_elevations = np.zeros(num_realizations)

    # Array to keep track of sampled n values
    sampled_n_values = np.zeros(num_realizations)

    # Run Monte Carlo realizations
    for i in range(num_realizations):
        # Sample n value from normal distribution
        n_ch = np.random.normal(mean_n, stddev_n)

        # Apply the sampled n value to the geometry
        apply_n_values_to_geometry(ras_controller, n_ch)

        # Save the project with new Manning's n values
        ras_controller.Project_Save()

        # Run the HEC-RAS computation
        ras_controller.Compute_HideComputationWindow()
        did_compute = ras_controller.Compute_CurrentPlan()

        # Get water surface elevation output for a specific river station
        wse_elevations[i] = ras_controller.Output_NodeOutput(1, 1, 1, 0, 1, 2)

        # Store sampled n value
        sampled_n_values[i] = n_ch

        # Show progress
        elapsed_time = round((time.time() - start_time) / 60, 2)
        print(f"Finished computing realization #{i+1} of {num_realizations}. "
              f"Sampled N Value = {round(n_ch, 4)}. Elapsed Time: {elapsed_time} minutes.")

    # Sort the water surface elevations to calculate exceedance probabilities
    sorted_wse_elevations = np.sort(wse_elevations)

    # Calculate exceedance probability water surface elevations
    wse_99 = np.percentile(sorted_wse_elevations, 99)
    wse_90 = np.percentile(sorted_wse_elevations, 90)
    wse_50 = np.percentile(sorted_wse_elevations, 50)
    wse_10 = np.percentile(sorted_wse_elevations, 10)
    wse_1 = np.percentile(sorted_wse_elevations, 1)

    # Display results
    elapsed_time = round((time.time() - start_time) / 60, 1)
    print(f"Total time: {elapsed_time} minutes.")
    print(f"99% Exceedance Water Surface Elevation = {round(wse_99, 2)}")
    print(f"90% Exceedance Water Surface Elevation = {round(wse_90, 2)}")
    print(f"50% Exceedance Water Surface Elevation = {round(wse_50, 2)}")
    print(f"10% Exceedance Water Surface Elevation = {round(wse_10, 2)}")
    print(f"1% Exceedance Water Surface Elevation = {round(wse_1, 2)}")

    # Close HEC-RAS
    ras_controller.QuitRAS()

    # Return exceedance probability water surface elevations
    return wse_99, wse_90, wse_50, wse_10, wse_1

def apply_n_values_to_geometry(ras_controller, n_ch):
    """
    This function applies the sampled n value to the main channel of each cross section.
    
    :param ras_controller: HEC-RAS controller object
    :param n_ch: Sampled Manning's n value for the main channel
    """
    # Retrieve the geometry data from the HEC-RAS project
    geom_data = ras_controller.Geometry_GetData()

    # Loop through each river, reach, and cross-section
    for river in geom_data["Rivers"]:
        river_name = river["RiverName"]
        for reach in river["Reaches"]:
            reach_name = reach["ReachName"]
            for cross_section in reach["CrossSections"]:
                river_station = cross_section["RiverStation"]

                # Apply Manning's n to the left overbank, main channel, and right overbank
                # In this example, I'm applying the same n_ch to the main channel
                n_left = 0.1  # Fixed value for left overbank
                n_right = 0.1  # Fixed value for right overbank

                # Apply the Manning's n values using the RASController method
                error_message = ras_controller.Geometry_SetManningsN(
                    river_name, reach_name, river_station, n_left, n_ch, n_right
                )

                if error_message:
                    print(f"Error setting Manning's n for {river_name} {reach_name} {river_station}: {error_message}")

