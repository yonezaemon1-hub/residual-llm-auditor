# Formal object in v0.9

The quantity is explicitly relative to three objects:

\[
\beta_{\Psi,C}(q;H)
=
\min\{|J|:J\subseteq C,\ \forall h\in H,\ \exists c\in J:\Psi(h,c)=1\}.
\]

- `q`: residual/decision site.
- `H`: finite certification contexts.
- `C`: explicit candidate continuation library.
- `Psi`: explicit correctness specification.

The binary matrix is `M[i,j] = Psi(h_i,c_j)`.

This notation prevents two overclaims:

1. a certificate over one candidate library does not quantify over arbitrary programs;
2. a certificate over one finite context set does not quantify over unseen contexts.

## Monotonicities

For fixed `H` and `Psi`, if `C subseteq C'`, then

\[
\beta_{\Psi,C'}(q;H)\le \beta_{\Psi,C}(q;H).
\]

More candidate continuations can only make covering easier.

For fixed `C` and `Psi`, if `H subseteq H'`, then

\[
\beta_{\Psi,C}(q;H')\ge \beta_{\Psi,C}(q;H).
\]

More certification contexts can only make covering harder.

For fixed `H` and `C`, if `Psi_strict` accepts a subset of every continuation's
`Psi_weak` successes, then

\[
\beta_{\Psi_{\rm strict},C}(q;H)\ge
\beta_{\Psi_{\rm weak},C}(q;H).
\]

A stricter correctness specification can only make covering harder.

## Fallback

Model/oracle hand-back is not a member of `C` unless the study explicitly treats a model
call as a candidate continuation. v0.9 defaults to separating deterministic `C` from
fallback-required contexts.
