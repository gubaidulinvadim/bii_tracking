import os
import sys

import numpy as np
import PyHEADTAIL
from PyHEADTAIL.general import pmath as pm
from PyHEADTAIL.general.printers import SilentPrinter
from PyHEADTAIL.ion_cloud.ion_cloud import BeamIonElement
from PyHEADTAIL.monitors.monitors import BunchMonitor
from PyHEADTAIL.particles import generators, particles
from PyHEADTAIL.trackers.longitudinal_tracking import RFSystems
from PyHEADTAIL.trackers.transverse_tracking import TransverseMap
from scipy.constants import m_p
from scipy.interpolate import interp1d
# this defines the constants related to the accelerator used in the simulation
from SOLEILII_parameters.SOLEILII_TDR_parameters import *
from tqdm import tqdm
from utils import get_parser_for_bii

# Main parameters for the simulation
PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
# path of the folder where to store the simulation results/data and some of the input
# FOLDER_PATH = '/home/dockeruser/bii_pyht_tracking/'
FOLDER_PATH = '/home/gubaidulin/scripts/bii_tracking/'

def run(n_macroparticles,
        gap_length=1,
        n_turns=int(3000),
        n_segments=50,
        n_gaps=4,
        h_rf=416,
        ion_field_model='weak',
        electron_field_model='strong',
        smooth=True,
        charge_variation=0.0,
        pressure_variation=[0.0],
        average_pressure=[3.9e12],
        beam_current=500e-3,
        ion_mass=[28],
        sigma_i=[1.78e-22]):
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
    # if interaction_model_ions == 'PIC':
    #     interaction_model = 'PIC'
    # else:
    #     interaction_model = 'weak'
    monitor_list, folder = _prepare_monitors(n_macroparticles,
        gap_length,
        n_turns,
        n_segments,
        n_gaps,
        h_rf,
        ion_field_model,
        electron_field_model,
        smooth,
        charge_variation,
        pressure_variation,
        average_pressure,
        beam_current,
        ion_mass,
        sigma_i)

    long_map, trans_one_turn = _prepare_maps(n_segments, h_rf, smooth)
    electron_bunch_list = _prepare_beam(n_macroparticles,
                                    gap_length,
                                    n_gaps,
                                    h_rf,
                                    charge_variation,
                                    beam_current,
                                    smooth)

    beam_ion_elements = _prepare_BI(folder,
                                    n_segments,
                                    h_rf,
                                    n_turns,
                                    gap_length,
                                    n_gaps,
                                    charge_variation,
                                    pressure_variation,
                                    average_pressure,
                                    ion_mass,
                                    sigma_i,
                                    ion_field_model,
                                    electron_field_model)

    N = len(average_pressure)
    trans_one_turn = [item for t_item, b_items in zip(trans_one_turn, [beam_ion_elements[i:i+N] for i in range(0, len(beam_ion_elements), N)]) for item in [t_item] + b_items]

    for turn in tqdm(range(n_turns)):
        for index, m_ in enumerate((trans_one_turn)):
            for bunch_index, electron_bunch in enumerate(electron_bunch_list):
                m_.track(electron_bunch_list[bunch_index])
                long_map.track(electron_bunch_list[bunch_index])
                if index % 2 == 0:
                    monitor_list[bunch_index].dump(
                        electron_bunch_list[bunch_index])
    return 0

