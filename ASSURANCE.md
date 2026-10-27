# Assurance

What has been checked and what has not. Each row is a separate kind of assurance; no row implies another.

| Dimension | State | Evidence |
|---|---|---|
| Availability | Public GitHub release and Zenodo DOI 10.5281/zenodo.23687327 | Release assets, [SHA256SUMS](SHA256SUMS) |
| Written proofs | Complete proofs in the manuscript for Proposition 2.1, Theorems 3.1, 4.1, 5.1, 6.1, 7.4, Corollary 6.2 and Lemmas 2.3–2.6, 7.1–7.3 | `paper/affinity_karpelevich.pdf`. Theorem 4.1 relies on the cited sector bound. Theorem 2.2 (Karpelevich, in Ito's form) is used as published, with the continuity reading stated in Section 2.3. |
| Exact certificates | Exact integer and rational arithmetic, standard library only | `code/verify_affine_counterexample.py`, `code/audit_karpelevich.py`, `code/audit_all_dimensions.py` |
| Computer-assisted certificate (n = 5, 6) | Exact, with outward-rounded rational intervals | `code/certify_higher_dimensions.py`. The terminal boxes are in `receipts/exterior_certificates.json`, and Appendix A prints the matrices, cycles, enclosures and per-pair data. |
| Stand-alone certificate check | Passed | `code/check_exterior_certificate.py` shares no code with the certifier and uses exact unrounded intervals. It recomputes the characteristic polynomial of Q, the cycle ratios and β bounds, the root bound, the box W and S, and the exact cover and zero-exclusion for every Farey pair. |
| Numerical results | Labelled as such | Radial margins, the ε-scale in Remark 7.5, and the single-cycle search in Problem 8.1 |
| Internal replay | Passed | `code/replay_all.py` regenerates every receipt from a clean copy. They are identical except for timing fields. See [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). |
| Semantic negative controls | Passed | `negative_controls.py` rejects eleven corruptions: a box moved inside Ω_5, a missing box, overlapping boxes, a perturbed rate, a loosened β bound, an omitted Farey pair, a too-small S, a one-unit change to the four-state witness (in two verifiers), an n = 5 instance with ε = 1/10, and a point 10⁻⁶ below the four-state arc. |
| Optimised mode | Not applicable by design | The verifiers use `assert`, so they refuse to run under `python -O` rather than silently skip checks. CI tests this refusal. |
| Implementation diversity | Partial | A targeted proof audit rebuilt both certified matrices and recertified them with python-flint ball arithmetic, independently of the package code. Its radial margins (4.669e-5, 2.210e-4) match Appendix A. The re-review reran the certifier from a fresh copy. All of this is diversity within one producer workflow, not independent reimplementation. |
| Internal AI-assisted review | Done | A five-perspective review; AI-assisted correctness audits by a different model (configured as OpenAI gpt-5.6-sol) of the draft and of the revision; a targeted proof audit; and a verification re-review. See [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). This is not peer review. |
| Independent reproduction by an unaffiliated party | Not established | |
| Specialist (human) review | Not established | |
| Editorial peer review | Not established | |
| Formal verification | Not attempted | No proof assistant was used. |
| Source fidelity | Checked | (S3) quoted verbatim from the arXiv:2507.08938v2 source, Supplement I.2. The re-review compared it word for word. |
| Novelty | Bounded search only | [RESEARCH_GATES.json](RESEARCH_GATES.json), `notes/` |
| Citations | Every DOI resolved, titles matched | [CITATION_AUDIT.md](CITATION_AUDIT.md) |

## Scope and limits

* Every counterexample uses the complete graph. The single-cycle case is open.
* Theorem 7.4 is asymptotic and non-uniform. Only n = 4, 5, 6 have explicit certified instances.
* The violations are thin: radial margins are about 10⁻⁴ or smaller for n ≥ 5, and the four-state vertical excess is 0.0087.
* Byte-identical replay shows that the shipped receipts are what the shipped programs produce. It does not by itself show that the programs implement the manuscript's definitions. That rests on the written proofs, the printed certificate data, the stand-alone checker and the negative controls.
