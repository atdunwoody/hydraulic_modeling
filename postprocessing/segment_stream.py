import geopandas as gpd
from shapely.geometry import LineString, Point, MultiLineString
from shapely.ops import split
import numpy as np
import os
from tqdm import tqdm

def buffer_centerline(input_gpkg, buffer_distance, output_gpkg = None):
    """
    Buffers the centerline network by a specified amount and saves the result to a new GeoPackage file.
    
    Parameters:
    input_gpkg (str): Path to the input GeoPackage file containing the centerline network.
    layer_name (str): Name of the layer in the GeoPackage containing the centerline network.
    output_gpkg (str): Path to the output GeoPackage file where the buffered result will be saved.
    buffer_distance (float): Buffer distance in the units of the centerline's coordinate system.
    """
    # Load the centerline network from the GeoPackage
    centerline = gpd.read_file(input_gpkg)

    # Buffer the centerline by the specified distance
    buffered_centerline = centerline.copy()
    buffered_centerline['geometry'] = centerline.geometry.buffer(buffer_distance)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_gpkg), exist_ok=True)

    # Save the buffered centerline to a new GeoPackage file
    if output_gpkg is not None:
        buffered_centerline.to_file(output_gpkg, driver='GPKG')
        print(f"Buffered centerline saved to {output_gpkg}")
    return buffered_centerline

def create_smooth_perpendicular_lines(centerline_path, line_length=60, spacing=5, window=200, output_path=None):
    # Load the centerline from the geopackage
    gdf = gpd.read_file(centerline_path)
    
    # Initialize an empty list to store perpendicular lines
    perpendiculars = []
    
    # Iterate through each feature in the GeoDataFrame
    for _, row in gdf.iterrows():
        geometry = row['geometry']
        
        # Handle MultiLineString appropriately using `geoms`
        if isinstance(geometry, MultiLineString):
            line_parts = geometry.geoms
        else:
            line_parts = [geometry]

        # Process each line part
        for line in line_parts:
            length = line.length
            num_samples = int(np.floor(length / spacing))
            for i in range(num_samples + 1):
                # Calculate the point at each meter
                point = line.interpolate(i * spacing)
                
                # Get points 20 meters ahead and behind
                point_back = line.interpolate(max(0, i * spacing - window))
                point_forward = line.interpolate(min(length, i * spacing + window))
                
                # Calculate vectors to these points
                dx_back, dy_back = point.x - point_back.x, point.y - point_back.y
                dx_forward, dy_forward = point_forward.x - point.x, point_forward.y - point.y
                
                # Average the vectors
                dx_avg = (dx_back + dx_forward) / 2
                dy_avg = (dy_back + dy_forward) / 2
                
                # Calculate the perpendicular vector
                len_vector = np.sqrt(dx_avg**2 + dy_avg**2)
                perp_vector = (-dy_avg, dx_avg)
                
                # Normalize and scale the vector
                perp_vector = (perp_vector[0] / len_vector * line_length, perp_vector[1] / len_vector * line_length)
                
                # Create the perpendicular line segment
                perp_line = LineString([
                    (point.x + perp_vector[0], point.y + perp_vector[1]),
                    (point.x - perp_vector[0], point.y - perp_vector[1])
                ])
                
                # Append the perpendicular line to the list
                perpendiculars.append({'geometry': perp_line})
    
    # Convert list to GeoDataFrame
    perpendiculars_gdf = gpd.GeoDataFrame(perpendiculars, crs=gdf.crs)
    
    # Save the perpendicular lines to the same geopackage
    if output_path is not None:
        perpendiculars_gdf.to_file(output_path, driver='GPKG')
    return perpendiculars_gdf

