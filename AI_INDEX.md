# Agent navigation

## Identity

- Release slug `affinity-karpelevich-threshold`, version `1.0.0-candidate`, tag `v1.0.0-candidate`. DOI 10.5281/zenodo.23687327; concept DOI 10.5281/zenodo.23687326.
- Repository: https://github.com/ipitchford/affinity-karpelevich-threshold. Release page: https://evidencepress.org/releases/affinity-karpelevich-threshold/
- Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md)).
- Manuscript: [PDF](paper/affinity_karpelevich.pdf) (20 pages) and [LaTeX source](paper/affinity_karpelevich.tex). Figures: [paper/region_overview.pdf](paper/region_overview.pdf) and [paper/spectral_geometry.pdf](paper/spectral_geometry.pdf) (illustration only).
- Claims: [CLAIMS.json](CLAIMS.json). Overview: [README.md](README.md). Assurance limits: [ASSURANCE.md](ASSURANCE.md). Review summary: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).
- Provenance: [PROVENANCE.md](PROVENANCE.md). Sources: [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [notes/novelty_report_four_state.md](notes/novelty_report_four_state.md), [notes/novelty_report_all_dimensions.md](notes/novelty_report_all_dimensions.md).
- Citation: [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json). Licences: [LICENSES.md](LICENSES.md), [PUBLIC_DOMAIN.md](PUBLIC_DOMAIN.md).

## Scientific map

Object: an irreducible continuous-time Markov rate matrix Q on n states with bidirectional edges. α = max_i |Q_ii|, and β = tanh(max_c |F_c|/(2|c|)), where F_c is the log-ratio of forward to backward rates around simple cycle c. Ω_n is the Karpelevich region (all eigenvalues of n×n stochastic matrices). The rescaled eigenvalue is ζ = 1 + Re λ/α + i Im λ/(αβ). Target: Xu, Kolchinsky, Delvenne & Ito, PRL 135, 257102 (2025), Supplement Eq. (S3), which implies ζ ∈ Ω_n for every eigenvalue (containment (C), Proposition 2.1).

- (C) is **false** for n = 4. Q_w = [[-2768,2727,27,14],[1427,-2768,1327,14],[1327,27,-2768,1414],[27,27,2727,-2781]] has eigenvalue −4745 + 450√3 i, with α = 2781 and dominant triangle ratio 177853829/38529, giving ζ ≈ −0.706221 + 0.316083 i, outside Ω_4. Theorem 3.1, **proved**; [receipts/affine_counterexample_verification.json](receipts/affine_counterexample_verification.json).
- (C) **holds** for n ≤ 3. Theorem 4.1, **proved**, given the Ohga–Ito–Kolchinsky sector bound.
- Mechanism: resetting at rate ε shifts eigenvalues by O(ε), while β falls by order ε^{2/3}. Theorems 5.1 and 6.1 and Corollary 6.2, **proved** (four states; explicit interval 0 < ε ≤ 1/100).
- Every n ≥ 4 fails. Theorem 7.4, **proved**; the order is fix n, then t, then ε → 0, and the thresholds are not explicit.
- n = 5, 6 explicit instances. Theorem 7.6, **certified by exact computation**; data in Appendix A, [receipts/higher_dimension_certificates.json](receipts/higher_dimension_certificates.json) and [receipts/exterior_certificates.json](receipts/exterior_certificates.json).

Do not read:
- any result as covering single-cycle (ring) networks: that case is **open** (Problem 8.1);
- the ring search as proof of containment;
- the ε-scale numbers (Remark 7.5) or the radial margins as exact;
- anything here as refuting the affinity ellipse or the Farey-polygon bound, which remain proved;
- internal AI-assisted review as peer review.

## Code

- [code/verify_affine_counterexample.py](code/verify_affine_counterexample.py) and [code/audit_karpelevich.py](code/audit_karpelevich.py): the four-state results, exactly.
- [code/audit_all_dimensions.py](code/audit_all_dimensions.py): exact checks for Section 7. [code/extension_fingerprint.py](code/extension_fingerprint.py): object fingerprints.
- [code/certify_higher_dimensions.py](code/certify_higher_dimensions.py): the n = 5, 6 certificate. [code/check_exterior_certificate.py](code/check_exterior_certificate.py): the stand-alone checker.
- [code/replay_all.py](code/replay_all.py): full replay. [negative_controls.py](negative_controls.py): semantic negative controls. [code/plot_geometry.py](code/plot_geometry.py): figures only.

## Replay

Python ≥ 3.11, standard library, **without -O**:

```sh
python3 -B code/replay_all.py
python3 -B negative_controls.py
```

Results: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). Environment: [ENVIRONMENT.txt](ENVIRONMENT.txt). CI: [.github/workflows/replay.yml](.github/workflows/replay.yml).

## Useful next research question

Does (C) hold for every rate matrix supported on a single bidirectional cycle (Problem 8.1)? The resetting mechanism needs a separate, more strongly driven triangle, so it cannot apply there.
