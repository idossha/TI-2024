import csv
import os

"""
This is the second step in source localization. 

Now you are working with .csv files.
This script will take all .csv file in a directory and convert them to .geo 

You will be able to view the net in 3D and load it to SimNIBS.

Created: March 01, 2024
Last Update: April 01, 2024

Ido 

"""


def format_electrode_data(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as csvfile, open(
        output_path, "w", encoding="utf-8"
    ) as outputfile:
        csvreader = csv.reader(csvfile)
        # Skip the header
        next(csvreader)
        outputfile.write('View""{\n')

        for row in csvreader:
            # Assuming columns are in the order of electrode name, X, Y, Z
            # Adjust the indices if your CSV format is different
            if len(row) < 4:
                continue  # Skip rows that don't have enough data
            x, y, z, name = row[1], row[2], row[3], row[0]
            outputfile.write(f"SP({x}, {y}, {z}){{0}};\n")
            outputfile.write(f'T3({x}, {y}, {z}, 0){{"{name}"}};\n')

        outputfile.write(
            """};\n
myView = PostProcessing.NbViews-1;
View[myView].PointType=1;
View[myView].PointSize=6;
View[myView].LineType=1;
View[myView].LineWidth=2; """
        )


def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.splitext(input_path)[0] + ".geo"
            format_electrode_data(input_path, output_path)
            print(f"Processed {input_path} -> {output_path}")


# Example usage
directory_path = "/Users/idohaber/Desktop/Geolocations"  # Update this with the path to your directory
process_directory(directory_path)
