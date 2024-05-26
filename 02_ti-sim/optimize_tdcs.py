#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-

"""

Based on the work of Guilherme B Saturnini 2019
Modified by Ido Haber, 2024
Project: STRENGTHEN
Center for Sleep & Consciousness, UW Madison



"""

import simnibs

# Initialize structure
opt = simnibs.opt_struct.TDCSoptimize()
# Select the leadfield file
opt.leadfield_hdf = "leadfield_directory/FEM_XXX_leadfield_net_used.hdf5"
# Select a name for the optimization
opt.name = "optimization/single_tdcs_target"

"""
Electrode parameters:
"""
# Select a maximum total current (in A)
opt.max_total_current = 5e-3
# Select a maximum current at each electrodes (in A)
opt.max_individual_current = 5e-3
# Select a maximum number of active electrodes (optional)
opt.max_active_electrodes = 2

"""
Target parameters:
"""
# Define optimization target
target_1 = opt.add_target()

target_1.positions = [-50.7, 5.1, 55.5]  # Position of target, in subject space!

# if you want to work in MNI space:
# target_1.positions = simnibs.mni2subject_coords([-37, -21, 58], "m2m_108")

target_1.intensity = 1  # Intensity of the electric field (in V/m)
target_1.direction = "normal"  # direction of the field to optimize
target_1.radius = 2  # Target radius around the specified coordinate

# avoid = opt.add_target()
# Choose targets to avoid. like 6 (eyes)
# avoid.tissues = None

# Run optimization
simnibs.run_simnibs(opt)
