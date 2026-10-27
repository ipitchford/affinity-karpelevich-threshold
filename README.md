# How fast can a driven Markov network oscillate?

**A four-state counterexample to the affine Karpelevich conjecture, and the exact dimension at which it fails.**

**Release 1.0.0-candidate (27 October 2026). Unrefereed research candidate.**
DOI: [10.5281/zenodo.23687327](https://doi.org/10.5281/zenodo.23687327) (this version) ·
concept DOI [10.5281/zenodo.23687326](https://doi.org/10.5281/zenodo.23687326) (all versions) ·
repository <https://github.com/ipitchford/affinity-karpelevich-threshold> (tag `v1.0.0-candidate`) ·
Evidence Press page <https://evidencepress.org/releases/affinity-karpelevich-threshold/>.

Checked by internal AI-assisted review only. This comprised a multi-perspective review, AI-assisted correctness audits by a different model before and after revision, a targeted proof audit and a verification re-review. It is not peer review, not independent reproduction and not formal verification. See [STATUS.md](STATUS.md) and [ASSURANCE.md](ASSURANCE.md).

Author: Anonymous. Text and data CC0-1.0; code MIT (see `LICENSE`).

The package concerns Supplement Eq. (S3) of Xu, Kolchinsky, Delvenne and Ito, *Thermodynamic geometric constraint on the spectrum of Markov rate matrices*, Phys. Rev. Lett. 135, 257102 (2025), doi:[10.1103/z4t2-18cx](https://doi.org/10.1103/z4t2-18cx); the supplement was read on arXiv:2507.08938v2. (S3) proposes that the eigenvalues of an n-state rate matrix fill the classical Karpelevich region Ω_n of n×n stochastic matrices, stretched by the largest escape rate α and flattened vertically by β′ = tanh(max_c F_c/(2n_c)). The rate matrix has largest escape rate α; F_c is the affinity of cycle c and n_c its length. Equivalently, every eigenvalue λ should give ζ = 1 + Re λ/α + i Im λ/(αβ′) ∈ Ω_n.

The paper is `paper/affinity_karpelevich.pdf` (20 pages); its source is `paper/affinity_karpelevich.tex`.

## Main results (status in brackets)

- (S3) implies the containment ζ ∈ Ω_n under either reading of its quantifiers (Proposition 2.1) [proved].
- An integer four-state rate matrix Q_w violates it. Its eigenvalue −4745 + 450√3 i gives ζ ≈ −0.706221 + 0.316083 i, which lies 0.0087 above the left boundary arc of Ω_4. The strongest cycle carries about 8.4 k_BT (Theorem 3.1) [proved by one integer inequality; exact verifier].
- For networks of at most three states the containment holds, so four is the smallest failing size (Theorem 4.1) [proved, using the published sector bound of Ohga, Ito and Kolchinsky].
- Mechanism: weak resetting of size ε moves eigenvalues by O(ε) but relaxes the affinity factor by order ε^{2/3}. This gives counterexamples near every point of the open left arc of Ω_4 (Theorem 5.1), an explicit interval 0 < ε ≤ 1/100 (Theorem 6.1) and an open set of positive-rate counterexamples (Corollary 6.2) [proved].
- Every dimension n ≥ 4 fails: fix n, then a small t, then let ε → 0 (Theorem 7.4) [proved; thresholds not explicit].
- Explicit five- and six-state instances Q_{5,3/5,1/40000} and Q_{6,1/2,1/8000} (Theorem 7.6) [computer-assisted exact certificate; data printed in Appendix A and re-checked by a separate checker].

**Scope.** Every counterexample uses the complete graph, where every pair of states is linked. Whether (S3) holds for single-cycle networks, the setting in which it was tested, is **open** (Open problem 8.1); a small numerical search found no violation, and that is evidence, not proof. The violations are thin: radial margins are about 10⁻⁴ or smaller for n ≥ 5. The proved affinity ellipse and Farey-polygon bounds are unaffected.

## Reproduce

Python ≥ 3.11, standard library only (tested with 3.11.14). Run **without** `-O`: the verifiers use `assert`, and they refuse to run under `-O`.

```bash
shasum -a 256 -c SHA256SUMS                       # or sha256sum -c
python3 -B code/replay_all.py                     # every verifier into a temp dir; receipts must match (about 1 min)
python3 -B negative_controls.py                   # 11 corrupted inputs must be rejected (1-3 min)
python3 -B code/check_exterior_certificate.py receipts/exterior_certificates.json   # stand-alone checker, seconds
cd paper && pdflatex affinity_karpelevich.tex && pdflatex affinity_karpelevich.tex
```

The figures come from `python3 code/plot_geometry.py --out DIR`, which needs numpy and matplotlib; they are illustration only. Every script writes only into `--out` and refuses to overwrite existing files.

## Files

- `code/verify_affine_counterexample.py`: the four-state witness, exactly (Theorem 3.1).
- `code/audit_karpelevich.py`: independent exact audit of the four-state results.
- `code/audit_all_dimensions.py`: exact checks of the all-dimension construction (Section 7).
- `code/extension_fingerprint.py`: exact fingerprints of the n = 4, 5, 6 constructions. These identify the objects but do not test separation.
- `code/certify_higher_dimensions.py`: the n = 5, 6 certificates (Theorem 7.6), with a re-certification of Q_w. It writes `receipts/higher_dimension_certificates.json` and the terminal boxes `receipts/exterior_certificates.json`.
- `code/check_exterior_certificate.py`: a small checker that shares no code with the certifier and uses exact unrounded rational intervals.
- `code/replay_all.py`, `negative_controls.py`: the replay driver and semantic negative controls.
- `receipts/`: exact JSON receipts. Fields marked as decimals or timings are for orientation only.
- `notes/`: the dated bounded novelty reports for the four-state and all-dimension results.

## Release records

[STATUS.md](STATUS.md), [ASSURANCE.md](ASSURANCE.md), [CLAIMS.json](CLAIMS.json), [AI_INDEX.md](AI_INDEX.md), [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt), [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [PROVENANCE.md](PROVENANCE.md), [LICENSES.md](LICENSES.md), [PUBLIC_DOMAIN.md](PUBLIC_DOMAIN.md). `SHA256SUMS` lists every file.

## Citation

Anonymous (2026). *How fast can a driven Markov network oscillate? A four-state counterexample to the affine Karpelevich conjecture, and the exact dimension at which it fails* (Version 1.0.0-candidate) [Unrefereed research candidate]. Evidence Press. https://doi.org/10.5281/zenodo.23687327

Scholarly creator: Anonymous. Ian Pitchford maintains and publishes the repository; that role is not authorship.
