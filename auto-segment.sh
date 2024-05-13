#!/bin/bash

# Define the main directory path containing the sub-directories
main_directory="/Users/idohaber/Desktop/Strengthen_MRI"

# Change to the main directory
cd "$main_directory"

# Loop over each sub-directory in the main directory (which should correspond to different subjects)
for subdir in */; do
  # Strip the trailing slash from subdir name (based on how your subject directories are named)
    subdir="${subdir%/}"

    # Extract the last three characters from the directory name
    x=${subdir: -3}

    # Define the paths for y and z (drop z if you are only using T1)
    y="/Users/idohaber/Desktop/Strengthen_MRI/sub-${x}/ses-base/anat/sub-${x}_ses-base_acq-MPRAGE_T1w.nii.gz"
    z="/Users/idohaber/Desktop/Strengthen_MRI/sub-${x}/ses-base/anat/sub-${x}_ses-base_acq-CUBE_T2w.nii.gz"



    # Run the command
    charm "$x" "$y" "$z" --forceqform
done

