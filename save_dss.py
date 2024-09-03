import csv

# Define the input and output file paths
input_file = r"Y:\ATD\GIS\Bennett\Site VIsits\231006\RTK GNSS\231006-ME-RAW.txt"
output_file = r"Y:\ATD\GIS\Bennett\Site VIsits\231006\RTK GNSS\231006-ME-RAW.csv"

# Initialize variables to hold the headers and data
headers = None
data = []

# Read the input file and extract headers and data
with open(input_file, 'r') as infile:
    for line in infile:
        # Check if the line contains the header
        if line.startswith("Header>> Delimiter(,) FileFormat("):
            # Extract the headers from the line
            headers = line.strip()[len("Header>> Delimiter(,) FileFormat("):-len(") <<")].split(',')
        else:
            # Add the data rows to the data list
            data.append(line.strip().split(','))

# Write the data to the CSV file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Write the headers first
    if headers:
        writer.writerow(headers)
    # Write the data rows
    writer.writerows(data)

print(f"Data has been successfully converted to {output_file}")
