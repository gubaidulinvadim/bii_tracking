# -*- coding: utf-8 -*-
"""
SOLEIL synchrotron parameters script.

@author: Alexis Gamelin
@date: 14/01/2020
"""

import numpy as np
from pathlib import Path
from mbtrack2.tracking import Synchrotron, Electron
from mbtrack2.utilities import Optics 

def soleil(mode = 'Uniform'):
    """
    
    """
    
    h = 416
    L = 3.540969742590899e+02
    E0 = 2.75e9
    particle = Electron()
    ac = 4.16e-4
    U0 = 1.171e6
    tau = np.array([6.56e-3, 6.56e-3, 3.27e-3])
    tune = np.array([18.15687, 10.22824, 0.00502])
    emit = np.array([3.9e-9, 3.9e-9*0.01])
    sigma_0 = 15e-12
    sigma_delta = 1.025e-3
    chro = [1.4,2.3]
    
    # mean values
    beta = np.array([3, 1.3])
    alpha = np.array([0, 0])
    dispersion = np.array([0, 0, 0, 0])
    optics = Optics(local_beta=beta, local_alpha=alpha, 
                      local_dispersion=dispersion)
    
    ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                       emit=emit, tune=tune, sigma_delta=sigma_delta, 
                       sigma_0=sigma_0, chro=chro)
    
    return ring

def v0313():
    """
    
    """
    
    h = 416
    particle = Electron()
    tau = np.array([7.3e-3, 13.1e-3, 11.7e-3])
    emit = np.array([53.47e-12, 53.47e-12])
    sigma_0 = 9.2e-12
    sigma_delta = 9e-4
    
    path_to_file = Path(__file__).parent
    lattice_file = path_to_file / "." / "data" / "lattice" / "SOLEIL_U_74BA_HOA_SYM02_V0313_cleaned.mat"
    
    # mean values
    alpha = np.array([0, 0])
    optics = Optics(lattice_file=lattice_file, local_alpha=alpha)
    
    ring = Synchrotron(h, optics, particle, tau=tau, emit=emit, 
                       sigma_0=sigma_0, sigma_delta=sigma_delta)
        
    return ring

def v0313_v2(IDs="noID", coupling="full", V_RF=None, ADTS=False):
    # Using RF table from 16/02/2021 (L. Nadolski) 
    
    h = 416
    L = 354.7373
    E0 = 2.75e9
    particle = Electron()
    ac = 9.12e-5
    chro = [1.6,1.6]
    tune = np.array([0.2,0.2])
    sigma_0 = 8e-12
    
    if IDs == "noID" and coupling == "full":
        tau = np.array([9.2e-3, 9.3e-3, 11.7e-3])
        emit = np.array([52e-12, 52e-12])
        sigma_delta = 9e-4
        U0 = 515e3
    
    if IDs == "ID1" and coupling == "full":
        tau = np.array([7.1e-3, 7.1e-3, 6.2e-3])
        emit = np.array([39e-12, 39e-12])
        sigma_delta = 8.9e-4
        U0 = 760e3
        
    if IDs == "ID2" and coupling == "full":
        tau = np.array([6.35e-3, 6.35e-3, 5.1e-3])
        emit = np.array([35e-12, 35e-12])
        sigma_delta = 8.8e-4
        U0 = 874e3
        
    if IDs == "noID" and coupling == "no":
        tau = np.array([7.1e-3, 13.2e-3, 11.7e-3])
        emit = np.array([81e-12, 1e-12])
        sigma_delta = 9e-4
        U0 = 515e3
    
    if IDs == "ID1" and coupling == "no":
        tau = np.array([5.6e-3, 8.8e-3, 6.2e-3])
        emit = np.array([64e-12, 1e-12])
        sigma_delta = 8.9e-4
        U0 = 760e3
        
    if IDs == "ID2" and coupling == "no":
        tau = np.array([5.1e-3, 7.6e-3, 5.1e-3])
        emit = np.array([58e-12, 1e-12])
        sigma_delta = 8.8e-4
        U0 = 874e3 
    
    # mean values
    beta = np.array([3.178, 4.197])
    alpha = np.array([0, 0])
    dispersion = np.array([0, 0, 0, 0])
    optics = Optics(local_beta=beta, local_alpha=alpha, 
                      local_dispersion=dispersion)
    
    if ADTS is True:
        # Name format : coef_yx means coef of vertical ADTS as a function of horizontal offset.
        coef_xx = np.array([2.10012957e+07, -1.95066506e+02, -1.87260829e+03,  
                            4.17160112e-02, 0])
        coef_yx = np.array([1.30396188e+07,  1.55792082e+04,  5.80031793e+02,
                            -2.52678776e-01, 0])
        coef_xy = np.array([9.88551670e+03, -2.80640442e-03, 0])
        coef_yy = np.array([1.84297492e+04, 7.24309395e-08, 0])
        
        adts = [coef_xx, coef_yx, coef_xy, coef_yy]
        
    else:
        adts = None

    ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                       emit=emit, tune=tune, sigma_delta=sigma_delta, 
                       sigma_0=sigma_0, chro=chro, adts=adts)
    
    if V_RF is not None:
        tuneS = ring.synchrotron_tune(V_RF)
        ring.sigma_0 = (ring.sigma_delta * np.abs(ring.eta()) 
                        / (tuneS * 2 * np.pi * ring. f0))
    
    return ring


