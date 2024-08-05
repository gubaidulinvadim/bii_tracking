import argparse

import numpy as np
from scipy.constants import c, pi
###
from scipy.optimize import curve_fit


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
                        default=int(5e3), help='Number of electron macroparticles in a bunch. ' +
                        'Defaults to 5000.')
    parser.add_argument('--gap_length', action='store', metavar='GAP_LENGTH', type=int,
                        default=1, help='Gap length as a multiple of rf bucket length. ' +
                        'Defaults to 1.')
    parser.add_argument('--n_turns', action='store', metavar='N_TURNS', type=int, default=3000, help='Number of turns. Defaults to 3000.')
    parser.add_argument('--n_gaps', action='store', metavar='N_GAPS', type=int,
                        default=4, help='Number of gaps symmetrically distributed along the ring. ' +
                        'Integer above 0. Defaults to 4.')
    parser.add_argument('--is_smooth', action='store', type=str,
                        default='True', help='A flag for smooth focusing approximation. Defaults to "True".')
    parser.add_argument('--n_segments', action='store', metavar='N_SEGMENTS', type=int, default=25,
                        help='Number of segments used for transverse tracking (same as the number of ion elements). ' +
                        'Defaults to 25.')
    parser.add_argument('--h_rf', action='store', metavar='H_RF', type=int, default=416,
                        help='rf harmonic, number of bunches without gaps is hardcoded such that every rf bucket is filled.')
    parser.add_argument('--ion_field_model', action='store', metavar='IINT_MODEL', type=str, default='strong',
                        help='Interaction model used to compute the effect of ion electromagnetic field on electrons.' +
                        ' The following values are allowed ["strong", "weak", "PIC"].' +
                        ' Defaults to "strong".')
    parser.add_argument('--electron_field_model', action='store', metavar='EINT_MODEL', type=str, default='weak',
                        help='Interaction model used to compute the effect of electron electromagnetic field on ions.' +
                        ' The following values are allowed ["weak", "PIC"].' +
                        ' Defaults to "weak".')
    parser.add_argument('--charge_variation', action='store',
                        metavar='CHARGE_VARIATION', type=float, default=0,
                        help='Gaussian charge variation standard deviation in percents. 0 would mean no variation. Defaults to 0.')
    parser.add_argument('--pressure_variation', action='store',
                        metavar='PRESSURE_VARIATION', type=float, default=0.0, nargs='+',
                        help='Gaussian residual gas pressure variation standard deviation in percents. 0 would mean no variation. Defaults to 0.')
    parser.add_argument('--average_pressure', action='store', nargs='+',
                        metavar='AVERAGE_PRESSURE', type=float, default=3.2e12, 
                        help='Average residual gas density. Defaults to 3.2e12.')
    parser.add_argument('--beam_current', action='store', metavar='BEAM_CURRENT',
                        type=float, default=500e-3, help='Total beam current. Defaults to 500 mA.')
    parser.add_argument('--ion_mass', action='store', metavar='A', type=int, default=28, nargs='+',
                        help='Ion molecular mass in a.u. Defaults to 28.')
    parser.add_argument('--sigma_i', action='store', metavar='SIGMA_I', type=float, default=1.78e-22, nargs='+',
                        help='Ionisation cross-section in m^2. Defaults to 1.78e-22.')
    parser.add_argument('--feedback_tau', action='store', metavar="FBT_GAIN", type=float, default=1.0,
                        help='Damping time of an ideal damper in turns.')
    parser.add_argument('--code', action='store', metavar="CODE", type=str, default='mbtrack2',
                    help='Backend code for the simulations. Currently supports ["mbtrack2", "pyht"].')
    return parser
