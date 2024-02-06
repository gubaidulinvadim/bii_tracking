import os

from utils import get_parser_for_bii


def get_command_string(script_name,
                       is_smooth,
                       gap_length,
                       n_gaps,
                       interaction_model_ions,
                       n_segments,
                       charge_variation,
                       pressure_variation,
                       average_pressure,
                       beam_current,
                       ion_mass,
                       sigma_i):
    command_string = f'python {script_name:} ' + \
        f'--is_smooth {is_smooth:} '+f'--gap_length {gap_length:} ' +\
        f'--n_gaps {n_gaps:} ' + f'--interaction_model_ions {interaction_model_ions:} ' +\
        f'--n_segments {n_segments:} ' + f'--charge_variation {charge_variation:} ' +\
        f'--pressure_variation {pressure_variation:} ' + f'--average_pressure {average_pressure:} ' +\
        f'--beam_current {beam_current:} ' + \
        f'--ion_mass {ion_mass:} ' + f'--sigma_i {sigma_i:.2e}\n'
    return command_string


def write_tmp_submission_script(mode,
                                is_gpu,
                                job_name,
                                job_time,
                                is_smooth,
                                gap_length,
                                n_gaps,
                                interaction_model_ions,
                                n_segments,
                                charge_variation,
                                pressure_variation,
                                average_pressure,
                                beam_current,
                                ion_mass,
                                sigma_i):
    script_name = 'bii_pyht_tracking/track_bii.py'
    command_string = get_command_string(script_name,
                                        is_smooth,
                                        gap_length,
                                        n_gaps,
                                        interaction_model_ions,
                                        n_segments,
                                        charge_variation,
                                        pressure_variation,
                                        average_pressure,
                                        beam_current,
                                        ion_mass,
                                        sigma_i)
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        if mode == 'ccrt':
            src_folder = '/ccc/work/cont003/soleil/gubaiduv/bii_pyht_tracking'
            f.write("#MSUB -m work,scratch\n")
            if is_gpu:
                f.write("#MSUB -q a100\n")
                image_name = 'pycompletecuda'
            else:
                f.write("#MSUB -q milan\n")
                image_name = 'pycomplete'
            f.write("#MSUB -Q long\n")
            f.write("#MSUB -n 1\n")
            f.write("#MSUB -c 32\n")
            f.write("#MSUB -T {:}\n".format(job_time))
            f.write("#MSUB -A soleil\n")
            f.write("#MSUB -@ gubaidulinvadim@gmail.com:begin,end,requeue\n")
            f.write(
                "#MSUB -o /ccc/cont003/home/soleil/gubaiduv/{0:}.err\n".format(job_name))
            f.write(
                "#MSUB -e /ccc/cont003/home/soleil/gubaiduv/{0:}.out\n".format(job_name))
            f.write('module purge\n')
            if is_gpu:
                f.write(
                    "ccc_mprun -C {0:} -E'--ctr-mount src={1:},dst=/home/dockeruser/bii_pyht_tracking' -E'--ctr-module nvidia' -- ".format(
                        image_name,
                        src_folder)
                    + command_string)
            else:
                f.write(
                    "ccc_mprun -C {0:} -E'--ctr-mount src={1:},dst=/home/dockeruser/bii_pyht_tracking' -- ".format(
                        image_name,
                        src_folder)
                    + command_string)
        elif mode == 'slurm':
            mount_folder = '/lustre/scratch/sources/physmach/gubaidulin/bii_pyht_tracking:/home/dockeruser/bii_pyht_tracking'
            image_name = '/lustre/scratch/sources/physmach/gubaidulin/pycompletecuda.sif'
            os.system('module load singularity')
            os.system('module load cuda')

            f.write("#SBATCH --partition sumo\n")
            f.write("#SBATCH -n 24\n")
            f.write("#SBATCH -N 1\n")
            f.write("#SBATCH --time=10000\n".format(job_time))
            f.write('#SBATCH --export=ALL\n')
            if is_gpu:
                f.write('#SBATCH --gres=gpu:1\n')
            else:
                pass
            f.write("#SBATCH --mail-user='gubaidulinvadim@gmail.com'\n")
            f.write('#SBATCH --mail-type=begin,end,requeue\n')
            f.write(
                "#SBATCH --error=/home/sources/physmach/gubaidulin/err/{0:}.err\n".format(job_name))
            f.write(
                "#SBATCH --output=/home/sources/physmach/gubaidulin/out/{0:}.out\n".format(job_name))
            f.write('module load tools/singularity/current\n')
            f.write(
                "singularity exec --no-home --nv -B {0:} {1:} ".format(mount_folder,
                                                                       image_name,
                                                                       )
                + command_string)
    return job_name


if __name__ == '__main__':
    parser = get_parser_for_bii()
    parser.add_argument('--job_name', action='store', metavar='JOB_NAME', type=str, default='job',
                        help='Name of the job and associated .our and .err files. Defaults to "job".')
    parser.add_argument('--job_time', action='store', metavar='JOB_TIME', type=int, default=10000,
                        help='Time allocated to the job. Defaults to 10000.')
    parser.add_argument('--sub_mode', action='store', metavar='SUB_MODE', type=str, default='ccrt',
                        help='Submission mode. Accepted values are ["local", "ccrt", "slurm"], defaults to "ccrt"')
    parser.add_argument('--is_gpu', action='store', metavar='IS_GPU', type=int, default=0,
                        help='GPU flag, integer value 0 or 1. Defaults to 0.')
    args = parser.parse_args()
    write_tmp_submission_script(args.sub_mode,
                                args.is_gpu,
                                args.job_name,
                                args.job_time,
                                args.is_smooth,
                                args.gap_length,
                                args.n_gaps,
                                args.interaction_model_ions,
                                args.n_segments,
                                args.charge_variation,
                                args.pressure_variation,
                                args.average_pressure,
                                args.beam_current,
                                args.ion_mass,
                                args.sigma_i)
    if args.sub_mode == 'ccrt':
        print(args)
        os.system('ccc_msub {:}'.format(args.job_name))
    elif args.sub_mode == 'slurm':
        print(args)
        os.system('sbatch {:}'.format(args.job_name))
    elif args.sub_mode == 'local':
        pass
    # os.system('rm -rf {:}'.format(args.job_name))
