
from pathlib import Path
import json
from candidate_relative_beta import beta_psi_c

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/tau2_telecom_task_beta3.json").read_text())

H=["DATA_USAGE_EXCEEDED","SIM_UNSEATED","APN_BROKEN"]
C0=["REFUEL","RESEAT_SIM","RESET_APN_REBOOT"]
M=[
 [1,0,0],
 [0,1,0],
 [0,0,1],
]
r=beta_psi_c(
    "stretto-telecom:check_apn_settings:three-fault-separation",
    "TAU2_TASK_SUCCESS",
    H,C0,M
)
assert r["audit"]["beta"]==3

out={
 "schema":"candidate-relative-task-success-certificate-v0.9",
 "notation":"beta_{Psi,C0}(q;H)",
 "specification":"TAU2_TASK_SUCCESS",
 "candidate_library_id":"C0_THREE_CANONICAL_FIX_SUFFIXES",
 "candidate_library":C0,
 "contexts":H,
 "matrix":M,
 "beta":3,
 "routing_bits_fixed_length":2,
 "source_level_separation_facts":e["static_separation_facts"],
 "claim_boundary":{
   "certifies":"beta=3 for exactly H and exactly C0 under the stated task-success tests",
   "does_not_certify":[
     "minimum over the full telecom action/program language",
     "minimum over every continuation emitted anywhere by the compiler",
     "that no additional continuation could solve two or three contexts"
   ]
 }
}
(ROOT/"results/tau2_task_beta3_candidate_relative_v09.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
