#!/bin/bash

#SBATCH --job-name=ions_mp
#SBATCH --partition=sumo
#SBATCH --mail-type=begin,end,requeue
#SBATCH --mail-user='gubaidulinvadim@gmail.com'
#SBATCH --time=24:00:00
#SBATCH --array=0-5
#SBATCH --export=ALL
#SBATCH --error=/home/sources/physmach/gubaidulin/err/job%J.err
#SBATCH --output=/home/sources/physmach/gubaidulin/out/job%J.out

module load tools/python/anaconda3
export PYTHONPATH='/lustre/scratch/sources/physmach/gubaidulin/PyHEADTAIL/'
export PYTHONPATH=${PYTHONPATH}:'/lustre/scratch/sources/physmach/gubaidulin/'

FILE='/lustre/scratch/sources/physmach/gubaidulin/fbii_pyht_tracking/track_convergence_ions.py'
python ${FILE} ${SLURM_ARRAY_TASK_ID}