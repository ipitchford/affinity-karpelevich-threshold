"""Independent exact certificate for a four-state affine-region counterexample.

All proof checks use Python's integer / Fraction arithmetic.  Decimal values at
the end are for orientation only.  There are no third-party dependencies.
"""

if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

from fractions import Fraction as F
from itertools import combinations, permutations
from math import log, sqrt, tanh
import json
from pathlib import Path

def _receipt_path(name):
    """Receipts go to --out DIR (default ./receipts); never overwrite shipped files."""
    import argparse, sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="receipts")
    ap.add_argument("--force", action="store_true")
    args, _ = ap.parse_known_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    if path.exists() and not args.force:
        sys.exit(f"refusing to overwrite {path}; use --force or another --out")
    return path



Q = [
    [-2768, 2727, 27, 14],
    [1427, -2768, 1327, 14],
    [1327, 27, -2768, 1414],
    [27, 27, 2727, -2781],
]


def polymul(a, b):
    """Multiply integer polynomials, low-order coefficients first."""
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += ai * bj
    return c


def characteristic_polynomial(matrix):
    """Leibniz determinant of lambda I - matrix (independent exact check)."""
    n = len(matrix)
    out = [0] * (n + 1)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = [(-1) ** inversions]
        for i, j in enumerate(p):
            factor = [-matrix[i][j], 1] if i == j else [-matrix[i][j]]
            term = polymul(term, factor)
        for i, c in enumerate(term):
            out[i] += c
    return out


def undirected_simple_cycles(n):
    """Enumerate one representative per rotation and reversal; lengths >= 3."""
    for length in range(3, n + 1):
        for vertices in combinations(range(n), length):
            first = vertices[0]
            for tail in permutations(vertices[1:]):
                if tail[0] < tail[-1]:
                    yield (first,) + tail


def cycle_ratio(c):
    forward = reverse = 1
    for i, j in zip(c, c[1:] + c[:1]):
        forward *= Q[i][j]
        reverse *= Q[j][i]
    ratio = F(forward, reverse)
    return max(ratio, 1 / ratio)


assert all(sum(row) == 0 for row in Q)
assert all(Q[i][j] > 0 for i in range(4) for j in range(4) if i != j)
alpha = max(-Q[i][i] for i in range(4))
assert alpha == 2781

char = characteristic_polynomial(Q)
factorized = polymul(polymul([0, 1], [1595, 1]), [4745**2 + 607500, 2 * 4745, 1])
assert char == factorized == [0, 36880427375, 38259075, 11085, 1]

cycles = []
for c in undirected_simple_cycles(4):
    k = cycle_ratio(c)
    margin = 19**len(c) * k.denominator - k.numerator
    assert margin > 0  # K_c < 19^{n_c}; hence beta' < 9/10.
    cycles.append({
        "cycle": "".join(str(v + 1) for v in c),
        "length": len(c),
        "ratio": str(k),
        "integer_margin": margin,
        "beta_decimal": tanh(log(float(k)) / (2 * len(c))),
    })
assert len(cycles) == 7

x = F(-1964, alpha)
original_y_squared = F(607500, alpha**2)
inverse_y_squared_lower = original_y_squared / F(9, 10)**2
assert inverse_y_squared_lower == F(250000, 2577987)
assert F(-1) < x < F(-1, 2)

# Karpelevich's upper-left arc is y^2 = A + 4 x sqrt(s), with s=-2x-1.
A = 3 * x**2 - 2 * x - 1
s = -2 * x - 1
gap_without_radical = A - inverse_y_squared_lower
assert s > 0 and gap_without_radical > 0 and -4 * x > 0
squared_margin = (-4 * x)**2 * s - gap_without_radical**2
assert squared_margin == F(19884434701, 2215338990723) > 0
# Squaring positive sides is reversible, so (-4x)sqrt(s) > A-r.
# Consequently g(x)=A+4x sqrt(s) < r < (Im lambda/(alpha beta'))^2.

boundary_y_squared = float(A) + 4 * float(x) * sqrt(float(s))
report = {
    "status": "All exact certificate checks passed",
    "Q": Q,
    "alpha": alpha,
    "characteristic_polynomial_ascending": char,
    "eigenvalues": ["0", "-1595", "-4745 + 450 sqrt(3) i", "-4745 - 450 sqrt(3) i"],
    "cycles": cycles,
    "beta_strict_upper_bound": "9/10",
    "x": str(x),
    "inverse_y_squared_strict_lower_bound": str(inverse_y_squared_lower),
    "squared_radical_comparison_margin": str(squared_margin),
    "illustrative_decimals_only": {
        "beta": max(c["beta_decimal"] for c in cycles),
        "lower_y_squared": float(inverse_y_squared_lower),
        "boundary_y_squared": boundary_y_squared,
        "strict_lower_excess": float(inverse_y_squared_lower) - boundary_y_squared,
    },
}
_receipt_path("karpelevich_audit_result.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
