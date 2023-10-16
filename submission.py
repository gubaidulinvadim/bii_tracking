import os
from utils import get_parser_for_bii


def write_tmp_submission_script_ccrt(job_name,
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
    MOUNT_FOLDER = '/ccc/work/cont003/soleil/gubaiduv/fbii_pyht_tracking:/home/dockeruser/fbii_pyht_tracking'
    IMAGE_NAME = 'pycomplete'
    SCRIPT_NAME = 'fbii_pyht_tracking/track_bii.py'
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#MSUB -m work,scratch\n")
        f.write("#MSUB -q milan\n")
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
        f.write(
            "pcocc run --mount {0:} -I {1:} --entry-point -- python {2:} --is_smooth {3:} --gap_length {4:} --n_gaps {5:} --interaction_model_ions {6:} --n_segments {7:} --charge_variation {8:} --pressure_variation {9:} --average_pressure {10:}\n".format(MOUNT_FOLDER,
                                                                                                                                                                                                                                                               IMAGE_NAME,
                                                                                                                                                                                                                                                               SCRIPT_NAME,
                                                                                                                                                                                                                                                               is_smooth,
                                                                                                                                                                                                                                                               gap_length,
                                                                                                                                                                                                                                                               n_gaps,
                                                                                                                                                                                                                                                               interaction_model_ions,
                                                                                                                                                                                                                                                               n_segments,
                                                                                                                                                                                                                                                               charge_variation,
                                                                                                                                                                                                                                                               pressure_variation,
                                                                                                                                                                                                                                                               average_pressure))


def write_tmp_submission_script_ccrt_gpu(job_name,
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
    MOUNT_FOLDER = '/ccc/work/cont003/soleil/gubaiduv/fbii_pyht_tracking:/home/dockeruser/fbii_pyht_tracking'
    IMAGE_NAME = 'pycompletecuda'
    SCRIPT_NAME = 'fbii_pyht_tracking/track_bii.py'
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#MSUB -m work,scratch\n")
        f.write("#MSUB -q a100\n")
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
        f.write(
            "pcocc run --mount {0:} -M nvidia -I {1:} --entry-point -- python {2:} --is_smooth {3:} --gap_length {4:} --n_gaps {5:} --interaction_model_ions {6:} --n_segments {7:} --charge_variation {8:} --pressure_variation {9:} --average_pressure {10:} --beam_current {11:}\n".format(MOUNT_FOLDER,
                                                                                                                                                                                                                                                                                              IMAGE_NAME,
                                                                                                                                                                                                                                                                                              SCRIPT_NAME,
                                                                                                                                                                                                                                                                                              is_smooth,
                                                                                                                                                                                                                                                                                              gap_length,
                                                                                                                                                                                                                                                                                              n_gaps,
                                                                                                                                                                                                                                                                                              interaction_model_ions,
                                                                                                                                                                                                                                                                                              n_segments,
                                                                                                                                                                                                                                                                                              charge_variation,
                                                                                                                                                                                                                                                                                              pressure_variation,
                                                                                                                                                                                                                                                                                              average_pressure,
                                                                                                                                                                                                                                                                                              beam_current)
        )


def write_submission_script_slurm(job_name,
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
    MOUNT_FOLDER = '/lustre/scratch/sources/physmach/gubaidulin/fbii_pyht_tracking:/home/dockeruser/fbii_pyht_tracking'
    IMAGE_NAME = '/lustre/scratch/sources/physmach/gubaidulin/pycompletecuda.sif'
    SCRIPT_NAME = '/home/dockeruser/fbii_pyht_tracking/track_bii.py'
    os.system('module load singularity')
    os.system('module load cuda')
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --partition sumo\n")
        f.write("#SBATCH -n 24\n")
        f.write("#SBATCH -N 1\n")
        f.write("#SBATCH --time=10000\n".format(job_time))
        f.write('#SBATCH --export=ALL\n')
        f.write('#SBATCH --gres=gpu:1\n')
        f.write("#SBATCH --mail-user='gubaidulinvadim@gmail.com'\n")
        f.write('#SBATCH --mail-type=begin,end,requeue\n')
        f.write(
            "#SBATCH --error=/home/sources/physmach/gubaidulin/err/{0:}.err\n".format(job_name))
        f.write('module load tools/singularity/current\n')
        f.write(
            "singularity exec --no-home --nv -B {0:} {1:} python {2:} --is_smooth {3:} --gap_length {4:} --n_gaps {5:} --interaction_model_ions {6:} --n_segments {7:} --charge_variation {8:} --pressure_variation {9:} --average_pressure {10:} --beam_current {11:}\n".format(MOUNT_FOLDER,
                                                                                                                                                                                                                                                                                 IMAGE_NAME,
                                                                                                                                                                                                                                                                                 SCRIPT_NAME,
                                                                                                                                                                                                                                                                                 is_smooth,
                                                                                                                                                                                                                                                                                 gap_length,
                                                                                                                                                                                                                                                                                 n_gaps,
                                                                                                                                                                                                                                                                                 interaction_model_ions,
                                                                                                                                                                                                                                                                                 n_segments,
                                                                                                                                                                                                                                                                                 charge_variation,
                                                                                                                                                                                                                                                                                 pressure_variation,
                                                                                                                                                                                                                                                                                 average_pressure,
                                                                                                                                                                                                                                                                                 beam_current))
    return job_name


if __name__ == '__main__':
    parser = get_parser_for_bii()
    parser.add_argument('--job_name', action='store', metavar='JOB_NAME', type=str, default='job',
                        help='Name of the job and associated .our and .err files. Defaults to "job"')
    parser.add_argument('--job_time', action='store', metavar='JOB_TIME', type=int, default=10000,
                        help='Time allocated to the job. Defaults to 10000')
    parser.add_argument('--sub_mode', action='store', metavar='SUB_MODE', type=str, default='ccrt',
                        help='Submission mode. Accepted values are ["local", "ccrt", "slurm"], defaults to "ccrt"')
    args = parser.parse_args()
    if args.sub_mode == 'ccrt':
        print(args)
        write_tmp_submission_script_ccrt(args.job_name,
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
        os.system('ccc_msub {:}'.format(args.job_name))
    elif args.sub_mode == 'ccrt_gpu':
        print(args)
        write_tmp_submission_script_ccrt_gpu(args.job_name,
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
        os.system('ccc_msub {:}'.format(args.job_name))
    elif args.sub_mode == 'slurm':
        write_submission_script_slurm(args.job_name,
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
        os.system('sbatch {:}'.format(args.job_name))
    elif args.sub_mode == 'local':
        pass
    os.system('rm -rf {:}'.format(args.job_name))
