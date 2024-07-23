#!/bin/bash

# Set the directory containing NIfTI files
nifti_dir="/Volumes/CSC-Ido/analysis/"

# Check if FSLDIR is set
if [ -z "$FSLDIR" ]; then
    echo "FSLDIR is not set. Please set the FSLDIR environment variable."
    exit 1
fi

# Ensure nifti_dir is not empty
if [ -z "$(ls $nifti_dir/*.nii.gz 2> /dev/null)" ]; then
    echo "No NIfTI files found in the designated directory: $nifti_dir"
    exit 1
fi

# Preliminary steps and registrations
echo "Starting preliminary steps and registrations..."
for subj in $nifti_dir/*.nii.gz; do
    echo "Processing $subj..."

    # Reorientation to standard
    fslreorient2std $subj ${subj%%.*}_reoriented.nii.gz

    # Brain extraction
    # This step is tricky, you might have to tweak it mannually for each ppt. 
    bet ${subj%%.*}_reoriented.nii.gz ${subj%%.*}_brain -f 0.3 -g -0.1

    # Bias field correction
    fast -B -t 1 -n 3 -H 0.1 -I 4 -l 20.0 ${subj%%.*}_brain.nii.gz

    # FLIRT registration to 2mm MNI template
    # Can potentially use 1mm MNI template for publication.
    flirt -in ${subj%%.*}_brain.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz \
          -out ${subj%%.*}_to_MNI2mm_linear \
          -omat ${subj%%.*}_to_MNI2mm_linear.mat \
          -cost corratio -dof 12 -interp trilinear
    if [ $? -ne 0 ]; then
        echo "FLIRT failed for ${subj%%.*}_brain.nii.gz. Exiting."
        exit 1
    fi

    # FNIRT registration to 2mm MNI template
    # same here. Just make sure it is the same atlas as above.
    fnirt --in=${subj%%.*}_brain.nii.gz --aff=${subj%%.*}_to_MNI2mm_linear.mat \
          --cout=${subj%%.*}_to_MNI2mm_nonlinear_warp \
          --config=$FSLDIR/etc/flirtsch/T1_2_MNI152_2mm.cnf \
          --ref=$FSLDIR/data/standard/MNI152_T1_2mm.nii.gz \
          --iout=${subj%%.*}_to_MNI2mm_nonlinear
    if [ $? -ne 0 ]; then
        echo "FNIRT failed for ${subj%%.*}_brain.nii.gz. Exiting."
        exit 1
    fi
done

echo "All registrations completed successfully."


# the output of interest is: ${subj%%.*}_to_MNI2mm_nonlinear.nii.gz
# to visualize all at once: run 
#   `fsleyes $(ls *.nii.gz)`
