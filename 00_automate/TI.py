
import os
import time
from copy import deepcopy
import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI

# Unipolar - Make sure you run at 5mA
montages = {
#         "Anterior_Florian": [("E066", "E079"), ("E164", "E143")],
#         "MP_Anterior_P2": [("E098", "E100"), ("E129", "E152")],
#         "Dorsal_RSC": [("E079", "E110"), ("E143", "E128")],
#         "Posterior_Florian": [("E088", "E142"), ("E077", "E163")],
#         "Ventral_RSC": [("E065", "E107"), ("E182" , "E160")],
#         "Middle_RSC": [("E059", "E109"), ("E183" , "E140")],
#         "L_insula_small": [("E070", "E095"), ("E020", "E034")]
#         "Another_posterior": [("E077", "E088"), ("E163", "E142")],
#         "MP_thala_1": [("E077", "E088"), ("E163", "E142")],
#         "MP_thala_2": [("E077", "E088"), ("E163", "E142")],
         "Default_RSC": [("E049", "E116"), ("E213", "E150")]
       #"thala_1": [("E062", "E096"), ("E211", "E170")],
      #"thala_2": [("E084", "E069"), ("E179" , "E202")]
}

# Multipolar - Make sure you run at half the Unipolar intensity.
# montages = {
#         "MP_1": [("E066", "E079"), ("E164", "E143")],
#         "MP_2": [("E098", "E100"), ("E129", "E152")],
# }

# montages = {
#         "L_insula_large": [("E070", "E095"), ("E020", "E034")]
# }

# Base paths
base_subpath = "m2m_101"
main_dir = os.path.abspath(os.path.join(base_subpath, os.pardir))
base_pathfem = os.path.join(main_dir, "Simulations")
conductivity_path = "m2m_101"
tensor_file = os.path.join(conductivity_path, "DTI_coregT1_tensor.nii.gz")

# Ensure the base_pathfem directory exists
if not os.path.exists(base_pathfem):
    os.makedirs(base_pathfem)

# Function to run simulations
def run_simulation(montage_name, montage):
    S = sim_struct.SESSION()
    S.subpath = base_subpath
    S.anisotropy_type = "dir"
    S.pathfem = os.path.join(base_pathfem, f"TI_{montage_name}")
    S.eeg_cap = "m2m_101/eeg_positions/EGI_template.csv"
    S.map_to_surf = False
    S.map_to_fsavg = False
    S.map_to_vol = False
    S.map_to_mni = False
    S.open_in_gmsh = False
    S.tissues_in_niftis = "all"

    # Load the conductivity tensors
    S.dti_nii = tensor_file

    # First electrode pair
    tdcs = S.add_tdcslist()
    tdcs.anisotropy_type = 'dir'  # Set anisotropy_type to 'dir'
    tdcs.currents = [0.0025, -0.0025]
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
    tdcs_2 = S.add_tdcslist(deepcopy(tdcs))
    tdcs_2.currents = [0.0025, -0.0025]
    tdcs_2.electrode[0].centre = montage[1][0]
    tdcs_2.electrode[1].centre = montage[1][1]

    run_simnibs(S)

    last_three_digits = base_subpath[-3:]
    anisotropy_type = S.anisotropy_type

    m1_file = os.path.join(S.pathfem, f"{last_three_digits}_TDCS_1_{anisotropy_type}.msh")
    m2_file = os.path.join(S.pathfem, f"{last_three_digits}_TDCS_2_{anisotropy_type}.msh")

    m1 = mesh_io.read_msh(m1_file)
    m2 = mesh_io.read_msh(m2_file)

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

# Run the simulations
for name, montage in montages.items():
    run_simulation(name, montage)