def create_points_along_line(centerline_path, spacing=5, output_path=None):
    # Load the centerline from the GeoPackage
    gdf = gpd.read_file(centerline_path)
    
    # Initialize an empty list to store points
    points = []
    
    # Iterate through each feature in the GeoDataFrame
    for _, row in gdf.iterrows():
        geometry = row['geometry']
        
        # Handle MultiLineString appropriately using `geoms`
        if isinstance(geometry, MultiLineString):
            line_parts = geometry.geoms
        else:
            line_parts = [geometry]

        # Process each line part
        for line in line_parts:
            length = line.length
            num_samples = int(np.floor(length / spacing))
            
            # Generate points along the line at regular intervals
            for i in range(num_samples + 1):
                # Calculate the point at each interval
                point = line.interpolate(i * spacing)
                
                # Append the point as a geometry
                points.append({'geometry': point})
    
    # Convert list to GeoDataFrame
    points_gdf = gpd.GeoDataFrame(points, crs=gdf.crs)
    
    # Save the points to the same GeoPackage if output path is provided
    if output_path is not None:
        points_gdf.to_file(output_path, driver='GPKG')
    
    return points_gdf

def segment_stream_polygon(stream_polygon_path, centerline_path, output_path, segment_spacing=20, window=100, scaling_factor=100):
    """
    Segments a stream polygon into smaller sections using cutting lines perpendicular 
    to a centerline. The cutting lines are placed at regular intervals along the centerline, 
    and the polygon is split along these lines.

    Parameters:
    -----------
    stream_polygon_path : str or gdf
        Path to the GeoPackage or shapefile containing the stream polygon.
        Or a GeoDataFrame containing the stream polygon.
    
    centerline_path : str
        Path to the GeoPackage or shapefile containing the centerline geometry.
    
    output_path : str
        Path to save the segmented polygons as a new GeoPackage or shapefile.
    
    segment_spacing : int, optional
        Width of each segment of the river corridor.
    
    window : int, optional
        The distance in meters to look ahead and behind the interpolation point on 
        the centerline for averaging the direction of the perpendicular cutting line 
        (default is 20 meters).

    Returns:
    --------
    None
        The function saves the segmented polygons to the specified output file.
    """
    
    # Load the shapefile and the centerline
    if isinstance(stream_polygon_path, str):
        gdf = gpd.read_file(stream_polygon_path)
    elif isinstance(stream_polygon_path, gpd.GeoDataFrame):
        gdf = stream_polygon_path
    else:
        raise ValueError("stream_polygon_path must be a string or GeoDataFrame")
    centerline_gdf = gpd.read_file(centerline_path)
    
    # Assuming the polygon to segment is the first feature in the shapefile
    polygon = gdf.geometry[0]
    centerline = centerline_gdf.geometry[0]
    
    # Set n_segments to the length of the centerline
    n_segments = int(centerline.length / segment_spacing)
    print(f"Segmenting into {n_segments} segments")
    # Calculate interval along the centerline to place cutting points
    line_length = centerline.length
    interval = line_length / n_segments
    
    # Initialize list to store cutting lines
    cutting_lines = []
    
    # tqdm progress bar added here
    for i in tqdm(range(1, n_segments), desc="Creating cutting lines"):
        # Calculate the primary interpolation point
        point = centerline.interpolate(i * interval)

        # Calculate points 20 meters behind and ahead for rolling average
        point_back = centerline.interpolate(max(0, i * interval - window))
        point_forward = centerline.interpolate(min(line_length, i * interval + window))
        
        # Determine vectors to these points
        dx_back, dy_back = point.x - point_back.x, point.y - point_back.y
        dx_forward, dy_forward = point_forward.x - point.x, point_forward.y - point.y
        
        # Average the vectors
        dx_avg = (dx_back + dx_forward) / 2
        dy_avg = (dy_back + dy_forward) / 2
        
        # Compute the perpendicular vector
        length_vector = np.sqrt(dx_avg**2 + dy_avg**2)
        perp_dx = -dy_avg / length_vector * scaling_factor
        perp_dy = dx_avg / length_vector * scaling_factor
        
        # Define a long perpendicular line for cutting
        start_point = Point(point.x + perp_dx, point.y + perp_dy)
        end_point = Point(point.x - perp_dx, point.y - perp_dy)
        cutting_lines.append(LineString([start_point, end_point]))
    
    # Initial set of segments
    segments = [polygon]

    # tqdm progress bar added here for splitting the polygon
    for line in tqdm(cutting_lines, desc="Splitting polygons"):
        new_segments = []
        for segment in segments:
            split_result = split(segment, line)
            new_segments.extend(split_result.geoms)
        segments = new_segments

    # Convert segments to GeoDataFrame
    segment_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(segments))

    # Set the same CRS as the original
    segment_gdf.crs = gdf.crs

    # Save to a new shapefile
    segment_gdf.to_file(output_path)

