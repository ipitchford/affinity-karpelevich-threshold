# Replay receipt

Producer-side replay, 27 October 2026, macOS (Apple silicon), Python 3.11.14 via `uv run python3 -I -B`, run from the assembled release tree. This is not independent reproduction.

| Command | Result |
|---|---|
| `python3 -B code/replay_all.py` | PASS. All six receipts were regenerated in a temporary directory and match `receipts/`, excluding timing fields and the interpreter-version field, with binary floating-point orientation fields compared to a relative tolerance of 1e-9: affine_counterexample_verification, karpelevich_audit_result, all_dimensions_audit_result, extension_fingerprints, higher_dimension_certificates and exterior_certificates. `check_exterior_certificate.py` passed on both the shipped and the regenerated certificates (n = 4: 6 Farey pairs, 166 boxes; n = 5: 10 pairs, 352 boxes; n = 6: 12 pairs, 578 boxes). Wall time about 1.5 min. |
| `python3 -B negative_controls.py` | PASS: all 11 corrupted inputs were rejected after an unmodified baseline passed. Wall time about 2.5 min. |
| `python3 -O -B code/<verifier>.py` | Refuses to run, by design: the verifiers rely on `assert`. |
| `pdflatex affinity_karpelevich.tex` (three runs) | 20 pages. No overfull boxes and no undefined references. Every page was inspected. |

Earlier replays: before packaging, every script was rerun from a clean copy, each in its own directory. The verification re-review and the proof audit also reran the certifier, and the proof audit recertified n = 5, 6 independently with python-flint ball arithmetic. GitHub Actions (`.github/workflows/replay.yml`) repeats the replay, the negative controls and the `-O` refusal on Ubuntu with Python 3.11.

Timing fields in receipts (`exterior_test_seconds_platform_dependent`) and decimal orientation fields may differ between machines. All decisive fields are exact.
