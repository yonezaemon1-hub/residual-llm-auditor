
from pathlib import Path
import json
from residual_auditor import audit_site

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/stretto_get_order_details_beta3.json").read_text())

counts=e["published_counts"]
labels=[
    ("GET_ORDER_DETAILS",counts["GET_ORDER_DETAILS"]),
    ("GET_PRODUCT_DETAILS",counts["GET_PRODUCT_DETAILS"]),
    ("HAND_BACK_RESPOND",counts["HAND_BACK_RESPOND"]),
]
assert sum(n for _,n in labels)==counts["total"]==9
assert all(n>0 for _,n in labels)

continuations=[x for x,_ in labels]
contexts=[]
matrix=[]
for label,n in labels:
    for k in range(n):
        contexts.append(f"{label}_{k+1}")
        matrix.append([1 if c==label else 0 for c in continuations])

a=audit_site(
    site="stretto:get_order_details",
    context_names=contexts,
    continuation_names=continuations,
    matrix=matrix,
)
assert a.beta==3
assert a.routing_bits_fixed_length==2

two=[
    x for x in a.lower_bound_certificate["exhaustive_failures"]
    if len(x["candidate_continuations"])==2
]
assert len(two)==3

out={
    "schema":"compiler-emitted-beta3-certificate-v0.7",
    "system":"Stretto",
    "site":"get_order_details",
    "specification":e["specification"],
    "published_counts":counts,
    "audit":a.__dict__,
    "interpretation":{
        "statement":"All three continuations occur in the published compiled-site decisions; under exact next-step reproduction, dropping any one continuation makes its labeled contexts impossible to reproduce.",
        "fixed_length_routing_bits":2,
        "scope":"trace-exact reproduction only; not benchmark-success necessity"
    }
}
(ROOT/"results/stretto_beta3_trace_exact_v07.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
