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

os.system('export PYTHONPATH=//lustre/scratch/sources/physmach/gubaidulin/PyHEADTAIL/')
os.system('echo ${PYTHONPATH}')
N_TURNS = int(100)
H_RF = 416
N_SEGMENTS = int(50)
PHI_RF = 0

if __name__ == "__main__":
    slurm_array_task_id = int(sys.argv[1])
    n_macroparticles = int(5e3)
    n_gaps = 50
    n_macroparticles_ions = int(1e4)
    n_segments = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    run(n_macroparticles = n_macroparticles,
        n_macroparticles_ions=n_macroparticles_ions,
        n_gaps=n_gaps,
        n_segments=n_segments[slurm_array_task_id],
        gap_every_104=False)
    sys.exit()