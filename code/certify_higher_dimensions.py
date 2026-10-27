#!/usr/bin/env python3
"""Exact, standard-library certificates of failure of (C) in dimensions 5 and 6.

For each instance (n, t, eps) the script proves, using only integers,
rational numbers and outward-rounded rational interval arithmetic:

  1. Q = P_n(t) - I + eps (1 v - V I) is a generator with positive
     off-diagonal rates, and det(zI - Q) = z * G(z + 1 + V eps), where
     G(z) = F_{n,t}(z)/(z - 1) and F_{n,t} = det(zI - P_n(t)).
  2. A root z* of F_{n,t} lies in an explicit rational disc (classical bound:
     some root lies within deg(p) |p(z0)|/|p'(z0)| of z0).  Hence
     lambda = z* - 1 - V eps is an eigenvalue of Q.
  3. Enumeration of every simple cycle of the complete graph gives rational
     bounds beta_lo <= beta(Q) <= beta_hi.
  4. The rescaled eigenvalue zeta lies in an explicit rational box W.
  5. Exterior test (Lemma "radial exterior test" in the paper): for every
     Farey pair of order n, the Ito polynomial
         f_a(z) = z^s (z^q - (1-a))^k - a^k z^{qk},  k = floor(n/q),
     has no zero z = sigma w with w in W, 1 <= sigma <= S, 0 <= a <= 1,
     where S >= 1/|w| on W.  By the Karpelevic theorem in Ito's form, this
     shows that W lies outside Omega_n.

The four-state witness Q_w of Theorem 3.1 is re-certified by the same
generic test as an independent cross-check of Lemma 2.1.

Usage:  python3 certify_higher_dimensions.py [--out DIR] [--force]
The receipt is written to DIR/higher_dimension_certificates.json
(default DIR = ./receipts).  Existing receipts are never overwritten
unless --force is given.
"""
if not __debug__:  # the checks below are assert statements
    raise SystemExit("refusing to run under python -O: this verifier relies on assert")

from fractions import Fraction as Fr
from itertools import permutations
from math import gcd, isqrt, comb, log
import argparse
import json
import sys
import time
from pathlib import Path

PBITS = 128  # fixed-point outward rounding grid 2^-128 for interval end points
ONE = 1 << PBITS


def _fdown(x):
    x = Fr(x)
    return (x.numerator << PBITS) // x.denominator


def _fup(x):
    x = Fr(x)
    return -((-x.numerator << PBITS) // x.denominator)


class I:
    """Closed real interval [a, b] * 2^-PBITS with integer end points a <= b.

    Every operation rounds outward, so the true value set is always enclosed."""
    __slots__ = ("a", "b")

    def __init__(self, lo, hi=None, raw=False):
        if raw:
            self.a, self.b = lo, hi
        else:
            self.a = _fdown(lo)
            self.b = _fup(lo if hi is None else hi)
        assert self.a <= self.b

    @property
    def lo(self):
        return Fr(self.a, ONE)

    @property
    def hi(self):
        return Fr(self.b, ONE)

    def __add__(self, o):
        o = o if isinstance(o, I) else I(o)
        return I(self.a + o.a, self.b + o.b, raw=True)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.b, -self.a, raw=True)

    def __sub__(self, o):
        o = o if isinstance(o, I) else I(o)
        return I(self.a - o.b, self.b - o.a, raw=True)

    def __rsub__(self, o):
        return I(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, I) else I(o)
        p = (self.a * o.a, self.a * o.b, self.b * o.a, self.b * o.b)
        return I(min(p) >> PBITS, -((-max(p)) >> PBITS), raw=True)

    __rmul__ = __mul__

    def contains0(self):
        return self.a <= 0 <= self.b

    def width(self):
        return Fr(self.b - self.a, ONE)


