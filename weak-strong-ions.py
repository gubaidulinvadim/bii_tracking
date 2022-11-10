import os, sys
os.system('export PYTHONPATH=/home/sources/physmach/gubaidulin/PyHEADTAIL')
os.system('echo ${PYTHONPATH}')
import PyHEADTAIL
from PyHEADTAIL.particles import generators
from PyHEADTAIL.general.printers import SilentPrinter
from PyHEADTAIL.trackers.longitudinal_tracking import RFSystems
from PyHEADTAIL.trackers.transverse_tracking import TransverseMap
from PyHEADTAIL.monitors.monitors import BunchMonitor
from PyHEADTAIL.ion_cloud.ion_cloud import BeamIonElement
# from PyHEADTAIL.particles.slicing import UniformBinSlicer
from PyHEADTAIL.general import pmath as pm
from scipy.constants import m_p
from SOLEILII_parameters.SOLEILII_CDR_parameters import *
import numpy as np
N_TURNS = int(1)
H_RF = 416
N_SEGMENTS = int(500)
np.random.seed(42)
PHI_RF = np.arccos(U_LOSS/V_RF) if (GAMMA**-2-GAMMA_T**-2) < 0 else pi+np.arccos(U_LOSS/V_RF)
PHI_RF=0

def run(n_macroparticles):
    np.random.seed(42)
    PHI_RF = np.arccos(U_LOSS/V_RF) if (GAMMA**-2-GAMMA_T**-2) < 0 else pi+np.arccos(U_LOSS/V_RF)
    long_map = RFSystems(
        CIRCUMFERENCE,
        [H_RF],
        [V_RF],
        [PHI_RF],
        [ALPHA_0],
        GAMMA,
        mass=m_e,
        charge=e
        )    
    electron_bunch_list = []
    monitor_list = []
    for ind, h in enumerate(range(H_RF)):
        electron_bunch = generators.ParticleGenerator(macroparticlenumber=n_macroparticles,
                                                    intensity=INTENSITY_PER_BUNCH,
                                                    charge=e, gamma=GAMMA, mass=m_p,
                                                    circumference=CIRCUMFERENCE,
                                                    distribution_x=generators.gaussian2D(EPSILON_X),
                                                    alpha_x=ALPHA_X_SMOOTH, beta_x=BETA_X_SMOOTH,
                                                    distribution_y=generators.gaussian2D(EPSILON_Y),
                                                    alpha_y=ALPHA_Y_SMOOTH, beta_y=BETA_Y_SMOOTH,
                                                    distribution_z=generators.gaussian2D_asymmetrical(SIGMA_Z, SIGMA_DP),
                                                    limit_n_rms_x=3., limit_n_rms_y=3.,
                                                    printer=SilentPrinter()
                                                    ).generate()
    electron_bunch.z += h*CIRCUMFERENCE/H_RF
    electron_bunch_list.append(electron_bunch)
    filename = 'Results/BM_(n_bunch={0:}, n_macro={1:.1e})'.format(int(h), n_macroparticles)
    bunch_monitor = BunchMonitor(filename, n_steps=N_SEGMENTS*N_TURNS, parameters_dict=None,
                 write_buffer_every=50, buffer_size=100,)
    monitor_list.append(bunch_monitor)


    s = np.arange(0, N_SEGMENTS + 1) * CIRCUMFERENCE / N_SEGMENTS
    alpha_x, alpha_y = ALPHA_X_SMOOTH * \
        np.ones(N_SEGMENTS), ALPHA_Y_SMOOTH * np.ones(N_SEGMENTS)
    beta_x, beta_y = BETA_X_SMOOTH * \
        np.ones(N_SEGMENTS), BETA_Y_SMOOTH * np.ones(N_SEGMENTS)
    D_x, D_y = np.zeros(N_SEGMENTS),  np.zeros(N_SEGMENTS)
    trans_map = TransverseMap(s, alpha_x, beta_x, D_x,
                              alpha_y, beta_y, D_y, Q_X, Q_Y)

    trans_one_turn = [m for m in trans_map]
    beam_ion_elements = []
    for ind, m in enumerate(trans_one_turn):
        beam_ion_elements.append(BeamIonElement())
    trans_one_turn = [item for sublist in zip(trans_one_turn, beam_ion_elements) for item in sublist]
    for turn in range(N_TURNS):
# turn = 0
        for index, m_ in enumerate(trans_one_turn):
            for bunch_index, electron_bunch in enumerate(electron_bunch_list):
                m_.track(electron_bunch)    
                long_map.track(electron_bunch)
                if index % 2 ==0:
                    monitor_list[bunch_index].dump(electron_bunch)    
        return 0

if __name__ == "__main__":
    n_macroparticles = int(sys.argv[1])
    run(n_macroparticles)
    sys.exit()
    