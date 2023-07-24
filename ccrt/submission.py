import os
from utils import get_parser_for_bii


def write_tmp_submission_script_ccrt(job_name, is_smooth, gap_length, n_gaps, interaction_model_ions):
    MOUNT_FOLDER = '/ccc/work/cont003/soleil/gubaiduv/fbii_pyht_tracking:/home/dockeruser/fbii_pyht_tracking'
    IMAGE_NAME = 'pycomplete'
    SCRIPT_NAME = 'fbii_pyht_tracking/track_bii.py'
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#MSUB -m work,scratch\n")
        f.write("#MSUB -q milan\n")
        f.write("#MSUB -Q long\n")
        f.write("#MSUB -n 1\n")
        f.write("#MSUB -c 16\n")
        f.write("#MSUB -T 150000\n")
        f.write("#MSUB -A soleil\n")
        f.write("#MSUB -@ gubaidulinvadim@gmail.com:begin,end,requeue\n")
        f.write(
            "#MSUB -o /ccc/cont003/home/soleil/gubaiduv/{0:}_%I.err\n".format(job_name))
        f.write(
            "#MSUB -e /ccc/cont003/home/soleil/gubaiduv/{0:}_%I.out\n".format(job_name))
        f.write(
            "pcocc run --mount {0:}  -I {1:} --entry-point -- python {2:} --is_smooth {3:} --gap_length {4:} --n_gaps {5:} --interaction_model_ions {6:}\n".format(MOUNT_FOLDER,
                                                                                                                                                                   IMAGE_NAME,
                                                                                                                                                                   SCRIPT_NAME,
                                                                                                                                                                   is_smooth,
                                                                                                                                                                   gap_length,
                                                                                                                                                                   n_gaps,
                                                                                                                                                                   interaction_model_ions))


def write_submission_script_slurm(job_name, is_smooth, gap_length, n_gaps, interaction_model_ions):
    MOUNT_FOLDER = '/lustre/scratch/sources/physmach/gubaidulin/fbii_pyht_tracking:/home/dockeruser/fbii_pyht_tracking'
    IMAGE_NAME = '/lustre/scratch/sources/physmach/gubaidulin/pycomplete.sif'
    SCRIPT_NAME = '/home/dockeruser/fbii_pyht_tracking/track_bii.py'
    with open(job_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --partition sumo\n")
        f.write("#SBATCH -n 8\n")
        f.write("#SBATCH --time={:}\n".format(job_time))
        f.write('#SBATCH --export=ALL\n')
        f.write("#SBATCH --mail-user='gubaidulinvadim@gmail.com'\n")
        f.write('#SBATCH --mail-type=begin,end,requeue\n')
        f.write(
            "#SBATCH --error=/home/sources/physmach/gubaidulin/err/{0:}_%I.err\n".format(job_name))
        f.write(
            "singularity exec --no-home --B {0:} {1:} python {2:} --is_smooth {3:} --gap_length {4:} --n_gaps {5:} --interaction_model_ions {6:}\n".format(MOUNT_FOLDER,
                                                                                                                                                           IMAGE_NAME,
                                                                                                                                                           SCRIPT_NAME,
                                                                                                                                                           is_smooth,
                                                                                                                                                           gap_length,
                                                                                                                                                           n_gaps,
                                                                                                                                                           interaction_model_ions))
    return job_name


if __name__ == '__main__':
    parser = get_parser_for_bii()
    parser.add_argument('--job_name', action='store', metavar='JOB_NAME', type=str, default='job',
                        help='Name of the job and associated .our and .err files. Defaults to "job"')
    parser.add_argument('--sub_mode', action='store', metavar='SUB_MODE', type=str, default='ccrt',
                        help='Submission mode. Accepted values are ["local", "ccrt", "slurm"], defaults to "ccrt"')
    args = parser.parse_args()
    if args.sub_mode == 'ccrt':
        write_tmp_submission_script_ccrt(args.job_name,
                                         args.is_smooth,
                                         args.gap_length,
                                         args.n_gaps,
                                         args.interaction_model_ions)
        os.system('ccc_msub {:}'.format(args.job_name))
    elif args.sub_mode == 'slurm':
        write_tmp_submission_script_ccrt(args.job_name,
                                         args.is_smooth,
                                         args.gap_length,
                                         args.n_gaps,
                                         args.interaction_model_ions)
        os.system('sbatch {:}'.format(args.job_name))
    elif args.sub_mode == 'local':
        pass
    os.system('rm -rf {:}'.format(args.job_name))
