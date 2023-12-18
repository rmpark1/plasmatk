import os
from os.path import join as pjoin

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import vectorize as ve
import scipy.constants as c

import plasmatk as ptk
from plasmatk import src_path
import plasmatk.parameters as p

def test_Beta_e():
    """Ensure magnetization parameter is 
    of the correct order of magnitude."""
    BE = ptk.parameters.Beta_e
    assert BE(200, 1e-15) > 10
    assert BE(200, 1e-15) >= 100

def test_c_extension():
    fi = pjoin(src_path, "a.cpp")
    res = os.system(f"g++ {fi} && ./a.out")
    assert res == 0

def test_params():
    ns = 1000
    n = np.ones(ns) * 1e24 # m^-3
    B = np.logspace(-1, 7, ns) # T
    T = np.ones(ns) * 100 # eV
    P = p.Parameters(n, T, B)
    be = P.beta_e()
    # print( be)
    P2 = p.Parameters(1e23, 100, 200)
    # print(p.Parameters(1e15*1e6, 2.5e-2).Gamma_e())
    # print(P2.beta_e())

def test_perp_sig():
    """Ensure that the connectino formula matches
    the strong and weakly magnetized scenarios
    in the correct limits."""
    ns = 1000
    n = np.ones(ns) * 1e14 # cm^-3
    B = np.logspace(-1, 4, ns) # T
    T = np.ones(ns) * 1.0774 

    P = p.Parameters(n*1e6, T, B)
    
    print(P.Gamma_e()) 
    bes = P.beta_e()
    # print(bes)

    e0 = 1/P.sig_0()
    es = P.eta_p_s()
    ew = P.eta_p_w()
    ec = P.eta_p_c()

    s0 = P.sig_0()
    ss = P.sig_p_s()
    sw = P.sig_p_w()
    sc = P.sig_p_c()

    fig, ax = plt.subplots()

    # ax.plot(bes, es/e0, color="red", label=r"Large $\beta_e$ limit")
    # ax.plot(bes, ew/e0, color="blue", label=r"Small $\beta_e$ limit")
    # ax.plot(bes, ec/e0, color="black", label=r"Connection formula")

    ax.plot(bes, ss/s0, color="red", label=r"Large $\beta_e$ limit")
    ax.plot(bes, sw/s0, color="blue", label=r"Small $\beta_e$ limit")
    ax.plot(bes, sc/s0, color="black", label=r"Connection formula")

    large = pd.read_csv("data/large.csv", header=None, names=["x", "y"])
    small = pd.read_csv("data/small.csv", header=None, names=["x", "y"])
    connection = pd.read_csv("data/connection.csv", header=None, names=["x", "y"])

    ax.plot(large.x, large.y.abs(), color="red", alpha=0.5)
    ax.plot(small.x, small.y.abs(), color="blue", alpha=0.5)
    ax.plot(connection.x, connection.y.abs(), color="black", alpha=0.5)

    ax.legend()
    ax.set_xscale("log")
    # ax.set_yscale("log")
    ax.grid(which="major", c="gray", alpha=0.8)
    ax.grid(which="minor", c="gray", alpha=0.5, ls="--")
    plt.show()

