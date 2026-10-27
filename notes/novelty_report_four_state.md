# Bounded novelty report: affinity-scaled Karpelevich counterexample

Search date: 20 October 2026. This report records the child agent's searches;
the parent agent may supplement them with independent checks.

## Frozen target and contribution units

The exact target is in `target.yaml`. Its principal contribution is the
refutation of the universal inclusion implied by Xu et al. (2025),
Supplement Eq. (S3): inverse affinity-scaled eigenvalues need not belong
to the classical Karpelevich region at the same matrix dimension.

The witness has four states and strictly positive bidirectional rates.
A two-parameter family explains the failure, and a one-parameter subfamily
has a rigorously certified interval 0<epsilon<=1/100. The construction uses
the known Karpelevich boundary and the known spectral effect of rank-one
resetting. Neither ingredient is claimed as new.

## Corpus and access boundary

Live web engines 1 and 2 were used. Primary source full text was inspected
on arXiv for the originating 2025 paper (v1 and v2), a closely related
2026 spectral localisation paper (v3, 8 October 2026), and a 2026 unicyclic
kinetic refinement (v2, 3 October 2026). The publisher abstract and an
institutional record were inspected for the 2018 resetting result.

The search does not include author correspondence, subscription citation
databases, or a systematic scan of unpublished manuscripts. Absence of a
matching result within this corpus does not establish historical priority.

## Queries actually issued

The following are the relevant query families, including their literal
queries. Initial unrelated scouting queries are omitted from the final
target-specific record.

1. Originating source, current status, direct challenge:
   - `"2507.08938" conjecture counterexample`
   - `"Karpelevich" "thermodynamic" "conjecture"`
   - `"Affinity-dependent bound" "counterexample"`
2. Formula/name translations and current cross-field sources:
   - `"Karpelevich" "affinity" counterexample`
   - `"Karpelevich" "thermodynamic" spectrum 2026`
   - `"Kinetic heterogeneity tightens thermodynamic bounds"`
3. Structural simplification / resetting alias rerun:
   - `"Karpelevich" "resetting"`
   - `"Karpelevich" "affinity" "counterexample"`
   - `"stochastic matrices" "lambda" "t^2" "Karpelevich"`
   - `"Spectral properties of simple classical and quantum reset processes"`

Source full-text searches additionally checked every occurrence of
`conjecture` and `Karpelevich` in the 2026 Kolchinsky–Ohga–Ito paper and
checked `Karpelevich` in the 2026 Xu–Meng paper. The literal integer matrix
is newly constructed evidence; the decisive collision risk is the
mathematical statement under alternate formulations, not whether those
particular entries occur in a search index.

## Inspected source comparisons

| Source | Material inspected | Load-bearing comparison |
|---|---|---|
| Xu et al. (2025), arXiv:2507.08938v2 | Full text and Supplement I.2 | Eq. (S3) proposes the exact affine image of Omega_n. Figure S1 samples single cycles. The counterexample has a multicyclic support. |
| Uhl & Seifert (2019), arXiv:1907.04260 | Abstract/source page | Proposes the affinity ellipse, a weaker statement. It is not the target of the present refutation. |
| Kolchinsky, Ohga & Ito (2026), arXiv:2605.15884v3 | Full text; Eq. (8), Theorems 4 and 5, all relevant term matches | Proves the ellipse and an affine-scaled convex polygon based on Farey roots. Does not identify that polygon with the curved Karpelevich region. Compatible with the new counterexample. No direct Eq. (S3) refutation found. |
| Xu & Meng (2026), arXiv:2608.22934v2 | Full text for scope and terminology | Restricts to unicyclic chains and refines bounds through geometric mean kinetics; not a general multicyclic Karpelevich theorem. |
| Rose et al. (2018), Phys. Rev. E 98, 022129 | Publisher abstract and institutional bibliographic record | Uniform spectral translation by reset rate is known. The construction's spectral simplification is an attributed ingredient, not an originality claim. |

## Formula fingerprints and verified translations

The canonical characteristic polynomial of the boundary family is

    (z^2-t)^2-(1-t)^2 z.

This is the n=4 Karpelevich/Ito arc joining the roots at angles pi and
2pi/3. Its use is a known-object collision, not a new spectral theorem.

The perturbation is state-independent resetting to the stationary
distribution, also equivalent to a continuous-time analogue of PageRank
teleportation. It translates the nonzero spectrum and preserves stationarity.

The new combination concerns a maximum cycle affinity: two missing reverse
edges of a three-cycle generate a normalising defect of order epsilon^(2/3),
while eigenvalues change at order epsilon. Thus the inverse-scaled point
crosses a curved classical spectral boundary.

Exact matrices for epsilon=1/10,1/100,1/1000, characteristic polynomials,
traces, row sums, ranks, sorted entries and hashes under transpose/state
relabelling are recorded in `affine_counterexample_verification.json`.

## Adjudication by contribution unit

| Unit | Outcome | Permitted wording |
|---|---|---|
| Classical n=4 Karpelevich boundary | COLLISION / known ingredient | Use and cite the established boundary. |
| Uniform reset-induced spectral translation | COLLISION / known ingredient | Attribute to existing resetting literature; include elementary derivation for transparency. |
| Refutation of Xu et al. Eq. (S3) | CLEAR TO PROVE within the recorded boundary; mathematical certificate now obtained | An exact counterexample to the stated conjectured inclusion. A prior refutation was not found in this bounded search. |
| Fractional-power obstruction family | BOUNDED UNCERTAINTY on priority; exact derivation available | An explicit mechanism and family demonstrating why the affine rule fails. |
| Exact standalone verifier | CLEAR within the created artefact boundary | A reproducible rational-arithmetic certificate; not a formal proof assistant verification. |

Forbidden wording includes 'first proof/refutation' without further priority
evidence, 'the Uhl–Seifert conjecture is false', or 'the exact thermodynamic
spectral region is now determined'. The strongest supported claim is the
specific four-state refutation, with the quantified family and its mechanism.

## Sources actually consulted

- Xu, G.-H., Kolchinsky, A., Delvenne, J.-C., & Ito, S. (2025).
  Thermodynamic geometric constraint on the spectrum of Markov rate matrices.
  Physical Review Letters, 135, 257102. https://arxiv.org/html/2507.08938v2
- Uhl, M., & Seifert, U. (2019). Affinity-dependent bound on the spectrum
  of stochastic matrices. Journal of Physics A: Mathematical and
  Theoretical, 52, 405002. https://doi.org/10.1088/1751-8121/ab3a7a
- Kolchinsky, A., Ohga, N., & Ito, S. (2026). Cycle affinity and winding
  localize eigenvalues of Markov generators (Version 3).
  https://arxiv.org/html/2605.15884v3
- Xu, R., & Meng, C. (2026). Kinetic heterogeneity tightens thermodynamic
  bounds on spectra of Markov cycles (Version 2).
  https://arxiv.org/html/2608.22934v2
- Rose, D. C., Touchette, H., Lesanovsky, I., & Garrahan, J. P. (2018).
  Spectral properties of simple classical and quantum reset processes.
  Physical Review E, 98, 022129. https://doi.org/10.1103/PhysRevE.98.022129
