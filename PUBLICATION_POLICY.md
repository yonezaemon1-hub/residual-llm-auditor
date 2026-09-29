# Publication-safe repository policy

This public-safe bundle intentionally contains **no extracted AppWorld task contents,
private-data records, database rows, task comments, song IDs, task IDs, or case-packet slices**.

Keep benchmark-derived material local. Put it only under ignored paths such as:

- `private_evidence/`
- `local_matrices/`
- `results_private/`

The public artifact should contain only:

1. the generic finite counterfactual auditor;
2. the matrix/certificate schema;
3. synthetic regression tests;
4. aggregate research claims that do not redistribute benchmark task data.

To reproduce benchmark-backed claims, an authorized user should obtain AppWorld through
its official installation/download flow, construct the finite success matrix locally,
and run `certify_matrix.py` on that local matrix.

This separation is deliberate: the official AppWorld repository asks users not to post
code or data extracted or derived from its protected bundle files in plain text or images.
Review the current AppWorld release disclaimer before publishing.


## Public third-party evidence

v0.7 includes only aggregate facts already published in the public Stretto repository:
the compiled site name, the three next-step labels, their counts (6/2/1), and Git blob SHAs.
It does not redistribute benchmark task records or conversation contents.
