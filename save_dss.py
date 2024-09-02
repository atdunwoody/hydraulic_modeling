import pyhecdss
import os 

def export_hecras_dss(dss_file_path, output_directory):
    # Open the DSS file
    with pyhecdss.DSSFile(dss_file_path) as dss_file:
        # Get the list of paths in the DSS file
        paths = dss_file.get_pathnames()

        for path in paths:
            # Read the data for each path
            data = dss_file.read(path)
            
            # Create an output filename based on the DSS path
            output_file = path.replace('/', '_').strip('_') + '.csv'
            output_path = os.path.join(output_directory, output_file)
            
            # Export the data to a CSV file
            if isinstance(data, pyhecdss.TimeSeriesContainer):
                data.write_csv(output_path)
            elif isinstance(data, pyhecdss.RegularTimeSeriesContainer):
                data.write_csv(output_path)
            elif isinstance(data, pyhecdss.GridContainer):
                data.write_grid_ascii(output_path)
            else:
                print(f"Unsupported data type for path: {path}")
            
            print(f"Exported {path} to {output_path}")

if __name__ == "__main__":
    dss_file_path = r"C:\ATD\Hydraulic Models\Bennett_Test\MW_Valleys.dss"
    output_directory = r"C:\ATD\Hydraulic Models\Bennett_Test\DSS_Outputs"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    export_hecras_dss(dss_file_path, output_directory)
