import os

"""
This script should be the first step from in the process of source localization.

It takes the txt file containing the digitazation of electrodes from EGI, parse the data, 
and outputs it into a .csv file. 

the second step is to run csv2geo.py .

Created: April 01, 2024

- Ido

"""


def process_electrode_file(input_filepath):
    # Generate an output filepath by changing the extension to .csv
    output_filepath = os.path.splitext(input_filepath)[0] + ".csv"

    with open(input_filepath, "r") as infile, open(output_filepath, "w") as outfile:
        # Write the CSV header
        outfile.write("electrode name,x,y,z\n")

        # Skip the first five lines (header)
        for _ in range(5):
            next(infile)

        # Process each line of the actual data
        for line in infile:
            parts = line.strip().split()
            if len(parts) == 5:  # Ensure the line has the correct number of parts
                electrode_name, x, y, z, _ = parts
                outfile.write(f"{electrode_name},{x},{y},{z}\n")

    print(f"Processed {input_filepath} -> {output_filepath}")


def process_directory(directory_path):
    # List all files in the given directory
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            # You can add additional checks here to process only specific file types
            process_electrode_file(filepath)


# Update 'path_to_directory' with the path to the directory containing your files
path_to_directory = "/Users/idohaber/Desktop/Geolocations"
process_directory(path_to_directory)
