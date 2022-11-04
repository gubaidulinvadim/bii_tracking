import PyHEADTAIL
from PyHEADTAIL.particles import generators
from PyHEADTAIL.general.printers import SilentPrinter
from PyHEADTAIL.trackers.longitudinal_tracking import RFbucket, RFSystems
from SOLEILII_parameters.SOLEIL_parameters import *
import numpy as np
N_MACROPARTICLES = int(1e3)
N_TURNS = int(1e3)
N_SEGMENTS = 1
INTENSITY = N_b
def run(N_MACROPARTICLES):
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
    
    bunch = generators.ParticleGenerator(macroparticlenumber=N_MACROPARTICLES, intensity=INTENSITY, charge=e,
                                         gamma=GAMMA, mass=m_e, circumference=CIRCUMFERENCE,
                                         distribution_x=generators.gaussian2D(EPS_X), alpha_x=ALPHA_X_SMOOTH, beta_x=BETA_X_SMOOTH,
                                         distribution_y=generators.gaussian2D(EPS_Y), alpha_y=ALPHA_Y_SMOOTH, beta_y=BETA_Y_SMOOTH,
                                         limit_n_rms_x=3., limit_n_rms_y=3.,
                                         distribution_z=generators.RF_bucket_distribution(long_map.get_bucket(gamma=GAMMA), sigma_z=SIGMA_Z,
                                                                                          warningprinter=SilentPrinter(), printer=SilentPrinter())
                                         ).generate()
    return 0

if __name__ == "__main__":
    print('{:.2e}'.format(N_b))
    PHI_RF = np.arccos(U_LOSS/V_RF) if (GAMMA**-2-GAMMA_T**-2) < 0 else pi+np.arccos(U_LOSS/V_RF)
    print('RF phase while compensating losses is: {0:.2f}'.format(PHI_RF))
    print('Transition energy: {0:.1e}, SOLEIL energy {1:.1e}'.format(GAMMA_T, GAMMA))
    