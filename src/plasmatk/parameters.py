import numpy as np
import pandas as pd
import scipy.constants as c

e = c.e
m_e = c.m_e
epsilon_0 = c.epsilon_0

class Parameters(object):
    r"""An enumeration of input plasma parameters.

    Args:
        T (array-like): Temperature (eV).
        n_e (array-like): Electron density :math:`\text{m}^{-3}`.
        B (array-like): Magnetic field strength (T).
    """
    def __init__(T=None, n_e=None, B=None):
        self.T = T
        self.n_e = n_e
        self.B = B

def Gamma_e(T, n_e):
    """Return the coupling constant.

    Args:
        p (Parameters): Termperature and density required
        T (float): The temperature in eV.
        n_e (float): The electron number density in cm^-3.
    Returns:
        The electron coupling parameter.
    """
    # Convert to meters
    n = n_e * 100**3
    a_e = (3/(4*np.pi*n))**(1/3)
    return c.e**2/(
        a_e*4*np.pi*c.epsilon_0*c.e*T)

def Beta_e(B, n_e):
    r"""Return the magnetization parameter
    :math:`B \equiv \frac{\omega_{ce}}{\omega_{pe}}`.

    Args:
        B (float): The magnetic field in Tesla.
        n_e (float): The electron number density in cm^-3.
    """
    n = n_e * 100**3
    return B*np.sqrt(c.epsilon_0 / (c.m_e * n))

def Theta(Gamma):
    """The generalized coulomn logarithm.

    Args:
        Gamma: The electron coupling parameter
    """
    return 0.65 * np.log(1 + 2.15/(np.sqrt(3)*Gamma**(3/2)))

def v_the(n, T, B):
    r"""Return the thermal speed. Defined as
    :math:`v_\mathrm{th} = \sqrt{\frac{k_\mathrm{B}T}{m_\mathrm{e}}}`.

    Args:
        1
    """
    # Convert from keV to Joules
    E = T * 1000 * e
    return np.sqrt(E/m_e)

def l_De(n, T, B):
    """The electron Debye length."""
    # Convert from keV to Joules
    E = T * 1000 * e
    return np.sqrt(epsilon_0 * E / (n*e**2))

def N_De(n, T, B):
    return n*l_De(n, T, B)**3

def wpe(n, T, B):
    return np.sqrt(c.e**2 * n / (epsilon_0 * m_e) )

def wce(n, T, B):
    """The electron cyclofrequency."""
    return e*B/m_e

def lcol_b(Gamma):
    """The boundary condition r_c = l_col"""
    return Theta(Gamma)*0.32*Gamma**(3/2)

def lD_b(Gamma):
    """The boundary condition r_c = l_D."""
    Aa = np.sqrt(3*.55/2)
    return max(min(1., Aa*np.sqrt(2/(3*Gamma))), lcol_b(Gamma))

def r_L(Gamma):
    """The boundary condition r_c = r_L."""
    Aa = np.sqrt(3*.55/2)
    AL = np.sqrt(6*.55**3)
    return max(AL*np.sqrt(1.0/(6*Gamma**3)),
       Aa*np.sqrt(2/(3*Gamma)), lcol_b(Gamma))
