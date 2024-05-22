#!/usr/bin/env python3

import argparse
import csv
import glob
import os


def process_electrode_file(input_file, output_file=None):
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".csv"

    with open(input_file, "r") as file:
        lines = file.readlines()

    # Find the line where electrode data starts
    start_index = 0
    for i, line in enumerate(lines):
        if line.startswith("Fid"):
            start_index = i
            break

    # Process the electrode data
    electrode_data = []
    for line in lines[start_index:]:
        parts = line.split()
        electrode_data.append(
            ["Electrode", float(parts[1]), float(parts[2]), float(parts[3]), parts[0]]
        )

    # Write the processed data to a CSV file
    with open(output_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(electrode_data)

    print(f"Processed {input_file} successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Process electrode text file and generate CSV."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        help="Path to the input text file (optional).",
    )
    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        help="Path to the output CSV file (optional)",
    )

    parser.add_argument(
        "no arguements",
        type=str,
        nargs="?",
        help=" If not given any arguements, it will loop through all .txt files in the directory",
    )

    args = parser.parse_args()

    if args.input_file:
        process_electrode_file(args.input_file, args.output_file)
    else:
        txt_files = glob.glob("*.txt")
        for txt_file in txt_files:
            process_electrode_file(txt_file)


if __name__ == "__main__":
    main()
