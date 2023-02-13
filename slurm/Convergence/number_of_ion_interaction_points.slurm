#!/bin/bash

#SBATCH --job-name=ions_ips
#SBATCH --partition=sumo
#SBATCH --mail-type=begin,end,requeue
#SBATCH --mail-user='gubaidulinvadim@gmail.com'
#SBATCH --time=24:00:00
#SBATCH --array=0-11
#SBATCH --export=ALL
#SBATCH --error=/home/sources/physmach/gubaidulin/err/job%J.err
#SBATCH --output=/home/sources/physmach/gubaidulin/out/job%J.out

module load tools/python/anaconda3
export PYTHONPATH='/home/sources/physmach/gubaidulin/PyHEADTAIL/'
export PYTHONPATH=${PYTHONPATH}:'/home/sources/physmach/gubaidulin/'

FILE='/home/sources/physmach/gubaidulin/fbii_pyht_tracking/track_convergence_ion_points.py'
python ${FILE} ${SLURM_ARRAY_TASK_ID}