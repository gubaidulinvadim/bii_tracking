import numpy as np
# this defines the constants related to the accelerator used in the simulation
from SOLEILII_parameters.SOLEILII_TDR_parameters import *
from scipy.constants import m_p
from PyHEADTAIL.general import pmath as pm
from PyHEADTAIL.ion_cloud.ion_cloud import BeamIonElement
from PyHEADTAIL.monitors.monitors import BunchMonitor
from PyHEADTAIL.trackers.transverse_tracking import TransverseMap
from PyHEADTAIL.trackers.longitudinal_tracking import RFSystems
from PyHEADTAIL.general.printers import SilentPrinter
from PyHEADTAIL.particles import generators, particles
import PyHEADTAIL
from tqdm import tqdm
from ccrt.utils import get_parser_for_bii
from scipy.interpolate import interp1d
import os
import sys
#os.system('export PYTHONPATH=/lustre/scratch/sources/physmach/gubaidulin/PyHEADTAIL/')
#os.system('echo ${PYTHONPATH}')
# Main parameters for the simulation
N_SEGMENTS = int(50)  # number of segments used for transverse tracking
PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
# path of the folder where to store the simulation results/data and some of the input
FOLDER_PATH = '/home/dockeruser/fbii_pyht_tracking/'
# path of the folder where to store the simulation results/data and some of the input
# FOLDER_PATH = '/home/gubaidulin/scripts/tracking/example_for_siwei/'


def run(n_macroparticles, n_macroparticles_ions, gap_length=1, n_turns=int(2000), n_segments=50, n_gaps=4, h_rf=416, interaction_model='weak', interaction_model_ions='strong', smooth=True):
    """
    Run the simulation with the specified parameters.

    Args:
        n_macroparticles (int): Number of macroparticles in the electron bunch.
        n_macroparticles_ions (int): Maximum number of macroparticles in the ion cloud.
        gap_length (int, optional): Length of the gap in rf buckets. Defaults to 0.
        n_segments (int, optional): Number of segments in the transverse map. Defaults to 50.
        n_gaps (int, optional): Number of gaps. Defaults to 4.
        interaction_model (str, optional): Interaction model for electomagnetic field of electrons acting on ions. Should be 'weak' or 'PIC'
        interaction_model_ions (str, optional): Interaction model for electomagnetic field of ions acting on electrons. Defaults to 'strong'. Should be 'weak', 'strong', or 'PIC'.
        smooth (bool, optional): Smooth focusing flag. Defaults to True. If False, one should provide the optics functions in separate .npy files.

    Returns:
        int: The value 0.
    """
    folder = FOLDER_PATH+'Results/TDR/n_mp={0:.1e},n_mp_ions={1:.1e},gap_length={2:.1e},n_gaps={6:},n_segments={3:.1e},int_model={4:},smooth={5:}/'.format(
        n_macroparticles,
        n_macroparticles_ions,
        gap_length,
        n_segments,
        interaction_model_ions,
        smooth,
        n_gaps
    )
    os.makedirs(folder, exist_ok=True)
    np.random.seed(42)
    print('Run with electron bunch macroparticle number equal to {:.1e}'.format(
        n_macroparticles))
    print('Run with ion cloud max macroparticle number equal to {:.1e}'.format(
        n_macroparticles_ions))
    # PHI_RF = np.arccos(U_LOSS/V_RF) if (GAMMA**-2-GAMMA_T**-

    # 2) < 0 else pi+np.arccos(U_LOSS/V_RF)
    long_map = RFSystems(
        CIRCUMFERENCE,
        [h_rf],
        [V_RF],
        [PHI_RF],
        [ALPHA_0],
        GAMMA,
        mass=m_e,
        charge=e
    )
    electron_bunch_list = []
    monitor_list = []
    # r_x = 2*np.sqrt(EPSILON_X*BETA_X_SMOOTH)
    # r_xp = 2*np.sqrt(EPSILON_X*BETA_X_SMOOTH)
    # r_y = 2*np.sqrt(EPSILON_Y*BETA_Y_SMOOTH)
    # r_yp = 2*np.sqrt(EPSILON_Y*BETA_Y_SMOOTH)
    if smooth:
        eta_x_0 = [0]
        alpha_x_0 = ALPHA_X_SMOOTH
        alpha_x_0 = ALPHA_Y_SMOOTH

    else:
        eta_x_0 = np.load(FOLDER_PATH+'lattice_functions/eta_x.npy')
    for ind, h in enumerate(range(h_rf)):
        np.random.seed(42)
        electron_bunch = generators.ParticleGenerator(macroparticlenumber=n_macroparticles,
                                                      intensity=INTENSITY_PER_BUNCH,
                                                      charge=e, gamma=GAMMA, mass=m_e,
                                                      circumference=CIRCUMFERENCE,
                                                      # distribution_x=generators.kv2D(r_x, r_xp),
                                                      distribution_x=generators.gaussian2D(
                                                          EPSILON_X),
                                                      alpha_x=ALPHA_X_SMOOTH, beta_x=BETA_X_SMOOTH,
                                                      # distribution_y=generators.kv2D(r_y, r_yp),
                                                      D_x=eta_x_0[0], D_y=0,
                                                      distribution_y=generators.gaussian2D(
                                                          EPSILON_Y),
                                                      alpha_y=ALPHA_Y_SMOOTH, beta_y=BETA_Y_SMOOTH,
                                                      distribution_z=generators.gaussian2D_asymmetrical(
                                                          SIGMA_Z, SIGMA_DP),
                                                      printer=SilentPrinter()
                                                      ).generate()
