import argparse


def get_parser_for_bii():
    parser = argparse.ArgumentParser(
        description="A script to track beam-ion instability in a light source storage ring. Source code is available at https://github.com/gubaidulinvadim/PyHEADTAIL\n" +
        "If you are using this script please cite the following:\n" +
        "V. Gubaidulin, A. Gamelin, and R. Nagaoka, 'Beam-ion Instabilities and Their Mitigation for SOLEIL II', Proc. of IPAC'23, Venice, Italy, 2023, paper WEPA004.\n" +
        "Oeftiger, A. (2019). An Overview of PyHEADTAIL, Tech. rep. CERN-ACC-NOTE-2019-0013. https://cds.cern.ch/record/2672381\n")
    parser.add_argument('--n_macroparticles', action='store', metavar='N_MACRO', type=int,
                        default=int(1e4), help='Number of electron macroparticles in a bunch')
    parser.add_argument('--gap_length', action='store', metavar='GAP_LENGTH', type=int,
                        default=1, help='Gap length as a multiple of rf bucket length')
    parser.add_argument('--n_gaps', action='store', metavar='N_GAPS', type=int,
                        default=4, help='Number of gaps symmetrically distributed along the ring')
    parser.add_argument('--is_smooth', action='store', metavar='IS_SMOOTH', type=bool,
                        default=True, help='A flag for smooth focusing approximation')
    parser.add_argument('--n_segments', action='store', metavar='N_SEGMENTS', type=int, default=25,
                        help='Number of segments used for transverse tracking (same as the number of ion elements)')
    parser.add_argument('--h_rf', action='store', metavar='H_RF', type=int, default=416,
                        help='rf harmonic, number of bunches without gaps is hardcoded such that every rf bucket is filled')
    parser.add_argument('--interaction_model_ions', action='store', metavar='INT_MODEL', type=str, default='weak',  nargs=1,
                        help='Interaction model used to compute the effect of ion electromagnetic field on electrons. The following values are allowed ["strong", "weak", "PIC"]')
    return parser
