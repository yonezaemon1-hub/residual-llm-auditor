
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

c=json.loads((ROOT/"results/stretto_5session_corrected_v08.json").read_text())
assert c["audit"]["beta_det_coverable"]==2
assert c["audit"]["fallback_required_count"]==1
assert c["audit"]["full_deterministic_cover_exists"] is False

b4=json.loads((ROOT/"results/stretto_reach_beta4_v08.json").read_text())
assert b4["audit"]["beta"]==4
assert b4["audit"]["routing_bits_fixed_length"]==2

t=json.loads((ROOT/"results/tau2_task_beta3_v08.json").read_text())
assert t["matrix"]["values"]==[[1,0,0],[0,1,0],[0,0,1]]
assert t["audit"]["beta"]==3
assert t["audit"]["routing_bits_fixed_length"]==2

print("PASS_HAND_BACK_SEPARATED")
print("PASS_REAL_COMPILER_DETERMINISTIC_BETA4")
print("PASS_TAU2_TASK_BETA3_STATIC")
