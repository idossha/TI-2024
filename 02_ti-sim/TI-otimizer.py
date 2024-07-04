# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:41:21 2022 by axthi

Modified by Ido Haber May 2024


This script runs all combinations of electrodes given in the lists.

Formula: (E+ electrodes * E- electrodes ) ^2
"""

import copy
import numpy as np
from simnibs import mesh_io
from simnibs.utils import TI_utils as TI
from itertools import product

# Function to generate all combinations
def generate_combinations(E1_plus, E1_minus, E2_plus, E2_minus):
    combinations = []
    for e1p, e1m in product(E1_plus, E1_minus):
        for e2p, e2m in product(E2_plus, E2_minus):
            combinations.append(((e1p, e1m), (e2p, e2m)))
    return combinations

# Example lists
E1_plus = ['E001', 'E002']
E1_minus = ['E003', 'E004']
E2_plus = ['E005', 'E006']
E2_minus = ['E007', 'E008']

# Generate all combinations
all_combinations = generate_combinations(E1_plus, E1_minus, E2_plus, E2_minus)

# load lead field
leadfield_hdf = "lf_normal/108_leadfield_test.hdf5"
leadfield, mesh, idx_lf = TI.load_leadfield(leadfield_hdf)

# Process each combination
for combo in all_combinations:
    (E1_pair, E2_pair) = combo
    TIpair1 = [E1_pair[0], E1_pair[1], 0.005]
    TIpair2 = [E2_pair[0], E2_pair[1], 0.005]

    # Get fields for the two pairs
    ef1 = TI.get_field(TIpair1, leadfield, idx_lf)
    ef2 = TI.get_field(TIpair2, leadfield, idx_lf)

    # Add to mesh for later visualization
    mout = copy.deepcopy(mesh)
    hlpvar = mesh_io.NodeData(ef1, mesh=mout)
    mout.add_node_field(hlpvar.norm(), f"E_magn1_{E1_pair[0]}_{E1_pair[1]}")
    hlpvar = mesh_io.NodeData(ef2, mesh=mout)
    mout.add_node_field(hlpvar.norm(), f"E_magn2_{E2_pair[0]}_{E2_pair[1]}")

    # Option 1: get maximal TI amplitude
    TImax = TI.get_maxTI(ef1, ef2)
    mout.add_node_field(TImax, f"TImax_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}")  # for visualization

    # Option 2: get TI amplitudes along x, y and z
    TIamp = TI.get_dirTI(ef1, ef2, [1, 0, 0])
    mout.add_node_field(TIamp, f"TIamp_x_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}")  # for visualization

    TIamp = TI.get_dirTI(ef1, ef2, [0, 1, 0])
    mout.add_node_field(TIamp, f"TIamp_y_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}")  # for visualization

    TIamp = TI.get_dirTI(ef1, ef2, [0, 0, 1])
    mout.add_node_field(TIamp, f"TIamp_z_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}")  # for visualization

    # Option 3: get TI amplitudes along local normal orientation
    surf_normals = mesh.nodes_normals().value
    TIamp = TI.get_dirTI(ef1, ef2, surf_normals)
    mout.add_node_field(TIamp, f"TIamp_localnorm_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}")  # for visualization

    # Write mesh to file
    mesh_filename = f"TI_via_leadfields_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}.msh"
    mesh_io.write_msh(mout, mesh_filename)
    v = mout.view(
        visible_tags=[1, 2, 1006],
        visible_fields=f"TImax_{E1_pair[0]}_{E1_pair[1]}_{E2_pair[0]}_{E2_pair[1]}"
    )
    v.write_opt(mesh_filename)
    mesh_io.open_in_gmsh(mesh_filename, True)

# Print total number of combinations
print(f'Total number of combinations: {len(all_combinations)}')
