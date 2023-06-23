import numpy as np
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
from scipy.interpolate import interp1d
import os
import sys
#os.system('export PYTHONPATH=/lustre/scratch/sources/physmach/gubaidulin/PyHEADTAIL/')
#os.system('echo ${PYTHONPATH}')
PHI_RF = 0

def run(n_macroparticles, n_macroparticles_ions, gap_length=0, n_turns=2000, n_segments=50, h_rf=416, gap_every_104=False, interaction_model='weak', interaction_model_ions='strong', smooth=False):
    if gap_every_104:
        folder = '/home/dockeruser/fbii_pyht_tracking/Results/TDR/n_mp={0:.1e},n_mp_ions={1:.1e},gap_length={2:.1e},n_segments={3:.1e}_every_104,int_model={4:},smooth={5:}/'.format(
        n_macroparticles,
        n_macroparticles_ions, 
        gap_length,
        n_segments,
        interaction_model_ions,
        smooth
    )
    else:
        folder = '/home/dockeruser/fbii_pyht_tracking/Results/TDR/n_mp={0:.1e},n_mp_ions={1:.1e},gap_length={2:.1e},n_segments={3:.1e},int_model={4:},smooth={5:}/'.format(
            n_macroparticles,
            n_macroparticles_ions, 
            gap_length,
            n_segments,
            interaction_model_ions,
            smooth
        )
    os.makedirs(folder, exist_ok=True)
    np.random.seed(42)
    print('Run with electron bunch macroparticle number equal to {:.1e}'.format(
        n_macroparticles))
    print('Run with ion cloud max macroparticle number equal to {:.1e}'.format(
        n_macroparticles_ions))
    np.random.seed(42)
    PHI_RF = np.arccos(U_LOSS/V_RF) if (GAMMA**-2-GAMMA_T**-
                                        2) < 0 else pi+np.arccos(U_LOSS/V_RF)
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
    r_x = 2*np.sqrt(EPSILON_X*BETA_X_SMOOTH)
    r_xp = 2*np.sqrt(EPSILON_X*BETA_X_SMOOTH)
    r_y = 2*np.sqrt(EPSILON_Y*BETA_Y_SMOOTH)
    r_yp = 2*np.sqrt(EPSILON_Y*BETA_Y_SMOOTH)
    eta_x_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/eta_x.npy')
    for ind, h in enumerate(range(H_RF)):
        np.random.seed(42)
        electron_bunch = generators.ParticleGenerator(macroparticlenumber=n_macroparticles,
                                                  intensity=INTENSITY_PER_BUNCH,
                                                  charge=e, gamma=GAMMA, mass=m_e,
                                                  circumference=CIRCUMFERENCE,
                                                  # distribution_x=generators.kv2D(r_x, r_xp),
                                                  distribution_x = generators.gaussian2D(EPSILON_X),
                                                  alpha_x=ALPHA_X_SMOOTH, beta_x=BETA_X_SMOOTH,
                                                  # distribution_y=generators.kv2D(r_y, r_yp),
                                                  D_x=eta_x_0[0], D_y = 0,
                                                  distribution_y = generators.gaussian2D(EPSILON_Y),
                                                  alpha_y=ALPHA_Y_SMOOTH, beta_y=BETA_Y_SMOOTH,
                                                  distribution_z=generators.gaussian2D_asymmetrical(SIGMA_Z, SIGMA_DP),
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
        electron_bunch.yp -= electron_bunch.mean_yp()
        electron_bunch.x -= electron_bunch.mean_x()
        electron_bunch.xp -= electron_bunch.mean_xp()
        electron_bunch.z += h*CIRCUMFERENCE/H_RF
        electron_bunch_list.append(electron_bunch)
        filename = folder+'BM(n_bunch={0:})'.format(int(h),
                                                    n_macroparticles,
                                                    n_macroparticles_ions)
        bunch_monitor = BunchMonitor(filename, n_steps=int(n_segments*n_turns), parameters_dict=None)
        monitor_list.append(bunch_monitor)
    for i in range(gap_length):
            electron_bunch_list[-i].intensity = 0
            if gap_every_104:
                electron_bunch_list[104-i].intensity = 0
                electron_bunch_list[208-i].intensity = 0
                electron_bunch_list[312-i].intensity = 0
    s = np.arange(0, n_segments + 1) * CIRCUMFERENCE / n_segments
    if smooth == True:
        print('smooth focusing')
        alpha_x, alpha_y = ALPHA_X_SMOOTH * \
            np.ones(n_segments), ALPHA_Y_SMOOTH * np.ones(n_segments)
        beta_x, beta_y = BETA_X_SMOOTH * \
            np.ones(n_segments), BETA_Y_SMOOTH * np.ones(n_segments)
        D_x, D_y = np.zeros(n_segments),  np.zeros(n_segments)
    else: 
        print('lattice function sampling')
        s_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/s.npy')
        beta_x_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/beta_x.npy')
        beta_y_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/beta_y.npy')
        alpha_x_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/alpha_x.npy')
        alpha_y_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/alpha_y.npy')
        eta_x_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/eta_x.npy')
        eta_y_0 = np.load('/home/dockeruser/fbii_pyht_tracking/lattice_functions/eta_y.npy')
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
    trans_map = TransverseMap(s, alpha_x, beta_x, D_x,
                            alpha_y, beta_y, D_y, Q_X, Q_Y)

    trans_one_turn = [m for m in trans_map]
    BI = BeamIonElement()
    beam_ion_elements = []
    for ind, m in enumerate(trans_one_turn):
    #     if ind == 0:
    #             beam_ion_elements.append(BeamIonElement(dist_ions='GS',
    #                                                     monitor_name=folder+'IM(ind={0:})'.format(int(ind)),
    #                                                     use_particle_monitor=True,
    #                                                     n_segments=n_segments,
    #                                                     set_aperture=True,
    #                                                     n_macroparticles_max = n_macroparticles_ions,
    #                                                     n_steps=int(H_RF*n_turns)))
        beam_ion_elements.append(BeamIonElement(dist_ions='GS',
                                                monitor_name=folder+'IM(ind={0:})'.format(int(ind)),
                                                set_aperture=True,
                                                n_segments=n_segments,
                                                n_macroparticles_max = n_macroparticles_ions,
                                                n_steps=int(H_RF*n_turns),
                                                interaction_model=interaction_model, 
                                                interaction_model_ions=interaction_model_ions)
                                                )
    trans_one_turn = [item for sublist in zip(trans_one_turn, beam_ion_elements) for item in sublist]
    for turn in tqdm(range(n_turns)):
        for index, m_ in enumerate((trans_one_turn)):
            for bunch_index, electron_bunch in enumerate(electron_bunch_list):
                m_.track(electron_bunch_list[bunch_index])    
                long_map.track(electron_bunch_list[bunch_index])
                if index % 2 == 0:
                    monitor_list[bunch_index].dump(electron_bunch_list[bunch_index])
    return 0


if __name__ == "__main__":
    slurm_array_task_id = int(sys.argv[1])
    is_smooth = bool(sys.arvg[2])
    n_macroparticles = np.array(
        [int(1e3), int(5e3), int(1e4), int(5e4)])
    run(n_macroparticles[slurm_array_task_id], n_macroparticles_ions=int(1e4), gap_length=50, n_segments=n_segments, smooth=is_smooth)
    sys.exit()
