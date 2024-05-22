Author: Ido Haber
Date: May 2024
Project: STRENGTHEN/TI_vs_Source_Reconstruction

---

### Step from getting structural Raw data to produce TI simulation output

This will desribe the conceptual and mannual steps to get from MRI data to simulation output, but feel free to reference [[https://github.com/idossha/TI-2024]] for script that will potentially make your life much easier.

---

Requirements: SimNIBS, FSL, Brainstorm, MATLAB, Python

- if you recieve DICOM files, make sure you tranform them to .nii files. See [[https://github.com/rordenlab/dcm2niix]] for that.

- Use Charm function to segment the scan:  
  Commnad: charm /path/T1 {path/T2}  
  you might need to force `forceqform` or storm to complete this process  
  First arguement is necessary, second is optional.  
  See `auto-charm.sh` for group preprocessing.

open the `report.html` file and inspect the segmentation of the tissues. If you use T2 scans, most likely you are g2g.

- Open a subject tab in Brainstorm
- Load the T1 MRI scan (original)
- Manually set fiducials based on MRI scan (you can create a surface to help you do this step)
- Generate head surface (okay to use suggested parameters)
- Load digitized net (in your preferred file format) or template. If digitized, you will need to figure out the correct file formatting, see `txt2mat.py`
- Depending on how to initial registration come to be you might need to do manual manipulation

If it is relatively close, do:

1. Automatic refine registration (preferably use 1, and save the output statistics)
2. Project electrodes on surface
3. Make sure you save changes
4. Export txt file and transform to simnibs file using `txt2csv.py`
5. Put new coordinates in the eeg-positions subdirectory in the subject directory
6. You might have to change the file `EEG10-10_UI_Jurak_2007.csv`. If you are running into problems, create a copy of that file, and take the data from you .csv file and paste it in a file named `EEG10-10_UI_Jurak_2007.csv` it will come in handy.

- Visually inspect SimNIBS GUI co-registration
- run TI.py simulation
- visualize results in Gmsh

- Run `msh2nii` (be in the results directory)

  - command should be: msh2nii TI.msh /path/T1.nii.gz TI

- Run `subject2mni` (be in the results directory)

  - comnand should be: subject2mni -I TI.msh -m /path/m2m_103 -o name

- ## Get locality and intensity statistics (done in Matlab)

  I will add this later on.

- Create TI Mask based on a specific threshold on the TI_MNI.nii outputs
  Commnad: fsl maths /path/file -thr X -bin output_name. or use `extract-thrsh.sh`

---

To do:

figure out how to use other .csv files for leadfields and TI stuff instead of hacking the name for the .csv