def soleil_rock():
    """
    lat_superbend_rock_run4_2021.mat
    """
    
    h = 416
    particle = Electron()
    tau = np.array([6.56e-3, 6.56e-3, 3.27e-3])
    emit = np.array([3.9e-9, 3.9e-9*0.01])
    sigma_0 = 15e-12
    sigma_delta = 1.025e-3
    
    path_to_file = Path(__file__).parent
    lattice_file = path_to_file / "." / "data" / "lattice" / "lat_superbend_rock_run4_2021.mat"
    
    # mean values
    alpha = np.array([0, 0])
    optics = Optics(lattice_file=lattice_file, local_alpha=alpha, n_points=1e4)
    
    ring = Synchrotron(h, optics, particle, tau=tau, emit=emit, 
                       sigma_0=sigma_0, sigma_delta=sigma_delta)
    
    return ring


def v0356(coupling=30, load_lattice=False):
    """
    TDR lattice using V0356_V223.mat

    Parameters
    ----------
    coupling : {0, 30, 100}, optional
        Amount of beam coupling in percentage. The default is 30% coupling.
    load_lattice : bool
        Load .mat file. The default is false.

    Returns
    -------
    ring : Synchrotron object

    """
    
    h = 416
    particle = Electron()
    tau = np.array([7.68e-3, 14.14e-3, 12.18e-3])
    sigma_0 = 9e-12
    sigma_delta = 9.07649e-4
    
    if coupling == 0:
        emit = np.array([84.4e-12, 84.4e-13])
    elif coupling == 100:
        emit = np.array([54.9e-12, 54.9e-12])
    elif coupling == 30:
        emit = np.array([84.4e-12, 25.3e-12])
        
    if load_lattice:
        path_to_file = Path(__file__).parent
        lattice_file = path_to_file / "." / "data" / "lattice" / "V0356_V223.mat"
        
        # mean values
        alpha = np.array([0, 0])
        optics = Optics(lattice_file=lattice_file, local_alpha=alpha, n_points=1e4)
        
        ring = Synchrotron(h, optics, particle, tau=tau, emit=emit, 
                           sigma_0=sigma_0, sigma_delta=sigma_delta)
    else:
        L = 353.92
        E0 = 2.75e9
        particle = Electron()
        ac = 1.05e-4
        U0 = 458.5e3
        tune = np.array([54.2, 18.3])
        chro = np.array([1.6, 1.6])
        
        beta = np.array([3.178, 4.197])
        alpha = np.array([0, 0])
        dispersion = np.array([0, 0, 0, 0])
        
        optics = Optics(local_beta=beta, local_alpha=alpha, 
                      local_dispersion=dispersion)
        ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                       emit=emit, tune=tune, sigma_delta=sigma_delta, 
                       sigma_0=sigma_0, chro=chro)
    
    return ring