def _prepare_maps(n_segments,
                h_rf,
                smooth):
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

    s = np.arange(0, n_segments + 1) * CIRCUMFERENCE / n_segments
    if smooth == 'True':
        print('smooth focusing')
        alpha_x, alpha_y = ALPHA_X_SMOOTH * \
            np.ones(n_segments), ALPHA_Y_SMOOTH * np.ones(n_segments)
        beta_x, beta_y = BETA_X_SMOOTH * \
            np.ones(n_segments), BETA_Y_SMOOTH * np.ones(n_segments)
        D_x, D_y = np.zeros(n_segments),  np.zeros(n_segments)
    else:
        try:
            print('lattice function sampling')
            data_files = ['s', 'beta_x', 'beta_y',
                          'alpha_x', 'alpha_y', 'eta_x', 'eta_y']
            data = {}
            for file in data_files:
                data[file] = np.load(
                    '/home/dockeruser/fbii_pyht_tracking/lattice_functions/' + file + '.npy')

            s = data['s'][::len(data['s']) // n_segments]
            beta_x = data['beta_x'][::len(data['beta_x']) // n_segments]
            beta_y = data['beta_y'][::len(data['beta_y']) // n_segments]
            alpha_x = data['alpha_x'][::len(data['alpha_x']) // n_segments]
            alpha_y = data['alpha_y'][::len(data['alpha_y']) // n_segments]
            eta_x = data['eta_x'][::len(data['eta_x']) // n_segments]
            eta_y = data['eta_y'][::len(data['eta_y']) // n_segments]

            D_x, D_y = np.array(eta_x), np.array(eta_y)
            alpha_x, alpha_y = np.array(alpha_x), np.array(alpha_y)
            beta_x, beta_y = np.array(beta_x), np.array(beta_y)
        except:
            raise RunTimeError(
                'There is some error with your lattice functions. Check names and sampling. The number of points in the files should be larger than number of segments in the code.')
    trans_map = TransverseMap(s, alpha_x, beta_x, D_x,
                              alpha_y, beta_y, D_y, Q_X, Q_Y)

    trans_one_turn = [m for m in trans_map]
    return long_map, trans_one_turn

def _prepare_beam(n_macroparticles,
                    gap_length,
                    n_gaps,
                    h_rf,
                    charge_variation,
                    beam_current,
                    smooth):

    if smooth:
        eta_x_0 = [0]
        alpha_x_0 = ALPHA_X_SMOOTH
        alpha_x_0 = ALPHA_Y_SMOOTH

    else:
        eta_x_0 = np.load(FOLDER_PATH+'lattice_functions/eta_x.npy')

    bunch_current = beam_current/(h_rf-n_gaps*gap_length)
    intensity_per_bunch = bunch_current/e*2*pi/OMEGA_REV
    electron_bunch_list = []
    for ind, h in enumerate(range(h_rf)):
        np.random.seed(42)
        electron_bunch = generators.ParticleGenerator(macroparticlenumber=n_macroparticles,
                                                      intensity=intensity_per_bunch,
                                                      charge=e, gamma=GAMMA, mass=m_e,
                                                      circumference=CIRCUMFERENCE,
                                                      distribution_x=generators.gaussian2D(
                                                          EPSILON_X),
                                                      alpha_x=ALPHA_X_SMOOTH, beta_x=BETA_X_SMOOTH,
                                                      D_x=eta_x_0[0], D_y=0,
                                                      distribution_y=generators.gaussian2D(
                                                          EPSILON_Y),
                                                      alpha_y=ALPHA_Y_SMOOTH, beta_y=BETA_Y_SMOOTH,
                                                      distribution_z=generators.gaussian2D_asymmetrical(
                                                          SIGMA_Z, SIGMA_DP),
                                                      printer=SilentPrinter()
                                                      ).generate()
        np.random.seed(ind)
        if charge_variation != 0:
            electron_bunch.intensity = np.random.normal(
                loc=intensity_per_bunch, scale=0.01*charge_variation*intensity_per_bunch, size=1)
        electron_bunch.y -= electron_bunch.mean_y()
        electron_bunch.x -= electron_bunch.mean_x()
        electron_bunch.yp -= electron_bunch.mean_yp()
        electron_bunch.xp -= electron_bunch.mean_xp()
        electron_bunch.z += h*CIRCUMFERENCE/h_rf
        electron_bunch_list.append(electron_bunch)
    
    train_length = h_rf//n_gaps
    for i in range(gap_length):
        for j in range(n_gaps):
            electron_bunch_list[train_length*j-i].intensity = 0
    return electron_bunch_list
    
def _prepare_BI(folder,
                n_segments,
                h_rf,
                n_turns,
                gap_length,
                n_gaps,
                charge_variation,
                pressure_variation,
                average_pressure,
                ion_mass,
                sigma_i,
                ion_field_model,
                electron_field_model
                ):
    beam_ion_elements = []
    np.random.normal(42)
    for ind in range(n_segments):
        for (p, pv, A, Si) in zip(average_pressure, pressure_variation, ion_mass, sigma_i):
            vacuum_pressure = np.random.normal(
                loc=p, scale=0.01*pv*p, size=1)
            monitor_name = folder + \
                'IM(ind={0:})'.format(int(ind)) if ind == 1 else None
            print('For ion elements with index {:} vacuum pressure is {:.1e}'.format(
                ind, vacuum_pressure[0]))
            beam_ion_elements.append(BeamIonElement(dist_ions='GS',
                                                    monitor_name=monitor_name,
                                                    set_aperture=True,
                                                    n_segments=n_segments,
                                                    n_macroparticles_max=int(1e8),
                                                    n_steps=int(h_rf*n_turns),
                                                    interaction_model=electron_field_model,
                                                    interaction_model_ions=ion_field_model,
                                                    n_g=vacuum_pressure[0],
                                                    sigma_i=Si,
                                                    A=A)
                                    )
    return beam_ion_elements

def _prepare_monitors(n_macroparticles,
        gap_length,
        n_turns,
        n_segments,
        n_gaps,
        h_rf,
        interaction_model,
        interaction_model_ions,
        smooth,
        charge_variation,
        pressure_variation,
        average_pressure,
        beam_current,
        ion_mass,
        sigma_i):
    # if sigma_i is float:
    #     sigma_i = [sigma_i]
    # if ion_mass is int:
    #     ion_mass = [ion_mass]
    # if pressure_variation is float:
    #     pressure_variation = [pressure_variation]
    # if average_pressure is float:
    #     average_pressure = [average_pressure]
    folder = FOLDER_PATH+'data/test/'
    folder += f'n_mp={n_macroparticles:.1e}'
    folder += f'gap_length={gap_length:}'
    folder += f'n_gaps={n_gaps:}'
    folder += f'n_segments={n_segments:}'
    folder += f'int_model={str(interaction_model_ions):}'
    folder += f'smooth={smooth:}'
    folder += f'charge_variation={charge_variation:}'
    folder += f'pressure_variation={pressure_variation[0]:}'
    folder += f'pressure={average_pressure[0]:.1e}'
    folder += f'beam_current={beam_current:.1e}'
    folder += f'A={ion_mass[0]:}/'

    os.makedirs(folder, exist_ok=True)
    monitor_list = []
    for ind, h in enumerate(range(h_rf)):
        filename = folder+'BM(n_bunch={0:03d})'.format(int(h))
        bunch_monitor = BunchMonitor(filename,
                                     n_steps=int(n_segments*n_turns),
                                     write_buffer_every=5000,
                                     buffer_size=6000,
                                     parameters_dict=None)
        monitor_list.append(bunch_monitor)
    return monitor_list, folder


if __name__ == "__main__":
    sys.exit()
