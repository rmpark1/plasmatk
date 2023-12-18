import numpy as np
import pandas as pd
import scipy.constants as c

class Parameters(object):
    r"""An enumeration of input plasma parameters.

    Args:
        T (array-like): Temperature (eV).
        n_e (array-like): Electron density :math:`\text{m}^{-3}`.
        B (array-like): Magnetic field strength (T).
    """
    def __init__(self, n=None, T=None, B=None):
        #: The independent parameters
        self.T = T
        self.n = n
        self.B = B

        #: Store computed dependend parameters
        self._Gamma_e = None
        self._beta_e = None
        self._Theta = None
        self._v_the = None
        self._l_De = None
        self._N_De = None
        self._wpe = None
        self._wce = None
        self._clog = None
        self._sptiz_res = None
        self._tau_ei = None
        self._hall = None
        self._sig_0 = None
        self._sig_p_w = None
        self._sig_p_s = None
        self._sig_p_c = None
        self._eta_p_w = None
        self._eta_p_s = None
        self._eta_p_c = None

    def get_units():
        """Get the units of a quantity."""
        pass

    def set_units(d):
        """Set the units of a certain independent variable."""
        pass

    def Gamma_e(self):
        """Return the coupling constant.

        Returns:
            The electron coupling parameter (dimensionless).
        """
        if self._Gamma_e is not None: return self._Gamma_e
        T, n = self.T, self.n
        a_e = (3/(4*np.pi*n))**(1/3)
        self.Gamma_e_ = c.e**2/(a_e*4*np.pi*c.epsilon_0*c.e*T)
        return self.Gamma_e_

    def beta_e(self):
        r"""Return the magnetization parameter
        :math:`B \equiv \frac{\omega_{ce}}{\omega_{pe}}`.
        """
        if self._beta_e is not None: return self._beta_e
        n, B = self.n, self.B
        self._beta_e = B*np.sqrt(c.epsilon_0 / (c.m_e * n))
        return self._beta_e

    def Theta(self):
        """The generalized coulomn logarithm."""
        if self._Theta is not None: return self._Theta
        Gamma = self.Gamme_e()
        self._Theta = 0.65 * np.log(1 + 2.15/(np.sqrt(3)*Gamma**(3/2)))
        return self._Theta

    def v_the(self):
        r"""Return the thermal speed. Defined as
        :math:`v_\mathrm{th} = \sqrt{\frac{k_\mathrm{B}T}{m_\mathrm{e}}}`.
        """
        # TODO: Implement the different kinds.
        T = self.T
        if self._v_the is not None: return self._v_the
        self._v_the = np.sqrt(c.e*T/m_e)
        return self._v_the

    def l_De(self):
        """The electron Debye length."""
        if self._l_De is not None: return self._l_De
        n, T = self.n, self.T
        # Convert from keV to Joules
        self._l_De = np.sqrt(c.epsilon_0 * c.e*T / (n*c.e**2))
        return self._l_De

    def N_De(self):
        """Number of particles in the debye sphere."""
        if self._N_De is not None: return self._N_De
        n = self.n
        self._N_De = n*self.l_De()**3
        return self._N_De

    def wpe(self):
        """Electron plasma freqency"""
        if self._wpe is not None: return self._wpe
        n = self.n
        self._wpe = np.sqrt(c.e**2 * n / (c.epsilon_0 * c.m_e) )
        return self._wpe

    def wce(self):
        """The electron cyclofrequency."""
        if self._wce is not None: return self._wce
        B = self.B
        self._wce = c.e*B/c.m_e
        return self._wce

    def clog(self):
        """The coulomn logarithm."""
        if self._clog is not None: return self._clog
        self._clog = np.log(self.Gamma_e()**(-3/2) / np.sqrt(3))
        return self._clog

    def spitz_res(self, Z=1.):
        """The Spitzer resistivity in ohm-m (parallel component).

        Args:
            Z (int): The net charge of the target.
        """
        if self._spitz_res is not None: return self._spitz_res
        T = self.T
        self._spitz_res = 5.2e-5 * Z * self.clog() * T**(-3/2)
        return self._spitz_res

    def tau_ei(self):
        """The electron-ion plasma collision time."""
        if self._tau_ei is not None: return self._tau_ei
        n, T = self.n, self.T
        # print(self.clog())
        self._tau_ei = (
            3 / (4 * np.sqrt(2*np.pi))
            * (4*np.pi*c.epsilon_0)**2
            * np.sqrt(c.m_e) * (c.e*T)**(3/2)
            / (2*n * c.e**4 * self.clog())
        )
        return self._tau_ei

    def hall(self):
        """Return the hall parameter."""
        if self._hall is not None: return self._hall
        wce, tau = self.wce(), self.tau_ei()
        self._hall = wce*tau
        return self._hall

    def sig_0(self):
        """Unmagnetized conductivity for OCP. density in cm^-3"""
        if self._sig_0 is not None: return self._sig_0
        n = self.n
        self._sig_0 = 2*n * c.e**2 * self.tau_ei() / c.m_e
        return self._sig_0

    def sig_p_w(self):
        """Weakly magnetized conductivity."""
        if self._sig_p_w is not None: return self._sig_p_w
        sig0 = self.sig_0()
        self._sig_p_w = sig0 / (1 + (self.hall())**2)
        return self._sig_p_w

    def sig_p_s(self):
        """Strongly magnetized perpendicular
        conductivity (high field limit)."""
        if self._sig_p_s is not None: return self._sig_p_s
        sig0, h = self.sig_0(), self.hall()
        self._sig_p_s = 3/4 * sig0 * np.log(c.m_p / c.m_e) / h**2
        return self._sig_p_s

    def sig_p_c(self):
        """Use the connection formula for the
        perpendicular conductivity."""
        if self._sig_p_c is not None: return self._sig_p_c
        hall = self.wce() * self.tau_ei()
        eta_we = self.eta_p_w() * hall
        eta_p = self.eta_p_c()
        self._sig_p_c = eta_p / (eta_p**2 + eta_we**2)
        return self._sig_p_c

    def eta_p_w(self):
        """Weakly magnetized perpendicular resistivity."""
        if self._eta_p_w is not None: return self._eta_p_w
        self._eta_p_w = 1 / self.sig_0()
        self._eta_0 = self._eta_p_w
        return self._eta_p_w

    def eta_p_s(self):
        """Strongly magnetized perpendicular resistivity."""
        if self._eta_p_s is not None: return self._eta_p_s
        e0 = self.eta_p_w()
        self._eta_p_s = 3/4 * e0 * np.log(c.m_p / c.m_e)
        return self._eta_p_s
        
    def eta_p_c(self):
        """Use the connection formula for the
        perpendicular resistivity."""
        if self._eta_p_c is not None: return self._eta_p_c
        be, eta0, clog = self.beta_e(), self.eta_p_w(), self.clog()
        Q = 3/4 * np.log(c.m_p/c.m_e) # Using proton mass
        LA = 40*clog*(Q-1)
        self._eta_p_c = eta0 * (LA + 2*Q*be**2) / (LA + 2*be**2)
        return self._eta_p_c

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
    # Convert from eV to Joules
    E = T * c.e
    return np.sqrt(E/c.m_e)