def segment_channel_directory(centerline_dir, channel_poly_dir, output_segments_dir):
    # centerline_dir = r"Y:\ATD\GIS\ETF\Watershed Stats\Channels\Centerlines"
    # input_dir = r"Y:\ATD\GIS\Bennett\Channel Polygons"

    # output_segment_dir = r"Y:\ATD\GIS\ETF\Watershed Stats\Channels\Perpendiculars"
    if not os.path.exists(output_segments_dir):
        os.makedirs(output_segments_dir)
    watersheds = ['LM2', 'LPM', 'MM', 'MPM', 'UM1', 'UM2']
    
    for watershed in watersheds:
        #search for right raster by matching the watershed name
        for file in os.listdir(channel_poly_dir):
            if watershed in file and file.endswith('.gpkg'):
                input_path = os.path.join(channel_poly_dir, file)
                print(f"Input: {input_path}")
                break

        centerline_path = os.path.join(centerline_dir, f'{watershed} centerline.gpkg')
        output_segment_path = os.path.join(output_segments_dir, f'{watershed}_channel_segmented.gpkg')
        print(f"Processing watershed: {watershed}")
        
        print(f"Centerline: {centerline_path}")
        print(f"Output: {output_segment_path}\n")
        #create_centerline(input_path, centerline_path)
        #multipolygon_to_polygon(chan_path, output_path)
        #segment_stream_polygon(input_path, centerline_path, output_segment_path, segment_spacing = 20)
        perp_lines = create_smooth_perpendicular_lines(centerline_path, line_length=60, spacing=500, window=10)
        
        out_perp_path = os.path.join(output_segments_dir, f'{watershed}_perpendicular.gpkg')
        perp_lines.to_file(out_perp_path, driver='GPKG')

def create_map_valleys_input_polygon(centerline_path, segmented_poly_path, buffer_distance=50, segment_spacing=20):
    """
    Create a polygon that represents the valley area around a centerline.
    
    Parameters:
    -----------
    centerline_path : str
        Path to the GeoPackage or shapefile containing the centerline geometry.
    
    output_path : str
        Path to save the valley polygon as a new GeoPackage or shapefile.
    
    buffer_distance : int, optional
        Width of the valley area around the centerline.
    
    Returns:
    --------
    None
        The function saves the valley polygon to the specified output file.
    """
    CL_buffered = buffer_centerline(centerline_path, buffer_distance)
    segment_stream_polygon(CL_buffered, centerline_path, segmented_poly_path, segment_spacing = segment_spacing, scaling_factor=1.1*buffer_distance)

def main():

    input_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Channel Polygons\Centerlines_LSDTopo\Centerlines\ME_clipped.gpkg"
    out_points_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Channel Polygons\Centerlines_LSDTopo\Centerlines\ME_points_50m.gpkg"
    out_perps_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leving Test\ME_perps_5m.gpkg"
    #create_points_along_line(input_path, spacing = 50, output_path = out_points_path)
    create_smooth_perpendicular_lines(input_path, line_length=100, spacing=5, output_path=out_perps_path)
    # centerline_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Channel Polygons\Centerlines_LSDTopo\Bennett_Centerlines_EPSG26913_single.gpkg"
    # output_segment_path = r"Y:\ATD\GIS\Bennett\Valley Widths\Valley_Footprints\Hydraulic Model\Depth Leving Test\Bennett_Centerlines_EPSG26913_20m.gpkg"
    # segment_stream_polygon(input_path, centerline_path, output_segment_path, segment_spacing = 5, scaling_factor=120)
    
if __name__ == '__main__':
    main()