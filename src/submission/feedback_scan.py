"""Feedback scan script that generates TOML config files and submits jobs."""

import os

import numpy as np


def write_toml(data: dict, filepath: str) -> None:
    """Write a dictionary to a TOML file.

    Args:
        data: Dictionary to write.
        filepath: Path to the output file.
    """
    def format_value(value):
        if isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            items = ', '.join(format_value(item) for item in value)
            return f'[{items}]'
        else:
            return str(value)

    with open(filepath, 'w') as f:
        # Write top-level key-value pairs
        for key, value in data.items():
            if not isinstance(value, dict):
                f.write(f'{key} = {format_value(value)}\n')

        # Write sections
        for key, value in data.items():
            if isinstance(value, dict):
                f.write(f'\n[{key}]\n')
                for subkey, subvalue in value.items():
                    f.write(f'{subkey} = {format_value(subvalue)}\n')


def create_config(job_name: str, feedback_tau: float, n_gaps: int, gap_length: int,
                  beam_current: float, job_time: int = 80000, n_turns: int = 1000,
                  n_segments: int = 5) -> dict:
    """Create a configuration dictionary for a simulation.

    Args:
        job_name: Name for the job.
        feedback_tau: Feedback damping time in turns.
        n_gaps: Number of gaps.
        gap_length: Gap length as a multiple of rf bucket length.
        beam_current: Total beam current in Amperes.
        job_time: Job time allocation.
        n_turns: Number of turns.
        n_segments: Number of segments.

    Returns:
        Configuration dictionary.
    """
    return {
        'title': f"Feedback scan: {job_name}",
        'environment': {
            'container': 'soleil-pa:mbtrack2dev',
            'mount_source': ['/ccc/work/cont003/soleil/gubaiduv/bii_tracking/'],
            'mount_destination': ['/home/dockeruser/bii_tracking/'],
            'server': 'ccrt',
        },
        'job': {
            'name': job_name,
            'time': job_time,
            'n_cpu': 24,
            'partition': 'milan',
            'err_folder': '/ccc/work/cont003/soleil/gubaiduv/err/',
            'out_folder': '/ccc/work/cont003/soleil/gubaiduv/out/',
            'is_gpu': False,
        },
        'script': {
            'name': '/home/dockeruser/bii_tracking/src/simulation/track_bii.py',
            'n_macroparticles': 10000,
            'n_turns': n_turns,
            'gap_length': gap_length,
            'n_gaps': n_gaps,
            'n_segments': n_segments,
            'is_smooth': True,
            'h_rf': 416,
            'beam_current': beam_current,
            'ion_field_model': 'weak',
            'electron_field_model': 'weak',
            'charge_variation': 0,
            'pressure_variation': [0],
            'average_pressure': [2.9e12],
            'sigma_i': [2.79e-22],
            'ion_mass': [44],
            'code': 'mbtrack2',
            'feedback_tau': feedback_tau,
        },
    }


def write_and_submit_config(config: dict) -> None:
    """Write config to a TOML file and submit the job.

    Args:
        config: Configuration dictionary.
    """
    job_name = config['job']['name']
    config_file = f"{job_name}_config.toml"

    # Write config to TOML file
    write_toml(config, config_file)

    # Submit the job using the new submission script
    os.system(f'python submission.py --config_file {config_file}')

    # Optionally remove config file after submission (uncomment if desired)
    # os.remove(config_file)


if __name__ == '__main__':
    # Feedback tau scan
    for feedback_tau in range(60, 10, -10):
        for n_gaps, gap_length in [(4, 2), (4, 4), (8, 2), (8, 4)]:
            for beam_current in [200e-3, 100e-3]:
                job_name = f'{n_gaps}x{gap_length}gap_{feedback_tau}FBT_{int(beam_current*1e3)}mA'
                config = create_config(
                    job_name=job_name,
                    feedback_tau=feedback_tau,
                    n_gaps=n_gaps,
                    gap_length=gap_length,
                    beam_current=beam_current,
                )
                write_and_submit_config(config)

    # Current scan with no feedback
    feedback_tau = 0
    for current in np.linspace(500e-3, 50e-3, 10):
        for n_gaps, gap_length in [(4, 1)]:
            job_name = f'{n_gaps}x{gap_length}gap_{feedback_tau}FBT_{int(current*1e3)}mA'
            config = create_config(
                job_name=job_name,
                feedback_tau=feedback_tau,
                n_gaps=n_gaps,
                gap_length=gap_length,
                beam_current=current,
            )
            write_and_submit_config(config)
