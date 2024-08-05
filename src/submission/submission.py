import os, sys

sys.path.append('../')
from simulation.utils import get_parser_for_bii


def get_command_string(script_name,
                       is_smooth,
                       n_turns,
                       gap_length,
                       n_gaps,
                       ion_field_model,
                       n_segments,
                       charge_variation,
                       pressure_variation,
                       average_pressure,
                       beam_current,
                       ion_mass,
                       sigma_i,
                       feedback_tau):
    command_string = f'python {script_name:} ' + \
        f'--n_turns {n_turns} ' +\
        f'--is_smooth {is_smooth:} '+f'--gap_length {gap_length:} ' +\
        f'--n_gaps {n_gaps:} ' + f'--ion_field_model {ion_field_model:} ' +\
        f'--n_segments {n_segments:} ' + f'--charge_variation {charge_variation:} ' +\
        f'--pressure_variation {pressure_variation:} ' + f'--average_pressure {average_pressure[0]:} ' +\
        f'--beam_current {beam_current:} ' + \
        f'--ion_mass {ion_mass[0]:} ' + f'--sigma_i {sigma_i[0]:.2e} '+\
        f'--feedback_tau {feedback_tau:} '+\
        '\n'
    return command_string


def write_tmp_submission_script(mode,
                                is_gpu,
                                job_name,
                                job_time,
                                n_turns,
                                is_smooth,
                                gap_length,
                                n_gaps,
                                ion_field_model,
                                n_segments,
                                charge_variation,
                                pressure_variation,
                                average_pressure,
                                beam_current,
                                ion_mass,
                                sigma_i,
                                feedback_tau,
                                code):
    script_name = '/home/dockeruser/bii_tracking/src/simulation/track_bii.py'
    command_string = get_command_string(script_name,
                                        is_smooth,
                                        n_turns,
                                        gap_length,
                                        n_gaps,
                                        ion_field_model,
                                        n_segments,
                                        charge_variation,
                                        pressure_variation,
                                        average_pressure,
                                        beam_current,
                                        ion_mass,
                                        sigma_i,
                                        feedback_tau)
    machine_data_folder = "/ccc/work/cont003/soleil/gubaiduv/machine_data"
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        if mode == 'ccrt':
            src_folder = '/ccc/work/cont003/soleil/gubaiduv/bii_tracking'
            f.write("#MSUB -m work,scratch\n")
            if is_gpu:
                f.write("#MSUB -q a100\n")
                image_name = 'pycompletecuda'
            else:
                f.write("#MSUB -q milan\n")
                if code=='pyht':
                    image_name = 'pycomplete'
                elif code=='mbtrack2':
                    image_name = 'mbtrack2_ions'
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
                    "ccc_mprun -C {0:} -E'--ctr-mount src={1:};,dst=/home/dockeruser/bii_tracking:src={2:},dst=/home/dockeruser/machine_data' -E'--ctr-module nvidia' -- ".format(
                        image_name,
                        src_folder,
                        machine_data_folder)
                    + command_string)
            else:
                f.write(
                    "ccc_mprun -C {0:} -E'--ctr-mount src={1:},dst=/home/dockeruser/bii_tracking:src={2:},dst=/home/dockeruser/machine_data' -- ".format(
                        image_name,
                        src_folder,
                        machine_data_folder)
                    + command_string)
        elif mode == 'slurm':
            mount_folder = '/lustre/scratch/sources/physmach/gubaidulin/bii_tracking:/home/dockeruser/bii_tracking'
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
                                args.n_turns,
                                args.is_smooth,
                                args.gap_length,
                                args.n_gaps,
                                args.ion_field_model,
                                args.n_segments,
                                args.charge_variation,
                                args.pressure_variation,
                                args.average_pressure,
                                args.beam_current,
                                args.ion_mass,
                                args.sigma_i,
                                args.feedback_tau,
                                args.code)
    if args.sub_mode == 'ccrt':
        print(args)
        os.system('ccc_msub {:}'.format(args.job_name))
    elif args.sub_mode == 'slurm':
        print(args)
        os.system('sbatch {:}'.format(args.job_name))
    elif args.sub_mode == 'local':
        pass
    os.system('rm -rf {:}'.format(args.job_name))
