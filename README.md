An example of a tracking script for Fast Beam-Ion Instability. We use our own implementation of beam-ion interaction in PyHEADTAIL code. 
The interactive notebook has several examples built into it:
- A fully linear tracking. Both electron bunch train and ion clouds are assumed to have linear field (and without boundaries). This model corresponds fully to the original analytical estimations.
- Both electron and ion beam are Gaussian. The Bassetti-Erskine formula is used to compute the electric fields and associated beam-ion kicks. The rms size of ion cloud and of an electron bunch are computed and updated for every interaction. 

Both electron bunches and ion cloud are recorded using Monitor classes of PyHEADTAIL. The first beam-ion element also records individual positions of each ion. 