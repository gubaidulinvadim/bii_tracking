import numpy as np
from SOLEILII_parameters.SOLEILII_TDR_parameters import *
from scipy.constants import m_p
import PyHEADTAIL
from PyHEADTAIL.general import pmath as pm
from PyHEADTAIL.ion_cloud.ion_cloud import BeamIonElement
from PyHEADTAIL.monitors.monitors import BunchMonitor
from PyHEADTAIL.trackers.transverse_tracking import TransverseMap
from PyHEADTAIL.trackers.longitudinal_tracking import RFSystems
from PyHEADTAIL.general.printers import SilentPrinter
from PyHEADTAIL.particles import generators, particles
import os, sys
from weak_strong_ions import run

os.system('export PYTHONPATH=/lustre/scratch/sources/physmach/gubaidulin/PyHEADTAIL/')
os.system('echo ${PYTHONPATH}')
N_TURNS = int(1000)
H_RF = 416
N_SEGMENTS = int(25)
PHI_RF = 0

if __name__ == "__main__":
    slurm_array_task_id = int(sys.argv[1])
    n_macroparticles = int(1e3)
    n_gaps = np.array([1, 2, 3, 10])
    run(n_macroparticles, n_macroparticles_ions=int(1e5), n_gaps=n_gaps[slurm_array_task_id], n_segments=N_SEGMENTS, gap_every_104=True, interaction_model_ions='PIC')
    sys.exit()