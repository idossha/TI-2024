#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-

"""
Based on the work of Guilherme B Saturnini 2019
Modified by Ido Haber, 2024
Project: STRENGTHEN
Center for Sleep & Consciousness, UW Madison
"""


from simnibs import run_simnibs, sim_struct

tdcs_lf = sim_struct.TDCSLEADFIELD()

# file handling
tdcs_lf.subpath = "m2m_108"  # subject directory
tdcs_lf.pathfem = "lf_test"  # output  directory
tdcs_lf.eeg_cap = "test.csv"  # eeg-cap directory


# electrode configuration
electrode = tdcs_lf.electrode
electrode.dimensions = [8, 8]  # in mm
electrode.shape = "ellipse"  # shape
electrode.thickness = [4, 2]  # argu1 = gel thickness , argu2=e thickness


"""
You can Uncoment to use the pardiso solver which is faster.
This solver is faster than the default. However, it requires much more memory (~12 GB)
However, do not use this for hd-EEG caps
"""

# tdcs_lf.solver_options = "pardiso"


run_simnibs(tdcs_lf)
