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