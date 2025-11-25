import sys
sys.path.append('../input')
import numpy as np
from mbtrack2.tracking import (Beam, LongitudinalMap, RFCavity,
                               SynchrotronRadiation, TransverseSpaceCharge)
from mbtrack2.tracking.aperture import ElipticalAperture
from mbtrack2.tracking.beam_ion_effects import BeamIonElement
from mbtrack2.tracking.monitors import IonMonitor 
from mbtrack2.tracking.element import (transverse_map_sector_generator)
from mbtrack2.tracking.monitors import BeamMonitor
from mbtrack2.tracking.feedback import TransverseExponentialDamper
from facilities_mbtrack2.SOLEIL_II import v3633
from scipy.constants import m_p, e, c
from tqdm import tqdm

PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
FOLDER_PATH = '/home/dockeruser/bii_tracking/'
                  
def run(beam_current=500e-3,
        n_macroparticles=1e3,
        n_turns=3000,
        n_gaps=4,
        h_rf=416,
        gap_length=1,
        ion_field_model='strong',
        electron_field_model='weak',
        n_segments=25,
        smooth=True,
        charge_variation=0.0,
        pressure_variation=[0.0],
        average_pressure=[3.9e12],
        ion_mass=[28],
        sigma_i=[1.78e-22],
        chromaticity=[0,0],
        sc=False,
        feedback_tau = 0,
        emittance_ratio=0.3):
    appendix = f'(Ib={int(beam_current*1e3)}mA,'+\
        f'n_macroparticles={n_macroparticles:.1e},'+\
            f'n_turns={int(n_turns)},'+\
                f'n_gaps={int(n_gaps)},'+\
                    f'gap_length={int(gap_length)},'+\
                        f'n_segments={int(n_segments)},'+\
                            f'charge_var={int(charge_variation)},'+\
                                f'smooth={smooth},'+\
                                    f'average_pressure={average_pressure[0]:.1e}'+\
                                    f'feedback_tau={feedback_tau:}'+\
                                    f'{chromaticity=:}' +\
                                    f'{sc=}'+\
                                    f'{emittance_ratio=}'+\
                                        f')'
    chro = np.array([chromaticity[0], chromaticity[1]])
    ring = v3633(IDs='open', V_RF=1.7e6, load_lattice=True)
    ring.emit = np.array([ring.emit[0], emittance_ratio*ring.emit[0]])
    ring.chro = chro
    
    np.random.seed(42)
    beam =_prepare_beam(ring, 
                        n_macroparticles,
                        gap_length,
                        n_gaps,
                        charge_variation,
                        beam_current)
    rf, long_map, trans_one_turn, sr = _prepare_maps(ring,
                                                n_segments,
                                                h_rf,
                                                smooth)
    folder = '/home/dockeruser/bii_tracking/data/'
    # folder = '/home/gubaidulin/'
    beam_monitor = BeamMonitor(ring.h,
                               save_every=1,
                               buffer_size=int(n_turns//4),
                               total_size=int(n_turns),
                               file_name=folder+'beam_monitor'+appendix,
                               mpi_mode=False)    
    
    fbt = TransverseExponentialDamper(ring,
                                      damping_time=np.array([feedback_tau,feedback_tau]),
                             phase_diff=np.array([90, 90]))
    
    
    spacecharge = TransverseSpaceCharge(ring, interaction_length=ring.L,
                                        n_bins=100)
    beam_ion_elements = _prepare_BI(ring,
                                    folder,
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
                                    electron_field_model,
                                    beam,
                                    n_turns*h_rf,
                                    feedback_tau,
                                    chromaticity,
                                    sc,
                                    smooth, 
                                    emittance_ratio
                                    )

    N = len(average_pressure)
    print('before implanting beam-ion elements', trans_one_turn)
    beam_ion_chunks = [beam_ion_elements[i:i+N] for i in range(0, len(beam_ion_elements), N)]
    new_list = []
    if trans_one_turn:  # Check if trans_one_turn is not empty
        new_list.append(trans_one_turn[0])
    for i in range(1, len(trans_one_turn)):
        # Add beam_ion_chunk if available
        if i-1 < len(beam_ion_chunks):
            new_list.extend(beam_ion_chunks[i-1])
        # Add the next TransverseMapSector
        new_list.append(trans_one_turn[i])

    # Add any remaining beam_ion_chunks (if beam_ion_elements is longer)
    remaining_chunks = beam_ion_chunks[len(trans_one_turn)-1:]
    for chunk in remaining_chunks:
        new_list.extend(chunk)

    trans_one_turn = new_list
    # trans_one_turn = [item for t_item, b_items in zip(trans_one_turn, [beam_ion_elements[i:i+N] for i in range(0, len(beam_ion_elements), N)]) for item in [t_item] + b_items]
    print('after implanting beam-ion_elements', trans_one_turn)
    for _ in tqdm(range(n_turns)):
        long_map.track(beam)
        rf.track(beam)
        # wp.track(beam)
        sr.track(beam)
        if feedback_tau != 0:
            fbt.track(beam)
        if sc:
            spacecharge.track(beam)
        for _t in trans_one_turn:
            _t.track(beam)
        beam_monitor.track(beam)
    beam_monitor.close()
    return 0

def _prepare_maps(ring,
                n_segments,
                h_rf,
                smooth):
    long_map = LongitudinalMap(ring)
    V_RF = 1.7e6
    rf = RFCavity(ring, m=1, Vc=V_RF, theta=np.arccos(ring.U0 / V_RF))
    sr = SynchrotronRadiation(ring, switch=np.array([1, 0, 0]))
    positions = np.linspace(0, ring.L, n_segments)
    trans_one_turn = transverse_map_sector_generator(ring, positions)
    return rf, long_map, trans_one_turn, sr

def _prepare_beam(ring,
                n_macroparticles,
                gap_length,
                n_gaps,
                charge_variation,
                beam_current):
    mybeam = Beam(ring)

    np.random.seed(42)
    bunch_current = beam_current/ring.h
    bunch_current = np.random.normal(loc=bunch_current,
                                    scale=.01*charge_variation*bunch_current,
                                    size=ring.h)
    filling_pattern = np.ones(ring.h)*bunch_current
    mybeam.init_beam(
        filling_pattern,
        current_per_bunch=bunch_current,
        mp_per_bunch=n_macroparticles,
        track_alive=False,
        mpi=False,
    )
    for i in range(gap_length):
        for j in range(n_gaps):
            mybeam.bunch_list[j*ring.h//n_gaps+i].charge=0
    for bunch in mybeam.bunch_list:
        if not bunch.is_empty:
            for stat in ['x', 'y', 'xp', 'yp']:
                bunch[stat] -= bunch[stat].mean()
    return mybeam
    
def _prepare_BI(ring,
                folder,
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
                electron_field_model,
                beam,
                n_steps,
                feedback_tau,
                chromaticity,
                sc,
                smooth,
                emittance_ratio,
                ):
    appendix = f'n_turns={int(n_turns)},'+\
                f'n_gaps={int(n_gaps)},'+\
                    f'gap_length={int(gap_length)},'+\
                        f'n_segments={int(n_segments)},'+\
                            f'charge_var={int(charge_variation)},'+\
                                f'smooth={smooth},'+\
                                    f'average_pressure={average_pressure[0]:.1e}'+\
                                    f'feedback_tau={feedback_tau:}'+\
                                    f'{chromaticity=:}' +\
                                    f'{sc=}'+\
                                    f'{emittance_ratio=}'+\
                                        f')'
    beam_ion_elements = []
    np.random.seed(42)
    for i in range(n_segments):
        for (p, pv, A, Si) in zip(average_pressure, pressure_variation, ion_mass, sigma_i):
            print(f'Making a beam-ion element for {p:}, {pv:}, ion mass {A:}, ionisation crosssection{Si:.2e}')
            pressure = np.random.normal(loc=p,
                                        scale=0.01*pv*p,
                                        size=1)
            bi = BeamIonElement(ion_mass=A*m_p,
                    ion_charge=e,
                    ionization_cross_section=Si,
                    residual_gas_density=pressure,
                    ring=ring,
                    ion_field_model=ion_field_model,
                    electron_field_model=electron_field_model,
                    ion_element_length=ring.L/n_segments,
                    )

            ion_aperture = ElipticalAperture(5*beam[0]['x'].std(),
                                              5*beam[0]['y'].std(),
                                              delete_particles=True)
            bi.apertures.append(ion_aperture)
            if i  == 0:
                ion_monitor = IonMonitor(save_every=1, buffer_size=416*n_turns//10,
                                     total_size=416*n_turns, file_name=folder +
                                         f'ion_monitor_{A}' + appendix + '.hdf5')
                bi.monitors.append(ion_monitor)
            beam_ion_elements.append(bi)

    return beam_ion_elements

if __name__ == "__main__":
    sys.exit()
