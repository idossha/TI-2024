""" Example of a SimNIBS tDCS leadfield in Python
    Run with:simnibs_python leadfield.py
    Copyright (C) 2019 Guilherme B Saturnino
"""

from simnibs import run_simnibs, sim_struct

tdcs_lf = sim_struct.TDCSLEADFIELD()
# subject folder
tdcs_lf.subpath = "/Path_to_subject/m2m_xxx/"
# output directory
tdcs_lf.pathfem = "/Path/FEM_xxx/ld_matrix"

# specific .csv file after refinement for each subject. This needs to sit in:
# m2m_xxx/eeg_positions/file_name.csv
tdcs_lf.eeg_cap = "xxx.csv"

"""
You can Uncoment to use the pardiso solver which is faster.
This solver is faster than the default. However, it requires much more memory (~12 GB)
However, do not use this for hd-EEG caps
"""

# tdcs_lf.solver_options = "pardiso"


run_simnibs(tdcs_lf)
