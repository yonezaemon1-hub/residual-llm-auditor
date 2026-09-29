
from pathlib import Path
import json
from candidate_relative_beta import beta_psi_c

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/stretto_reach_retail_beta4.json").read_text())
counts=e["published_lookup_counts"]
C=["GET_ORDER_DETAILS","GET_PRODUCT_DETAILS","GET_USER_DETAILS","LIST_ALL_PRODUCT_TYPES"]
H=[]; M=[]
for j,c in enumerate(C):
    for i in range(counts[c]):
        H.append(f"{c}_{i+1}")
        row=[0]*4; row[j]=1; M.append(row)

r=beta_psi_c(
    "stretto:reach-retail:get_order_details",
    "TRACE_EXACT_LOOKUP_LABEL",
    H,C,M
)
assert r["audit"]["beta"]==4
out={
 "schema":"candidate-relative-real-compiler-beta4-v0.9",
 "notation":"beta_{Psi,C}(q;H)",
 "result":r,
 "claim_boundary":"Exact for the four published deterministic lookup arms and the 1,565 lookup-labeled transitions; excludes fallback and all unlisted continuations."
}
(ROOT/"results/stretto_beta4_candidate_relative_v09.json").write_text(json.dumps(out,indent=2))
print(json.dumps({"beta":4,"contexts":len(H),"candidates":C},indent=2))
