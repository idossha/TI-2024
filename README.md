A repo containing the scripts used for this project.

Ido Haber, 2024, STRENGTHEN Project

---

[pipe_me.png]

---

#### Dependencies:

SimNIBS, FSL, Brainstorm, MATLAB, Jupyter

Brainstorm sits on top of MATLAB  
SimNIBS & FSL can be downloaded from their respective websites.

To create the conda env for simnibs: `conda env create -f sn_env.yml`  
To create the conda env for YASA: `conda env create -f yasa_env.yml `

---

### Scripts:

1. **txt2csv.py:** will take .txt output from Brainstorm/EGI system and will put in a .csv format for SimNIBS to work with.
2. **csv2geo.py:** will take the data and format it to Gmsh language for 3D visualization.
3. **txt2mat.py:** will give you a .mat file compatible for Brainstorm co-registration.
4. **auto-charm.sh:** will run through all your ppt directories and run the `charm` function from SimNIBS to segment and mesh MRIs.

5. **fsl-pipeline.py:** take an MRI and will do the following:

   - a. reorient the scan using `fslreorient2std`
   - b. Extract brain using `bet` (this is still funky)
   - c. Perform linear tranformation using `FLIRT`
   - d. Perform non-linear tranformation using `FNIRT`
     The user needs to decide what template to register the tranformation to.

6. **extract-thrsh.sh:** creates a binary mask from an MRI scan.

   - Uses `fslmaths`

7. **leadfield.py** calculates the forward model for optimization / faster TI testing.

8. **TI.py** calculates TI field based on the paper from Grossman et al 2017.

9. **gm_extract.py** creates a seperated mesh for TI field in the cortex.

10. **norm_TI.py** ... coming soon

11. **SW_detect.ipynb** EEG processing.

---

### Want to make your life easier?

Make your scripts executable from anywhere by:

1. Add the Script Directory to Your PATH:
   The PATH environment variable tells the shell which directories to search for executable files in response to commands issued by a user. You can add your script’s directory to this variable.
   • Find the full path to where your scripts are located. For example, if it’s in /home/username/scripts, you would use this path.
   • Edit your shell profile file (like .bashrc or .bash_profile for Bash shell, .zshrc for Zsh) located in your home directory. Add the following line at the end of the file:

`export PATH=$PATH:/home/username/scripts`

Source your profile file to apply the changes immediately without needing to logout or restart your terminal: `source ~/.bashrc`

**for Python scripts:**

Ensure your Python script starts with a shebang line pointing to the Python interpreter: `#!/usr/bin/env python3`

Make the script executable: `chmod +x /path/to/your/script.py`

Then follow the steps above.

---

To make your life even easier, create symlinks for all your scripts to a single directory like `/usr/local/bin/` and just add that to your path.

---

### References:

#### csv2geo:

https://gmsh.info/
https://gmsh.info/doc/texinfo/gmsh.pdf

#### txt2mat:

source code of Brainstorm -> defaults -> eeg -> ICBM152

#### SimNIBS Documentation

[https://simnibs.github.io/simnibs/build/html/index.html]

#### YASA Documentation

[https://github.com/raphaelvallat/yasa]

#### FSL

[https://fsl.fmrib.ox.ac.uk/fsl/fslwiki]

---

Feel free to modify these for your specific needs.

Ido
