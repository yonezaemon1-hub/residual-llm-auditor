
from __future__ import annotations
from residual_auditor import audit_site

def beta_psi_c(site, specification, contexts, candidates, matrix):
    """
    Exact finite continuation-cover number beta_{Psi,C}(q).

    Psi: correctness specification used to construct the binary success matrix.
    C: explicit candidate continuation library.
    H: explicit certification contexts.

    The result is NEVER a claim over continuations outside C or contexts outside H.
    """
    a=audit_site(site,contexts,candidates,matrix)
    return {
        "site":site,
        "specification":specification,
        "candidate_library":list(candidates),
        "certification_contexts":list(contexts),
        "audit":a.__dict__,
    }

def candidate_extension_monotonicity(old_matrix,new_matrix):
    """
    Premise checker for C subset C'. New matrix must contain the old columns
    unchanged as its prefix. If true, minimum cover under C' cannot exceed
    minimum cover under C.
    """
    if len(old_matrix)!=len(new_matrix):
        return False
    if not old_matrix:
        return True
    m=len(old_matrix[0])
    for ro,rn in zip(old_matrix,new_matrix):
        if len(ro)!=m or len(rn)<m or rn[:m]!=ro:
            return False
    return True

def context_extension_monotonicity(old_matrix,new_matrix):
    """
    Premise checker for H subset H'. Old rows must occur as the prefix and the
    candidate columns must be identical. If true, adding contexts cannot lower beta.
    """
    if len(new_matrix)<len(old_matrix):
        return False
    if not old_matrix:
        return True
    m=len(old_matrix[0])
    return all(len(r)==m for r in new_matrix) and new_matrix[:len(old_matrix)]==old_matrix
