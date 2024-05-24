#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-
from simnibs import mesh_io

"""
Load your original mesh
Crop the mesh to only include grey matter (tag #2)
Save this grey matter mesh to a new file

This is now embedded in the `TI.py` script.
"""


full_mesh = mesh_io.read_msh("TI.msh")
gm_mesh = full_mesh.crop_mesh(tags=[2])
mesh_io.write_msh(gm_mesh, "grey_TI.msh")
