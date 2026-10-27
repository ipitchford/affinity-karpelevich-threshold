# Status

Version 1.0.0-candidate (27 October 2026). DOI [10.5281/zenodo.23687327](https://doi.org/10.5281/zenodo.23687327) (concept DOI [10.5281/zenodo.23687326](https://doi.org/10.5281/zenodo.23687326)). Scholarly creator: Anonymous.

**Unrefereed research candidate.** No journal and no named human specialist has reviewed it. It was checked by internal AI-assisted review only (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)). That is not peer review, independent reproduction or formal verification.

Target: Supplement Eq. (S3) of Xu, Kolchinsky, Delvenne and Ito, Phys. Rev. Lett. 135, 257102 (2025), doi:10.1103/z4t2-18cx, quoted verbatim from arXiv:2507.08938v2. "Exact dimension" means universal containment over irreducible rate matrices with bidirectional edges: it fails for every n ≥ 4 and holds for n ≤ 3.

* **Proved in writing** (section numbers refer to `paper/affinity_karpelevich.pdf`)
  * Proposition 2.1: (S3) implies the containment (C) under both readings of its quantifiers.
  * Theorem 3.1: the integer matrix Q_w violates (C); one integer inequality decides it, and exact scripts check it.
  * Theorem 4.1: (C) holds for n ≤ 3. This depends on the sector bound as stated in Ohga, Ito and Kolchinsky, PRL 131, 077101 (2023), Eq. (10).
  * Theorems 5.1 and 6.1 and Corollary 6.2: counterexamples near every point of the open left arc of Ω_4; the explicit interval 0 < ε ≤ 1/100; an open set of positive-rate counterexamples.
  * Theorem 7.4: failure in every dimension n ≥ 4. The order is: fix n, then t ∈ (0, η_n), then ε below ε₀(n, t). Nothing is uniform, and η_n and ε₀ are not explicit.
* **Certified by exact computation**
  * Theorem 7.6: Q_{5,3/5,1/40000} and Q_{6,1/2,1/8000} violate (C). The method is exact rationals with outward-rounded rational intervals and a radial exterior test against every Ito boundary polynomial (Lemma 2.5). A separate checker re-verifies the data printed in Appendix A.
* **Numerical only**
  * Remark 7.5 (the ε-scale at t = 1/20) and the radial margins in Table 4 and Appendix A.
  * The single-cycle search in Open problem 8.1: 400 starts each for 4- and 5-state rings, no violation found. This is evidence, not proof, and no claim is made either way.
* **Open**: single-cycle networks (Problem 8.1); the true region for given n, α and β (Problem 8.2); explicit η_n, ε₀(n, t) and other arcs (Problem 8.3).

Not claimed: anything about sparse topologies, single cycles or the true region. Nothing here bears on the proved ellipse (Uhl–Seifert, proved by Kolchinsky, Ohga and Ito) or on the Farey-polygon bound, both of which remain valid. No historical priority is claimed; the literature search was bounded (see [RESEARCH_GATES.json](RESEARCH_GATES.json)).
