import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import encoding_techniques as enc

def test_all_eight_encoders_sample_input():
    bits = "01001100011"
    expected = {
        "NRZ-L": [1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1],
        "NRZI": [-1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1],
        "Bipolar-AMI": [0, 1, 0, 0, -1, 1, 0, 0, 0, -1, 1],
        "Pseudoternary": [1, 0, -1, 1, 0, 0, -1, 1, -1, 0, 0],
        "Manchester": [1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1],
        "Differential Manchester": [1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1],
        "B8ZS": [0, 1, 0, 0, -1, 1, 0, 0, 0, -1, 1],
        "HDB3": [0, 1, 0, 0, -1, 1, 0, 0, 0, -1, 1],
    }
    for name, (function, _) in enc.SCHEMES.items():
        assert function(bits) == expected[name]

def test_b8zs_substitution_example():
    assert enc.b8zs("1000000001") == [1, 0, 0, 0, 1, -1, 0, -1, 1, -1]

def test_hdb3_substitution_example():
    assert enc.hdb3("1000011000010000") == [1, 0, 0, 0, 1, -1, 1, -1, 0, 0, -1, 1, 0, 0, 0, 1]

def test_invalid_bits_are_rejected_by_cli_helper():
    import pytest
    with pytest.raises(ValueError):
        enc.run_cli("01012")
    with pytest.raises(ValueError):
        enc.run_cli("")

def test_cli_helper_accepts_one_scheme(capsys):
    enc.run_cli("1", "NRZ-L")
    output = capsys.readouterr().out
    assert "NRZ-L" in output and "Signal : -" in output
    assert "Manchester" not in output
