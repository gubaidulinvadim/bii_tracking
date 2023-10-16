import argparse
import numpy as np
from scipy.constants import pi, c
###


@np.vectorize
def f_ions(n, omega_I, n_empty=1, L_sep=0.85, n_gaps=1, h_rf=416, N_ions=30, approximation='exp'):
    k = np.linspace(0, n-1, n, dtype=np.int64)
    if approximation == "arctan":
        f = N_ions*(h_rf//n_gaps-n_empty) * \
            np.sum((2/pi*np.arctan((omega_I*n_empty*L_sep/(2*c))**-1))**k)
    elif approximation == 'exp':
        L_diff = c/(omega_I/(2*pi))
        f = N_ions*(h_rf//n_gaps-n_empty) * \
            np.sum(np.exp(-k*n_empty*L_sep/L_diff))
    else:
        f = 0
    return f


def get_parser_for_bii():
    parser = argparse.ArgumentParser(
        description="A script to track beam-ion instability in a light source storage ring. Source code is available at https://github.com/gubaidulinvadim/PyHEADTAIL\n" +
        "If you are using this script please cite the following:\n" +
        "V. Gubaidulin, A. Gamelin, and R. Nagaoka, 'Beam-ion Instabilities and Their Mitigation for SOLEIL II', Proc. of IPAC'23, Venice, Italy, 2023, paper WEPA004.\n" +
        "Oeftiger, A. (2019). An Overview of PyHEADTAIL, Tech. rep. CERN-ACC-NOTE-2019-0013. https://cds.cern.ch/record/2672381\n")
    parser.add_argument('--n_macroparticles', action='store', metavar='N_MACRO', type=int,
                        default=int(5e3), help='Number of electron macroparticles in a bunch')
    parser.add_argument('--gap_length', action='store', metavar='GAP_LENGTH', type=int,
                        default=1, help='Gap length as a multiple of rf bucket length')
    parser.add_argument('--n_gaps', action='store', metavar='N_GAPS', type=int,
                        default=4, help='Number of gaps symmetrically distributed along the ring')
    parser.add_argument('--is_smooth', action='store', type=str,
                        default='True', help='A flag for smooth focusing approximation')
    parser.add_argument('--n_segments', action='store', metavar='N_SEGMENTS', type=int, default=25,
                        help='Number of segments used for transverse tracking (same as the number of ion elements)')
    parser.add_argument('--h_rf', action='store', metavar='H_RF', type=int, default=416,
                        help='rf harmonic, number of bunches without gaps is hardcoded such that every rf bucket is filled')
    parser.add_argument('--interaction_model_ions', action='store', metavar='INT_MODEL', type=str, default='weak',
                        help='Interaction model used to compute the effect of ion electromagnetic field on electrons. The following values are allowed ["strong", "weak", "PIC"]')
    parser.add_argument('--charge_variation', action='store',
                        metavar='CHARGE_VARIATION', type=float, default=0,
                        help='Gaussian charge variation standard deviation in percents. 0 would mean no variation. Defaults to 0.')
    parser.add_argument('--pressure_variation', action='store',
                        metavar='PRESSURE_VARIATION', type=float, default=0,
                        help='Gaussian residual gas pressure variation standard deviation in percents. 0 would mean no variation. Defaults to 0.')
    parser.add_argument('--average_pressure', action='store',
                        metavar='AVERAGE_PRESSURE', type=float, default=2.4e13,
                        help='Average residual gas density. Defaults to 2.4e13.')
    parser.add_argument('--beam_current', action='store', metavar='BEAM_CURRENT',
                        type=float, default=500e-3, help='Total beam current. Defaults to 500 mA.')
    parser.add_argument('--ion_mass', action='store', metavar='A', type=int, default=28,
                        help='Ion molecular mass in a.u.')
    parser.add_argument('--sigma_i', action='store', metavar='SIMGA_I', type=float, default=1.78e-22,
                        help='Ionisation cross-section in m^2.')
    return parser
