"""Basic plotting tools."""
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import scipy.constants as c

from plasmatk import parameters as p

def plot_mag_regimes(
        couple_bounds=(1e-3, 1e2), mag_bounds=(1e-4,1e3),
        add_regions=True, region_txt=True, colors=None,
        line_params=None, boundary_labels=False,
    ):
    """Create a plot of the 4 magnetic/coupling regimes
    and the boundaries between them.
    
    Args:
        couple_bounds (tuple[float]): The coupling constant
            axis limits.
        mag_bounds (tuple[float]): The magnetization parameter
            axis limits.
        add_regions (bool): 

    """
    fig, ax = plt.subplots()
    ax.set_xlim(*couple_bounds)
    ax.set_ylim(*mag_bounds)
    if line_params is None:
        line_params = {"c": "k"}
    # Number of sample
    ns = 1000
    log_cb = (np.log10(couple_bounds[0]),
              np.log10(couple_bounds[1]))
    Gamma = np.logspace(*log_cb, ns)
    # Unmagnitized boundary
    _make_boundary(ax, p.lcol_b, Gamma, 1e-2, r"$r_c = \lambda_\text{col}$",
       {"xytext": (0,1)}, region_txt, **line_params)
    # Weakly magnetized boundary
    _make_boundary(ax, p.lD_b, Gamma, 1e-2, r"$r_c = \lambda_\text{D}$",
       {"xytext": (0,-1)}, region_txt, **line_params)
    _make_boundary(ax, p.r_L, Gamma, .03, r"$r_c = r_\text{L}$",
       {"xytext": (0,-1)}, region_txt, **line_params)
    _make_boundary(ax, p.r_L, Gamma, .9, r"$r_c = a$",
       {"xytext": (0,0)}, region_txt, **line_params)
    # Color regions
    if colors:
        if colors is True:
            colors = ["#fbe8c4", "#f88e90", "#c8dbf6", "#bbd8bd"]
            # TODO: color in regions
    
    # MITL condition boundaries
    T_b = (1e1, 1e5)
    n_b = (1e13, 1e17)
    B_b = (20, 200)
    G_b = (p.Gamma_e(T_b[1], n_b[0]),
           p.Gamma_e(T_b[0], n_b[1]))
    Be_b = (p.Beta_e(B_b[0], n_b[1]),
           p.Beta_e(B_b[1], n_b[0]))
    _add_region(ax, G_b, Be_b, label=r"z-machine\nMITL")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Magnetization-Coupling Phase Space")
    ax.set_xlabel(r"Coupling Strength ($\Gamma$)")
    ax.set_ylabel(r"Magnetization ($\omega_c/\omega_p$)")
    fig.tight_layout()
    return fig, ax

def _make_boundary(ax, f, G, sp, text, tp, rt, **line_params):
    B = np.vectorize(f)(G)
    ax.plot(G, B, **line_params)
    if rt:
        # Find rotation based off dB/dG
        pct = .08
        xl, yl = ax.get_xlim(), ax.get_ylim()
        log_rng = np.log10(xl[1]/xl[0])
        log_yrng = np.log10(yl[1]/yl[0])
        ar = log_yrng / log_rng
        bbox = ax.get_window_extent().transformed(
               ax.figure.dpi_scale_trans.inverted())
        dar = bbox.width / bbox.height
        x1, x2 = np.log10(sp), np.log10(sp) + pct*log_rng
        y1, y2 = np.log10(f(sp)), np.log10(f(10**x2))
        # ax.scatter([10**x1, 10**x2], [10**y1, 10**y2])
        rot = 180/np.pi*np.arctan((y2-y1)/(x2-x1)) / ar / dar
        ax.annotate(text, (sp, f(sp)), fontsize=12,
            rotation=rot, # rotation_mode="anchor",
            horizontalalignment="left",
            textcoords="offset fontsize", **tp)

def _add_region(ax, x, y, label=None):
    """Mark out a region of the phase space."""
    # Draw rectangle
    rect = plt.Rectangle(
        (x[0], y[0]), x[1]-x[0], y[1]-y[0],
        ls="--", fill=False
        )
    ax.add_patch(rect)

def plot_mag_regimes_nT():
    """Create a plot of the 4 magnetic/coupling regimes
    in density-temperature space."""
    # Change
    pass

def plot_mag_regimes_nTB():
    pass
