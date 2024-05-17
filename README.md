This package is designed for a **specific case** of structuring the electrode digitization output from EGI scanner to ready `good to go` files.

1. txt2csv.py: will take .txt output from Brainstorm after refinement and will put in a .csv format for SimNIBS to work with.

   - Execution from command line: python3 txt2csv.py input.txt output.csv

2. csv2geo.py: will take the data and format it to Gmsh language for 3D visualization.
3. txt2mat.py: will give you a .mat file compatible for Brainstorm co-registration.
4. auto-charm.sh: will run through all your ppt directories and run the `charm` function from SimNIBS to segment and mesh MRIs.

5. fsl-pipeline.py: take an MRI and will do the following:
   a. reorient the scan using `fslreorient2std`
   b. Extract brain using `bet` (this is still funky)
   c. Perform linear tranformation using `FLIRT`
   d. Perform non-linear tranformation using `FNIRT`
   The user needs to decide what template to register the tranformation to.

6. extract-thrsh.sh: creates a binary mask from an MRI scan.
   - Uses `fslmaths`

---

![3D hdEEG](/example_dataset/3D_hdEEG_net.png)

---

References:

#### csv2geo:

https://gmsh.info/
https://gmsh.info/doc/texinfo/gmsh.pdf

#### txt2mat:

source code of Brainstorm -> defaults -> eeg -> ICBM152

---

Feel free to modify these for your specific needs.

Ido
