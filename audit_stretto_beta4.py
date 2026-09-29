
from pathlib import Path
import json
from residual_auditor import audit_site

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/stretto_reach_retail_beta4.json").read_text())
counts=e["published_lookup_counts"]
cont=["GET_ORDER_DETAILS","GET_PRODUCT_DETAILS","GET_USER_DETAILS","LIST_ALL_PRODUCT_TYPES"]

ctx=[]; M=[]
for j,name in enumerate(cont):
    n=counts[name]
    assert n>0
    for i in range(n):
        ctx.append(f"{name}_{i+1}")
        row=[0]*len(cont); row[j]=1; M.append(row)

assert len(ctx)==counts["total"]==1565
a=audit_site(
    "stretto:reach-retail:get_order_details",
    ctx,cont,M
)
assert a.beta==4
assert a.routing_bits_fixed_length==2
assert len([x for x in a.lower_bound_certificate["exhaustive_failures"]
            if len(x["candidate_continuations"])==3])==4

out={
 "schema":"compiler-emitted-deterministic-beta4-v0.8",
 "specification":e["specification"],
 "published_lookup_counts":counts,
 "audit":a.__dict__,
 "claim_boundary":e["claim_boundary"]
}
(ROOT/"results/stretto_reach_beta4_v08.json").write_text(json.dumps(out,indent=2))
print(json.dumps({
 "site":a.site,"beta":a.beta,"routing_bits":a.routing_bits_fixed_length,
 "minimum_cover":a.minimum_cover,
 "n_contexts":a.n_contexts
},indent=2))
