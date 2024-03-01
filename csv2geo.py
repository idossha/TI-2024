'''
Script that takes a .csv file with with any number of EEG coordinates and trasforms it to a 3D .geo file 
For meashing with individualized models.
By Ido Haber March 1, 2024
'''

# You have to make sure that the CODEC is UTF-8 otherwise it will fail.
# If in doubt - open your file and Safe it as ".csv".
import csv
def format_electrode_data(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as csvfile, open(output_path, "w") as outputfile:
        csvreader = csv.reader(csvfile)
        outputfile.write('View""{\n')

        for row in csvreader:
            # Assuming columns are in the order of ID, X, Y, Z, Name
            # Adjust the indices according to your CSV file
            x, y, z, name = row[1], row[2], row[3], row[4]
            outputfile.write(f"SP({x}, {y}, {z}){{0}};\n")
            outputfile.write(f'T3({x}, {y}, {z}, 0){{"{name}"}};')

        # Append the provided block at the end
        outputfile.write("};\n")
        outputfile.write("\nmyView = PostProcessing.NbViews-1;\n")
        outputfile.write("View[myView].PointType=1;\n")
        outputfile.write("View[myView].PointSize=6;\n")
        outputfile.write("View[myView].LineType=1;\n")
        outputfile.write("View[myView].LineWidth=2;\n")



input_path = "/Users/idohaber/Desktop/conversion/EGI_256.csv"
output_path = "/Users/idohaber/Desktop/conversion/EGI_256.geo"

# Replace 'your_input.csv' and 'your_output.txt' with your actual file paths
format_electrode_data(input_path , output_path)