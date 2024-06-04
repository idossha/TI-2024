import os
import time
from copy import deepcopy

import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI


start_time = time.time()

S = sim_struct.SESSION()
S.subpath = "/Path_to/m2m_XXX/"     # folder of the subject
S.pathfem = "/Path_to/output_dir/"  # Directory for the simulation output

m1 = mesh_io.read_msh(os.path.join(S.pathfem, "TI_1.msh"))
m2 = mesh_io.read_msh(os.path.join(S.pathfem, "TI_2.msh"))

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

mesh_io.write_msh(mout, os.path.join(S.pathfem, "TI_MultiPolar.msh"))
v = mout.view(visible_tags=[1002, 1006], visible_fields="TI_Max")
v.write_opt(os.path.join(S.pathfem, "TI_MultiPolar.msh"))
mesh_io.open_in_gmsh(os.path.join(S.pathfem, "TI_MultiPolar.msh"), True)

end_time = time.time()
total_time = end_time - start_time
print("Total time: " + str(total_time) + " seconds")
