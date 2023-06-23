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
N_TURNS = int(100)
H_RF = 416
N_SEGMENTS = int(50)
PHI_RF = 0

if __name__ == "__main__":
    slurm_array_task_id = int(sys.argv[1])
    n_macroparticles = int(5e3)
    gap_length = 50
    n_macroparticles_ions = np.array([1e3, 5e3, 1e4, 2e4, 3e4, 4e4, 5e4, 1e5])
    run(n_macroparticles = n_macroparticles,
        n_macroparticles_ions=n_macroparticles_ions[slurm_array_task_id],
        gap_length=gap_length,
        n_segments=N_SEGMENTS,
        gap_every_104=False)
    sys.exit()