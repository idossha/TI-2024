import os
import sys
import time
from copy import deepcopy

import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI

def run_simulation(subpath, pathfem, TI_1, TI_2):
    start_time = time.time()

    S = sim_struct.SESSION()
    S.subpath = subpath
    S.pathfem = pathfem

    m1 = mesh_io.read_msh(TI_1)
    m2 = mesh_io.read_msh(TI_2)

    # calculate the maximal amplitude of the TI envelope
    ef1 = m1.field["TI_1_vectors"]
    ef2 = m2.field["TI_2_vectors"]

    # Use the get_maxTI function
    TI_MultiPolar, TI_MultiPolar_vectors = TI.get_maxTI(ef1.value, ef2.value)

    # make a new mesh for visualization of the field strengths
    # and the amplitude of the TI envelope
    mout = deepcopy(m1)
    mout.elmdata = []

    mout.add_element_field(TI_MultiPolar, "TI_Max")
    mout.add_element_field(TI_MultiPolar_vectors, "TI_MP_vectors")

    output_mesh_path = os.path.join(pathfem, "TI_BiPolar.msh")
    mesh_io.write_msh(mout, output_mesh_path)
    v = mout.view(visible_tags=[1002, 1006], visible_fields="TI_Max")
    v.write_opt(output_mesh_path)
    mesh_io.open_in_gmsh(output_mesh_path, True)

    end_time = time.time()
    total_time = end_time - start_time
    print("Total time: " + str(total_time) + " seconds")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Bipolar TI.')
    parser.add_argument('-sp', required=True, help='Path to the subject folder (m2m_XXX)')
    parser.add_argument('-pf', default=os.getcwd(), help='Directory for the simulation output (default: current working directory)')
    parser.add_argument('-M1', required=True, help='Path to the first TI mesh file (TI_1.msh)')
    parser.add_argument('-M2', required=True, help='Path to the second TI mesh file (TI_2.msh)')

    args = parser.parse_args()

    run_simulation(args.subpath, args.pathfem, args.TI_1, args.TI_2)

if __name__ == "__main__":
    main()
