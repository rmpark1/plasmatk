import os
from os.path import join as pjoin

import plasmatk as ptk
from plasmatk import src_path

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
