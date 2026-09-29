
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/"results/stretto_beta3_trace_exact_v07.json").read_text())
assert d["published_counts"]=={
 "GET_ORDER_DETAILS":6,
 "GET_PRODUCT_DETAILS":2,
 "HAND_BACK_RESPOND":1,
 "total":9
}
assert d["audit"]["beta"]==3
assert d["audit"]["routing_bits_fixed_length"]==2
two=[x for x in d["audit"]["lower_bound_certificate"]["exhaustive_failures"]
     if len(x["candidate_continuations"])==2]
assert len(two)==3
print("PASS_STRETTO_COMPILER_SITE_BETA3")
