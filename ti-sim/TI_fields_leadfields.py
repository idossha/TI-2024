# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:41:21 2022

@author: axthi
"""

import copy
import os

import numpy as numpy
from simnibs import mesh_io, sim_struct
from simnibs.utils import TI_utils as TI

tdcs_lf = sim_struct.TDCSLEADFIELD()
S = sim_struct.SESSION()
# subject folder

"""

tdcs_lf.subpath = "/Volumes/CSC-Ido/Piloting/DARPA_Present/m2m_108/"
# output directory
tdcs_lf.pathfem = "/Volumes/CSC-Ido/Piloting/DARPA_Present/leadfield_int_gm"

run_simnibs(tdcs_lf)


"""

# load lead field
leadfield_hdf = "lf_normal/108_leadfield_test.hdf5"
leadfield, mesh, idx_lf = TI.load_leadfield(leadfield_hdf)


# specify two electrode pairs with current intensities
TIpair1 = ["E096", "E076", 0.005]
TIpair2 = ["E211", "E222", 0.005]

# get fields for the two pairs
ef1 = TI.get_field(TIpair1, leadfield, idx_lf)
ef2 = TI.get_field(TIpair2, leadfield, idx_lf)

# add to mesh for later visualization
mout = copy.deepcopy(mesh)
hlpvar = mesh_io.NodeData(ef1, mesh=mout)
mout.add_node_field(hlpvar.norm(), "E_magn1")
hlpvar = mesh_io.NodeData(ef2, mesh=mout)
mout.add_node_field(hlpvar.norm(), "E_magn2")


# Option 1: get maximal TI amplitude
#TImax = TI.get_maxTI(ef1, ef2)
#mout.add_node_field(TImax, "TImax")  # for visualization
#mout.elmdata = []

# Option 2: get TI amplitudes along x, y and z
TIamp = TI.get_dirTI(ef1, ef2, [1, 0, 0])
mout.add_node_field(TIamp, "TIamp_x")  # for visualization

TIamp = TI.get_dirTI(ef1, ef2, [0, 1, 0])
mout.add_node_field(TIamp, "TIamp_y")  # for visualization

TIamp = TI.get_dirTI(ef1, ef2, [0, 0, 1])
mout.add_node_field(TIamp, "TIamp_z")  # for visualization


# Option 3: get TI amplitudes along local normal orientation
surf_normals = mesh.nodes_normals().value
TIamp = TI.get_dirTI(ef1, ef2, surf_normals)
mout.add_node_field(TIamp, "TIamp_localnorm")  # for visualization


mesh_io.write_msh(mout, "thala.msh")
v = mout.view(
    visible_tags=[1, 2, 1006],
    visible_fields="TImax",
)
v.write_opt("thala.msh")

"""
mout.add_element_field(TImax, "TImax")

# Crop mout to only include grey matter (tag #2)
gm_mesh = mout.crop_mesh(tags=[2])

# save this grey matter mesh to a new file
mesh_io.write_msh(gm_mesh, os.path.join(S.pathfem, "GM_TI.msh"))



"""
mesh_io.open_in_gmsh("thala.msh", True)
