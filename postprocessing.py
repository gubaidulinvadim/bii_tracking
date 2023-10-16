
import h5py as hp
import numpy as np
import matplotlib.pyplot as plt

def plot_ion_density(ax, n_ion_macroparticles, n_segments, h_rf=416, n_macroions=30, n_g = 2.4e13, Sigma_I = 1.22e-22, circumference=354, **mpl_kwargs):
    data_length = n_ion_macroparticles.shape[0]
    n_ions_per_bunch = n_g*Sigma_I*circumference/n_segments/n_macroions
    n_bunches_passed = np.linspace(0, data_length/h_rf, int(data_length))
    eta = 100*n_ions_per_bunch*n_ion_macroparticles
    ax.plot(n_bunches_passed, eta, **mpl_kwargs)
    ax.set_xlabel('Time, $t$ (turns)')
    ax.set_ylabel('Neutralisation factor, $\eta$ ($\%$)')
    ax.set_xlim(0, 10)
    return 0

def read_bunch(bunch_number, n_macroparticles, folder):
    filename = folder+'BM(n_bunch={:}).h5'.format(bunch_number)
    file = hp.File(filename)
    mean_x = file['Bunch']['mean_x'][:]
    sigma_x = file['Bunch']['sigma_x'][:]
    mean_xp = file['Bunch']['mean_xp'][:]
    mean_y = file['Bunch']['mean_y'][:]
    sigma_y = file['Bunch']['sigma_y'][:]
    mean_yp = file['Bunch']['mean_yp'][:]
    mean_z = file['Bunch']['mean_z'][:] 
    mean_dp = file['Bunch']['mean_dp'][:]
    mean_x = np.trim_zeros(mean_x)
    mean_xp = np.trim_zeros(mean_xp)
    mean_y = np.trim_zeros(mean_y)
    mean_yp = np.trim_zeros(mean_yp)
    sigma_x = np.trim_zeros(sigma_x)
    sigma_y = np.trim_zeros(sigma_y)
    file.close()
    return mean_x, sigma_x, mean_xp, mean_y, sigma_y, mean_yp, mean_z, mean_dp
def read_bunch_emittance(bunch_number, folder):
    filename = folder+'BM(n_bunch={:}).h5'.format(bunch_number)
    file = hp.File(filename)
    epsn_x = file['Bunch']['epsn_x'][:]
    epsn_y = file['Bunch']['epsn_y'][:] 
    epsn_x = np.trim_zeros(epsn_x)
    epsn_y = np.trim_zeros(epsn_y)
    file.close()
    return epsn_x, epsn_y
def read_ion_element(index, folder):
    filename = folder+'IM(ind={0:}).h5'.format(int(index))
    file = hp.File(filename)
    mean_x = file['Bunch']['mean_x'][:]
    sigma_x = file['Bunch']['sigma_x'][:]
    mean_xp = file['Bunch']['mean_xp'][:]
    mean_y = file['Bunch']['mean_y'][:]
    sigma_y = file['Bunch']['sigma_y'][:]
    mean_yp = file['Bunch']['mean_yp'][:]
    mean_z = file['Bunch']['mean_z'][:]
    mean_dp = file['Bunch']['mean_dp'][:]
    n_ion_macroparticles = file['Bunch']['macroparticlenumber'][:]
    mean_x = np.trim_zeros(mean_x)
    mean_xp = np.trim_zeros(mean_xp)
    mean_y = np.trim_zeros(mean_y)
    mean_yp = np.trim_zeros(mean_yp)
    sigma_x = np.trim_zeros(sigma_x)
    sigma_y = np.trim_zeros(sigma_y)
    file.close()
    return mean_x, sigma_x, mean_xp, mean_y, sigma_y, mean_yp, mean_z, mean_dp, n_ion_macroparticles
def read_ion_particles(index, step, folder):
    filename = folder+'IM(ind={0:}).h5'.format(int(index))
    file = hp.File(filename)
    # for step in range(file['Step']['x'][:])
    mean_x = file['Step#{:}'.format(step)]['x'][:]
    mean_xp = file['Step#{:}'.format(step)]['xp'][:]
    mean_y = file['Step#{:}'.format(step)]['y'][:]
    mean_yp = file['Step#{:}'.format(step)]['yp'][:]
    mean_z = file['Step#{:}'.format(step)]['z'][:] 
    mean_dp = file['Step#{:}'.format(step)]['dp'][:]
    mean_x = np.trim_zeros(mean_x)
    mean_xp = np.trim_zeros(mean_xp)
    mean_y = np.trim_zeros(mean_y)
    mean_yp = np.trim_zeros(mean_yp)
    file.close()
    return mean_x, mean_xp, mean_y, mean_yp, mean_z, mean_dp

def plot_fft(ax, mean_y_beam, f_sampling, n_segments, **mpl_kwargs):
    turns = np.linspace(0, mean_y_beam.shape[0]/f_sampling/n_segments, mean_y_beam.shape[0])
    fft_beam = np.abs(np.fft.rfft((mean_y_beam-np.mean(mean_y_beam))))
    fftfreq_beam = f_sampling*np.fft.rfftfreq(mean_y_beam.shape[0])
    ax.plot(fftfreq_beam, fft_beam/max(fft_beam), **mpl_kwargs)
    ax.set_xlabel('Coherent oscillation frequency, $\omega_y/\omega_0$')
    ax.set_ylabel('Normalised spectrum power')
    ax.set_ylim(0,)
    return 0