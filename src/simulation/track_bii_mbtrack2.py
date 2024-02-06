import os
import sys

import numpy as np
from scipy.constants import m_p
from scipy.interpolate import interp1d
from SOLEILII_parameters.SOLEILII_TDR_parameters import *
from tqdm import tqdm
from utils import get_parser_for_bii

PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
FOLDER_PATH = '/home/gubaidulin/scripts/tracking/fbii_pyht_tracking/'

def run_mbtrack2(ring,
                beam_current=500e-3,
                mp_per_bunch=1e3,
                turns=3000,
                n_gaps=4,
                gap_length=1,
                ion_field_model='strong',
                electron_field_model='weak',
                n_segments=25,
                smooth=True,
                charge_variation=0.0,
                pressure_variation=0.0,
                averge_pressure=3.9e12,
                ion_mass=28,
                sigma_i=1.78e-22):
    # n_macroparticles,
    #     n_macroparticles_ions,
    #     gap_length=1,
    #     n_turns=int(3000),
    #     n_segments=50,
    #     n_gaps=4,
    #     h_rf=416,
    #     interaction_model='weak',
    #     interaction_model_ions='strong',
    #     smooth=True,
    #     charge_variation=0.0,
    #     pressure_variation=0.0,
    #     average_pressure=3.9e12,
    #     beam_current=500e-3,
    #     ion_mass=28,
    #     sigma_i=1.78e-22
    from mbtrack2 import (CircularResistiveWall, Electron, Synchrotron,
                          WakePotential)
    from mbtrack2.tracking import (Beam, Bunch, LongitudinalMap, RFCavity,
                                   SynchrotronRadiation, TransverseMap)
    from mbtrack2.tracking.beam_ion_effects import BeamIonElement
    from mbtrack2.tracking.element import (TransverseMap, TransverseMapSector,
                                           transverse_map_sector_generator)
    from mbtrack2.tracking.monitors import BeamMonitor
    from mbtrack2.utilities import Optics
    particle = Electron()
    chro = [0, 0]
    ring2 = v2366_v2(IDs='open', V_RF=1.7e6)
    ring = Synchrotron(
        h=ring2.h,
        optics=ring2.optics,
        particle=particle,
        L=ring2.L,
        E0=ring2.E0,
        ac=ring2.ac,
        U0=ring2.U0,
        tau=ring2.tau,
        emit=[ring2.emit[0], 0.3*ring2.emit[0]],
        tune=ring2.tune,
        sigma_delta=ring2.sigma_delta,
        sigma_0=ring2.sigma_0,
        chro=chro,
    )
    
    np.random.seed(42)
    mybeam = Beam(ring)
    is_mpi = False
    bunch_current = beam_current/ring.h
    filling_pattern = np.ones(ring.h) * bunch_current
    mybeam.init_beam(
        filling_pattern,
        current_per_bunch=bunch_current,
        mp_per_bunch=mp_per_bunch,
        track_alive=False,
        mpi=is_mpi,
    )
    mybeam.bunch_list[0].charge = 0
    mybeam.bunch_list[104].charge = 0
    mybeam.bunch_list[208].charge = 0
    mybeam.bunch_list[312].charge = 0
    
    for bunch in mybeam.bunch_list:
        for stat in ['x', 'y', 'xp', 'yp']:
            bunch[stat] -= bunch[stat].mean()
    
    
    long_map = LongitudinalMap(ring)
    rf = RFCavity(ring, m=1, Vc=V_RF, theta=np.arccos(ring.U0 / V_RF))

    beam_monitor = BeamMonitor(ring.h,
                               save_every=1,
                               buffer_size=1,
                               total_size=turns,
                               file_name='beam_monitor',
                               mpi_mode=False)    
    sr = SynchrotronRadiation(ring, switch=[1, 1, 1])
    trans_map = TransverseMap(ring)

    beam_ion_element = BeamIonElement(ion_mass=28*m_p,
                                     ion_charge=e,
                                     ionization_cross_section=sigma_i,
                                     residual_gas_density=average_pressure,
                                     ring=ring,
                                     n_max_macropaticles=int(1e8),
                                     ion_field_model=ion_field_model,
                                     electron_field_model=electron_field_model,
                                     bunch_spacing=0.85,
                                     ion_element_length=ring.L,
                                     ion_beam_monitor_name=None,
                                     use_ion_phase_space_monitor=False,
                                     use_aperture=True,
                                     x_radius=5*mybeam[0]['x'].std(),
                                     y_radius = 5*mybeam[0]['y'].std()
                                     )
    for i in tqdm(range(turns)):
        trans_map.track(mybeam)
        long_map.track(mybeam)
        rf.track(mybeam)
        for bunch in mybeam.bunch_list:
            beam_ion_element.track(bunch)
        # wp.track(mybeam)
        # sr.track(mybeam)
        beam_monitor.track(mybeam)
    return 0
if __name__ == "__main__":
    parser = get_parser_for_bii()
    args = parser.parse_args()
    run(args.n_macroparticles,
        n_macroparticles_ions=int(1e6),
        gap_length=args.gap_length,
        n_gaps=args.n_gaps,
        n_segments=args.n_segments,
        smooth=args.is_smooth,
        h_rf=args.h_rf,
        interaction_model_ions=args.interaction_model_ions,
        charge_variation=args.charge_variation,
        pressure_variation=args.pressure_variation,
        average_pressure=args.average_pressure,
        beam_current=args.beam_current,
        sigma_i=args.sigma_i,
        ion_mass=args.ion_mass)
    sys.exit()
