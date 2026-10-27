"""Independent finite fingerprints for the all-dimensional Markov proof.

The proof for all n is analytic. These exact checks detect indexing errors
in the two matrix families, their stationary vectors and cycle coefficients.
Only the Python standard library is needed.
"""
if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb
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



def matrix(n, t):
    P = [[F(0) for _ in range(n)] for _ in range(n)]
    if n % 2 == 0:
        for j in range(0, n, 2):
            P[j][j + 1] = 1
            P[j + 1][j] = t
            P[j + 1][j + 2 if j + 2 < n else 1] = 1 - t
    else:
        P[0][1] = 1
        for j in range(1, n, 2):
            P[j][j + 1] = 1
            P[j + 1][j] = t
            P[j + 1][j + 2 if j + 2 < n else 0] = 1 - t
    return P


def product(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n)), F(0))
             for j in range(n)] for i in range(n)]


def characteristic_by_traces(P):
    n = len(P)
    power = [[F(i == j) for j in range(n)] for i in range(n)]
    traces = [None]
    for _ in range(n):
        power = product(power, P)
        traces.append(sum(power[i][i] for i in range(n)))
    desc = [F(1)]
    for k in range(1, n + 1):
        desc.append(-sum((desc[k - i] * traces[i]
                          for i in range(1, k + 1)), F(0)) / k)
    return list(reversed(desc))


def characteristic_expected(n, t):
    m = n // 2
    coeff = [F(0) for _ in range(n + 1)]
    for j in range(m + 1):
        coeff[2 * j + n % 2] += comb(m, j) * (-t)**(m - j)
    coeff[1 if n % 2 == 0 else 0] -= (1 - t)**m
    return coeff


def canonical(cycle):
    k = cycle.index(min(cycle))
    a = cycle[k:] + cycle[:k]
    b = [a[0]] + list(reversed(a[1:]))
    return min(a, b)


results = []
t, eps = F(2, 7), F(1, 101)
for n in range(4, 13):
    P = matrix(n, t)
    c = t if n % 2 == 0 else 1 - t
    v = [c] + [F(1)] * (n - 1)
    assert all(sum(row) == 1 for row in P)
    assert all(P[i][i] == 0 for i in range(n))
    assert [sum(v[i] * P[i][j] for i in range(n))
            for j in range(n)] == v
    assert characteristic_by_traces(P) == characteristic_expected(n, t)

    # Off-diagonal resetting; the diagonal is not used in affinity ratios.
    rates = [[P[i][j] + eps * v[j] if i != j else F(0)
              for j in range(n)] for i in range(n)]
    assert max(map(sum, rates)) == 1 + (n - 1) * eps
    triangle = [n - 1, 1, 2] if n % 2 == 0 else [n - 1, 0, 1]
    K = F(1)
    for i, j in zip(triangle, triangle[1:] + triangle[:1]):
        K *= rates[i][j] / rates[j][i]
    if n == 4:
        expected = (1 - t + eps)**2 * (1 + eps) / (eps**2 * (t + eps))
    elif n % 2 == 0:
        expected = (1 - t + eps)**2 / eps**2
    else:
        expected = (1 + eps)**2 / eps**2
    assert K == expected
    record = {"n": n, "stationarity": True, "characteristic_polynomial": True,
              "escape_rate": True, "triangle_ratio": True}

    if n <= 8:
        valuation = [[int(P[i][j] > 0) - int(P[j][i] > 0)
                      for j in range(n)] for i in range(n)]
        best, maximisers, count = F(0), [], 0
        for length in range(3, n + 1):
            for vertices in combinations(range(n), length):
                for tail in permutations(vertices[1:]):
                    if tail[0] > tail[-1]:
                        continue
                    cycle = [vertices[0]] + list(tail)
                    score = F(abs(sum(valuation[i][j]
                                      for i, j in zip(cycle, cycle[1:] + cycle[:1]))),
                              length)
                    count += 1
                    if score > best:
                        best, maximisers = score, [cycle]
                    elif score == best:
                        maximisers.append(cycle)
        assert best == F(2, 3)
        assert maximisers == [canonical(triangle)]
        record.update({"enumerated_unoriented_cycles": count,
                       "maximum_cycle_valuation": str(best),
                       "unique_maximising_cycle": [i + 1 for i in maximisers[0]]})
    results.append(record)

output = {"status": "All exact independent checks passed",
          "fixed_test_t": str(t), "fixed_test_eps": str(eps),
          "scope": "Finite fingerprints; analytic proof separately audited for every n.",
          "results": results}
_receipt_path("all_dimensions_audit_result.json").write_text(
    json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
