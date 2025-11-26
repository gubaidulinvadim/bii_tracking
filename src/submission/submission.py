#!/usr/bin/env python
"""Submit a beam-ion instability simulation job using a TOML configuration file.

DEPRECATION WARNING: This script is deprecated. Please use 'jobsmith submit' instead.

New usage:
    jobsmith submit --config_file config.toml

This script is maintained for backward compatibility only.
"""

import argparse
import os
import sys
import warnings

# Add parent directory to path for jobsmith import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobsmith import Job, Submitter, submit
from jobsmith.utils import load_config, validate_config


# Legacy functions for backward compatibility
def get_command_string(config_file: str, script_name: str) -> str:
    """Generate the command string for running the simulation script.

    DEPRECATED: Use jobsmith.Submitter._get_command_string instead.
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


if __name__ == '__main__':
    warnings.warn(
        "submission.py is deprecated. Please use 'jobsmith submit' instead.",
        DeprecationWarning,
        stacklevel=2
    )

    parser = argparse.ArgumentParser(
        description="Submit a beam-ion instability simulation job using a TOML configuration file.\n\n"
                    "DEPRECATED: Please use 'jobsmith submit --config_file config.toml' instead.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--config_file', action='store', metavar='CONFIG_FILE',
                        type=str, required=True,
                        help='Path to the .toml configuration file.')
    args = parser.parse_args()

    # Use the new jobsmith interface
    submit(args.config_file)
