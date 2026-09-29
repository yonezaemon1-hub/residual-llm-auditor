# Residual LLM Necessity Auditor v0.6 — PUBLIC SAFE

Generic proof-carrying auditor for finite residual decision sites.

For contexts `H`, candidate deterministic continuations `C`, and a binary success matrix
`M[i,j]`, the auditor computes the exact minimum number of continuation columns needed
to cover every certified context:

    beta(q) = min |J|  such that every context is covered by some j in J.

It emits:

- an exact minimum cover;
- exhaustive lower-bound witnesses for every smaller candidate cover (small instances);
- fixed-length routing width `ceil(log2(beta))`;
- optional router validation when observable labels are supplied.

## Public/private split

This bundle contains only generic code and synthetic examples. Benchmark-derived AppWorld
evidence is intentionally excluded. Generate any benchmark matrix locally from an official
AppWorld installation and keep it out of the public repository.

## Quick test

    python test_public_core.py

## Certify a matrix

    python certify_matrix.py examples/synthetic_beta3.json

Expected:

- beta=3
- routing bits=2
- every one- or two-continuation candidate has an uncovered-context witness.

See `PUBLICATION_POLICY.md` before publishing benchmark-backed artifacts.


## v0.7: specification-indexed branch number and a real compiler-emitted beta=3 site

The branch number is now written `beta_Psi(q)` because "success" depends on an explicit
correctness specification `Psi`:

    M^Psi[i,j] = 1  iff continuation j satisfies Psi on context i.

This prevents three distinct questions from being conflated:

- exact trace reproduction;
- benchmark task success;
- safety-only admissibility.

### Specification monotonicity

If a stricter specification has a subset of the success entries of a weaker specification
(entrywise `M_strict <= M_weak`), then:

    beta_strict >= beta_weak.

Tightening correctness can never reduce the minimum continuation cover.

### Real compiler-emitted beta=3

Stretto's public `flow-show` review for its compiled retail flow reports that after the
`get_order_details` site the agent did next:

- `get_order_details`: 6 of 9 decisions;
- `get_product_details`: 2 of 9;
- `respond` / hand back: 1 of 9.

The standard Stretto program explicitly decides between hand-back and the lookups offered
at the site. Under `Psi = exact recorded next-step reproduction`, all three continuations
are therefore required:

    beta_TRACE_EXACT(get_order_details) = 3
    fixed-length routing width = 2 bits.

This is an actual compiler-emitted multiway decision site. The certificate is deliberately
narrow: it proves trace-exact branch necessity, not benchmark-success necessity.


## v0.8: deterministic branches, fallback, and task-success beta

v0.8 fixes a semantic mistake in v0.7: a hand-back to the agent/model is not a
deterministic continuation.

Three new results are included:

1. **Corrected Stretto 5-session site:** two deterministic lookup branches cover 8/9
   trace-exact contexts; one context requires model/agent fallback.
2. **Actual deterministic multiway compiler site:** Stretto's public reach retail flow has
   four distinct deterministic lookup transitions after `get_order_details`; on the
   lookup-labeled trace-exact certification set, `beta_TRACE = 4`.
3. **Task-success certificate:** three official τ² telecom fault contexts and three complete
   deterministic fix suffixes yield a source-level identity success matrix, hence
   `beta_TASK = 3` on that finite certification set.

See `CLAIM_BOUNDARIES_V08.md` for the exact scope.


## v0.9: candidate-relative beta

The formal quantity is now:

    beta_{Psi,C}(q;H)

where `Psi` is the correctness specification, `C` is the explicit candidate continuation
library, and `H` is the finite certification context set.

This fixes an important overclaim: adding a new continuation (for example a universal
multi-fault recovery program) may reduce the cover number. Therefore no certificate over
a finite library `C` is a lower bound over arbitrary programs unless closure/exhaustiveness
of `C` is proved separately.

The telecom three-fault result is now correctly stated as:

    beta_{TAU2_TASK_SUCCESS,C0}(q;H) = 3

for `C0 = {REFUEL, RESEAT_SIM, RESET_APN_REBOOT}` and the three explicit official fault
contexts. It is a strong separation witness, not a full-language minimum.

The Stretto reach-retail example remains exact on its published four deterministic lookup
arms and 1,565 lookup-labeled transitions:

    beta_{TRACE_EXACT_LOOKUP_LABEL,C}(q;H) = 4.
