from scipy.constants import physical_constants, c, e, m_e, m_p, epsilon_0, pi, N_A, R
from numpy import sqrt

r_e = physical_constants["classical electron radius"][0]
m_u = physical_constants["unified atomic mass unit"][0]
r_u = 1/(4*pi*epsilon_0)*e**2/(m_u*c**2)

CIRCUMFERENCE = 354.10
R = CIRCUMFERENCE/(2*pi)
ENERGY = 2.75e9
GAMMA = 1 + ENERGY * e / (m_e * c**2)
BETA = sqrt(1 - GAMMA**-2)
OMEGA_REV = 2*pi*BETA*c/CIRCUMFERENCE
EPSILON_X = 4000e-12
EPSILON_Y = 53e-12
SIGMA_DP = 0.1e-2
SIGMA_Z = 4.6e-3
H_RF = 416
F_RF = 352.2e9
U_LOSS = 917e3
V_RF = 1.38e6
ALPHA_0 = 4.4e-4
GAMMA_T = 1. / sqrt(ALPHA_0)
F_S = 4.5e3
Q_S = 2*pi*F_S/OMEGA_REV
TAU_X = 6.9e-3
TAU_Y = 6.9e-3
TAU_Z = 3.5e-3
Q_X = 18.16
Q_Y = 10.22
Qp_X = 1.3
Qp_Y = 2.2
PRESSURE = 1e-7
BETA_X_SMOOTH = 8.22
BETA_Y_SMOOTH = 8.13
ALPHA_X_SMOOTH = 0
ALPHA_Y_SMOOTH = 0
I = 500e-3
INTENSITY_PER_BUNCH = I/H_RF/e/OMEGA_REV*2*pi

if __name__ == '__main__':
    print(BETA_X_SMOOTH)
    print(BETA_Y_SMOOTH)
