import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt
import numpy as np

def extract_max_depths_by_point(shapefile, flow_raster_dict):
    """
    Extract maximum max depth colocated with each thalweg point for each flow value.

    Parameters:
    shapefile (str): Path to input shapefile containing thalweg points.
    flow_raster_dict (dict): Dictionary where keys are flow values and values are paths to corresponding max depth rasters.

    Returns:
    dict: Dictionary where keys are point indices and values are dictionaries of flow values vs corresponding max depths.
    """
    # Load thalweg points from shapefile
    points_gdf = gpd.read_file(shapefile)

    # Initialize a dictionary to store max depths for each point
    point_depths = {}

    # Iterate through the points
    for idx, point in enumerate(points_gdf.geometry):
        point_depths[idx] = {}
        # For each point, iterate over flow values and rasters
        for flow_value, raster_path in flow_raster_dict.items():
            with rasterio.open(raster_path) as src:
                # Get the raster row and column for this point
                row, col = src.index(point.x, point.y)

                # Extract the pixel value (max depth) for this point
                max_depth = src.read(1)[row, col]

                # Store the max depth for this point and flow value
                point_depths[idx][flow_value] = max_depth

    return point_depths

def plot_flow_vs_depth_by_point(point_depths):
    """
    Plot flow values vs max depths for each point, compute second-order derivative,
    and identify where the graph levels out.

    Parameters:
    point_depths (dict): Dictionary where keys are point indices and values are dictionaries of flow values vs max depths.
    """
    flow_value_dict = {}
    for point_idx, depths in point_depths.items():
        flow_values = list(depths.keys())
        max_depths = list(depths.values())

        # Compute first and second derivatives of the max_depths with respect to flow_values
        first_derivative = np.gradient(max_depths, flow_values)
        second_derivative = np.gradient(first_derivative, flow_values)

        # Find where the second derivative is closest to zero (indicating leveling out)
        leveling_out_index = np.argmin(np.abs(second_derivative))

        plt.figure(figsize=(10, 6))
        plt.plot(flow_values, max_depths, marker='o', label='Max Depths')
        plt.axvline(flow_values[leveling_out_index], color='red', linestyle='--', label=f'Leveling out at Flow = {flow_values[leveling_out_index]}')
        plt.title(f'Flow Value vs Max Depth for Point {point_idx}')
        plt.xlabel('Flow Value')
        plt.ylabel('Max Depth')
        plt.grid(True)
        plt.legend()

        plt.figure(figsize=(10, 6))
        plt.plot(flow_values, second_derivative, marker='o', color='green', label='Second Derivative')
        plt.axhline(0, color='black', linestyle='--')
        plt.title(f'Second Derivative of Flow vs Max Depth for Point {point_idx}')
        plt.xlabel('Flow Value')
        plt.ylabel('Second Derivative')
        plt.grid(True)
        plt.legend()

        #plt.show()
        flow_value_dict[point_idx] = flow_values[leveling_out_index]
    return flow_value_dict

thalweg_shapefile = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leving Test\ME_Thalweg_Points.gpkg"
flow_raster_dict = {
    # 0.25 : r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_0025cms.tif",
    0.5: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_005cms.tif",
    1: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_01cms.tif",
    2: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_02cms.tif",
    3: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_03cms.tif",
    4: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_04cms.tif",
    5: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_05cms.tif",
    6: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_06cms.tif",
    7: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_07cms.tif",
    8: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_08cms.tif",
    9: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_09cms.tif",
    10: r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_10cms.tif",
}

# Extract max depths
max_depths = extract_max_depths_by_point(thalweg_shapefile, flow_raster_dict)

# Plot flow vs max depth and second derivative
flow_value_dict = plot_flow_vs_depth_by_point(max_depths)

for point, flow in flow_value_dict.items():
    print(f"Point {point} levels out at flow value {flow}")