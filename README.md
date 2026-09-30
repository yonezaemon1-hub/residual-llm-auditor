# Residual LLM Auditor

Author: Ryutaro Yonezu

**Research code snapshot based on v0.9.** This repository computes exact finite
continuation-cover certificates for a supplied binary success matrix. It does
not establish that an LLM is necessary. There is no paper PDF, Venmo case study,
or three-valued counterfactual replay implementation in this snapshot.

The `NO21` / `NO22` prefixes in earlier working archives are internal project
names, not publication sequence numbers.

## What is certified

For a finite context set H, an explicit candidate continuation library C, and an
explicit correctness specification Psi, define

```
beta_{Psi,C}(q;H) = min |J|, J subset C,
                  such that each h in H succeeds with some c in J.
```

This is the ordinary finite minimum set-cover problem applied to continuation
success sets. The implementation enumerates candidate covers, returns a minimum
cover, and gives uncovered-row witnesses for smaller nonempty covers. For a
nonempty context set the empty cover fails trivially. A zero-success row has no
full cover; the hybrid auditor reports such rows separately.

The result is conditional on the supplied matrix being correct and complete.
The auditor does not independently certify the matrix entries or execute the
candidate programs in an external environment. Candidate-library expansion can
reduce beta; context expansion or a stricter specification can increase it.

`ceil(log2(beta))` is a fixed-length candidate-index encoding width, not the
memory, compute cost, or existence of an implementable observation-based router.

## Reproduce locally

Python 3.10 or later; standard library only. No API, network, LLM, or paid service
is required to run the included checks.

```
python verify_snapshot.py
python certify_matrix.py examples/synthetic_beta3.json
```

The verifier checks SHA-256 hashes, runs the five assertion-based regression
scripts as scripts, regenerates six result files in a temporary directory, and
compares their JSON contents with the stored results. It does not download or
validate the upstream evidence sources and does not run an external benchmark.

## Included examples and their limits

| Example | Result | Evidence boundary |
|---|---|---|
| Synthetic matrices | beta = 1, 2, 3 | Explicit finite matrix arithmetic |
| Stretto five-session summary | 8/9 labels covered by two deterministic lookup arms; one fallback label | Constructed from stored aggregate next-step counts; fallback is relative to those arms |
| Stretto reach-retail summary | beta = 4 for four lookup labels and 1,565 expanded count rows | Trace-label reproduction; count-expanded rows are not replayed environment states |
| tau2 telecom | beta = 3 for a supplied 3-by-3 identity matrix | Static source-level separation claim in the input bundle; no fresh task replay |

Source repository paths and Git blob identifiers are recorded under
`evidence_public/`. These aggregate annotations came from the supplied v0.9
archive; the present verification certifies reproducibility of the calculations,
not an independent re-audit of those upstream source claims.

## Important historical limitations

- v0.7 counted hand-back/respond as a deterministic continuation. That
  interpretation is withdrawn. `test_v07_public.py` checks only historical
  three-label arithmetic; a PASS does not restore the withdrawn interpretation.
- Use the v0.9 candidate-relative results for current descriptions. Older JSON
  files and scripts are retained for provenance and regression history.
- Legacy output labels such as `IRREDUCIBLE_RELATIVE_TO_INTERFACE` are not proof
  that an observation-based router or a different deterministic program cannot
  exist. With no validated router supplied, routing remains unassessed.
- Inputs must be well-formed, complete binary matrices with correctly aligned,
  unique context and continuation identifiers. The inherited API is not a
  hardened input validator. Unknown outcomes must not be encoded as failures.
- No general-language lower bound, unseen-context guarantee, or novelty of set
  cover itself is claimed.

See `FORMAL_DEFINITION_V09.md`, `DEPRECATIONS_V09.md`, and
`PUBLICATION_POLICY.md`. `HISTORY_V09.md` preserves the earlier README, including
superseded interpretations.

## Archival record

- GitHub release: `v0.9.0`
- Frozen release commit: `1bd60c86895267a8572d61322bea5ab4ced74956`
- Zenodo Software DOI: `10.5281/zenodo.23043042`
- Zenodo record: `https://zenodo.org/records/23043042`
- Archived file SHA-256: `7360309bed0becd252ea7259f5f72bd227707dc54146e361834b468709e5c05e`

## License

Original code and repository documentation are provided under the MIT License.
Upstream projects and benchmark materials retain their own licenses. No private
AppWorld tasks or raw conversation transcripts are included.
