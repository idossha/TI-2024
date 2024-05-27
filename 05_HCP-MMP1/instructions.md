If you want to replicate the ROI with the atlas we use follow these steps:

---

Download the 05_HCP-MMP1 folder.

Place the .xml file in `path_to/fsl/data/atlases/HCP-Multi-Modal-Parcellation-1.0.xml`

Place the .gz file in `path_to/fsl/data/atlases/HCP-MMP1/MNI_Glasser_HCP_v1.0.nii.gz`

Run the following command to be sure orientation is okay:

'''bash
$ fslreorient2std MNI_Glasser_HCP_v1.0.nii.gz MNI_Glasser_HCP_v1.0.nii.gz
'

The .xlsx file contains the names corresponding to the labels. Also, you could take the info from the .xlsx file and place them in the .xml for convenience.

---

referece:

https://github.com/idossha/The-HCP-MMP1.0-atlas-in-FSL

https://www.nature.com/articles/nature18933
