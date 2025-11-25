import argparse
import json
import os
import sys

# Add parent directory to path for config module import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_toml_config, merge_config_and_args

pypath = os.getenv('PYTHONPATH', '')
pypath = pypath + ':/home/dockeruser/machine_data'
os.environ['PYTHONPATH'] = pypath

# Main parameters for the simulation
PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
# path of the folder where to store the simulation results/data and some of the input
FOLDER_PATH = '/home/dockeruser/bii_tracking/'


def run(n_macroparticles=int(5e3),
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
        sigma_i=[1.78e-22],
        feedback_tau=0,
        chromaticity=[0, 0],
        sc=False,
        emittance_ratio=0.3,
        code='pyht'):
    if code == 'pyht':
        import pyht_context as context
    elif code == 'mbtrack2':
        import mbtrack2_context as context
    else:
        raise ValueError(f"Unknown code '{code}'. Supported codes are 'pyht' \
        and 'mbtrack2'.")
    context.run(n_macroparticles=n_macroparticles,
                gap_length=gap_length,
                n_turns=n_turns,
                n_segments=n_segments,
                n_gaps=n_gaps,
                h_rf=h_rf,
                ion_field_model=ion_field_model,
                electron_field_model=electron_field_model,
                smooth=smooth,
                charge_variation=charge_variation,
                pressure_variation=pressure_variation,
                average_pressure=average_pressure,
                beam_current=beam_current,
                ion_mass=ion_mass,
                sigma_i=sigma_i,
                chromaticity=chromaticity,
                sc=sc,
                feedback_tau=feedback_tau,
                emittance_ratio=emittance_ratio)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Track beam-ion instability in a light source storage ring.

Supports both CLI arguments and TOML configuration files. CLI arguments
override values from the config file. If no config file is provided,
all simulation parameters must be specified via CLI or will use defaults.

