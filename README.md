An example of a tracking script for Fast Beam-Ion Instability. We use our own implementation of beam-ion interaction in PyHEADTAIL code. 
The interactive notebook has several examples built into it:
- A fully linear tracking. Both electron bunch train and ion clouds are assumed to have linear field (and without boundaries). This model corresponds fully to the original analytical estimations.
- Both electron and ion beam are Gaussian. The Bassetti-Erskine formula is used to compute the electric fields and associated beam-ion kicks. The rms size of ion cloud and of an electron bunch are computed and updated for every interaction. 

Both electron bunches and ion cloud are recorded using Monitor classes of PyHEADTAIL. The first beam-ion element also records individual positions of each ion. 

## Configuration

The simulation scripts support both TOML configuration files and CLI arguments. CLI arguments take precedence over configuration file values, allowing you to easily override specific parameters.

### Using a Configuration File

Create a TOML file (see `example_config.toml` for a template) and pass it to the script:

```bash
python src/simulation/track_bii.py --config example_config.toml
python src/simulation/mbtrack2_context.py --config example_config.toml
```

### Overriding Configuration with CLI Arguments

You can override any configuration value using CLI arguments:

```bash
# Use config file but override n_turns and beam_current
python src/simulation/track_bii.py --config example_config.toml --n_turns 5000 --beam_current 0.3
```

### CLI-Only Usage

You can also run the scripts without a configuration file by specifying all parameters via CLI:

```bash
python src/simulation/track_bii.py --n_macroparticles 10000 --n_turns 3000 --code mbtrack2
```

### Available Parameters

Run with `--help` to see all available parameters:

```bash
python src/simulation/track_bii.py --help
```

### Python Version Compatibility

- Python >= 3.11: Uses built-in `tomllib` for TOML parsing
- Python < 3.11: Requires `tomli` package (`pip install tomli`)

## Job Submission with jobsmith

The repository provides `jobsmith` - a unified interface for submitting simulation jobs to HPC clusters (CCRT, SLURM) or running locally.

### Installation

Add the `src` directory to your PYTHONPATH:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/fbii_pyht_tracking/src
```

Or install numpy (required dependency):

```bash
pip install numpy
```

### Using the CLI

**Submit a single job:**

```bash
python -m jobsmith.cli submit --config_file config.toml
```

**Submit a parameter scan:**

```bash
python -m jobsmith.cli submit-scan --config_file scan_config.toml
```

**Preview scan without submitting (dry run):**

```bash
python -m jobsmith.cli submit-scan --config_file scan_config.toml --dry-run
```

**Keep generated config files after submission:**

```bash
python -m jobsmith.cli submit-scan --config_file scan_config.toml --keep-configs
```

### Using the Python API

```python
from jobsmith import Job, Submitter, submit, submit_scan

# Submit a single job from config file
submit("config.toml")

# Or use the object-oriented API
job = Job.from_toml("config.toml")
submitter = Submitter(server="ccrt")
submitter.submit(job)

# Submit a parameter scan
submit_scan("scan_config.toml", dry_run=False)
```

### Configuration File Format

Configuration files use TOML format with three main sections:

```toml
[environment]
container = "soleil-pa:mbtrack2dev"
mount_source = ["/path/to/source/"]
mount_destination = ["/path/to/dest/"]
server = "ccrt"  # or "slurm" or "local"

[job]
name = "my_simulation"
time = 86000
n_cpu = 24
partition = "milan"

[script]
name = "/path/to/track_bii.py"
n_macroparticles = 10000
n_turns = 3000
# ... other simulation parameters
```

For parameter scans, add a `[scan]` section:

```toml
[scan]
# Explicit array of values
beam_current = [0.1, 0.2, 0.3, 0.4, 0.5]

# Or use a range specification (linspace)
feedback_tau = {start = 10, stop = 100, num = 10}
```

See `src/submission/example_config.toml` and `src/submission/example_scan_config.toml` for complete examples.

### Migration from Old Submission Scripts

The old submission scripts (`submission/submission.py`, `submission/submit_scan.py`) are deprecated but still work for backward compatibility. Please migrate to `jobsmith`:

| Old Way (Deprecated) | New Way (Recommended) |
|---------------------|----------------------|
| `python submission/submission.py --config_file config.toml` | `python -m jobsmith.cli submit --config_file config.toml` |
| `python submission/submit_scan.py --config_file scan_config.toml` | `python -m jobsmith.cli submit-scan --config_file scan_config.toml` |
| `from submission.utils import load_config` | `from jobsmith.utils import load_config` |
| `from submission import submit_scan` | `from jobsmith import submit_scan` |