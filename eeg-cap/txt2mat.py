#!/usr/bin/env python3

import os
import sys

import numpy as np
import scipy.io as sio


def create_mat_from_txt(input_text, output_path):
    # Parse the text data
    lines = input_text.strip().split("\n")

    # Temporary list to collect channel data
    temp_channels = []

    # Dictionaries to hold fiducial data
    fiducials = {}

    # Iterate over each line to parse the data
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            # Skip comments and empty lines
            continue

        parts = line.split()
        if len(parts) != 5:
            # Skip lines that do not have exactly five parts
            continue

        name = parts[0]
        x = float(parts[1])
        y = float(parts[2])
        z = float(parts[3])
        weight = int(parts[4])

        if name.startswith("Fid"):
            fiducials[name] = np.array([x, y, z], dtype=np.float32)
        else:
            # Assuming electrode names start with 'E'
            temp_channels.append(
                (
                    np.array([x, y, z], dtype=np.float32),
                    weight,
                    "EEG",
                    f"E{int(name[1:]):03d}",
                )
            )

    # Convert list of tuples to a structured array
    dtype = [
        ("Loc", np.float32, (3,)),
        ("weight", np.int32),
        ("type", "U3"),
        ("name", "U10"),
    ]
    channels = np.array(temp_channels, dtype=dtype)

    # Struct for the system and fiducials
    SCS = {
        "system": "CTF",
        "nas": fiducials["FidNz"],
        "lpa": fiducials["FidT9"],
        "rpa": fiducials["FidT10"],
    }

    # Identity matrix for transformation
    TransfEeg = np.identity(4, dtype=np.float32)

    # Create the output structure
    mat_data = {
        "Channel": channels,
        "SCS": SCS,
        "TransfEeg": TransfEeg,
    }

    # Save to .mat file
    sio.savemat(output_path, mat_data, do_compression=True)


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.startswith("Strength") and filename.endswith(".txt"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.splitext(input_path)[0] + ".mat"

            with open(input_path, "r") as file:
                input_text = file.read()

            create_mat_from_txt(input_text, output_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory>")
    else:
        process_directory(sys.argv[1])
