import matplotlib.pyplot as plt
"""Basic plotting tools."""

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
    return fig, ax

def plot_mag_regimes_nT():
    """Create a plot of the 4 magnetic/coupling regimes
    in density-temperature space."""
    # Change
    pass