def l_De(n, T, B):
    """The electron Debye length."""
    # Convert from keV to Joules
    E = T * 1000 * c.e
    return np.sqrt(c.epsilon_0 * E / (n*c.e**2))

def N_De(n, T, B):
    return n*l_De(n, T, B)**3

def wpe(n, T, B):
    return np.sqrt(c.e**2 * n / (c.epsilon_0 * c.m_e) )

def wce(n, T, B):
    """The electron cyclofrequency."""
    return c.e*B/c.m_e

def lcol_b(Gamma):
    """The boundary condition r_c = l_col"""
    return Theta(Gamma)*0.32*Gamma**(3/2)

def lD_b(Gamma):
    """The boundary condition r_c = l_D."""
    Aa = np.sqrt(3*.55/2)
    try:
        return max(min(1., Aa*np.sqrt(2/(3*Gamma))), lcol_b(Gamma))
    except ZeroDivisionError:
        # return np.empty(Gamma.shape)
        return np.nan

def r_L(Gamma):
    """The boundary condition r_c = r_L."""
    Aa = np.sqrt(3*.55/2)
    AL = np.sqrt(6*.55**3)
    try:
        return max(AL*np.sqrt(1.0/(6*Gamma**3)),
           Aa*np.sqrt(2/(3*Gamma)), lcol_b(Gamma))
    except ZeroDivisionError:
        # return np.empty(Gamma.shape)
        return np.nan

def clog(n, T):
    """The coulomn logarithm."""
    return np.log(Gamma_e(T, n)**(-3/2) /  np.sqrt(3))

def spitz_res(n, T, Z=1.):
    """The Spitzer resistivity in ohm-m (parallel component)."""
    return 5.2e-5 * Z * clog(n, T) * T**(-3/2)

def tau_ei(n_e, T):
    """The electron-ion plasma collision time."""

    return (
        3 / (4 * np.sqrt(2*np.pi))
        * (4*np.pi*c.epsilon_0)**2
        * np.sqrt(c.m_e) * (c.e*T)**(3/2)
        / (n_e * c.e**4 * clog(n_e, T))
    )

def sig_0(n, T):
    """Unmagnetized conductivity for OCP. density in cm^-3"""
    tau = tau_ei(n, T)    
    return n * c.e**2 * tau / c.m_e

def sig_p_w(n, T, B):
    """Weakly magnetized conductivity."""
    tau = tau_ei(n, T)    
    wc = wce(n, T, B)
    return sig_0(n, T) / (1 + (wc*tau)**2)

def sig_p_s(n, T, B):
    """Strongly magnetized perpendicular
    conductivity (high field limit)."""
    M = 5.6 * c.m_e**2 / c.e**2
    tau = tau_ei(n, T)    
    return M * sig_0(n, T) / (B*tau)**2

def sig_p_c(n, T, B):
    """Use the connection formula for the
    perpendicular conductivity."""
    hall = wce(n, T, B) * tau_ei(n, T)
    eta0 = 1/sig_0(n, T)
    eta_we = eta0 * hall
    eta_prp = eta_p_c(n, T, B)
    return eta_prp / (eta_prp**2 + eta_we**2)

def eta_p_w(n, T, B):
    """Weakly magnetized perpendicular resistivity."""
    return 1 / sig_0(n, T)

def eta_p_s(n, T, B):
    """Strongly magnetized perpendicular resistivity."""
    eta_0 = 1 / sig_0(n, T)
    return 3/4 * eta_0 * np.log(c.m_p / c.m_e)
    
def eta_p_c(n, T, B):
    """Use the connection formula for the
    perpendicular resistivity."""
    be = Beta_e(B, n)
    eta0 = 1/sig_0(n, T)
    Q = 3/4 * np.log(c.m_p/c.m_e) # Using proton mass
    LA = 40*clog(n, T)*(Q-1)
    eta_prp = (eta0 * LA + 2*Q*be**2 /
        (LA + 2*be**2))
    return eta_prp

