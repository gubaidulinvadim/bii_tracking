"""Backward compatibility shim for the submission module.

DEPRECATION WARNING: The submission module is deprecated and will be removed
in a future release. Please migrate to using jobsmith instead.

Migration guide:
    # Old way (deprecated):
    from submission.submission import write_tmp_submission_script, get_command_string
    from submission.utils import load_config, validate_config, write_toml
    from submission.submit_scan import expand_scan_values, generate_scan_configs

    # New way (recommended):
    from jobsmith import Job, Submitter, submit, submit_scan
    from jobsmith.utils import load_config, validate_config, write_toml
    from jobsmith.scan import expand_scan_values, generate_scan_configs

CLI migration:
    # Old way (deprecated):
    python submission/submission.py --config_file config.toml
    python submission/submit_scan.py --config_file scan_config.toml

    # New way (recommended):
    jobsmith submit --config_file config.toml
    jobsmith submit-scan --config_file scan_config.toml

Installation:
    Add the src directory to your PYTHONPATH:
        export PYTHONPATH=$PYTHONPATH:/path/to/fbii_pyht_tracking/src

    Or install in development mode:
        pip install -e /path/to/fbii_pyht_tracking
"""

import warnings

# Issue deprecation warning when this module is imported
warnings.warn(
    "The 'submission' module is deprecated. Please use 'jobsmith' instead. "
    "See submission/shim.py for migration guide.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export jobsmith components for backward compatibility
from jobsmith import Job, Submitter, submit, submit_scan
from jobsmith.utils import load_config, validate_config, write_toml
from jobsmith.scan import expand_scan_values, generate_scan_configs


def get_command_string(config_file: str, script_name: str) -> str:
    """Generate the command string for running the simulation script.

    DEPRECATED: Use jobsmith.Submitter._get_command_string instead.

    Args:
        config_file: Path to the .toml configuration file.
        script_name: Path to the simulation script.

    Returns:
        Command string to execute the simulation.
    """
    warnings.warn(
        "get_command_string is deprecated. Use jobsmith.Submitter instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return f'python {script_name} --config_file {config_file}\n'


def write_tmp_submission_script(config: dict, config_file: str) -> str:
    """Write a temporary submission script based on the configuration.

    DEPRECATED: Use jobsmith.Submitter.submit instead.

    Args:
        config: Parsed configuration dictionary from .toml file.
        config_file: Path to the .toml configuration file.

    Returns:
        Path to the generated job script.
    """
    warnings.warn(
        "write_tmp_submission_script is deprecated. Use jobsmith.Submitter.submit instead.",
        DeprecationWarning,
        stacklevel=2
    )
    job = Job.from_dict(config)
    job.config_file = config_file
    submitter = Submitter(server=job.server)
    return submitter._write_submission_script(job, config_file)


def submit_job(config: dict, config_file: str) -> None:
    """Submit a single job using the jobsmith interface.

    DEPRECATED: Use jobsmith.submit or jobsmith.Submitter.submit instead.

    Args:
        config: Configuration dictionary.
        config_file: Path to save the config file.
    """
    warnings.warn(
        "submit_job is deprecated. Use jobsmith.submit instead.",
        DeprecationWarning,
        stacklevel=2
    )
    write_toml(config, config_file)
    job = Job.from_dict(config)
    job.config_file = config_file
    submitter = Submitter(server=job.server)
    submitter.submit(job, cleanup=True)


__all__ = [
    # jobsmith classes and functions
    "Job",
    "Submitter",
    "submit",
    "submit_scan",
    "load_config",
    "validate_config",
    "write_toml",
    "expand_scan_values",
    "generate_scan_configs",
    # Legacy functions (deprecated)
    "get_command_string",
    "write_tmp_submission_script",
    "submit_job",
]
