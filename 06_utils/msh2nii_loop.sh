#!/bin/bash

# Define the directory containing .msh files
MESH_DIR="mesh_2"
# Define the path to the reference nifti file
FN_REFERENCE="m2m_101"
# Define the output directory
OUTPUT_DIR="niftis"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .msh files in the directory
for FN_MESH in "$MESH_DIR"/*.msh; do
  # Check if any .msh files are found
  if [ ! -f "$FN_MESH" ]; then
    echo "Error: No .msh files found in $MESH_DIR."
    exit 1
  fi
  
  # Get the base name of the .msh file (without directory and extension)
  BASE_NAME=$(basename "$FN_MESH" .msh)
  
  # Define the output file name
  FN_OUT="$OUTPUT_DIR/${BASE_NAME}_output.nii"
  
  # Run the msh2nii command or subject2mni
  subject2mni -i "$FN_MESH" -m "$FN_REFERENCE" -o "$FN_OUT"
  #msh2nii  "$FN_MESH" "$FN_REFERENCE" "$FN_OUT"
 
done

echo "Processing complete!"
