#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-

"""
 script that runs two simnibs tDCS simulations
 and calculates the TI envelope based on the suggested equation by Grossman et al 2017.
 
 Created on Thu Jun 23 17:41:21 2022 @author: axthi
 Modified in Feb 2024 by idohaber

Last update: May 21st, Ido Haber for STRENGTHEN Study

"""

import os
import time
from copy import deepcopy

import numpy as np
from simnibs import mesh_io, run_simnibs, sim_struct
from simnibs.utils import TI_utils as TI

start_time = time.time()

S = sim_struct.SESSION()
S.subpath = "/Users/idohaber/Desktop/Melanie/m2m_MB"  # folder of the subject
S.pathfem = "/Users/idohaber/Desktop/Melanie/thalamus/TI_B"  # Directory for the simulation output
S.eeg_cap = "m2m_MB/eeg_positions/MB_EGI.csv"  # eeg-cap directory
# Set the mapping to surface, fsaverage space, nifti volume, and MNI space
S.map_to_surf = False  # This will interpolate to cortical surface
S.map_to_fsavg = False# This will transform to fsaverage space
S.map_to_vol = False # This will interpolate to a nifti volume
S.map_to_mni = False  # This will transform to MNI space
S.open_in_gmsh = False

# Specify the tissues for nifti volume interpolation
S.tissues_in_niftis = (
    "all"  # This will interpolate all tissues; you can specify tissue indices if needed
)


# specify first electrode pair
tdcs = S.add_tdcslist()
tdcs.currents = [0.005, -0.005]
electrode = tdcs.add_electrode()
electrode.channelnr = 1
electrode.centre = "E029"
electrode.shape = "ellipse"
electrode.dimensions = [8, 8]
electrode.thickness = [4, 4]

electrode = tdcs.add_electrode()
electrode.channelnr = 2
electrode.centre = "E116"
electrode.shape = "ellipse"
electrode.dimensions = [8, 8]
electrode.thickness = [4, 4]

# specify second electrode pair
tdcs = S.add_tdcslist(deepcopy(tdcs))
tdcs.electrode[0].centre = "E005"
tdcs.electrode[1].centre = "E150"

run_simnibs(S)


"""
    generate the TI field from the simulation results
"""


m1 = mesh_io.read_msh(os.path.join(S.pathfem, "MB_TDCS_1_scalar.msh"))
m2 = mesh_io.read_msh(os.path.join(S.pathfem, "MB_TDCS_2_scalar.msh"))

# remove all tetrahedra and triangles belonging to the electrodes so that
# the two meshes have the same number of elements, keep all else.
tags_keep = np.hstack((np.arange(1, 100), np.arange(1001, 1100)))
m1 = m1.crop_mesh(tags=tags_keep)
m2 = m2.crop_mesh(tags=tags_keep)

# calculate the maximal amplitude of the TI envelope and vectors
ef1 = m1.field["E"]
ef2 = m2.field["E"]
TImax, TImax_vectors = TI.get_maxTI(ef1.value, ef2.value)

# make a new mesh for visualization of the field strengths
# and the amplitude of the TI envelope
mout = deepcopy(m1)
mout.elmdata = []

# add TImax and TImax_vectors to the mesh
mout.add_element_field(TImax, "TI_max")
mout.add_element_field(TImax_vectors, "TI_vectors")
mesh_io.write_msh(mout, os.path.join(S.pathfem, "TI_vectors.msh"))

# Visualize the results
v = mout.view(visible_tags=[1002, 1006], visible_fields=["TI_max", "TI_vectors"])
v.write_opt(os.path.join(S.pathfem, "TI_vectors.msh"))
mesh_io.open_in_gmsh(os.path.join(S.pathfem, "TI_vectors.msh"), True)

# Crop mout to only include grey matter (tag #2)
# gm_mesh = mout.crop_mesh(tags=[2])

# save this grey matter mesh to a new file
# mesh_io.write_msh(gm_mesh, os.path.join(S.pathfem, "GM_TI.msh"))


end_time = time.time()
total_time = end_time - start_time
print("Total time: " + str(total_time) + " seconds")
