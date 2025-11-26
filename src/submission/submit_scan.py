#!/usr/bin/env python
"""Generic parameter scan submission script.

DEPRECATION WARNING: This script is deprecated. Please use 'jobsmith submit-scan' instead.

New usage:
    jobsmith submit-scan --config_file scan_config.toml
    jobsmith submit-scan --config_file scan_config.toml --dry-run
    jobsmith submit-scan --config_file scan_config.toml --keep-configs

This script is maintained for backward compatibility only.

The [scan] section can contain any parameter from [script]. Each parameter
can be specified as:
    - An explicit array: [10, 20, 30, 40, 50]
    - A range specification: {start = 0.1, stop = 0.5, num = 5}

When multiple parameters are scanned, all combinations are submitted.
"""

import argparse
import os
import sys
import warnings

# Add parent directory to path for jobsmith import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobsmith import submit_scan
from jobsmith.scan import expand_scan_values, generate_scan_configs


def main():
    """Main entry point for the scan submission script."""
    warnings.warn(
        "submit_scan.py is deprecated. Please use 'jobsmith submit-scan' instead.",
        DeprecationWarning,
        stacklevel=2
    )

    parser = argparse.ArgumentParser(
        description="Submit a parameter scan using a TOML configuration file.\n\n"
                    "DEPRECATED: Please use 'jobsmith submit-scan --config_file scan_config.toml' instead.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--config_file', action='store', metavar='CONFIG_FILE',
                        type=str, required=True,
                        help='Path to the .toml configuration file with [scan] section.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print jobs that would be submitted without actually submitting.')
    parser.add_argument('--keep-configs', action='store_true',
                        help='Keep generated config files after submission (default: remove them).')
    args = parser.parse_args()

    # Use the new jobsmith interface
    submit_scan(
        args.config_file,
        dry_run=args.dry_run,
        keep_configs=args.keep_configs
    )


if __name__ == '__main__':
    main()
