
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from residual_auditor import audit_site

def beta_for_spec(site, specification, context_names, continuation_names, matrix):
    """
    Compute beta_Psi(q) for an explicit finite correctness specification Psi.
    The caller constructs matrix[i][j]=1 iff continuation j satisfies Psi on context i.
    """
    result = audit_site(site, context_names, continuation_names, matrix)
    return {
        "site":site,
        "specification":specification,
        "audit":result.__dict__,
    }

def verify_specification_monotonicity(strict_matrix, weak_matrix):
    """
    If every strict success is also a weak success (entrywise strict <= weak),
    return True. Under this premise beta_strict >= beta_weak.
    """
    if len(strict_matrix)!=len(weak_matrix):
        return False
    for rs,rw in zip(strict_matrix,weak_matrix):
        if len(rs)!=len(rw):
            return False
        for a,b in zip(rs,rw):
            if a and not b:
                return False
    return True