class CI:
    """Rectangular complex interval."""
    __slots__ = ("re", "im")

    def __init__(self, re, im):
        self.re = re if isinstance(re, I) else I(re)
        self.im = im if isinstance(im, I) else I(im)

    def __add__(self, o):
        return CI(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return CI(self.re - o.re, self.im - o.im)

    def __mul__(self, o):
        if isinstance(o, CI):
            return CI(self.re * o.re - self.im * o.im,
                      self.re * o.im + self.im * o.re)
        return CI(self.re * o, self.im * o)

    def contains0(self):
        return self.re.contains0() and self.im.contains0()


def cpow(z, k):
    ans = CI(I(1), I(0))
    base = z
    while k:
        if k & 1:
            ans = ans * base
        k >>= 1
        if k:
            base = base * base
    return ans


# ------------------------------------------------------------ exact algebra
def polymul(a, b):
    ans = [Fr(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                ans[i + j] += u * v
    return ans


def polyadd(a, b):
    ans = [Fr(0)] * max(len(a), len(b))
    for i, v in enumerate(a):
        ans[i] += v
    for i, v in enumerate(b):
        ans[i] += v
    return ans


def charpoly(m):
    """Ascending coefficients of det(zI - m), by permutation expansion."""
    n = len(m)
    ans = [Fr(0)] * (n + 1)
    for p in permutations(range(n)):
        sign = (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = [Fr(sign)]
        for i in range(n):
            term = polymul(term, [-m[i][p[i]], Fr(int(i == p[i]))])
            if not any(term):
                break
        ans = polyadd(ans, term)
    return ans


def peval(c, z):
    """Evaluate ascending coefficients at a complex rational (re, im)."""
    re, im = Fr(0), Fr(0)
    for a in reversed(c):
        re, im = re * z[0] - im * z[1] + a, re * z[1] + im * z[0]
    return re, im


def pderiv(c):
    return [i * c[i] for i in range(1, len(c))]


def shift(c, h):
    """Coefficients of p(z + h)."""
    ans = [Fr(0)]
    for a in reversed(c):
        ans = polyadd(polymul(ans, [h, Fr(1)]), [a])
    while len(ans) > 1 and ans[-1] == 0:
        ans.pop()
    return ans


def divide_by_linear(c, r):
    """Synthetic division of p by (z - r); returns quotient, remainder."""
    n = len(c) - 1
    q = [Fr(0)] * n
    acc = Fr(0)
    for i in range(n, 0, -1):
        acc = acc * r + c[i]
        q[i - 1] = acc
    rem = acc * r + c[0]
    return q, rem


def boundary_matrix(n, t):
    P = [[Fr(0)] * n for _ in range(n)]
    m = n // 2
    if n % 2 == 0:
        for k in range(1, m + 1):
            P[2 * k - 2][2 * k - 1] = Fr(1)
            P[2 * k - 1][2 * k - 2] = t
        for k in range(1, m):
            P[2 * k - 1][2 * k] = 1 - t
        P[n - 1][1] = 1 - t
        c = t
    else:
        P[0][1] = Fr(1)
        for k in range(1, m + 1):
            P[2 * k - 1][2 * k] = Fr(1)
            P[2 * k][2 * k - 1] = t
        for k in range(1, m):
            P[2 * k][2 * k + 1] = 1 - t
        P[n - 1][0] = 1 - t
        c = 1 - t
    v = [c] + [Fr(1)] * (n - 1)
    return P, v


def ito_reduced(n, t):
    """Ascending coefficients of F_{n,t}."""
    m = n // 2
    a = [Fr(0)] * (n + 1)
    off = n % 2
    for k in range(m + 1):
        a[2 * k + off] += comb(m, k) * (-t) ** (m - k)
    a[0 if off else 1] -= (1 - t) ** m
    return a


def simple_cycles(n):
    for length in range(3, n + 1):
        for c in permutations(range(n), length):
            if c[0] == min(c) and c[1] < c[-1]:
                yield c


def iroot_bounds(x, k, digits=60):
    """Rationals lo <= x^(1/k) <= hi for rational x > 0 (exact checks)."""
    scale = 10 ** digits
    # integer k-th root of x * scale^k
    N = (x.numerator * scale ** k) // x.denominator
    r = 1 << (N.bit_length() // k + 1)  # start above the root
    while True:
        nr = ((k - 1) * r + N // r ** (k - 1)) // k
        if nr >= r:
            break
        r = nr
    while r ** k > N:
        r -= 1
    while (r + 1) ** k <= N:
        r += 1
    lo, hi = Fr(r, scale), Fr(r + 1, scale)
    assert lo ** k <= x <= hi ** k
    return lo, hi


def farey_pairs(n):
    F = sorted({Fr(p, q) for q in range(1, n + 1) for p in range(0, q + 1)})
    for a, b in zip(F[:-1], F[1:]):
        assert b.numerator * a.denominator - a.numerator * b.denominator == 1
        q, s = sorted((a.denominator, b.denominator))
        yield (str(a), str(b), q, s)


# ------------------------------------------------------------- exterior test
def ito_interval(z, a, q, s, k):
    """Interval enclosure of f_a(z) = z^s (z^q - (1-a))^k - a^k z^{qk}."""
    zq = cpow(z, q)
    inner = CI(zq.re - (I(1) - a), zq.im)
    return cpow(z, s) * cpow(inner, k) - cpow(z, q * k) * cpow_real(a, k)


def cpow_real(a, k):
    ans = I(1)
    for _ in range(k):
        ans = ans * a
    return ans


def _gap(iv):
    """Distance of a real interval from 0 (0 if it contains 0)."""
    if iv.contains0():
        return Fr(0)
    return min(abs(iv.lo), abs(iv.hi))


def exterior_test(n, W, S, max_boxes=2_000_000):
    """Return (per-family summary, terminal boxes); raise if a box fails.

    Each terminal box (sigma0, sigma1, tau0, tau1) is reported with the
    enclosure of Re f and Im f; at least one of them excludes 0, and its
    distance from 0 is the box's exclusion margin."""
    report, boxes_out = [], []
    for left, right, q, s in farey_pairs(n):
        k = n // q
        stack = [(Fr(1), S, Fr(0), Fr(1))]
        boxes, terminal, margin = 0, [], None
        while stack:
            s0, s1, a0, a1 = stack.pop()
            boxes += 1
            if boxes > max_boxes:
                raise RuntimeError("box budget exceeded")
            sig = I(s0, s1)
            z = CI(W[0] * sig, W[1] * sig)
            val = ito_interval(z, I(a0, a1), q, s, k)
            if not val.contains0():
                g = max(_gap(val.re), _gap(val.im))
                margin = g if margin is None else min(margin, g)
                terminal.append([str(s0), str(s1), str(a0), str(a1)])
                continue
            # bisect the coordinate with larger relative width
            if (s1 - s0) / (S - 1) >= (a1 - a0):
                sm = (s0 + s1) / 2
                stack += [(s0, sm, a0, a1), (sm, s1, a0, a1)]
            else:
                am = (a0 + a1) / 2
                stack += [(s0, s1, a0, am), (s0, s1, am, a1)]
        print(f"  n={n} pair {left},{right}: {boxes} boxes", file=sys.stderr, flush=True)
        report.append({"farey_pair": [left, right], "q": q, "s": s,
                       "floor_n_over_q": k, "boxes_visited": boxes,
                       "terminal_boxes": len(terminal),
                       "min_exclusion_margin": f"{float(margin):.6e}"})
        boxes_out.append({"farey_pair": [left, right], "q": q, "s": s,
                          "k": k, "boxes": terminal})
    return report, boxes_out


def radial_margin(n, x, y):
    """Float estimate (scale only, not part of the proof) of |w| minus the
    modulus of the outermost Ito-boundary point on the ray through w."""
    import cmath
    w = complex(x, y)
    u = w / abs(w)
    best = None
    for left, right, q, s in farey_pairs(n):
        k = n // q
        for j in range(0, 101):
            tau = j / 100
            for i in range(0, 21):
                r = 0.5 + i / 40
                # Newton in (r, tau) on f(r u, tau) = 0
                R, T = r, tau
                ok = False
                for _ in range(60):
                    z = R * u
                    f = z**s * (z**q - (1 - T))**k - T**k * z**(q * k)
                    fr = (s * z**(s - 1) * (z**q - (1 - T))**k
                          + z**s * k * (z**q - (1 - T))**(k - 1) * q * z**(q - 1)
                          - T**k * q * k * z**(q * k - 1)) * u
                    ft = (z**s * k * (z**q - (1 - T))**(k - 1)
                          - k * T**(k - 1) * z**(q * k))
                    det = (fr.real * ft.imag - fr.imag * ft.real)
                    if det == 0:
                        break
                    dR = (f.real * ft.imag - f.imag * ft.real) / det
                    dT = (fr.real * f.imag - fr.imag * f.real) / det
                    R, T = R - dR, T - dT
                    if abs(dR) + abs(dT) < 1e-15:
                        ok = True
                        break
                if ok and 0 <= T <= 1 and 0 < R <= 1:
                    best = R if best is None else max(best, R)
    return abs(w) - best


# ------------------------------------------------------------------ helpers
def float_root(coeffs, guess, steps=200):
    c = [float(x) for x in coeffs]
    d = [i * c[i] for i in range(1, len(c))]
    z = guess
    for _ in range(steps):
        pv = sum(a * z ** i for i, a in enumerate(c))
        dv = sum(a * z ** i for i, a in enumerate(d))
        z = z - pv / dv
    return z


def continued_root(n, t):
    """Float continuation of the root branch from exp(i(pi - pi/s)) at t=0."""
    import cmath
    s = n - 1 if n % 2 == 0 else n
    z = cmath.exp(1j * (cmath.pi - cmath.pi / s))
    for j in range(1, 401):
        z = float_root(ito_reduced(n, Fr(t) * j / 400), z, 30)
    return z


def refine_exact(coeffs, z, rounds=6):
    """Newton in rational complex arithmetic, rounded to a 2^-200 grid."""
    G = 2 ** 200
    zr = (Fr(round(z.real * 2 ** 50), 2 ** 50), Fr(round(z.imag * 2 ** 50), 2 ** 50))
    d = pderiv(coeffs)
    for _ in range(rounds):
        pr, pi = peval(coeffs, zr)
        dr, di = peval(d, zr)
        den = dr * dr + di * di
        qr = (pr * dr + pi * di) / den
        qi = (pi * dr - pr * di) / den
        zr = (Fr(round((zr[0] - qr) * G), G), Fr(round((zr[1] - qi) * G), G))
    return zr


def root_disc(coeffs, z0):
    """Rational R with a root of p inside |z - z0| <= R."""
    deg = len(coeffs) - 1
    pr, pi = peval(coeffs, z0)
    dr, di = peval(pderiv(coeffs), z0)
    R2 = Fr(deg * deg) * (pr * pr + pi * pi) / (dr * dr + di * di)
    R = Fr(isqrt(R2.numerator * 10 ** 120 // R2.denominator) + 1, 10 ** 60)
    assert R * R >= R2
    return R


# ---------------------------------------------------------------- instances
def certify_family(n, t, eps):
    t, eps = Fr(t), Fr(eps)
    P, v = boundary_matrix(n, t)
    V = sum(v)
    Q = [[P[i][j] - (i == j) + eps * (v[j] - (V if i == j else 0))
          for j in range(n)] for i in range(n)]
    assert all(sum(r) == 1 for r in P)
    assert all(sum(v[i] * P[i][j] for i in range(n)) == v[j] for j in range(n))
    assert all(sum(r) == 0 for r in Q)
    assert all(Q[i][j] > 0 for i in range(n) for j in range(n) if i != j)
    alpha = max(-Q[i][i] for i in range(n))
    assert alpha == 1 + (n - 1) * eps

    Fpoly = ito_reduced(n, t)
    assert charpoly(P) == Fpoly, "charpoly of P_n(t) differs from F_{n,t}"
    G, rem = divide_by_linear(Fpoly, Fr(1))
    assert rem == 0
    # det(zI - Q) = z * G(z + 1 + V eps)
    assert charpoly(Q) == polymul([Fr(0), Fr(1)], shift(G, 1 + V * eps))

    z0 = refine_exact(Fpoly, continued_root(n, float(t)))
    R = root_disc(Fpoly, z0)
    assert (z0[0] - 1) ** 2 + z0[1] ** 2 > R * R  # the root is not z = 1
    assert z0[1] > R                              # and lies in Im z > 0
    re_lam = I(z0[0] - R, z0[0] + R) - (1 + V * eps)
    im_lam = I(z0[1] - R, z0[1] + R)
    return certify_generic(n, Q, alpha, re_lam, im_lam,
                           {"t": str(t), "epsilon": str(eps),
                            "root_centre": [str(z0[0]), str(z0[1])],
                            "root_radius": str(R),
                            "eigenvalue_shift": str(1 + V * eps)})


def certify_generic(n, Q, alpha, re_lam, im_lam, extra):
    # every simple cycle of the complete graph
    ratios = []
    for c in simple_cycles(n):
        r = Fr(1)
        for i, j in zip(c, c[1:] + c[:1]):
            r *= Q[i][j] / Q[j][i]
        ratios.append((max(r, 1 / r), len(c), c))

    def better(a, b):  # a^(1/la) > b^(1/lb)
        return a[0] ** b[1] > b[0] ** a[1]

    best = ratios[0]
    for r in ratios[1:]:
        if better(r, best):
            best = r
    second = None
    for r in ratios:
        if r is not best and (second is None or better(r, second)):
            second = r
    K, L, cyc = best
    mlo, mhi = iroot_bounds(K, L)
    assert all(r[0] <= mhi ** r[1] for r in ratios)   # max mean <= log mhi
    beta_lo = (mlo - 1) / (mlo + 1)
    beta_hi = (mhi - 1) / (mhi + 1)
    X = I(1) + re_lam * I(1 / alpha)
    Y = I(im_lam.lo / (alpha * beta_hi), im_lam.hi / (alpha * beta_lo))
    assert Y.lo > 0
    # S >= 1/|w| for every w in W = X x Y
    xmin2 = min(X.lo ** 2, X.hi ** 2) if not X.contains0() else Fr(0)
    m2 = xmin2 + Y.lo ** 2
    S = Fr(isqrt(m2.denominator * 10 ** 40 // m2.numerator) + 1, 10 ** 20)
    assert S * S * m2 >= 1
    t0 = time.time()
    families, boxes = exterior_test(n, (X, Y), S)
    xm, ym = float((X.lo + X.hi) / 2), float((Y.lo + Y.hi) / 2)
    out = {
        "dimension": n, **extra,
        "Q": [[str(x) for x in row] for row in Q],
        "alpha": str(alpha),
        "dominant_cycle_1_based": [i + 1 for i in cyc],
        "dominant_ratio": str(K),
        "dominant_mean_log_ratio": f"{log(float(K)) / L:.12f}",
        "runner_up_cycle_1_based": [i + 1 for i in second[2]],
        "runner_up_ratio": str(second[0]),
        "runner_up_mean_log_ratio": f"{log(float(second[0])) / second[1]:.12f}",
        "number_of_unoriented_simple_cycles": len(ratios),
        "beta_bounds": [str(beta_lo), str(beta_hi)],
        "beta_decimal": f"{float(beta_lo):.15f}",
        "zeta_box_decimal": {"x": [f"{float(X.lo):.15f}", f"{float(X.hi):.15f}"],
                             "y": [f"{float(Y.lo):.15f}", f"{float(Y.hi):.15f}"]},
        "W_exact": {"x": [str(X.lo), str(X.hi)], "y": [str(Y.lo), str(Y.hi)]},
        "zeta_box_width_bound": f"{float(max(X.width(), Y.width())):.3e}",
        "sigma_max": str(S),
        "exterior_test": families,
        "radial_margin_float_scale_only": f"{radial_margin(n, xm, ym):.4e}",
        "exterior_test_seconds_platform_dependent": round(time.time() - t0, 2),
        "verdict": "zeta lies outside Omega_n: (C) fails for Q",
    }
    return out, boxes


def q_witness():
    Q = [[-2768, 2727, 27, 14], [1427, -2768, 1327, 14],
         [1327, 27, -2768, 1414], [27, 27, 2727, -2781]]
    Q = [[Fr(x) for x in r] for r in Q]
    assert charpoly(Q) == polymul([Fr(0), Fr(1), ], polymul([Fr(1595), Fr(1)],
                                  [Fr(4745 ** 2 + 607500), Fr(2 * 4745), Fr(1)]))
    # lambda = -4745 + 450 sqrt(3) i ; enclose sqrt(3)
    lo, hi = iroot_bounds(Fr(3), 2)
    return certify_generic(4, Q, Fr(2781), I(-4745), I(450 * lo, 450 * hi),
                           {"instance": "Q_w of Theorem 3.1 (cross-check)"})


INSTANCES = [(5, Fr(3, 5), Fr(1, 40000)), (6, Fr(1, 2), Fr(1, 8000))]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="receipts")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "higher_dimension_certificates.json"
    if path.exists() and not args.force:
        sys.exit(f"refusing to overwrite {path}; use --force or another --out")
    cert = out / "exterior_certificates.json"
    if cert.exists() and not args.force:
        sys.exit(f"refusing to overwrite {cert}; use --force or another --out")
    pairs = [q_witness()] + [certify_family(*inst) for inst in INSTANCES]
    results = [r for r, _ in pairs]
    cert.write_text(json.dumps({
        "format": "terminal boxes (sigma0, sigma1, tau0, tau1) per Farey pair; "
                  "checked by check_exterior_certificate.py",
        "instances": [{"dimension": r["dimension"], "Q": r["Q"],
                       "root_centre": r.get("root_centre"),
                       "root_radius": r.get("root_radius"),
                       "eigenvalue_shift": r.get("eigenvalue_shift"),
                       "beta_bounds": r["beta_bounds"], "W_exact": r["W_exact"],
                       "sigma_max": r["sigma_max"], "families": b}
                      for r, b in pairs]}, indent=1) + "\n")
    receipt = {"status": "PASS", "python": sys.version.split()[0],
               "method": "exact rationals; outward-rounded rational intervals "
                         "(fixed-point grid 2^-128); classical root-disc bound; "
                         "radial exterior test against all Ito polynomials",
               "instances": results}
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "receipt": str(path),
                      "instances": [(r["dimension"], r.get("t"), r.get("epsilon"),
                                     r["zeta_box_decimal"]) for r in results]}, indent=2))


if __name__ == "__main__":
    main()
