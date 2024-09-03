# HEC-RAS Automation and Geospatial Processing Scripts

## Overview

This repository contains Python scripts designed to automate HEC-RAS model workflows and perform geospatial data processing, specifically related to hydraulic modeling in the context of 2D flow areas. The scripts cover a range of tasks, including extracting and saving rasters from HDF5 files, exporting geospatial points as shapefiles, creating and updating hydrographs for Monte Carlo simulations, and running multiple HEC-RAS plans programmatically.

## Scripts

### 1. `save_results_as_raster.py`
This script processes data stored in an HDF5 file, extracts geospatial data, rasterizes it, and saves it as a GeoTIFF raster file.

- **Key Functions**:
  - `get_georeferencing_info(hdf_file)`: Extracts cell center coordinates and calculates the bounding box of the grid.
  - `rasterize_points(...)`: Converts point data into a raster format and saves it as a GeoTIFF file.
  - `extract_and_save_rasters(hdf_path, output_dir, resolution)`: Handles the overall process of extracting, rasterizing, and saving data.

- **Usage**:
  Specify the path to the HDF5 file, the output directory, and the desired resolution in the main block of the script. The script will process the data and save the output as a raster file.

### 2. `save_results_as_shp.py`
This script processes data from an HDF5 file, extracts geospatial point data, and exports it as a shapefile containing points with associated data values.

- **Key Functions**:
  - `get_georeferencing_info(hdf_file)`: Extracts cell center coordinates and calculates the bounding box of the grid.
  - `export_as_points(...)`: Converts point data into a GeoDataFrame and exports it as a shapefile.
  - `extract_and_save_rasters(hdf_path, output_dir)`: Orchestrates the extraction and shapefile export process.

- **Usage**:
  Specify the path to the HDF5 file and the output directory in the main block of the script. The script will process the data and save the output as a shapefile.

### 3. `unsteady_MC.py`
This script automates the creation and updating of flow hydrographs for Monte Carlo simulations in HEC-RAS. It modifies HEC-RAS flow and plan files, ensuring that each simulation run has a unique identifier.

- **Key Functions**:
  - `create_hydrograph(max_flow_value, ramp_steps, steady_steps)`: Generates a hydrograph that ramps up to the maximum flow value.
  - `update_flow_hydrograph(input_file, new_hydrograph, new_title, max_flow_value)`: Updates the flow hydrograph and title in the specified HEC-RAS flow file.
  - `update_plan_file(file_path, new_flow_file, new_title, max_flow_value)`: Updates the plan file with the new flow file and plan title.
  - `update_prj_file(prj_file_path, new_unsteady_file, new_plan_file)`: Updates the HEC-RAS project file with the new unsteady and plan files.
  - `generate_hydrograph_and_update_plan(...)`: Combines the previous functions to automate the entire process for a list of flow values.

- **Usage**:
  Specify the paths to the input flow file, plan file, and project file in the main block of the script. The script will generate hydrographs for a list of maximum flow values and update the HEC-RAS files accordingly.

### 4. `run_multiple_plans.py`
This script allows for the automated execution of multiple HEC-RAS plans. It leverages the `pyHMT2D` package to interact with HEC-RAS, running each specified plan and handling the project and terrain files.

- **Key Functions**:
  - `run_multiple_HEC_RAS_plans(project_file, terrain_file, plan_array)`: Runs the specified HEC-RAS plans in sequence.

- **Usage**:
  Define the paths to the project file and terrain file, and specify the array of plan identifiers in the main block of the script. The script will run each plan and output the results.

## Prerequisites

- Python 3.x
- HDF5 files should be in the correct format as expected by the scripts.
- The following Python libraries must be installed:
  - `h5py`
  - `numpy`
  - `rasterio`
  - `shapely`
  - `geopandas`
  - `pyHMT2D` (for `run_multiple_plans.py`)

## How to Use

 
