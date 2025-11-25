import argparse
import os
import sys
import tomllib

pypath = os.getenv('PYTHONPATH', '')
pypath = pypath + ':/home/dockeruser/machine_data'
os.environ['PYTHONPATH'] = pypath

# Main parameters for the simulation
PHI_RF = 0  # RF phase, just leave it here, if you are above transition energy
# path of the folder where to store the simulation results/data and some of the input
FOLDER_PATH = '/home/dockeruser/bii_tracking/'


def load_config(config_file: str) -> dict:
    """Load and parse a .toml configuration file.

    Args:
        config_file: Path to the .toml configuration file.

    Returns:
        Parsed configuration dictionary.

    Raises:
        SystemExit: If the configuration file is not found or invalid.
    """
    try:
        with open(config_file, 'rb') as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except tomllib.TOMLDecodeError as e:
        print(f"Error: Invalid TOML in '{config_file}': {e}")
        sys.exit(1)


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
        description="Track beam-ion instability in a light source storage ring using a TOML configuration file."
    )
    parser.add_argument('--config_file', action='store', metavar='CONFIG_FILE',
                        type=str, default='config.toml',
                        help='Configuration file in the TOML format (default: config.toml).')
    args = parser.parse_args()

    full_config = load_config(args.config_file)

    if 'script' not in full_config:
        print(f"Error: Configuration file '{args.config_file}' must contain a [script] section.")
        sys.exit(1)

    config = full_config['script']

    run(n_macroparticles=config['n_macroparticles'],
        n_turns=config['n_turns'],
        gap_length=config['gap_length'],
        n_gaps=config['n_gaps'],
        n_segments=config['n_segments'],
        smooth=config['is_smooth'],
        h_rf=config['h_rf'],
        ion_field_model=config['ion_field_model'],
        electron_field_model=config['electron_field_model'],
        charge_variation=config['charge_variation'],
        pressure_variation=config['pressure_variation'],
        average_pressure=config['average_pressure'],
        beam_current=config['beam_current'],
        sigma_i=config['sigma_i'],
        ion_mass=config['ion_mass'],
        code=config['code'],
        feedback_tau=config['feedback_tau'],
        sc=config.get('sc', False),
        chromaticity=config.get('chromaticity', [0, 0]),
        emittance_ratio=config.get('emittance_ratio', 0.3))

    sys.exit()
