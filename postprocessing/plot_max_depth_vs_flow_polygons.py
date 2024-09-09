import rasterio
import rasterio.mask  # Add this line to explicitly import the mask function
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import segment_stream as ss
import geopandas as gpd
from rasterio.merge import merge
import os

def extract_and_clip_selected_raster_by_segment(shapefile, flow_raster_dict, selected_flow_dict, output_dir):
    if isinstance(shapefile, str):
        segments_gdf = gpd.read_file(shapefile)
    elif isinstance(shapefile, gpd.GeoDataFrame):
        segments_gdf = shapefile
    else:
        raise ValueError("shapefile must be a path to a shapefile or a GeoDataFrame.")
    
    stitched_rasters = []

    for idx, segment in enumerate(segments_gdf.geometry):
        # Get the selected flow value for this segment
        selected_flow_value = selected_flow_dict[idx]
        
        # Get the corresponding raster path for the selected flow value
        raster_path = flow_raster_dict.get(selected_flow_value)
        
        if raster_path:
            with rasterio.open(raster_path) as src:
                # Mask raster with polygon
                out_image, out_transform = rasterio.mask.mask(src, [segment], crop=True)
                out_meta = src.meta.copy()
                
                # Update metadata to reflect the new dimensions and transform
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform
                })
                
                # Save the clipped raster for the current segment and flow value
                clipped_raster_path = f"{output_dir}/segment_{idx}_flow_{selected_flow_value}.tif"
                with rasterio.open(clipped_raster_path, "w", **out_meta) as dest:
                    dest.write(out_image)
                
                # Append to the list of clipped rasters for merging later
                stitched_rasters.append(clipped_raster_path)
        else:
            print(f"Flow value {selected_flow_value} not found in flow_raster_dict for segment {idx}")

    return stitched_rasters

def stitch_rasters(raster_paths, output_stitched_path):
    # Open all clipped raster files for merging
    src_files_to_mosaic = []
    for path in raster_paths:
        src = rasterio.open(path)
        src_files_to_mosaic.append(src)
    
    # Merge the rasters
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    # Copy metadata from one of the source files
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })
    
    # Write the mosaic to a new file
    with rasterio.open(output_stitched_path, "w", **out_meta) as dest:
        dest.write(mosaic)
    
    # Close all source files
    for src in src_files_to_mosaic:
        src.close()

def extract_max_depths_by_segment(shapefile, flow_raster_dict, percentile=90):
    if isinstance(shapefile, str):
        segments_gdf = gpd.read_file(shapefile)
    elif isinstance(shapefile, gpd.GeoDataFrame):
        segments_gdf = shapefile
    else:
        raise ValueError("shapefile must be a path to a shapefile or a GeoDataFrame.")
    
    segment_depths = {}

    for idx, segment in enumerate(segments_gdf.geometry):
        segment_depths[idx] = {}
        for flow_value, raster_path in flow_raster_dict.items():
            with rasterio.open(raster_path) as src:
                # Mask raster with polygon
                out_image, out_transform = rasterio.mask.mask(src, [segment], crop=True)
                #max_depth = np.median(out_image)  # Get the maximum depth within the segment
                #get 90th percentile depth
                max_depth = np.percentile(out_image, percentile)
                segment_depths[idx][flow_value] = max_depth

    return segment_depths

def smooth_data(data, window_length=5, polyorder=2):
    """
    Apply Savitzky-Golay filter for data smoothing.
    """
    return savgol_filter(data, window_length=window_length, polyorder=polyorder)

def fit_polynomial(x, y, degree=3):
    """
    Fit a polynomial to the data.
    """
    coeffs = np.polyfit(x, y, degree)
    return np.poly1d(coeffs)

def find_leveling_out_point(flow_values, smoothed_depths):
    """
    Use first and second derivatives to find the leveling out point.
    """
    first_derivative = np.gradient(smoothed_depths, flow_values)
    second_derivative = np.gradient(first_derivative, flow_values)

    # Use both the first derivative approaching zero and second derivative being small
    leveling_out_index = np.argmin(np.abs(second_derivative))  # closest to zero

    return leveling_out_index

def plot_flow_vs_depth_by_segment(segment_depths):
    flow_value_dict = {}

    for segment_idx, depths in segment_depths.items():
        flow_values = list(depths.keys())
        max_depths = list(depths.values())

        # Smooth the max depths
        smoothed_depths = smooth_data(max_depths)

        # Find leveling out point
        leveling_out_index = find_leveling_out_point(flow_values, smoothed_depths)

        # Fit a polynomial to the smoothed data
        poly = fit_polynomial(flow_values, smoothed_depths)
        fitted_values = poly(flow_values)

        # Plot original and smoothed data
        # plt.figure(figsize=(10, 6))
        # plt.plot(flow_values, max_depths, marker='o', label='Original Max Depths')
        # plt.plot(flow_values, smoothed_depths, label='Smoothed Depths', color='orange')
        # plt.plot(flow_values, fitted_values, label='Fitted Polynomial', color='green')
        # plt.axvline(flow_values[leveling_out_index], color='red', linestyle='--', 
        #             label=f'Leveling out at Flow = {flow_values[leveling_out_index]}')
        # plt.title(f'Flow Value vs Max Depth for Segment {segment_idx}')
        # plt.xlabel('Flow Value')
        # plt.ylabel('Max Depth')
        # plt.grid(True)
        # plt.legend()

        flow_value_dict[segment_idx] = flow_values[leveling_out_index]

    return flow_value_dict

# Update input paths
segmented_polygon_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leveling Test\Inputs\Segmented_Buffered_Valley_5m.gpkg"
flow_raster_dict = {
    0.25 : r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Max Depth Rasters\ME_0025cms.tif",
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

scratch_dir = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leveling Test\Clipped_Rasters"
output_dir =r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leveling Test\Results"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(scratch_dir, exist_ok=True)
percentile_array = np.arange(5, 95, 5)
for percentile in percentile_array:
    print(f"Processing {percentile}th percentile...")
    stitched_raster_title = f"Stitched_Raster_{percentile}th_per_5m.tif"
    stitched_raster_output_path = os.path.join(output_dir, 
                                               stitched_raster_title)

    
    
    # Extract max depths for each segment
    segmented_polygons_gdf = gpd.read_file(segmented_polygon_path)
    max_depths = extract_max_depths_by_segment(segmented_polygons_gdf, flow_raster_dict, percentile)

    # Plot and get the flow values where depth levels out for each segment
    flow_value_dict = plot_flow_vs_depth_by_segment(max_depths)

    # Clip only the selected raster for each segment based on flow_value_dict
    clipped_rasters = extract_and_clip_selected_raster_by_segment(segmented_polygons_gdf, flow_raster_dict, flow_value_dict, output_dir)

    # Stitch clipped rasters into a single output
    stitch_rasters(clipped_rasters, stitched_raster_output_path)

    for segment, flow in flow_value_dict.items():
        print(f"Segment {segment} levels out at flow value {flow}")
