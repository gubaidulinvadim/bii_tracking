"""Generic parameter scan submission script.

This script reads a TOML configuration file with a [scan] section that defines
arrays of parameter values to scan over. It generates and submits a separate
job for each combination of parameter values.

Usage:
    python submit_scan.py --config_file scan_config.toml

The [scan] section can contain any parameter from [script]. Each parameter
can be specified as:
    - An explicit array: [10, 20, 30, 40, 50]
    - A range specification: {start = 0.1, stop = 0.5, num = 5}

When multiple parameters are scanned, all combinations are submitted.
"""

import argparse
import copy
import itertools
import subprocess
import sys
import tomllib

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
        elif isinstance(value, (int, float, np.integer, np.floating)):
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


def expand_scan_values(scan_spec) -> list:
    """Expand a scan specification into a list of values.

    Args:
        scan_spec: Either a list of explicit values or a dict with
                   {start, stop, num} for linspace.

    Returns:
        List of values to scan.
    """
    if isinstance(scan_spec, list):
        return scan_spec
    elif isinstance(scan_spec, dict):
        start = scan_spec.get('start', 0)
        stop = scan_spec.get('stop', 1)
        num = scan_spec.get('num', 10)
        return np.linspace(start, stop, num).tolist()
    else:
        return [scan_spec]


def validate_config(config: dict) -> None:
    """Validate that required configuration sections exist.

    Args:
        config: Configuration dictionary to validate.

    Raises:
        SystemExit: If required sections are missing.
    """
    if 'script' not in config:
        print("Error: Configuration file must contain a [script] section.")
        sys.exit(1)
    if 'job' not in config:
        print("Error: Configuration file must contain a [job] section.")
        sys.exit(1)


def generate_scan_configs(base_config: dict) -> list:
    """Generate configurations for all parameter combinations.

    Args:
        base_config: Base configuration with [scan] section.

    Returns:
        List of (job_name, config) tuples for each parameter combination.
    """
    scan_params = base_config.get('scan', {})

    if not scan_params:
        print("Warning: No [scan] section found. Submitting single job.")
        job_name = base_config.get('job', {}).get('name', 'job')
        return [(job_name, base_config)]

    # Expand all scan specifications
    param_names = list(scan_params.keys())
    param_values = [expand_scan_values(scan_params[p]) for p in param_names]

    configs = []
    base_job_name = base_config.get('job', {}).get('name', 'scan')

    # Generate all combinations
    for combo in itertools.product(*param_values):
        # Create a copy of the base config without the scan section
        config = copy.deepcopy(base_config)
        if 'scan' in config:
            del config['scan']

        # Build job name suffix from parameter values
        name_parts = []
        for param, value in zip(param_names, combo):
            # Update script parameter
            config['script'][param] = value
            # Format value for job name
            if isinstance(value, float):
                if value >= 1:
                    name_parts.append(f"{param}_{value:.1f}")
                else:
                    name_parts.append(f"{param}_{value:.3f}")
            else:
                name_parts.append(f"{param}_{value}")

        job_name = f"{base_job_name}_{'_'.join(name_parts)}"
        config['job']['name'] = job_name
        configs.append((job_name, config))

    return configs


def submit_job(config: dict, config_file: str) -> None:
    """Submit a single job using submission.py.

    Args:
        config: Configuration dictionary.
        config_file: Path to save the config file.
    """
    # Write config to a temporary TOML file
    write_toml(config, config_file)

    # Submit using submission.py with subprocess for safety
    subprocess.run(['python', 'submission.py', '--config_file', config_file], check=False)


def main():
    """Main entry point for the scan submission script."""
    parser = argparse.ArgumentParser(
        description="Submit a parameter scan using a TOML configuration file."
    )
    parser.add_argument('--config_file', action='store', metavar='CONFIG_FILE',
                        type=str, required=True,
                        help='Path to the .toml configuration file with [scan] section.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print jobs that would be submitted without actually submitting.')
    args = parser.parse_args()

    config = load_config(args.config_file)
    validate_config(config)
    scan_configs = generate_scan_configs(config)

    print(f"Generated {len(scan_configs)} job(s) from scan configuration.")

    for i, (job_name, job_config) in enumerate(scan_configs, 1):
        if args.dry_run:
            script_section = job_config.get('script', {})
            scan_params = {k: script_section.get(k) for k in config.get('scan', {}).keys()}
            print(f"  [{i}/{len(scan_configs)}] {job_name}: {scan_params}")
        else:
            print(f"Submitting [{i}/{len(scan_configs)}]: {job_name}")
            config_file = f"{job_name}_config.toml"
            submit_job(job_config, config_file)
            # Optionally clean up config file after submission
            # os.remove(config_file)

    if args.dry_run:
        print("\n(Dry run mode - no jobs were submitted)")


if __name__ == '__main__':
    main()
