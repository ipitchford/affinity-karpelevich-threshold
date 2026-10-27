#!/usr/bin/env python3
"""Replay every exact verifier into a fresh temporary directory and compare.

Usage (from the repository root):  python3 -B code/replay_all.py
Each verifier in code/ is run as  python3 -B code/<script>.py --out <tmp>/<script>
and every JSON receipt it writes must equal the shipped file in receipts/
after removing timing fields (keys containing "seconds"), which depend on the
machine. The stand-alone checker is then run on the shipped and on the
regenerated exterior certificates. Exit status 0 means everything matched.
Standard library only. Run without -O: the verifiers rely on assert.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE, RECEIPTS = ROOT / "code", ROOT / "receipts"
VERIFIERS = ["verify_affine_counterexample", "audit_karpelevich", "audit_all_dimensions",
             "extension_fingerprint", "certify_higher_dimensions"]


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if "seconds" not in k}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def main():
    if not __debug__:
        sys.exit("run without -O: the verifiers rely on assert")
    failures, seen = [], set()
    with tempfile.TemporaryDirectory(prefix="karpelevich-replay-") as td:
        for name in VERIFIERS:
            out = Path(td) / name
            r = subprocess.run([sys.executable, "-B", str(CODE / f"{name}.py"), "--out", str(out)],
                               cwd=td, capture_output=True, text=True)
            if r.returncode:
                failures.append(f"{name}: exit {r.returncode}: {r.stderr[-400:]}")
                continue
            for f in sorted(out.glob("*.json")):
                seen.add(f.name)
                ship = RECEIPTS / f.name
                if not ship.exists():
                    failures.append(f"{name}: unexpected receipt {f.name}")
                elif strip(json.loads(f.read_text())) != strip(json.loads(ship.read_text())):
                    failures.append(f"{name}: {f.name} differs from receipts/")
                else:
                    print(f"match  {f.name}")
        missing = {p.name for p in RECEIPTS.glob("*.json")} - seen
        if missing:
            failures.append(f"shipped receipts not regenerated: {sorted(missing)}")
        for cert in (RECEIPTS / "exterior_certificates.json",
                     Path(td) / "certify_higher_dimensions" / "exterior_certificates.json"):
            r = subprocess.run([sys.executable, "-B", str(CODE / "check_exterior_certificate.py"), str(cert)],
                               capture_output=True, text=True)
            if r.returncode or '"PASS"' not in r.stdout:
                failures.append(f"checker rejected {cert}: {r.stderr[-400:]}")
            else:
                print("checker PASS", "shipped" if cert.parent == RECEIPTS else "regenerated")
    if failures:
        print("FAIL")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print("PASS: every receipt reproduced (timing fields excluded); certificates checked")


if __name__ == "__main__":
    main()
