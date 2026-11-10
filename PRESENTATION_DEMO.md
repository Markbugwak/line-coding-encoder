# Live Demonstration Guide

## Goal
Show how the program converts one binary input into eight digital line-coding waveforms and explain how it handles long runs of zeros.

## 1. Start the program
In the repository folder, open a terminal and run:

```bash
python -m pip install -r requirements.txt
python encoding_techniques.py
```

Enter this sample input when prompted:

```text
01001100011
```

## 2. Show all eight encodings
At the menu, choose `9` (Show ALL). Explain that the program prints the signal levels and opens one combined plot.

The eight techniques are:
1. NRZ-L
2. NRZI
3. Bipolar-AMI
4. Pseudoternary
5. Manchester
6. Differential Manchester
7. B8ZS
8. HDB3

## 3. Explain the waveform
- `+` means positive voltage, `0` means zero voltage, and `-` means negative voltage.
- Most schemes use one signal level per bit.
- Manchester and Differential Manchester use two half-bit levels and always have a middle transition.
- B8ZS replaces eight consecutive zeros with `000VB0VB`.
- HDB3 replaces four consecutive zeros with `000V` or `B00V`, based on pulse parity.
- Yellow plot highlights identify B8ZS/HDB3 substitutions.

## 4. Demonstrate one scheme from the command line
Close the plot, then run:

```bash
python encoding_techniques.py 01001100011 --scheme Manchester
```

Point out that each input bit produces two half-bit signal levels.

## 5. Demonstrate zero-run handling
Run:

```bash
python encoding_techniques.py 0000000000000000
```

Explain that B8ZS handles two groups of eight zeros and HDB3 handles four-zero groups, avoiding an indefinitely flat zero-level signal.

## 6. Show input validation and tests
Try an invalid input:

```bash
python encoding_techniques.py 01012
```

The CLI should reject it with a clear error. Then run:

```bash
python -m pytest -q
```

## Suggested closing
"This project demonstrates how the same binary data can be represented by different digital signal patterns. The output makes it easier to compare transitions, voltage levels, and zero-substitution techniques."
