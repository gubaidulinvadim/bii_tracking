import argparse
import os
import sys

from utils import load_config, validate_config


def get_command_string(config_file: str, script_name: str) -> str:
    """Generate the command string for running the simulation script.

    Args:
        config_file: Path to the .toml configuration file.
        script_name: Path to the simulation script.

    Returns:
        Command string to execute the simulation.
    """
    return f'python {script_name} --config_file {config_file}\n'


def write_tmp_submission_script(config: dict, config_file: str) -> str:
    """Write a temporary submission script based on the configuration.

    Args:
        config: Parsed configuration dictionary from .toml file.
        config_file: Path to the .toml configuration file.

    Returns:
        Path to the generated job script.
    """
    env = config.get('environment', {})
    job = config.get('job', {})
    script = config.get('script', {})

    server = env.get('server', 'ccrt')
    mount_source = env.get('mount_source', ['/ccc/work/cont003/soleil/gubaiduv/bii_tracking/'])
    mount_dest = env.get('mount_destination', ['/home/dockeruser/bii_tracking'])
    image_name = job.get('container', '')

    job_name = job.get('name', 'job')
    job_time = job.get('time', 86000)
    n_cpu = job.get('n_cpu', 24)
    partition = job.get('partition', 'milan')
    err_folder = job.get('err_folder', '/ccc/work/cont003/soleil/gubaiduv/err/')
    out_folder = job.get('out_folder', '/ccc/work/cont003/soleil/gubaiduv/out/')
    is_gpu = job.get('is_gpu', False)

    script_name = script.get('name', '/home/dockeruser/bii_tracking/src/simulation/track_bii.py')
    code = script.get('code', 'mbtrack2')

    command_string = get_command_string(config_file, script_name)
    machine_data_folder = "/ccc/work/cont003/soleil/gubaiduv/machine_data"

    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        if server == 'ccrt':
            src_folder = mount_source[0]
            src_dest = mount_dest[0]
            data_folder = mount_source[1]
            data_dest = mount_dest[1]
            f.write("#MSUB -m work,scratch\n")
            if is_gpu:
                f.write("#MSUB -q a100\n")
            else:
                f.write(f"#MSUB -q {partition}\n")
            f.write("#MSUB -Q long\n")
            f.write("#MSUB -n 1\n")
            f.write(f"#MSUB -c {n_cpu}\n")
            f.write(f"#MSUB -T {job_time}\n")
            f.write("#MSUB -A soldai\n")
            f.write("#MSUB -@ gubaidulinvadim@gmail.com:begin,end,requeue\n")
            f.write(f"#MSUB -o {err_folder}{job_name}.err\n")
            f.write(f"#MSUB -e {out_folder}{job_name}.out\n")
            f.write('module purge\n')
            if is_gpu:
                f.write(
                    f"ccc_mprun -C {image_name} -E'--ctr-mount src={src_folder},dst={src_dest}:src={data_folder},dst={data_dest}' -E'--ctr-module nvidia' -- "
                    + command_string)
            else:
                f.write(
                    f"ccc_mprun -C {image_name} -E'--ctr-mount src={src_folder},dst={src_dest}:src={data_folder},dst={data_dest}' -- "
                    + command_string)
        elif server == 'slurm':
            mount_folder = '/lustre/scratch/sources/physmach/gubaidulin/bii_tracking:/home/dockeruser/bii_tracking'
            slurm_image_name = '/lustre/scratch/sources/physmach/gubaidulin/pycompletecuda.sif'
            os.system('module load singularity')
            os.system('module load cuda')

            f.write(f"#SBATCH --partition {partition}\n")
            f.write(f"#SBATCH -n {n_cpu}\n")
            f.write("#SBATCH -N 1\n")
            f.write(f"#SBATCH --time={job_time}\n")
            f.write('#SBATCH --export=ALL\n')
            if is_gpu:
                f.write('#SBATCH --gres=gpu:1\n')
            f.write("#SBATCH --mail-user='gubaidulinvadim@gmail.com'\n")
            f.write('#SBATCH --mail-type=begin,end,requeue\n')
            f.write(f"#SBATCH --error={err_folder}{job_name}.err\n")
            f.write(f"#SBATCH --output={out_folder}{job_name}.out\n")
            f.write('module load tools/singularity/current\n')
            f.write(
                f"singularity exec --no-home --nv -B {mount_folder} {slurm_image_name} "
                + command_string)
    return job_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Submit a beam-ion instability simulation job using a TOML configuration file."
    )
    parser.add_argument('--config_file', action='store', metavar='CONFIG_FILE',
                        type=str, required=True,
                        help='Path to the .toml configuration file.')
    args = parser.parse_args()

    config = load_config(args.config_file)
    validate_config(config, args.config_file)
    
    env = config.get('environment', {})
    job = config.get('job', {})

    server = env.get('server', 'ccrt')
    job_name = job.get('name', 'job')

    write_tmp_submission_script(config, args.config_file)

    if server == 'ccrt':
        print(f"Submitting job '{job_name}' to CCRT...")
        os.system(f'ccc_msub {job_name}')
    elif server == 'slurm':
        print(f"Submitting job '{job_name}' to SLURM...")
        os.system(f'sbatch {job_name}')
    elif server == 'local':
        print(f"Local mode: job script '{job_name}' created but not submitted.")
    else:
        print(f"Unknown server type: {server}")

    os.system(f'rm -rf {job_name}')
