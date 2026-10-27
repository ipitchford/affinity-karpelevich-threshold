#!/usr/bin/env python3
"""Exact standard-library certificate for the four-state affine-spectrum counterexample.

The mathematical input not proved by this script is the n=4 Karpelevich
boundary y^2 <= 3*x^2 - 2*x - 1 + 4*x*sqrt(-2*x-1), -1 <= x <= -1/2.
Every arithmetic comparison below uses rational numbers and integers.
"""
if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

from fractions import Fraction as F
from itertools import permutations
from functools import reduce
from math import gcd, lcm
import hashlib
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



def polyadd(a, b):
    ans = [F(0)] * max(len(a), len(b))
    for i, v in enumerate(a):
        ans[i] += v
    for i, v in enumerate(b):
        ans[i] += v
    return ans


def polymul(a, b):
    ans = [F(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            ans[i + j] += u * v
    return ans


def characteristic(matrix):
    n = len(matrix)
    ans = [F(0)] * (n + 1)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = [F((-1) ** inversions)]
        for i in range(n):
            term = polymul(term, [-matrix[i][p[i]], F(i == p[i])])
        ans = polyadd(ans, term)
    return ans


def cycle_ratios(matrix):
    n = len(matrix)
    ans = []
    for length in range(3, n + 1):
        for c in permutations(range(n), length):
            if c[0] != min(c) or c[1] > c[-1]:
                continue
            ratio = F(1)
            for i, j in zip(c, c[1:] + c[:1]):
                ratio *= F(matrix[i][j], matrix[j][i])
            ans.append((c, max(ratio, 1 / ratio)))
    return ans


def rational_family(eps):
    t = F(14, 27)
    base = [[0, 1, 0, 0], [t, 0, 1-t, 0], [1-t, 0, 0, t], [0, 0, 1, 0]]
    v = [F(1), F(1), F(1), t]
    return [[F(base[i][j]) - (i == j) + eps*(v[j] - (3+t)*(i == j))
             for j in range(4)] for i in range(4)]


def primitive_integer_matrix(matrix):
    multiplier = lcm(*(v.denominator for row in matrix for v in row))
    ints = [[int(v * multiplier) for v in row] for row in matrix]
    divisor = reduce(gcd, (abs(v) for row in ints for v in row))
    return [[v // divisor for v in row] for row in ints], F(multiplier, divisor)


def fingerprint(eps):
    matrix, time_scale = primitive_integer_matrix(rational_family(eps))
    char = characteristic(matrix)
    serials = []
    for transposed in (False, True):
        for p in permutations(range(4)):
            candidate = [[matrix[p[j]][p[i]] if transposed else matrix[p[i]][p[j]]
                          for j in range(4)] for i in range(4)]
            serials.append(json.dumps(candidate, separators=(",", ":")))
    return {
        "epsilon": str(eps), "matrix": matrix, "time_scale": str(time_scale),
        "characteristic_coefficients_ascending": [str(v) for v in char],
        "dimension": 4, "rank": 3 if char[1] != 0 else "not established",
        "trace": sum(matrix[i][i] for i in range(4)), "determinant": str(char[0]),
        "row_sums": [sum(row) for row in matrix],
        "sorted_entries": sorted(v for row in matrix for v in row),
        "canonical_matrix_sha256_under_transpose_and_relabelling": hashlib.sha256(min(serials).encode()).hexdigest(),
        "cycle_ratios": [{"cycle": [v+1 for v in c], "ratio": str(k)} for c, k in cycle_ratios(matrix)]
    }


def verify():
    Q = [[-2768, 2727, 27, 14],
         [1427, -2768, 1327, 14],
         [1327, 27, -2768, 1414],
         [27, 27, 2727, -2781]]
    assert all(sum(row) == 0 for row in Q)
    assert all(Q[i][j] > 0 for i in range(4) for j in range(4) if i != j)
    assert Q == primitive_integer_matrix(rational_family(F(1, 100)))[0]
    alpha = max(-Q[i][i] for i in range(4))
    assert alpha == 2781
    stationary_numerators = [27, 27, 27, 14]
    assert all(sum(stationary_numerators[i]*Q[i][j] for i in range(4)) == 0 for j in range(4))
    actual_char = characteristic(Q)
    expected_char = polymul([0, 1], polymul([1595, 1], [4745**2 + 607500, 9490, 1]))
    assert actual_char == expected_char
    cycles = cycle_ratios(Q)
    assert len(cycles) == 7
    # Two-cycles have zero affinity. Repeated closed walks give weighted
    # averages of simple-cycle mean affinities, hence cannot increase the max.
    assert all(k < 19 ** len(c) for c, k in cycles)
    dominant_K = cycles[0][1]
    assert dominant_K == F(177853829, 38529)
    assert all(dominant_K ** len(c) >= k**3 for c, k in cycles)
    # tanh(log(19)/2)=9/10, so beta<9/10 follows without evaluating logs.
    beta_upper = F(9, 10)
    x = 1 - F(4745, alpha)
    unscaled_y_squared = F(607500, alpha**2)
    Y = unscaled_y_squared / beta_upper**2
    assert x == -F(1964, 2781)
    assert Y == F(250000, 2577987)
    assert -1 < x < -F(1, 2)
    A = 3*x*x - 2*x - 1 - Y
    B = -4*x
    C = -2*x - 1
    assert A > 0 and B > 0 and C > 0
    squared_margin = B*B*C - A*A
    assert squared_margin == F(19884434701, 2215338990723)
    assert squared_margin > 0
    # A < B*sqrt(C), so 3x^2-2x-1+4x*sqrt(-2x-1) < Y < y^2.
    return {
        "status": "PASS", "proof_arithmetic": "exact Python Fraction and integer arithmetic",
        "mathematical_input": "Karpelevich n=4 left-hand boundary formula",
        "matrix": Q, "alpha": alpha,
        "stationary_distribution": [str(F(v, 95)) for v in stationary_numerators],
        "eigenvalues": ["0", "-1595", "-4745 + 450*sqrt(3)*i", "-4745 - 450*sqrt(3)*i"],
        "characteristic_coefficients_ascending": [str(v) for v in actual_char],
        "cycles": [{"cycle": [v+1 for v in c], "length": len(c), "max_forward_reverse_ratio": str(k),
                    "ratio_below_19_power_length": k < 19**len(c)} for c, k in cycles],
        "dominant_cycle": [1,2,3], "dominant_cycle_ratio": str(dominant_K),
        "beta_upper": str(beta_upper), "transformed_x": str(x),
        "transformed_y_squared_lower_bound": str(Y),
        "A": str(A), "B": str(B), "C": str(C),
        "positive_rational_square_margin": str(squared_margin),
        "fingerprints": [fingerprint(F(1, n)) for n in (10, 100, 1000)]
    }


if __name__ == "__main__":
    result = verify()
    path = _receipt_path("affine_counterexample_verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "receipt": str(path),
                      "square_margin": result["positive_rational_square_margin"]}, indent=2))
