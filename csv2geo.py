import argparse
import csv
import os


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


def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV files to GEO format for SimNIBS."
    )
    parser.add_argument(
        "directory", type=str, help="Directory containing the CSV files"
    )

    args = parser.parse_args()

    if os.path.isdir(args.directory):
        process_directory(args.directory)
    else:
        print("The provided directory does not exist or is not a directory.")


# python csv_to_geo.py path_to_your_directory
if __name__ == "__main__":
    main()
