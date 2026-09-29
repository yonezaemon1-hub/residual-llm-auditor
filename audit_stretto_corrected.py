
from pathlib import Path
import json
from hybrid_auditor import audit_deterministic_with_fallback

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/stretto_5session_corrected.json").read_text())

ctx=[]
M=[]
for i in range(e["published_counts"]["GET_ORDER_DETAILS"]):
    ctx.append(f"GET_ORDER_DETAILS_{i+1}"); M.append([1,0])
for i in range(e["published_counts"]["GET_PRODUCT_DETAILS"]):
    ctx.append(f"GET_PRODUCT_DETAILS_{i+1}"); M.append([0,1])
for i in range(e["published_counts"]["HAND_BACK_RESPOND"]):
    ctx.append(f"HAND_BACK_RESPOND_{i+1}"); M.append([0,0])

a=audit_deterministic_with_fallback(
    "stretto:get_order_details:5session",
    ctx,
    e["deterministic_continuations"],
    M,
)
assert a["beta_det_coverable"]==2
assert a["fallback_required_count"]==1
assert a["full_deterministic_cover_exists"] is False
assert len(a["deterministically_coverable_contexts"])==8

out={
  "schema":"corrected-stretto-hybrid-certificate-v0.8",
  "specification":e["specification"],
  "audit":a,
  "interpretation":{
    "statement":"Two deterministic lookup branches exactly cover 8/9 published next-step labels; the remaining 1/9 is a hand-back/model-fallback context under trace-exact reproduction.",
    "correction":"v0.7's HAND_BACK-as-deterministic interpretation is superseded."
  }
}
(ROOT/"results/stretto_5session_corrected_v08.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
