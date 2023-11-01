import plasmatk as ptk

def test_Beta_e():
    BE = ptk.parameters.Beta_e
    assert BE(200, 1e-15) > 10

