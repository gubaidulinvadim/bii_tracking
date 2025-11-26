"""Backward compatibility module - delegates to jobsmith.

DEPRECATION WARNING: This module is deprecated. Please use 'jobsmith' instead.

Migration guide:
    # Old way (deprecated):
    from submission import submit_scan
    from submission.utils import load_config

    # New way (recommended):
    from jobsmith import submit_scan
    from jobsmith.utils import load_config

CLI migration:
    # Old way (deprecated):
    python submission/submission.py --config_file config.toml
    python submission/submit_scan.py --config_file scan_config.toml

    # New way (recommended):
    jobsmith submit --config_file config.toml
    jobsmith submit-scan --config_file scan_config.toml
"""

# Re-export everything from the shim for backward compatibility
from submission.shim import (
    Job,
    Submitter,
    submit,
    submit_scan,
    load_config,
    validate_config,
    write_toml,
    expand_scan_values,
    generate_scan_configs,
    get_command_string,
    write_tmp_submission_script,
    submit_job,
)

__all__ = [
    "Job",
    "Submitter",
    "submit",
    "submit_scan",
    "load_config",
    "validate_config",
    "write_toml",
    "expand_scan_values",
    "generate_scan_configs",
    "get_command_string",
    "write_tmp_submission_script",
    "submit_job",
]
