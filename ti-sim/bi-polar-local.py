import os
import sys
import time
from copy import deepcopy

import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI


# Base paths
subpath = "m2m_101"
pathfem = "test"
conductivity_path = "/m2m_101/"
tensor_file = os.path.join(conductivity_path, "DTI_coregT1_tensor.nii.gz")


S = sim_struct.SESSION()
S.subpath = subpath
S.pathfem = pathfem

m1 = mesh_io.read_msh("TI_1.msh")
m2 = mesh_io.read_msh("TI_2.msh")

# calculate the maximal amplitude of the TI envelope
ef1 = m1.field["TI_vectors"]
ef2 = m2.field["TI_vectors"]

# Use the get_maxTI function
TI_MultiPolar = TI.get_maxTI(ef1.value, ef2.value)

# make a new mesh for visualization of the field strengths
# and the amplitude of the TI envelope
mout = deepcopy(m1)
mout.elmdata = []

mout.add_element_field(TI_MultiPolar, "MP_TI_Max")

output_mesh_path = os.path.join(pathfem, "TI_BiPolar.msh")
mesh_io.write_msh(mout, output_mesh_path)

