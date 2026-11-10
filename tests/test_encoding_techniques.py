import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import encoding_techniques as enc


SAMPLE = "01001100011"


def test_all_eight_encoders_sample_input():
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
        assert function(SAMPLE) == expected[name]


@pytest.mark.parametrize(
    "bits",
    [
        "0",
        "1",
        "01",
        "10",
        "1010101010",
        "111111111111",
        "00000000",
        "0000000000000000",
        "10000000000000001",
        "101000001000000010000000",
        "0" * 256,
        "1" * 256,
        ("01001100011" * 24),
    ],
)
def test_all_eight_encoders_handle_multiple_and_long_inputs(bits):
    for name, (function, samples_per_bit) in enc.SCHEMES.items():
        levels = function(bits)
        assert len(levels) == len(bits) * samples_per_bit, name
        assert set(levels) <= {-1, 0, 1}, name


def test_b8zs_substitution_example():
    assert enc.b8zs("1000000001") == [1, 0, 0, 0, 1, -1, 0, -1, 1, -1]


def test_b8zs_replaces_two_consecutive_groups_of_eight_zeros():
    levels = enc.b8zs("0" * 16)
    assert levels == [0, 0, 0, -1, 1, 0, 1, -1] + [0, 0, 0, -1, 1, 0, 1, -1]


def test_hdb3_substitution_example():
    assert enc.hdb3("1000011000010000") == [1, 0, 0, 0, 1, -1, 1, -1, 0, 0, -1, 1, 0, 0, 0, 1]


def test_hdb3_handles_long_zero_runs_without_changing_length():
    for count in (4, 8, 16, 64, 256):
        levels = enc.hdb3("0" * count)
        assert len(levels) == count
        assert set(levels) <= {-1, 0, 1}
        assert any(level != 0 for level in levels)


@pytest.mark.parametrize("bad_bits", ["", "01012", "10a01", "  ", "01-01"])
def test_invalid_bits_are_rejected_by_cli_helper(bad_bits):
    with pytest.raises(ValueError, match="bit string"):
        enc.run_cli(bad_bits)


def test_cli_helper_accepts_one_scheme(capsys):
    enc.run_cli("1", "NRZ-L")
    output = capsys.readouterr().out
    assert "NRZ-L" in output and "Signal : -" in output
    assert "Manchester" not in output


def test_cli_helper_rejects_unknown_scheme():
    with pytest.raises(ValueError, match="unknown scheme"):
        enc.run_cli("0101", "unknown")


def test_main_requires_bits_when_scheme_is_given(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["encoding_techniques.py", "--scheme", "Manchester"])
    with pytest.raises(SystemExit) as exc:
        enc.main()
    assert exc.value.code == 2
    assert "bits argument is required" in capsys.readouterr().err


def test_main_accepts_spaced_bits(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["encoding_techniques.py", "0100 1100 011", "--scheme", "NRZ-L"])
    enc.main()
    output = capsys.readouterr().out
    assert "NRZ-L" in output
    assert "+ - + + - - + + + - -" in output


def test_menu_show_all_does_not_overwrite_png(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    responses = iter(["01001100011", "9", "q"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))
    monkeypatch.setattr(enc.plt, "show", lambda: None)
    try:
        enc.menu()
    finally:
        enc.plt.close("all")
    assert not (tmp_path / "all_encodings.png").exists()


def test_menu_exits_cleanly_on_eof(monkeypatch):
    def raise_eof(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    enc.menu()
