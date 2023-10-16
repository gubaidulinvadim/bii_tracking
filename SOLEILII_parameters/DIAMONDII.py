from scipy.constants import physical_constants, c, e, m_e, m_p, epsilon_0, pi, N_A, R
from numpy import sqrt

r_e = physical_constants["classical electron radius"][0]
m_u = physical_constants["unified atomic mass unit"][0]
r_u = 1/(4*pi*epsilon_0)*e**2/(m_u*c**2)


CIRCUMFERENCE = 561.571
R = CIRCUMFERENCE/(2*pi)
ENERGY = 3.5e9
GAMMA = 1 + ENERGY * e / (m_e * c**2)
BETA = sqrt(1 - GAMMA**-2)
OMEGA_REV = 2*pi*BETA*c/CIRCUMFERENCE
EPSILON_X = 3.14e-9  # 163e-12 #3.14e-9
EPSILON_Y = 8e-12  # 8e-9
SIGMA_DP = 0.09e-2
SIGMA_Z = c*11.7e-12
H_RF = 936
F_RF = 499.654e6
U_LOSS = 490e3
V_RF = 1.38e6
ALPHA_0 = 9.1e-5
GAMMA_T = 1. / sqrt(ALPHA_0)
F_S = 1.4e3
Q_S = 2*pi*F_S/OMEGA_REV
TAU_X = 7.3e-3
TAU_Y = 13.1e-3
TAU_Z = 11.7e-3
Q_X = 54.2
Q_Y = 18.3
Qp_X = 1.6
Qp_Y = 1.6
PRESSURE = 1e-7
BETA_X_SMOOTH = R/Q_X
BETA_Y_SMOOTH = R/Q_Y
SIG_X = sqrt(BETA_X_SMOOTH*EPSILON_X)
SIG_Y = sqrt(BETA_Y_SMOOTH*EPSILON_Y)
ALPHA_X_SMOOTH = 0
ALPHA_Y_SMOOTH = 0
I = 300e-3
INTENSITY_PER_BUNCH = I/H_RF/e/OMEGA_REV*2*pi
if __name__ == '__main__':
    print('{:.1e}, {:.1e}'.format(SIG_X, SIG_Y))
    print('Bunch spacing in uniform filling is {:.1e}'.format(
        CIRCUMFERENCE/H_RF))
