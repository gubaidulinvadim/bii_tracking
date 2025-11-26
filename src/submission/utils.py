"""Backward compatibility module for submission utilities.

DEPRECATION WARNING: This module is deprecated. Please use 'jobsmith.utils' instead.

Migration:
    # Old way (deprecated):
    from submission.utils import load_config, validate_config, write_toml

    # New way (recommended):
    from jobsmith.utils import load_config, validate_config, write_toml
"""

import sys
import warnings

# Issue deprecation warning when this module is imported
warnings.warn(
    "submission.utils is deprecated. Please use 'jobsmith.utils' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Try to import from jobsmith - it should be available if src is in PYTHONPATH
try:
    from jobsmith.utils import write_toml, load_config, validate_config
except ImportError:
    # Fallback: add parent directory to path
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from jobsmith.utils import write_toml, load_config, validate_config

__all__ = ["write_toml", "load_config", "validate_config"]
