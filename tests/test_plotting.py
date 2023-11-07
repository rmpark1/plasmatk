import matplotlib as mpl

import plasmatk as ptk
from plasmatk import plotting as ppl

def test_plot_mag_regimes():
    # Test with text
    fig, ax = ppl.plot_mag_regimes(region_txt=True)
    assert len([a for a in ax.get_children()
               if isinstance(a, mpl.text.Text)
               and "$" in a.get_text()]) == 4
    # Test without text
    fig, ax = ppl.plot_mag_regimes(region_txt=False)
    assert len([a for a in ax.get_children()
               if isinstance(a, mpl.text.Text)
               and "$" in a.get_text()]) == 0

def test_plot_mag_regimes_nT():
    pass