def v2366(IDs="close", lat="V004", load_lattice=True):
    """
    TDR lattice using V2366_V004_Physical_Aperture.m

    Returns
    -------
    ring : Synchrotron object

    """    
    
    h = 416
    particle = Electron()
    tau = np.array([7.68e-3, 14.14e-3, 12.18e-3])
    sigma_0 = 9e-12
    sigma_delta = 9.07649e-4
    emit = np.array([84.4e-12, 84.4e-13])
    
    if load_lattice:
        path_to_file = Path(__file__).parent
        if IDs=="close":
            if lat == "V004":
                lattice_file = path_to_file / "." / "data" / "lattice" / "V2366_V004_Physical_Aperture_wID.m"
            elif lat == "2023feb07":
                lattice_file = path_to_file / "." / "data" / "lattice" / "V2366_SYM1_180_180_2023feb07_Physical_Aperture_wID.m"
        else:
            if lat == "V004":
                lattice_file = path_to_file / "." / "data" / "lattice" / "V2366_V004_Physical_Aperture_woID.m"
            elif lat == "2023feb07":
                lattice_file = path_to_file / "." / "data" / "lattice" / "V2366_SYM1_180_180_2023feb07_Physical_Aperture_woID.m"
    
        # mean values
        alpha = np.array([0, 0])
        optics = Optics(lattice_file=lattice_file, local_alpha=alpha, n_points=1e4)
        
        ring = Synchrotron(h, optics, particle, tau=tau, emit=emit, 
                           sigma_0=sigma_0, sigma_delta=sigma_delta)
    else:
        L = 353.97
        E0 = 2.75e9
        particle = Electron()
        ac = 1.0695e-4
        U0 = 452.6e3
        tune = np.array([54.2, 18.3])
        chro = np.array([1.6, 1.6])
        
        beta = np.array([3.288, 4.003])
        alpha = np.array([0, 0])
        dispersion = np.array([0, 0, 0, 0])
        
        optics = Optics(local_beta=beta, local_alpha=alpha, 
                      local_dispersion=dispersion)
        ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                       emit=emit, tune=tune, sigma_delta=sigma_delta, 
                       sigma_0=sigma_0, chro=chro)
    
    return ring

def v2366_v2(IDs="open", V_RF=1.8e6):
    """
    TDR lattice v2366 w/ RF parameters from June 2023 RF budget.
    Natural emittance and 1% coupling because of Synchrotron Radiation 
    implementation.

    Parameters
    ----------
    IDs : {"open","close","close_phase2"}, optional
        ID configuration to consider. The default is "open".
    V_RF : float, optional
        Total RF voltage in [V]. The default is 1.8e6.

    Returns
    -------
    ring : Synchrotron object
        TDR lattice v2366.

    """
    L = 353.97
    E0 = 2.75e9
    particle = Electron()
    ac = 1.05751e-04
    tune = np.array([54.2, 18.3])
    chro = np.array([1.6, 1.6])
    beta = np.array([3.288, 4.003])
    alpha = np.array([0, 0])
    dispersion = np.array([0, 0, 0, 0])
    h = 416
    particle = Electron()
    mcf_order = np.array([-0.00192226,  0.00061511,  0.00010695])
    
    if IDs == "open":    
        U0 = 457e3
        tau = np.array([7.78e-3, 14.3e-3, 12.4e-3])
        sigma_delta = 9.080e-4
        emit = np.array([83.1e-12, 83.1e-12*0.01])
    elif IDs == "close":
        U0 = 457e3 + 230e3
        tau = np.array([6.10e-3, 9.50e-3, 6.58e-3])
        sigma_delta = 8.820e-4
        emit = np.array([65.7e-12, 65.7e-12*0.01])
    elif IDs == "close_phase2":
        U0 = 457e3 + 272e3
        tau = np.array([5.61e-3, 8.36e-3, 5.53e-3])
        sigma_delta = 8.976e-4
        emit = np.array([61.0e-12, 65.7e-12*0.01])
    else:
        raise ValueError("Invalid ID configuration")
        
    optics = Optics(local_beta=beta, local_alpha=alpha, 
                  local_dispersion=dispersion)
    ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                   emit=emit, tune=tune, sigma_delta=sigma_delta, chro=chro, 
                   mcf_order=mcf_order)
    
    tuneS = ring.synchrotron_tune(V_RF)
    ring.sigma_0 = (ring.sigma_delta * np.abs(ring.eta()) 
                    / (tuneS * 2 * np.pi * ring. f0))
        
    return ring

