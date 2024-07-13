#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-
import argparse
from simnibs import mesh_io

def main(input_file):
    """
    Load the original mesh
    Crop the mesh to only include grey matter (tag #2)
    Save this grey matter mesh to a new file
    """
    full_mesh = mesh_io.read_msh(input_file)
    gm_mesh = full_mesh.crop_mesh(tags=[2])
    output_file = "grey_" + input_file
    mesh_io.write_msh(gm_mesh, output_file)
    print(f"Grey matter mesh saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a mesh file.')
    parser.add_argument('input_file', type=str, help='Path to the input mesh file')
    args = parser.parse_args()
    main(args.input_file)
