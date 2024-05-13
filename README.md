This package is designed for a **specific case** of structuring the electrode digitization output from EGI scanner to ready `good to go` files.

1. txt2csv: will give you a clean csv file with the critical data.
2. csv2geo: will take the data and format it to Gmsh language for 3D visualization.
3. txt2mat: will give you a .mat file compatible for Brainstorm co-registration.
4. auto-segment: will run through all your ppt directories and run the `charm` function from SimNIBS to segment and mesh MRIs.

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