def v2366_v3(IDs="open", V_RF=1.7e6, HC_power=50e3):
    """
    TDR lattice v2366 w/ RF parameters from November 2023 RF budget.
    Natural emittance and 1% coupling because of Synchrotron Radiation 
    implementation.

    Parameters
    ----------
    IDs : {"open","close","close_phase2", "close_phase2_margin"}, optional
        ID configuration to consider. 
        "open": bare lattice
        "close": ID phase 1
        "close_phase2": ID phase 2
        "close_phase2_margin": ID phase 2 + 15 % margin
        The default is "open".
    V_RF : float, optional
        Total RF voltage in [V]. 
        The default is 1.7e6.
    HC_power : float, optional
        HC dissipated power at 500 mA.
        Should be taken as 0 if the HC dissipation is taken into account in the 
        simulation, for example by simulating the HC as a CavityResonator.
        The default is 50e3.

    Returns
    -------
    ring : Synchrotron object
        TDR lattice v2366_v3.

    """
    L = 353.97
    E0 = 2.75e9
    particle = Electron()
    ac = 1.05751e-04
    tune = np.array([54.2, 18.3])
    chro = np.array([1.6, 1.6])
    beta = np.array([3.288, 4.003])
    alpha = np.array([0, 0])
    dispersion = np.array([0, 0, 0, 0])
    h = 416
    particle = Electron()
    mcf_order = np.array([-0.00192226,  0.00061511,  0.00010695])

    U0 = 469e3 + HC_power*2
    
    if IDs == "open":    
        tau = np.array([7.64e-3, 13.83e-3, 11.64e-3])
        sigma_delta = 9.063e-4
        emit = np.array([83.7e-12, 83.7e-12*0.01])
    elif IDs == "close":
        U0 += 136e3*2
        tau = np.array([5.78e-3, 8.75e-3, 5.89e-3])
        sigma_delta = 8.547e-4
        emit = np.array([66.2e-12, 66.2e-12*0.01])
    elif IDs == "close_phase2":
        U0 += 169e3*2
        tau = np.array([5.46e-3, 8.04e-3, 5.25e-3])
        sigma_delta = 8.770e-4
        emit = np.array([60.9e-12, 60.9e-12*0.01])
    elif IDs == "close_phase2_margin":
        U0 += 195e3*2
        tau = np.array([5.46e-3, 8.04e-3, 5.25e-3])
        sigma_delta = 8.770e-4
        emit = np.array([60.9e-12, 60.9e-12*0.01])
    else:
        raise ValueError("Invalid ID configuration")
        
    optics = Optics(local_beta=beta, local_alpha=alpha, 
                  local_dispersion=dispersion)
    ring = Synchrotron(h, optics, particle, L=L, E0=E0, ac=ac, U0=U0, tau=tau,
                   emit=emit, tune=tune, sigma_delta=sigma_delta, chro=chro, 
                   mcf_order=mcf_order)
    
    tuneS = ring.synchrotron_tune(V_RF)
    ring.sigma_0 = (ring.sigma_delta * np.abs(ring.eta()) 
                    / (tuneS * 2 * np.pi * ring. f0))
    ring.get_longitudinal_twiss(V_RF)
        
    return ring