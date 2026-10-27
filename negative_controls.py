#!/usr/bin/env python3
"""Semantic negative controls: the checks must reject corrupted claims and data.

Usage (from the repository root):  python3 -B negative_controls.py
First an unmodified baseline must pass. Then each control corrupts one thing in a
temporary copy and requires the relevant verifier to fail. Nothing in the
repository is modified. Standard library only; run without -O.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODE, RECEIPTS = ROOT / "code", ROOT / "receipts"
CHECK = CODE / "check_exterior_certificate.py"


def run(argv, cwd):
    return subprocess.run([sys.executable, "-B"] + argv, cwd=cwd, capture_output=True, text=True)


def cert_control(td, label, mutate):
    d = json.loads((RECEIPTS / "exterior_certificates.json").read_text())
    mutate(d)
    p = Path(td) / f"{label}.json"
    p.write_text(json.dumps(d))
    return run([str(CHECK), str(p)], td).returncode != 0


def script_control(td, script, old, new):
    work = Path(td) / f"mut-{script}-{abs(hash(old + new)) % 10**6}"
    work.mkdir()
    src = (CODE / script).read_text()
    assert src.count(old) >= 1, (script, old)
    (work / script).write_text(src.replace(old, new, 1))
    return run([str(work / script), "--out", str(work / "out")], work).returncode != 0


def inst(d, n):
    return next(i for i in d["instances"] if i["dimension"] == n)


def main():
    if not __debug__:
        sys.exit("run without -O")
    results = []
    with tempfile.TemporaryDirectory(prefix="karpelevich-controls-") as td:
        base = run([str(CHECK), str(RECEIPTS / "exterior_certificates.json")], td)
        if base.returncode:
            sys.exit("baseline certificate check failed; controls are meaningless")
        b2 = run([str(CODE / "verify_affine_counterexample.py"), "--out", str(Path(td) / "base")], td)
        if b2.returncode:
            sys.exit("baseline four-state verifier failed")

        def shift_w_inward(d):  # n = 5 box moved 1e-3 towards the region
            i = inst(d, 5)
            i["W_exact"]["y"] = [str(F(x) - F(1, 1000)) for x in i["W_exact"]["y"]]

        def drop_box(d):  # remove one terminal box from the tightest Farey pair
            fam = next(f for f in inst(d, 6)["families"] if f["farey_pair"] == ["2/5", "1/2"])
            fam["boxes"].pop(len(fam["boxes"]) // 2)

        def widen_box(d):  # stretch one box so the boxes overlap
            fam = inst(d, 5)["families"][0]
            fam["boxes"][0][1] = str(F(fam["boxes"][0][1]) + F(1, 10**6))

        def change_rate(d):  # perturb one off-diagonal rate of the n = 5 matrix
            q = inst(d, 5)["Q"]
            q[0][1] = str(F(q[0][1]) + F(1, 40000)); q[0][0] = str(F(q[0][0]) - F(1, 40000))

        def loosen_beta(d):  # claim a larger affinity factor than the cycles give
            i = inst(d, 6)
            i["beta_bounds"][1] = str((F(i["beta_bounds"][1]) + 1) / 2)

        def drop_pair(d):  # omit one Farey pair
            inst(d, 4)["families"].pop()

        def small_S(d):  # sigma range too short to reach the unit circle
            i = inst(d, 5)
            i["sigma_max"] = str(1 + (F(i["sigma_max"]) - 1) / 2)

        for label, f in [("W shifted inside the region (n=5)", shift_w_inward),
                         ("terminal box removed (n=6, pair 2/5,1/2)", drop_box),
                         ("overlapping box (n=5)", widen_box),
                         ("rate perturbed (n=5)", change_rate),
                         ("beta upper bound loosened (n=6)", loosen_beta),
                         ("Farey pair omitted (n=4)", drop_pair),
                         ("S too small (n=5)", small_S)]:
            results.append((label, cert_control(td, label.split()[0], f)))

        results.append(("four-state witness: one rate changed (2727 -> 2726)",
                        script_control(td, "verify_affine_counterexample.py",
                                       "[-2768, 2727, 27, 14]", "[-2768, 2726, 27, 14]")))
        results.append(("four-state witness in audit: one rate changed",
                        script_control(td, "audit_karpelevich.py",
                                       "[-2768, 2727, 27, 14]", "[-2768, 2726, 27, 14]")))
        results.append(("certifier: n = 5 at eps = 1/10 (affinity too weak)",
                        script_control(td, "certify_higher_dimensions.py",
                                       "(5, Fr(3, 5), Fr(1, 40000))", "(5, Fr(3, 5), Fr(1, 10))")))

        # a point strictly inside Omega_4, 1e-6 below the left arc at x = -0.75,
        # must not pass the radial exterior test
        sys.path.insert(0, str(CODE))
        import certify_higher_dimensions as c
        x = F(-3, 4)
        g = 3 * x * x - 2 * x - 1  # + 4x sqrt(-2x-1); sqrt(1/2) bracketed below
        lo, hi = c.iroot_bounds(F(1, 2), 2)
        y2 = g + 4 * x * hi  # x < 0, so this is a lower bound for g(x)
        ylo, _ = c.iroot_bounds(y2, 2)
        y = ylo - F(1, 10**6)
        W = (c.I(x), c.I(y))
        S = F(2)
        try:
            c.exterior_test(4, W, S, max_boxes=20000)
            ok = False
        except (RuntimeError, AssertionError):
            ok = True
        results.append(("point 1e-6 below the n=4 arc fails the exterior test", ok))

    width = max(len(l) for l, _ in results)
    for label, ok in results:
        print(f"{'rejected' if ok else 'ACCEPTED'}  {label}")
    if not all(ok for _, ok in results):
        sys.exit("FAIL: a corrupted input was accepted")
    print(f"PASS: all {len(results)} corrupted inputs rejected")


if __name__ == "__main__":
    main()
