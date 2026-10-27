#!/usr/bin/env python3
"""Illustration only; the paper and exact verifiers provide the proof."""
from pathlib import Path
import os
import tempfile
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "markov-mpl-cache"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--out", default="receipts")
OUT = Path(_ap.parse_known_args()[0].out)
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.facecolor": "white"})
x = -1964 / 2781
K = 177853829 / 38529
beta = (K**(1/3) - 1) / (K**(1/3) + 1)
y_plain = 450*np.sqrt(3)/2781
y_scaled = y_plain/beta

def g(xx):
    return np.maximum(0, 3*xx*xx - 2*xx - 1 + 4*xx*np.sqrt(-2*xx - 1))

fig, axes = plt.subplots(1, 2, figsize=(10, 5.625), gridspec_kw={"width_ratios": [1.02, 1]})
teal, plum, grey = "#126B67", "#9C315C", "#72717A"
xx = np.linspace(-1, -0.5, 900)
yy = np.sqrt(g(xx))
ax = axes[0]
ax.fill_between(xx, 0, yy, color=teal, alpha=.11)
ax.plot(xx, yy, color=teal, lw=2.2, label=r"Karpelevich boundary")
ax.plot(xx, np.sqrt(3)*(xx+1), color=grey, lw=1.5, ls="--", label="Farey polygon boundary")
ax.scatter([x], [y_scaled], color=plum, s=58, zorder=5, label="Inverse-scaled eigenvalue")
ax.set(xlim=(-1, -.5), ylim=(0, .9), xlabel=r"Real coordinate $x$", ylabel=r"Imaginary coordinate $y$")
ax.set_title("The left arc for four states", loc="left", fontweight="bold", fontsize=12)
ax.legend(loc="upper left", frameon=False, fontsize=8.5, handlelength=2.4)
ax.text(-.98, .055, r"Allowed by $\Omega_4$", color=teal, fontsize=10)
ax.grid(alpha=.15)

ax = axes[1]
ax.fill_between(xx, 0, yy, color=teal, alpha=.11)
ax.plot(xx, yy, color=teal, lw=2.2)
ax.plot([x, x], [y_plain, y_scaled], color=grey, lw=1.1, zorder=3)
ax.scatter([x], [y_plain], s=45, facecolors="white", edgecolors=grey, linewidths=1.6, zorder=6)
ax.scatter([x], [y_scaled], color=plum, s=60, zorder=6)
ax.scatter([x], [float(np.sqrt(g(x)))], s=26, color=teal, zorder=5)
ax.annotate(r"$1+\lambda/\alpha$", (x, y_plain), xytext=(-.74, .263),
            arrowprops={"arrowstyle": "-", "color": grey}, fontsize=11, color=grey)
ax.annotate(r"$\zeta(\lambda)$", (x, y_scaled), xytext=(-.699, .333),
            arrowprops={"arrowstyle": "-", "color": plum}, fontsize=11, color=plum)
ax.text(-.744, .357, "Exact proof certifies a strict crossing", fontsize=9.5)
ax.text(-.6975, .2965, "Boundary", color=teal, fontsize=9)
ax.set(xlim=(-.748, -.67), ylim=(.247, .368), xlabel=r"Real coordinate $x$")
ax.set_title("The certified crossing, enlarged", loc="left", fontweight="bold", fontsize=12)
ax.grid(alpha=.15)
fig.subplots_adjust(left=.085, right=.98, top=.87, bottom=.15, wspace=.26)
fig.text(.085, .045, "Curves and markers are illustrative. The separation is established by integer arithmetic.",
         fontsize=9, color="#494750")
for ext in ("pdf", "png"):
    fig.savefig(OUT / f"spectral_geometry.{ext}", dpi=220)
print(f"Created {OUT / 'spectral_geometry.pdf'}")

# ---------------------------------------------------------------- overview
# Fig. 1 of the paper: the whole region Omega_4, the valid outer bounds and
# the rescaled eigenvalue of the witness.  Boundary computed from the Ito
# polynomials of all Farey pairs of order 4 (illustration only).
from math import gcd
NB = 3600
rad = np.zeros(NB)
fr = sorted({p/q for q in range(1, 5) for p in range(0, q+1) if gcd(p, q) == 1})
den = {p/q: q for q in range(1, 5) for p in range(0, q+1) if gcd(p, q) == 1}
for f0, f1 in zip(fr[:-1], fr[1:]):
    q, s = sorted((den[f0], den[f1])); k = 4//q
    for a in np.linspace(0, 1, 3001):
        poly = np.poly1d([1]+[0]*s)*(np.poly1d([1]+[0]*q)-(1-a))**k - a**k*np.poly1d([1]+[0]*(q*k))
        for z in np.roots(poly.coeffs):
            for zz in (z, np.conj(z)):
                i = int((np.angle(zz) % (2*np.pi))/(2*np.pi)*NB) % NB
                rad[i] = max(rad[i], abs(zz))
ang = (np.arange(NB)+.5)/NB*2*np.pi
fig, ax = plt.subplots(figsize=(6.2, 6.6))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color=grey, lw=1, ls=":", label="Unit disc (ellipse bound)")
poly = np.exp(2j*np.pi*np.array([0, 1/4, 1/3, 1/2, 2/3, 3/4, 1]))
ax.plot(poly.real, poly.imag, color=grey, lw=1.3, ls="--", label="Farey polygon (proved bound)")
bx, by = rad*np.cos(ang), rad*np.sin(ang)
ax.fill(bx, by, color=teal, alpha=.13)
ax.plot(np.append(bx, bx[0]), np.append(by, by[0]), color=teal, lw=2, label=r"Karpelevich region $\Omega_4$")
ax.scatter([x], [y_scaled], color=plum, s=55, zorder=5, label=r"Rescaled eigenvalue $\zeta$ of $Q_*$")
ax.scatter([x], [y_plain], s=40, facecolors="white", edgecolors=grey, zorder=5, label=r"Plain uniformisation $1+\lambda/\alpha$")
ax.set_aspect("equal"); ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), xlabel="Re", ylabel="Im")
ax.grid(alpha=.15)
fig.legend(*ax.get_legend_handles_labels(), loc="lower center", ncol=2, fontsize=8, frameon=False)
fig.subplots_adjust(bottom=.24, top=.98)
for ext in ("pdf", "png"):
    fig.savefig(OUT / f"region_overview.{ext}", dpi=220)
print(f"Created {OUT / 'region_overview.pdf'}")
