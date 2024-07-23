

import os
import subprocess
import argparse
import time

def run_ti_simulation(script_dir):
    # Run the TI.py script
    print("Running TI simulation...")
    ti_script_path = os.path.join(script_dir, "TI.py")
    start_time = time.time()
    subprocess.run(["simnibs_python", ti_script_path])
    end_time = time.time()
    print(f"TI simulation completed in {end_time - start_time:.2f} seconds")

def extract_gm_mesh(script_dir, input_file, output_file):
    # Run the gm_extract.py script
    print(f"Extracting GM from {input_file}...")
    gm_extract_script_path = os.path.join(script_dir, "gm_extract.py")
    cmd = ["simnibs_python", gm_extract_script_path, input_file, "--output_file", output_file]
    start_time = time.time()
    subprocess.run(cmd)
    end_time = time.time()
    print(f"GM extraction completed in {end_time - start_time:.2f} seconds")

def transform_gm_to_nifti(script_dir, gm_mesh_dir):
    # Run the mesh2nii_loop.sh script
    print("Transforming GM mesh to NIfTI in MNI space...")
    mesh2nii_script_path = os.path.join(script_dir, "mesh2nii_loop.sh")
    start_time = time.time()
    subprocess.run(["bash", mesh2nii_script_path])
    end_time = time.time()
    print(f"GM mesh to NIfTI transformation completed in {end_time - start_time:.2f} seconds")

def process_mesh_files(script_dir, whole_brain_mesh_dir):
    # Run the process_mesh_files.sh script
    print("Processing mesh files...")
    process_mesh_script_path = os.path.join(script_dir, "field-analysis", "process_mesh_files.sh")
    start_time = time.time()
    subprocess.run(["bash", process_mesh_script_path, whole_brain_mesh_dir])
    end_time = time.time()
    print(f"Mesh files processed in {end_time - start_time:.2f} seconds")

def main(m2m_path, script_dir):
    # Ensure we are using absolute paths
    m2m_path = os.path.abspath(m2m_path)
    script_dir = os.path.abspath(script_dir)
    sim_dir = os.path.join(script_dir, "Simulations")
    gm_mesh_dir = os.path.join(script_dir, "GM_mesh")
    whole_brain_mesh_dir = os.path.join(script_dir, "Whole-Brain-mesh")
    niftis_dir = os.path.join(script_dir, "niftis")

    # Ensure the mesh and niftis directories exist
    os.makedirs(gm_mesh_dir, exist_ok=True)
    os.makedirs(whole_brain_mesh_dir, exist_ok=True)
    os.makedirs(niftis_dir, exist_ok=True)

    # Run TI simulation
    run_ti_simulation(script_dir)
    
    # Extract GM from TI_vectors.msh
    for subdir in os.listdir(sim_dir):
        subdir_path = os.path.join(sim_dir, subdir)
        if os.path.isdir(subdir_path):
            ti_vectors_file = os.path.join(subdir_path, "TI_vectors.msh")
            if os.path.exists(ti_vectors_file):
                output_file = os.path.join(gm_mesh_dir, f"grey_{subdir}.msh")
                extract_gm_mesh(script_dir, ti_vectors_file, output_file)
                # Rename and move TI_vectors.msh to Whole-Brain-mesh directory
                new_name = f"{subdir}_TI_vectors.msh"
                new_path = os.path.join(whole_brain_mesh_dir, new_name)
                os.rename(ti_vectors_file, new_path)

    # Transform GM mesh to NIfTI in MNI space
    transform_gm_to_nifti(script_dir, gm_mesh_dir)
    
    # Process mesh files
    process_mesh_files(script_dir, whole_brain_mesh_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the full simulation pipeline.')
    parser.add_argument('m2m_path', type=str, help='Path to the m2m directory')
    parser.add_argument('script_dir', type=str, help='Path to the directory containing the scripts')
    args = parser.parse_args()
    main(args.m2m_path, args.script_dir)

