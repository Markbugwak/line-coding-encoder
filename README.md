# Line Coding Encoder

A Python program that converts digital data into digital signal levels using eight line-coding techniques. The existing encoder conventions follow Stallings, *Data and Computer Communications*, Section 5.1.

## Supported techniques

- NRZ-L
- NRZI
- Bipolar-AMI
- Pseudoternary
- Manchester
- Differential Manchester
- B8ZS
- HDB3

## Requirements

Python 3.9+ and the packages in `requirements.txt`.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Interactive menu

```powershell
.\.venv\Scripts\python.exe encoding_techniques.py
```

## CLI mode

Encode all eight schemes for the sample bit string:

```powershell
.\.venv\Scripts\python.exe encoding_techniques.py 01001100011
```

Show only one scheme:

```powershell
.\.venv\Scripts\python.exe encoding_techniques.py 01001100011 --scheme Manchester
```

NRZ and ternary schemes return one signal level per bit. Manchester schemes return two levels per bit (first half, second half). Levels are printed as `+`, `0`, and `-`.

## Waveform plot

The interactive menu can plot one scheme or all eight together. The combined figure is saved as `all_encodings.png`. Yellow shading marks B8ZS/HDB3 zero substitutions.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The automated tests check all eight encoders, invalid input, and the documented B8ZS/HDB3 substitution examples.

## Encoding conventions

- **NRZ-L:** 0 = high (+1), 1 = low (-1).
- **NRZI:** 1 = transition at the start of the bit; 0 = no transition.
- **Bipolar-AMI:** each 1 alternates polarity; 0 = zero voltage.
- **Pseudoternary:** each 0 alternates polarity; 1 = zero voltage.
- **Manchester:** 1 = low-to-high mid-bit transition; 0 = high-to-low.
- **Differential Manchester:** every bit has a mid-bit transition; 0 also has a transition at the start.
- **B8ZS:** eight consecutive zeros become 000VB0VB.
- **HDB3:** four consecutive zeros become 000V after an odd pulse count, or B00V after an even pulse count.

Initial pulse polarity for AMI-based substitutions is negative. HDB3 pulse counting begins at zero (even).

## Project files

- `encoding_techniques.py` — encoders, plots, interactive menu, and CLI.
- `tests/test_encoding_techniques.py` — automated tests.
- `all_encodings.png` — combined waveform plot.
- `presentation.pptx` — eight-slide presentation with speaker notes.
