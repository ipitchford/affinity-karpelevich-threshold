# Review summary (internal, AI-assisted)

This file summarises the substantive objections raised in internal AI-assisted review and how each was resolved. It is not peer review. The original review records are kept privately.

Rounds:
1. A five-perspective review: editor, methodology, domain, perspective and devil's advocate.
2. An AI-assisted correctness audit of the draft by a different model, configured as OpenAI gpt-5.6-sol.
3. Revision.
4. A verification re-review of the revision.
5. A targeted proof audit of the new and changed proofs, with independent symbolic and ball-arithmetic scripts.
6. A second correctness audit by the same different model, of the revised text.
7. Final editor fixes.

## Objections and resolutions

| Objection | Resolution |
|---|---|
| Quote (S3) verbatim, with its quantifiers, and show that it implies the tested containment | Quoted from arXiv:2507.08938v2, Supplement I.2. Both readings (per matrix; union at fixed α, β′) are stated, with Proposition 2.1. The re-review checked the quotation against the source. The second audit noted that the implication is conditional on these two readings; the paper states both. |
| Exterior side of the general arc; explicit Ito/Johnson–Paparella substitution | Lemma 7.1 (which arc), Lemma 2.3 (star shape) and Lemma 7.2(ii), proved by a connected-component argument |
| Order of the small-t and small-ε limits | Stated at the start of Section 7 and in Theorem 7.4: fix n, then t, then ε. Nothing is uniform. |
| Explicit higher-dimensional instances | Theorem 7.6 certifies n = 5 and 6 exactly. The proof audit reproduced both independently. |
| Certificate not checkable from the paper (second audit, main point) | Appendix A prints the matrices, cycles and ratios, the root enclosures, W and S, and per-Farey-pair box counts and margins. The terminal boxes ship in `receipts/exterior_certificates.json`. A small stand-alone checker re-verifies them, and the interval extension and cover property are defined in the proof. |
| Lemma 2.6: endpoints were justified by closedness, which is invalid (second audit) | Replaced by unit-disc containment: g(−1) = 0 and g(−1/2) = 3/4. |
| Lemma 2.6: the slice relied on an unproved sector-confinement reading (second audit) | The reading is removed. The proof now checks directly that no root of any order-4 Ito equation lies in the region above the arc. |
| Lemma 2.3 is false for n = 1 (proof audit; second audit) | It is now stated for n ≥ 2, with an explicit matrix for the z = 1 case. All uses have n ≥ 4. |
| Lemma 7.1 claimed the matrix is the Johnson–Paparella realising matrix without giving the relabelling (attribution) | The claim is weakened to the characteristic polynomial, which is all the proofs use. |
| Remark 7.5: the onset of violation at n = 5, t = 1/20 was misstated as near e⁻²⁰ (proof audit) | Corrected. The triangle dominates near e⁻¹⁸ ≈ t⁶, the margin is positive from about e⁻¹⁶·³, and ε ≲ t⁶ is the proof's sufficient scale, not a violation threshold. The sharper ε ≲ t⁶/(1−t)³ is noted. |
| Scope; qualify "exact dimension" | Section 1.4 and the abstract state that every counterexample uses the complete graph and that the single-cycle case is open. |
| Single-cycle networks | Not resolved. Open problem 8.1, with the numerical evidence labelled as evidence. |
| Physical regime and size of the effect | Section 1.4 gives 8.4 k_BT, coherence ≈ 0.164 and the 0.0087 excess, and Table 1 lists the bounds that remain safe. |
| Missing citations; Kolchinsky et al. attribution | Six references were added. The polygon is attributed to Kolchinsky et al. Theorem 5, and the sector bound to Barato–Seifert (conjecture) and Ohga et al. (proof). |
| Narrow the novelty claim | Section 1.5 separates the known ingredients from the new ones. The literature search is bounded and makes no priority claim. |

## Not done

Explicit η_n and ε₀(n, t), the true region, β-dependence and a proof-assistant formalisation are listed as open problems or out of scope. Two optional citations were declined as not needed for any claim.
