#!/Users/idohaber/Applications/SimNIBS-4.1/bin/simnibs_python
# -*- coding: utf-8 -*-

"""
Ido Haber, 2024
Project: STRENGTHEN
Center for Sleep & Consciousness, UW Madison

Based on the work of Guilherme B Saturnini 2019


"""

import simnibs

# Initialize structure
opt = simnibs.opt_struct.TDCSoptimize()
# Select the leadfield file
opt.leadfield_hdf = 'lf_path/subect_eeg-net.hdf5'
# Select a name for the optimization
opt.name = 'optimization/xxx_target'

# Select a maximum total current (in A)
opt.max_total_current = 2e-3
# Select a maximum current at each electrodes (in A)
opt.max_individual_current = 1e-3
# Select a maximum number of active electrodes (optional)
opt.max_active_electrodes = 8

# Define optimization target
target = opt.add_target()
# Position of target, in subject space!
# please see tdcs_optimize_mni.py for how to use MNI coordinates
target.positions = [-50.7, 5.1, 55.5]

# radius around the target coordinates
target.radius = 2

# Intensity of the electric field (in V/m)
target.intensity = 0.2

# Run optimization
simnibs.run_simnibs(opt)positions


'''
direction

tissues


'''

