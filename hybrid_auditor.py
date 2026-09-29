
from __future__ import annotations
from itertools import combinations
from math import ceil, log2

def _covers_rows(matrix, cols, rows):
    return all(any(matrix[i][j] for j in cols) for i in rows)

def audit_deterministic_with_fallback(
    site,
    context_names,
    deterministic_continuations,
    deterministic_matrix,
    *,
    fallback_label="MODEL_OR_ORACLE_FALLBACK",
):
    """
    Audit deterministic continuations separately from model/oracle fallback.

    Rows with at least one deterministic success are "deterministically coverable".
    Rows with all zeros require fallback relative to the supplied deterministic interface.

    beta_det_coverable is the exact minimum deterministic cover on the coverable rows.
    If fallback_required_contexts is nonempty, there is NO full deterministic cover.
    """
    n=len(context_names)
    if len(deterministic_matrix)!=n:
        raise ValueError("matrix/context mismatch")
    m=len(deterministic_continuations)
    if any(len(row)!=m for row in deterministic_matrix):
        raise ValueError("ragged matrix")

    coverable=[i for i,row in enumerate(deterministic_matrix) if any(row)]
    fallback=[i for i,row in enumerate(deterministic_matrix) if not any(row)]

    if not coverable:
        beta=0
        cover=()
    else:
        cover=None
        beta=None
        for k in range(1,m+1):
            for cols in combinations(range(m),k):
                if _covers_rows(deterministic_matrix,cols,coverable):
                    beta=k; cover=cols; break
            if cover is not None:
                break
        if cover is None:
            raise AssertionError("coverable rows were not coverable")

    lower=[]
    for k in range(1,beta or 0):
        for cols in combinations(range(m),k):
            witness=next(i for i in coverable if not any(deterministic_matrix[i][j] for j in cols))
            lower.append({
                "candidate_continuations":[deterministic_continuations[j] for j in cols],
                "uncovered_context_index":witness,
                "uncovered_context":context_names[witness],
            })

    return {
        "site":site,
        "n_contexts":n,
        "n_deterministic_continuations":m,
        "deterministically_coverable_contexts":[context_names[i] for i in coverable],
        "fallback_required_contexts":[context_names[i] for i in fallback],
        "fallback_required_count":len(fallback),
        "full_deterministic_cover_exists":len(fallback)==0,
        "beta_det_coverable":beta,
        "routing_bits_det_coverable":0 if beta<=1 else ceil(log2(beta)),
        "minimum_deterministic_cover":[deterministic_continuations[j] for j in (cover or ())],
        "lower_bound_certificate":lower,
        "fallback_label":fallback_label,
    }