Example usage:
  # Using config file only:
  python track_bii.py --config config.toml

  # Using config file with CLI overrides:
  python track_bii.py --config config.toml --n_turns 5000 --beam_current 0.3

  # Using CLI arguments only (without config file):
  python track_bii.py --n_macroparticles 10000 --n_turns 3000 --code mbtrack2
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Config file argument (optional, for backward compatibility)
    parser.add_argument('-c', '--config', metavar='CONFIG_FILE', type=str,
                        default=None,
                        help='Path to TOML configuration file. CLI args override config values.')

    # Legacy config_file argument for backward compatibility
    parser.add_argument('--config_file', metavar='CONFIG_FILE', type=str,
                        default=None,
                        help='(Deprecated) Alias for --config. Use --config instead.')

    # Simulation parameters - all optional with defaults
    parser.add_argument('--n_macroparticles', type=int, default=None,
                        help='Number of macroparticles per electron bunch (default: 5000)')
    parser.add_argument('--gap_length', type=int, default=None,
                        help='Gap length as multiple of RF bucket length (default: 1)')
    parser.add_argument('--n_turns', type=int, default=None,
                        help='Number of turns to simulate (default: 3000)')
    parser.add_argument('--n_segments', type=int, default=None,
                        help='Number of segments for transverse tracking (default: 50)')
    parser.add_argument('--n_gaps', type=int, default=None,
                        help='Number of gaps symmetrically distributed (default: 4)')
    parser.add_argument('--h_rf', type=int, default=None,
                        help='RF harmonic number (default: 416)')
    parser.add_argument('--ion_field_model', type=str, default=None,
                        choices=['weak', 'strong', 'PIC'],
                        help='Ion field model (default: weak)')
    parser.add_argument('--electron_field_model', type=str, default=None,
                        choices=['weak', 'strong', 'PIC'],
                        help='Electron field model (default: strong)')
    parser.add_argument('--smooth', type=bool, default=None,
                        help='Use smooth focusing approximation (default: True)')
    parser.add_argument('--is_smooth', type=bool, default=None,
                        help='Alias for --smooth (for config file compatibility)')
    parser.add_argument('--charge_variation', type=float, default=None,
                        help='Charge variation std dev in percent (default: 0.0)')
    parser.add_argument('--pressure_variation', type=json.loads, default=None,
                        help='Pressure variation per species as JSON array (default: [0.0])')
    parser.add_argument('--average_pressure', type=json.loads, default=None,
                        help='Average residual gas density per species as JSON array (default: [3.9e12])')
    parser.add_argument('--beam_current', type=float, default=None,
                        help='Total beam current in Amperes (default: 0.5)')
    parser.add_argument('--ion_mass', type=json.loads, default=None,
                        help='Ion molecular mass per species as JSON array (default: [28])')
    parser.add_argument('--sigma_i', type=json.loads, default=None,
                        help='Ionization cross-section per species as JSON array (default: [1.78e-22])')
    parser.add_argument('--feedback_tau', type=float, default=None,
                        help='Feedback damping time in turns, 0=no feedback (default: 0)')
    parser.add_argument('--chromaticity', type=json.loads, default=None,
                        help='Chromaticity [horizontal, vertical] as JSON array (default: [0, 0])')
    parser.add_argument('--sc', type=bool, default=None,
                        help='Enable space charge effects (default: False)')
    parser.add_argument('--emittance_ratio', type=float, default=None,
                        help='Emittance ratio (default: 0.3)')
    parser.add_argument('--code', type=str, default=None,
                        choices=['pyht', 'mbtrack2'],
                        help='Simulation backend (default: pyht)')

    args = parser.parse_args()

    # Default configuration values
    defaults = {
        'n_macroparticles': 5000,
        'gap_length': 1,
        'n_turns': 3000,
        'n_segments': 50,
        'n_gaps': 4,
        'h_rf': 416,
        'ion_field_model': 'weak',
        'electron_field_model': 'strong',
        'smooth': True,
        'charge_variation': 0.0,
        'pressure_variation': [0.0],
        'average_pressure': [3.9e12],
        'beam_current': 0.5,
        'ion_mass': [28],
        'sigma_i': [1.78e-22],
        'feedback_tau': 0,
        'chromaticity': [0, 0],
        'sc': False,
        'emittance_ratio': 0.3,
        'code': 'pyht'
    }

    # Determine which config file to use (--config takes precedence over --config_file)
    config_path = args.config if args.config else args.config_file

    # Load config from file if provided
    if config_path:
        full_config = load_toml_config(config_path)

        # Support both 'script' section (for backward compatibility) and flat structure
        if 'script' in full_config:
            config = full_config['script']
        else:
            config = full_config

        # Handle 'is_smooth' alias from config file
        if 'is_smooth' in config and 'smooth' not in config:
            config['smooth'] = config.pop('is_smooth')
    else:
        config = {}

    # Merge defaults with config, then override with CLI args
    merged = dict(defaults)
    merged.update(config)
    merged = merge_config_and_args(merged, args)

    # Handle 'is_smooth' alias from CLI
    if args.is_smooth is not None:
        merged['smooth'] = args.is_smooth

    run(n_macroparticles=merged['n_macroparticles'],
        n_turns=merged['n_turns'],
        gap_length=merged['gap_length'],
        n_gaps=merged['n_gaps'],
        n_segments=merged['n_segments'],
        smooth=merged['smooth'],
        h_rf=merged['h_rf'],
        ion_field_model=merged['ion_field_model'],
        electron_field_model=merged['electron_field_model'],
        charge_variation=merged['charge_variation'],
        pressure_variation=merged['pressure_variation'],
        average_pressure=merged['average_pressure'],
        beam_current=merged['beam_current'],
        sigma_i=merged['sigma_i'],
        ion_mass=merged['ion_mass'],
        code=merged['code'],
        feedback_tau=merged['feedback_tau'],
        sc=merged['sc'],
        chromaticity=merged['chromaticity'],
        emittance_ratio=merged['emittance_ratio'])

    sys.exit()
