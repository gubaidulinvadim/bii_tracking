#!/bin/bash

#SBATCH --job-name=FBII_convergence
#SBATCH --partition=sumo
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gubaidulinvadim@gmail.com
#SBATCH --time=20:00:00
#SBATCH --array=0-10
#SBATCH --export=ALL
#SBATCH --error=/home/sources/physmach/gubaidulin/err/job%J.err
#SBATCH --output=/home/sources/physmach/gubaidulin/out/job%J.out

module load tools/python/anaconda3 
export PYTHONPATH='/home/sources/physmach/gubaidulin/PyHEADTAIL/'

FILE='/home/sources/physmach/gubaidulin/fbii_pyht_tracking/weak-strong-ions.py'
python ${FILE} ${SLURM_ARRAY_TASK_ID}