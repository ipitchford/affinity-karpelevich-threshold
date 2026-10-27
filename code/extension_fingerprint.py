"""Exact object fingerprints for the all-dimensional extension.

Finite instances identify the construction. They are not floating-point
substitutes for the analytic small-parameter existence proof.
"""
if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import hashlib
import json

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



def boundary_matrix(n, t):
    p = [[F(0) for _ in range(n)] for _ in range(n)]
    if n % 2 == 0:
        for k in range(n // 2):
            p[2*k][2*k+1] = 1
            p[2*k+1][2*k] = t
            p[2*k+1][2*k+2 if 2*k+2 < n else 1] = 1-t
        v = [t] + [F(1)]*(n-1)
    else:
        p[0][1] = 1
        for k in range((n-1)//2):
            p[2*k+1][2*k+2] = 1
            p[2*k+2][2*k+1] = t
            p[2*k+2][2*k+3 if 2*k+3 < n else 0] = 1-t
        v = [1-t] + [F(1)]*(n-1)
    return p, v


def characteristic_coefficients(matrix):
    """Faddeev-LeVerrier in exact rational arithmetic, descending order."""
    n = len(matrix)
    b = [[F(i == j) for j in range(n)] for i in range(n)]
    coefficients = [F(1)]
    for k in range(1, n+1):
        ab = [[sum(matrix[i][r]*b[r][j] for r in range(n))
               for j in range(n)] for i in range(n)]
        c = -sum(ab[i][i] for i in range(n))/k
        coefficients.append(c)
        b = [[ab[i][j]+(c if i == j else 0) for j in range(n)] for i in range(n)]
    return coefficients


def simple_cycles(n):
    for length in range(3, n+1):
        for vertices in combinations(range(n), length):
            first = vertices[0]
            for tail in permutations(vertices[1:]):
                if tail[0] < tail[-1]:
                    yield (first,)+tail


def canonical_hash(matrix):
    n = len(matrix)
    least = None
    for order in permutations(range(n)):
        forward = tuple(matrix[i][j] for i in order for j in order)
        transpose = tuple(matrix[j][i] for i in order for j in order)
        key = min(forward, transpose)
        if least is None or key < least:
            least = key
    return hashlib.sha256(
        json.dumps([str(x) for x in least], separators=(",", ":")).encode()
    ).hexdigest()


def fingerprint(n, t=F(1,2), e=F(1,1000)):
    p, v = boundary_matrix(n, t)
    total = sum(v)
    q = [[p[i][j]+e*v[j]-(1+e*total if i == j else 0)
          for j in range(n)] for i in range(n)]
    assert all(sum(row) == 1 for row in p)
    assert all(sum(row) == 0 for row in q)
    assert all(sum(v[i]*p[i][j] for i in range(n)) == v[j] for j in range(n))
    assert all(q[i][j] > 0 for i in range(n) for j in range(n) if i != j)
    assert max(-q[i][i] for i in range(n)) == 1+(n-1)*e
    m = n//2
    expected_ascending = [F(0)]*(n+1)
    for k in range(m+1):
        expected_ascending[2*k+(n%2)] = comb(m,k)*(-t)**(m-k)
    expected_ascending[1 if n%2 == 0 else 0] -= (1-t)**m
    cp = characteristic_coefficients(p)
    assert cp == list(reversed(expected_ascending))
    slopes = []
    for c in simple_cycles(n):
        value = sum(int(p[i][j]>0)-int(p[j][i]>0)
                    for i,j in zip(c,c[1:]+c[:1]))
        slopes.append((F(abs(value),len(c)),c))
    maximum = max(s for s,c in slopes)
    assert maximum == F(2,3)
    maximisers = [list(i+1 for i in c) for s,c in slopes if s == maximum]
    assert len(maximisers) == 1
    scale = 2000
    integer_q = [[int(x*scale) for x in row] for row in q]
    assert all(F(integer_q[i][j],scale)==q[i][j] for i in range(n) for j in range(n))
    return {
        "dimension": n, "t": str(t), "epsilon": str(e),
        "P": [[str(x) for x in row] for row in p],
        "stationary_vector_unnormalised": [str(x) for x in v],
        "Q_integer_scale": scale, "Q_integer": integer_q,
        "P_charpoly_descending": [str(x) for x in cp],
        "Q_charpoly_descending": [str(x) for x in characteristic_coefficients(q)],
        "Q_rank": n-1, "Q_trace": str(sum(q[i][i] for i in range(n))),
        "Q_determinant": "0", "Q_row_sums": [str(sum(row)) for row in q],
        "Q_sorted_entries": [str(x) for x in sorted(x for row in q for x in row)],
        "canonical_Q_hash_transpose_and_relabelling": canonical_hash(q),
        "maximum_cycle_valuation_mean": str(maximum),
        "unique_unoriented_critical_cycle": maximisers[0],
        "zero_pattern_P": [[int(x!=0) for x in row] for row in p],
        "warning": "Fingerprint only; no numerical spectral separation is used as proof."
    }


if __name__ == "__main__":
    result = {"status": "PASS", "instances": [fingerprint(n) for n in (4,5,6)]}
    path = _receipt_path("extension_fingerprints.json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":result["status"], "receipt":str(path)},indent=2))
