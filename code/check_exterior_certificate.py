#!/usr/bin/env python3
"""Small stand-alone checker for exterior_certificates.json.

Independent of certify_higher_dimensions.py: it shares no code with it and
uses exact rational interval arithmetic with no rounding at all.  For each
instance it checks, from the matrix Q and the data in the certificate:

  1. Q is a generator (rows sum to 0, off-diagonal rates > 0); alpha = max|Q_ii|.
  2. beta_lo <= beta(Q) <= beta_hi, by enumerating every simple cycle.
  3. An eigenvalue lambda of Q (exact for n = 4; for n = 5, 6 the classical
     bound: a root of p lies within deg(p)|p(l0)|/|p'(l0)| of l0, applied to
     the characteristic polynomial of Q itself) has rescaled image
     zeta = (1 + Re lambda/alpha) + i Im lambda/(alpha beta) inside W.
  4. S^2 |w|^2 >= 1 on W.
  5. For every Farey pair of order n, the listed terminal boxes cover
     [1, S] x [0, 1] exactly (inside, pairwise interior-disjoint, total area
     equal), and on each box an interval enclosure of the real or imaginary
     part of  (sigma w)^s ((sigma w)^q - tau)^k - (1 - tau)^k (sigma w)^(qk)
     excludes 0.  Boxes are listed in the coordinate a = 1 - tau.
By the radial exterior test of the paper, W, and hence zeta, lies outside
Omega_n.  Usage: python3 -I check_exterior_certificate.py CERT.json
"""
if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

import json
import sys
from fractions import Fraction as F
from itertools import permutations


class Iv:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        assert self.lo <= self.hi

    def __add__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    def __sub__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __mul__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Iv(min(p), max(p))

    def has0(self):
        return self.lo <= 0 <= self.hi


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cpow(z, k):
    """Binary powering (the interval extension the certificate is built on)."""
    r, b = (Iv(1), Iv(0)), z
    while k:
        if k & 1:
            r = cmul(r, b)
        k >>= 1
        if k:
            b = cmul(b, b)
    return r


def rpow(x, k):
    r = Iv(1)
    for _ in range(k):
        r = r * x
    return r


