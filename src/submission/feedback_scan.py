
import os
import numpy as np
for feedback_tau in range(60, 10, -10):
# feedback_tau = '515'
    for n_gaps, gap_length in [(4,2), (4, 4), (8, 2), (8, 4)]: 
        os.system(f'python submission.py --feedback_tau {feedback_tau} --job_name {n_gaps}x{gap_length}gap_{feedback_tau}FBT --is_gpu 0 --sub_mode ccrt --job_time 80000 --n_turns 1000 --is_smooth True --gap_length {gap_length} --n_gaps {n_gaps} --n_segments 5 --charge_variation 0.0  --average_pressure 2.9e12 --beam_current 200e-3 --ion_mass 44 --sigma_i 2.79e-22')
        os.system(f'python submission.py --feedback_tau {feedback_tau} --job_name {n_gaps}x{gap_length}gap_{feedback_tau}FBT --is_gpu 0 --sub_mode ccrt --job_time 80000 --n_turns 1000 --is_smooth True --gap_length {gap_length} --n_gaps {n_gaps} --n_segments 5 --charge_variation 0.0  --average_pressure 2.9e12 --beam_current 100e-3 --ion_mass 44 --sigma_i 2.79e-22')

feedback_tau = 0
for current in np.linspace(500e-3, 50e-3, 10):
    for n_gaps, gap_length in [(4, 1)]:
        os.system(f'python submission.py --feedback_tau {feedback_tau} --job_name {n_gaps}x{gap_length}gap_{feedback_tau}FBT --is_gpu 0 --sub_mode ccrt --job_time 80000 --n_turns 1000 --is_smooth True --gap_length {gap_length} --n_gaps {n_gaps} --n_segments 5 --charge_variation 0.0  --average_pressure 2.9e12 --beam_current {current:.1e} --ion_mass 44 --sigma_i 2.79e-22')
