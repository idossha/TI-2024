
import os
import time
from copy import deepcopy
import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI


# Dictionary of montages, where each montage contains two electrode pairs
montages = {
    "1": [("E079", "E143"), ("E066", "E164")],
    "2": [("E077", "E088"), ("E163", "E142")],
    "3": [("E024", "E044"), ("E207" , "E185")],
    "4": [("E064", "E079") , ("E194" , "E066")],
    "5": [("E068" , "E143") , ("E202" , "E164")]
    "6": [("E139" , "E149") , ("E138" , "E160")]
}

# Base paths
base_subpath = "/Path/m2m_XXX"
base_pathfem = "/Path/Output"

# Function to run simulations
def run_simulation(montage_name, montage):
    S = sim_struct.SESSION()
    S.subpath = base_subpath
    S.pathfem = os.path.join(base_pathfem, f"TI_{montage_name}")
    S.eeg_cap = "m2m_XXX/eeg_positions/XXX_EGI.csv"
    S.map_to_surf = False
    S.map_to_fsavg = False
    S.map_to_vol = False
    S.map_to_mni = False
    S.open_in_gmsh = False
    S.tissues_in_niftis = "all"
    
    # First electrode pair
    tdcs = S.add_tdcslist()
    tdcs.currents = [0.005, -0.005]
    electrode = tdcs.add_electrode()
    electrode.channelnr = 1
    electrode.centre = montage[0][0]
    electrode.shape = "ellipse"
    electrode.dimensions = [8, 8]
    electrode.thickness = [4, 4]

    electrode = tdcs.add_electrode()
    electrode.channelnr = 2
    electrode.centre = montage[0][1]
    electrode.shape = "ellipse"
    electrode.dimensions = [8, 8]
    electrode.thickness = [4, 4]

    # Second electrode pair
    tdcs = S.add_tdcslist(deepcopy(tdcs))
    tdcs.electrode[0].centre = montage[1][0]
    tdcs.electrode[1].centre = montage[1][1]

    run_simnibs(S)

    m1 = mesh_io.read_msh(os.path.join(S.pathfem, "XXX_TDCS_1_scalar.msh"))
    m2 = mesh_io.read_msh(os.path.join(S.pathfem, "XXX_TDCS_2_scalar.msh"))

    tags_keep = np.hstack((np.arange(1, 100), np.arange(1001, 1100)))
    m1 = m1.crop_mesh(tags=tags_keep)
    m2 = m2.crop_mesh(tags=tags_keep)

    ef1 = m1.field["E"]
    ef2 = m2.field["E"]
    TImax = TI.get_maxTI(ef1.value, ef2.value)
    TImax_vectors = TI.get_TImax_vectors(ef1.value, ef2.value)

    mout = deepcopy(m1)
    mout.elmdata = []
    mout.add_element_field(TImax, "TI_max")
    mout.add_element_field(TImax_vectors, "TI_vectors")
    mesh_io.write_msh(mout, os.path.join(S.pathfem, "TI_vectors.msh"))

    v = mout.view(visible_tags=[1002, 1006], visible_fields=["TI_max", "TI_vectors"])
    v.write_opt(os.path.join(S.pathfem, "TI_vectors.msh"))
    mesh_io.open_in_gmsh(os.path.join(S.pathfem, "TI_vectors.msh"), True)

# Run the simulations
for name, montage in montages.items():
    run_simulation(name, montage)
