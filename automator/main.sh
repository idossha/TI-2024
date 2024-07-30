
#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Gather arguments from the prompter script
subject_id=$1
conductivity=$2
shift 2
selected_montages=("$@")

# Set the script directory to the present working directory
script_dir="$(pwd)"

# Set subdirectory paths
sim_dir="$script_dir/Simulations"
gm_mesh_dir="$script_dir/GM_mesh"
whole_brain_mesh_dir="$script_dir/Whole-Brain-mesh"
nifti_dir="$script_dir/niftis"
output_dir="$script_dir/ROI_analysis"
screenshots_dir="$script_dir/screenshots"

# Ensure directories exist
mkdir -p "$gm_mesh_dir" "$whole_brain_mesh_dir" "$nifti_dir" "$output_dir" "$screenshots_dir"

# Main script: Run TI.py with the selected parameters
simnibs_python TI.py "$subject_id" "$conductivity" "${selected_montages[@]}"

# Function to extract GM mesh
extract_gm_mesh() {
    local input_file="$1"
    local output_file="$2"
    echo "Extracting GM from $input_file..."
    gm_extract_script_path="$script_dir/gm_extract.py"
    simnibs_python "$gm_extract_script_path" "$input_file" --output_file "$output_file"
    echo "GM extraction completed"
}

# Function to transform GM mesh to NIfTI
transform_gm_to_nifti() {
    echo "Transforming GM mesh to NIfTI in MNI space..."
    mesh2nii_script_path="$script_dir/mesh2nii_loop.sh"
    bash "$mesh2nii_script_path" "$subject_id"
    echo "GM mesh to NIfTI transformation completed"
}

# Function to process mesh files
process_mesh_files() {
    echo "Processing mesh files..."
    process_mesh_script_path="$script_dir/field-analysis/process_mesh_files.sh"
    bash "$process_mesh_script_path" "$whole_brain_mesh_dir"
    echo "Mesh files processed"
}

# Function to run sphere analysis
run_sphere_analysis() {
    echo "Running sphere analysis..."
    sphere_analysis_script_path="$script_dir/sphere-analysis.sh"
    bash "$sphere_analysis_script_path" "$nifti_dir" "$output_dir"
    echo "Sphere analysis completed"
}

# Function to generate screenshots
generate_screenshots() {
    local input_dir="$1"
    local output_dir="$2"
    echo "Generating screenshots..."
    screenshot_script_path="$script_dir/screenshot.sh"
    bash "$screenshot_script_path" "$input_dir" "$output_dir"
    echo "Screenshots generated"
}

# Extract GM from TI_vectors.msh
for subdir in "$sim_dir"/*/; do
    mesh_file="$subdir/TI.msh"
    if [ -e "$mesh_file" ]; then
        subdir_name=$(basename "$subdir")
        output_file="$gm_mesh_dir/grey_${subdir_name}.msh"
        extract_gm_mesh "$mesh_file" "$output_file"
        new_name="${subdir_name}_TI.msh"
        new_path="$whole_brain_mesh_dir/$new_name"
        mv "$mesh_file" "$new_path"
    fi
done

transform_gm_to_nifti
process_mesh_files
run_sphere_analysis
generate_screenshots "$nifti_dir" "$screenshots_dir"

echo "All tasks completed successfully for subject ID: $subject_id"
