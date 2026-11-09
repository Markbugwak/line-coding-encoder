"""
Encoding Techniques: Digital Data -> Digital Signals
Reference: Stallings, Data and Computer Communications (8e), Section 5.1

Schemes: NRZ-L, NRZI, Bipolar-AMI, Pseudoternary, Manchester,
         Differential Manchester, B8ZS, HDB3

Each encoder takes a bit string such as "01001100011" and returns a list of
signal levels (+1, 0, -1). Biphase schemes return 2 levels per bit
(first half, second half); all others return 1 level per bit.

Run:  python encoding_techniques.py
Needs: matplotlib  (pip install matplotlib)
"""

import matplotlib.pyplot as plt

HIGH, LOW = 1, -1


# ---------------------------------------------------------------- encoders
def nrz_l(bits):
    """NRZ-L: 0 = high level, 1 = low level."""
    return [LOW if b == "1" else HIGH for b in bits]


def nrzi(bits, level=LOW):
    """NRZI: 1 = transition at start of bit, 0 = no transition."""
    out = []
    for b in bits:
        if b == "1":
            level = -level
        out.append(level)
    return out


def bipolar_ami(bits, last=LOW):
    """Bipolar-AMI: 0 = no line signal, 1 = pulse, alternating +/-."""
    out = []
    for b in bits:
        if b == "1":
            last = -last
            out.append(last)
        else:
            out.append(0)
    return out


def pseudoternary(bits, last=LOW):
    """Pseudoternary: 1 = no line signal, 0 = pulse, alternating +/-."""
    out = []
    for b in bits:
        if b == "0":
            last = -last
            out.append(last)
        else:
            out.append(0)
    return out


def manchester(bits):
    """Manchester: 1 = low-to-high mid-bit, 0 = high-to-low mid-bit."""
    out = []
    for b in bits:
        out += [LOW, HIGH] if b == "1" else [HIGH, LOW]
    return out


def diff_manchester(bits, level=LOW):
    """Differential Manchester: always a mid-bit transition;
    0 = transition at start of bit, 1 = no transition at start."""
    out = []
    for b in bits:
        if b == "0":
            level = -level          # transition at start of bit
        out += [level, -level]      # mid-bit transition
        level = -level              # level at end of bit
    return out


def _b8zs(bits, last=LOW):
    """B8ZS core: returns (levels, substitutions). Substitutions are
    (start_bit, end_bit, label) tuples used to highlight the plot."""
    out, subs, i = [], [], 0
    while i < len(bits):
        if bits[i:i + 8] == "0" * 8:
            p = last
            out += [0, 0, 0, p, -p, 0, -p, p]
            subs.append((i, i + 8, "000VB0VB"))
            i += 8                  # last pulse polarity stays p
        elif bits[i] == "1":
            last = -last
            out.append(last)
            i += 1
        else:
            out.append(0)
            i += 1
    return out, subs


def b8zs(bits, last=LOW):
    """B8ZS: bipolar-AMI, but 8 zeros become 000VB0VB
    (V = violation, same polarity as previous pulse; B = valid bipolar)."""
    return _b8zs(bits, last)[0]


def _hdb3(bits, last=LOW):
    """HDB3 core: returns (levels, substitutions)."""
    out, subs, i, pulses = [], [], 0, 0   # pulses counted since last substitution
    while i < len(bits):
        if bits[i:i + 4] == "0000":
            if pulses % 2 == 1:
                out += [0, 0, 0, last]          # 000V
                subs.append((i, i + 4, "000V"))
            else:
                last = -last
                out += [last, 0, 0, last]       # B00V
                subs.append((i, i + 4, "B00V"))
            pulses = 0
            i += 4
        elif bits[i] == "1":
            last = -last
            out.append(last)
            pulses += 1
            i += 1
        else:
            out.append(0)
            i += 1
    return out, subs


def hdb3(bits, last=LOW):
    """HDB3: bipolar-AMI, but 4 zeros become 000V or B00V.
    Odd number of pulses since last substitution -> 000V, even -> B00V."""
    return _hdb3(bits, last)[0]


SUB_FUNCS = {"B8ZS": _b8zs, "HDB3": _hdb3}


# name -> (function, samples per bit)
SCHEMES = {
    "NRZ-L": (nrz_l, 1),
    "NRZI": (nrzi, 1),
    "Bipolar-AMI": (bipolar_ami, 1),
    "Pseudoternary": (pseudoternary, 1),
    "Manchester": (manchester, 2),
    "Differential Manchester": (diff_manchester, 2),
    "B8ZS": (b8zs, 1),
    "HDB3": (hdb3, 1),
}
NAMES = list(SCHEMES)