def charpoly(Q):
    """Faddeev-LeVerrier: coefficients c[0..n] of det(zI - Q), c[n] = 1."""
    n = len(Q)
    c = [F(0)] * (n + 1)
    c[n] = F(1)
    M = [[F(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        M = [[sum(Q[i][l] * M[l][j] for l in range(n)) + (c[n - k + 1] if i == j else 0)
              for j in range(n)] for i in range(n)]
        AM = [[sum(Q[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c[n - k] = -sum(AM[i][i] for i in range(n)) / k
    return c


def ceval(c, z):
    re, im = F(0), F(0)
    for a in reversed(c):
        re, im = re * z[0] - im * z[1] + a, re * z[1] + im * z[0]
    return re, im


def check(inst):
    n = inst["dimension"]
    Q = [[F(x) for x in row] for row in inst["Q"]]
    assert all(sum(r) == 0 for r in Q)
    assert all(Q[i][j] > 0 for i in range(n) for j in range(n) if i != j)
    alpha = max(-Q[i][i] for i in range(n))
    # 2. beta bounds: m = (1+beta)/(1-beta) = max_c K_c^(1/|c|)
    blo, bhi = (F(x) for x in inst["beta_bounds"])
    mlo, mhi = (1 + blo) / (1 - blo), (1 + bhi) / (1 - bhi)
    attained = False
    for L in range(3, n + 1):
        for c in permutations(range(n), L):
            if c[0] != min(c) or c[1] > c[-1]:
                continue
            K = F(1)
            for i, j in zip(c, c[1:] + c[:1]):
                K *= Q[i][j] / Q[j][i]
            K = max(K, 1 / K)
            assert K <= mhi ** L
            attained |= K >= mlo ** L
    assert attained
    # 3. eigenvalue enclosure, as a rectangle (re +- R, im +- R) in lambda
    p = charpoly(Q)
    W = inst["W_exact"]
    X = (F(W["x"][0]), F(W["x"][1]))
    Y = (F(W["y"][0]), F(W["y"][1]))
    if n == 4:  # lambda = -4745 + 450 sqrt(3) i, a root of z^2 + 9490 z + 4745^2 + 607500
        quad = [F(4745 ** 2 + 607500), F(9490), F(1)]
        # exact division of p by quad
        rem = p[:]
        for k in range(len(rem) - 1, 1, -1):
            f = rem[k]
            for j in range(3):
                rem[k - 2 + j] -= f * quad[j]
        assert rem[0] == rem[1] == 0
        re0, R2re = F(-4745), F(0)
        # Im lambda = 450 sqrt 3: check the zeta interval by squares
        assert X[0] <= 1 + re0 / alpha <= X[1]
        assert (Y[0] * alpha * bhi) ** 2 <= 450 ** 2 * 3 <= (Y[1] * alpha * blo) ** 2
    else:
        l0 = (F(inst["root_centre"][0]) - F(inst["eigenvalue_shift"]),
              F(inst["root_centre"][1]))
        dp = [k * p[k] for k in range(1, len(p))]
        pr, pi = ceval(p, l0)
        dr, di = ceval(dp, l0)
        R2 = F(n * n) * (pr * pr + pi * pi) / (dr * dr + di * di)
        assert l0[1] > 0 and l0[1] ** 2 > R2       # the enclosed root is nonreal
        # slack of W around the image of the disc, in lambda units
        sl = [alpha * (X[1] - 1) - l0[0],
              l0[0] - alpha * (X[0] - 1)]
        assert all(d > 0 and d * d >= R2 for d in sl)
        # Y: need Y0 <= (im - R)/(alpha bhi) and (im + R)/(alpha blo) <= Y1
        d1 = l0[1] - Y[0] * alpha * bhi
        d2 = Y[1] * alpha * blo - l0[1]
        assert d1 > 0 and d2 > 0 and d1 * d1 >= R2 and d2 * d2 >= R2
    # 4. S
    S = F(inst["sigma_max"])
    assert Y[0] > 0
    xmin2 = 0 if X[0] <= 0 <= X[1] else min(X[0] ** 2, X[1] ** 2)
    assert S * S * (xmin2 + Y[0] ** 2) >= 1
    # 5. Farey pairs and boxes
    fr = sorted({F(a, b) for b in range(1, n + 1) for a in range(b + 1)})
    pairs = list(zip(fr[:-1], fr[1:]))
    fams = inst["families"]
    assert len(fams) == len(pairs)
    wx, wy = Iv(*X), Iv(*Y)
    nboxes = 0
    for (a, b), fam in zip(pairs, fams):
        assert [F(x) for x in fam["farey_pair"]] == [a, b]
        q, s = sorted((a.denominator, b.denominator))
        assert (fam["q"], fam["s"], fam["k"]) == (q, s, n // q)
        k = n // q
        boxes = [tuple(F(x) for x in bx) for bx in fam["boxes"]]
        area = F(0)
        for s0, s1, t0, t1 in boxes:
            assert 1 <= s0 < s1 <= S and 0 <= t0 < t1 <= 1
            area += (s1 - s0) * (t1 - t0)
        assert area == (S - 1) * 1
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                A, B = boxes[i], boxes[j]
                assert (A[1] <= B[0] or B[1] <= A[0] or A[3] <= B[2] or B[3] <= A[2])
        for s0, s1, t0, t1 in boxes:
            sg = Iv(s0, s1)
            z = (wx * sg, wy * sg)
            tau = Iv(1 - t1, 1 - t0)  # boxes are in a = 1 - tau
            zq = cpow(z, q)
            inner = (zq[0] - tau, zq[1])
            lhs = cmul(cpow(z, s), cpow(inner, k))
            rhs = cpow(z, q * k)
            c = rpow(Iv(1) - tau, k)
            val = (lhs[0] - rhs[0] * c, lhs[1] - rhs[1] * c)
            assert not (val[0].has0() and val[1].has0())
        nboxes += len(boxes)
    return {"dimension": n, "farey_pairs": len(pairs), "terminal_boxes": nboxes}


def main():
    cert = json.load(open(sys.argv[1]))
    out = [check(i) for i in cert["instances"]]
    print(json.dumps({"status": "PASS", "checked": out}))


if __name__ == "__main__":
    main()