#        electron_bunch_twin = particles.Particles(macroparticlenumber=n_macroparticles//2,
#                                                  particlenumber_per_mp=INTENSITY_PER_BUNCH/n_macroparticles,
#                                                  charge=e, gamma=GAMMA, mass=m_e,
#                                                  circumference=CIRCUMFERENCE,
#                                                  coords_n_momenta_dict={
#                                                    'x': -electron_bunch.x,
#                                                    'xp': -electron_bunch.xp,
#                                                    'y': -electron_bunch.y,
#                                                    'yp': -electron_bunch.yp,
#                                                   'z': -electron_bunch.z,
#                                                    'dp': -electron_bunch.dp
#                                                  },
#                                                  printer=SilentPrinter()
#                                     )
#        electron_bunch += electron_bunch_twin
#        np.random.seed(ind)
#        electron_bunch.y += np.random.normal(scale=0.02*electron_bunch.sigma_y(), size=1)
        electron_bunch.y -= electron_bunch.mean_y()
        electron_bunch.x -= electron_bunch.mean_x()
        electron_bunch.z += h*CIRCUMFERENCE/h_rf
        electron_bunch_list.append(electron_bunch)
        filename = folder+'BM(n_bunch={0:})'.format(int(h))
        bunch_monitor = BunchMonitor(filename, n_steps=int(
            n_segments*n_turns), parameters_dict=None)
        monitor_list.append(bunch_monitor)
    train_length = h_rf//n_gaps
    for i in range(gap_length):
        for j in range(n_gaps):
            electron_bunch_list[train_length*j-i].intensity = 0

    s = np.arange(0, n_segments + 1) * CIRCUMFERENCE / n_segments
    if smooth == True:
        print('smooth focusing')
        alpha_x, alpha_y = ALPHA_X_SMOOTH * \
            np.ones(n_segments), ALPHA_Y_SMOOTH * np.ones(n_segments)
        beta_x, beta_y = BETA_X_SMOOTH * \
            np.ones(n_segments), BETA_Y_SMOOTH * np.ones(n_segments)
        D_x, D_y = np.zeros(n_segments),  np.zeros(n_segments)
    else:
        try:
            print('lattice function sampling')
            s_0 = np.load(FOLDER_PATH+'lattice_functions/s.npy')
            beta_x_0 = np.load(FOLDER_PATH+'lattice_functions/beta_x.npy')
            beta_y_0 = np.load(FOLDER_PATH+'lattice_functions/beta_y.npy')
            alpha_x_0 = np.load(FOLDER_PATH+'lattice_functions/alpha_x.npy')
            alpha_y_0 = np.load(FOLDER_PATH+'lattice_functions/alpha_y.npy')
            eta_x_0 = np.load(FOLDER_PATH+'lattice_functions/eta_x.npy')
            eta_y_0 = np.load(FOLDER_PATH+'lattice_functions/eta_y.npy')
            beta_x = []
            beta_y = []
            alpha_x = []
            alpha_y = []
            eta_x = []
            eta_y = []
            s = []
            for a in range(n_segments):
                index = int(a*len(s)/n_segments)
                s.append(s_0[index])
                beta_x.append(beta_x_0[index])
                beta_y.append(beta_y_0[index])
                alpha_x.append(alpha_x_0[index])
                alpha_y.append(alpha_y_0[index])
                eta_x.append(eta_x_0[index])
                eta_y.append(eta_y_0[index])
            alpha_x, alpha_y = np.array(alpha_x), np.array(alpha_y)
            beta_x, beta_y = np.array(beta_x), np.array(beta_y)
            D_x, D_y = np.array(eta_x),  np.array(eta_y)
        except:
            raise RunTimeError(
                'There is some error with your lattice functions. Check names and sampling. The number of points in the files should be larger than number of segments in the code.')
    trans_map = TransverseMap(s, alpha_x, beta_x, D_x,
                              alpha_y, beta_y, D_y, Q_X, Q_Y)

    trans_one_turn = [m for m in trans_map]
    BI = BeamIonElement()
    beam_ion_elements = []

    # create beam_ion_elements for each segment of transverse map
    for ind, m in enumerate(trans_one_turn):
        # Uncomment to record 6D coordinates of every ion macroparticle in the first beam-ion element
        #     if ind == 0:
        #             beam_ion_elements.append(BeamIonElement(dist_ions='GS',
        #                                                     monitor_name=folder+'PIM(ind={0:})'.format(int(ind)),
        #                                                     use_particle_monitor=True,
        #                                                     n_segments=n_segments,
        #                                                     set_aperture=True,
        #                                                     n_macroparticles_max = n_macroparticles_ions,
        #                                                     n_steps=int(h_rf*n_turns)))
        beam_ion_elements.append(BeamIonElement(dist_ions='GS',
                                                monitor_name=folder +
                                                'IM(ind={0:})'.format(
                                                    int(ind)),
                                                set_aperture=True,
                                                n_segments=n_segments,
                                                n_macroparticles_max=n_macroparticles_ions,
                                                n_steps=int(h_rf*n_turns),
                                                interaction_model=interaction_model,
                                                interaction_model_ions=interaction_model_ions)
                                 )
    # Place beam_ion_element after each segment o transverse map
    trans_one_turn = [item for sublist in zip(
        trans_one_turn, beam_ion_elements) for item in sublist]
    # tracking loop
    for turn in tqdm(range(n_turns)):
        for index, m_ in enumerate((trans_one_turn)):
            for bunch_index, electron_bunch in enumerate(electron_bunch_list):
                m_.track(electron_bunch_list[bunch_index])
                long_map.track(electron_bunch_list[bunch_index])
                if index % 2 == 0:
                    monitor_list[bunch_index].dump(
                        electron_bunch_list[bunch_index])
    return 0


if __name__ == "__main__":
    parser = get_parser_for_bii()
    args = parser.parse_args()
    run(args.n_macroparticles, n_macroparticles_ions=int(1e6), gap_length=args.gap_length,
        n_gaps=args.n_gaps, n_segments=args.n_segments, smooth=args.is_smooth, h_rf=args.h_rf)
    sys.exit()