# ---------------------------------------------------------------- plotting
COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd",
          "#ff7f0e", "#17becf", "#8c564b", "#e377c2"]


def draw(ax, bits, name, color, bits_top=False, bits_bottom=False):
    """Draw one waveform: labeled levels, bit grid, highlighted substitutions."""
    func, spb = SCHEMES[name]
    subs = []
    if name in SUB_FUNCS:
        levels, subs = SUB_FUNCS[name](bits)
    else:
        levels = func(bits)
    n = len(bits)

    for s, e, label in subs:                       # highlight B8ZS / HDB3 patterns
        ax.axvspan(s, e, color="gold", alpha=0.35, lw=0)
        ax.text((s + e) / 2, -1.55, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color="#7a5c00")

    x = [k / spb for k in range(len(levels) + 1)]
    ax.step(x, levels + [levels[-1]], where="post", linewidth=2.8, color=color)
    ax.axhline(0, color="black", linewidth=0.8)
    for k in range(n + 1):
        ax.axvline(k, color="gray", linestyle=":", linewidth=0.8)

    t = ax.get_xaxis_transform()
    for k, b in enumerate(bits):
        if bits_top:
            ax.text(k + 0.5, 1.12, b, ha="center", va="bottom", transform=t,
                    fontsize=15, fontweight="bold")
        if bits_bottom:
            ax.text(k + 0.5, -0.12, b, ha="center", va="top", transform=t,
                    fontsize=15, fontweight="bold")

    ax.set_ylim(-1.9, 1.5)
    ax.set_xlim(0, n)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["-V", "0", "+V"], fontsize=10)
    ax.set_xticks([])
    ax.set_ylabel(name.replace(" ", "\n"), rotation=0, ha="right", va="center",
                  fontsize=13, fontweight="bold", color=color, labelpad=14)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def plot_one(bits, name):
    fig, ax = plt.subplots(figsize=(max(11, len(bits) * 0.9), 3.8))
    draw(ax, bits, name, COLORS[NAMES.index(name)], bits_top=True)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.78, bottom=0.12)
    fig.suptitle(f"{name}   |   data: {bits}", fontsize=14, fontweight="bold")
    plt.show()


def plot_all(bits, save=True):
    n = len(NAMES)
    fig, axes = plt.subplots(n, 1, figsize=(max(13, len(bits) * 1.0), 1.8 * n + 1.5))
    for i, (ax, name) in enumerate(zip(axes, NAMES)):
        draw(ax, bits, name, COLORS[i], bits_top=(i == 0), bits_bottom=(i == n - 1))
    fig.subplots_adjust(left=0.15, right=0.98, top=0.90, bottom=0.07, hspace=0.55)
    fig.suptitle(f"Digital data -> digital signals     data: {bits}",
                 fontsize=16, fontweight="bold")
    fig.text(0.98, 0.012, "yellow = B8ZS / HDB3 substitution", ha="right",
             fontsize=9, color="#7a5c00")
    if save:
        fig.savefig("all_encodings.png", dpi=150)
        print("Saved: all_encodings.png")
    plt.show()


# ---------------------------------------------------------------- text output
SYM = {1: "+", 0: "0", -1: "-"}


def as_text(levels):
    return " ".join(SYM[v] for v in levels)


def show_text(bits, name):
    func, spb = SCHEMES[name]
    levels = func(bits)
    print(f"\n{name}")
    print(f"  Input  : {' '.join(bits)}")
    if spb == 2:
        pairs = [as_text(levels[i:i + 2]).replace(" ", "") for i in range(0, len(levels), 2)]
        print(f"  Signal : {'  '.join(pairs)}   (first half, second half of each bit)")
    else:
        print(f"  Signal : {as_text(levels)}")


# ---------------------------------------------------------------- menu
def get_bits():
    while True:
        s = input("Enter a bit string (e.g. 01001100011): ").strip().replace(" ", "")
        if s and set(s) <= {"0", "1"}:
            return s
        print("  Invalid: use only 0 and 1.")


def menu():
    bits = get_bits()
    while True:
        print(f"\nCurrent data: {bits}")
        for i, name in enumerate(NAMES, 1):
            print(f"  {i}. {name}")
        print("  9. Show ALL (text + one combined plot)")
        print("  0. Enter new bit string")
        print("  q. Quit")
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            break
        if choice == "0":
            bits = get_bits()
        elif choice == "9":
            for name in NAMES:
                show_text(bits, name)
            plot_all(bits)
        elif choice.isdigit() and 1 <= int(choice) <= len(NAMES):
            name = NAMES[int(choice) - 1]
            show_text(bits, name)
            plot_one(bits, name)
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    menu()