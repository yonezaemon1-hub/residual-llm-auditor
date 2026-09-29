
from dataclasses import dataclass
from itertools import combinations
from math import ceil, log2
from typing import Sequence, Mapping, Optional, Dict, Any, List, Tuple

@dataclass(frozen=True)
class AuditResult:
    site: str
    n_contexts: int
    n_continuations: int
    beta: int
    routing_bits_fixed_length: int
    minimum_cover: List[str]
    lower_bound_certificate: Dict[str, Any]
    router_certificate: Optional[Dict[str, Any]]
    classification: str

def _covers_all(matrix, cols):
    return all(any(matrix[i][j] for j in cols) for i in range(len(matrix)))

def exact_min_cover(matrix):
    if not matrix:
        return 0, tuple()
    m=len(matrix[0])
    if any(len(r)!=m for r in matrix):
        raise ValueError("ragged matrix")
    if any(not any(r) for r in matrix):
        raise ValueError("context with no successful continuation")
    for k in range(1,m+1):
        for cols in combinations(range(m),k):
            if _covers_all(matrix,cols):
                return k,cols
    raise AssertionError

def lower_bound_certificate(matrix,beta,names):
    failures=[]
    for k in range(1,beta):
        for cols in combinations(range(len(names)),k):
            witness=next(i for i,row in enumerate(matrix) if not any(row[j] for j in cols))
            failures.append({
                "candidate_continuations":[names[j] for j in cols],
                "uncovered_context_index":witness,
            })
    return {"claim":f"no cover of size < {beta}","exhaustive_failures":failures}

def verify_router(matrix,feature_values,feature_to_continuation,continuation_names):
    if len(feature_values)!=len(matrix):
        raise ValueError("feature length mismatch")
    name_to_col={n:j for j,n in enumerate(continuation_names)}
    bad=[]
    for i,label in enumerate(feature_values):
        cont=feature_to_continuation.get(label)
        if cont not in name_to_col:
            bad.append({"context_index":i,"reason":"unmapped_label","label":label})
        elif not matrix[i][name_to_col[cont]]:
            bad.append({"context_index":i,"reason":"routed_to_failing_continuation","label":label,"continuation":cont})
    return {
        "valid":not bad,
        "labels_used":sorted(set(feature_values)),
        "label_count":len(set(feature_values)),
        "mapping":dict(feature_to_continuation),
        "failures":bad,
    }

def audit_site(site,context_names,continuation_names,matrix,*,observable_feature_values=None,feature_to_continuation=None):
    if len(matrix)!=len(context_names):
        raise ValueError("matrix/context mismatch")
    beta,cover=exact_min_cover(matrix)
    bits=0 if beta<=1 else ceil(log2(beta))
    lb=lower_bound_certificate(matrix,beta,continuation_names)
    router=None
    if observable_feature_values is not None and feature_to_continuation is not None:
        router=verify_router(matrix,observable_feature_values,feature_to_continuation,continuation_names)
    if beta==1:
        cls="COUNTERFACTUAL_REDUNDANT"
    elif router and router["valid"] and router["label_count"]==beta:
        cls="ABSTRACTION_INDUCED"
    elif router and router["valid"]:
        cls="ROUTABLE_WITH_OBSERVABLE_FEATURE"
    else:
        cls="IRREDUCIBLE_RELATIVE_TO_INTERFACE"
    return AuditResult(
        site=site,n_contexts=len(context_names),n_continuations=len(continuation_names),
        beta=beta,routing_bits_fixed_length=bits,
        minimum_cover=[continuation_names[j] for j in cover],
        lower_bound_certificate=lb,router_certificate=router,classification=cls
    )
