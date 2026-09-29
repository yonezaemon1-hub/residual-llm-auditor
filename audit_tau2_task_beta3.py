
from pathlib import Path
import json
from residual_auditor import audit_site

ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/"evidence_public/tau2_telecom_task_beta3.json").read_text())

contexts=[x["id"] for x in e["contexts"]]
branches=[x["id"] for x in e["branch_programs"]]
assert contexts==["DATA_USAGE_EXCEEDED","SIM_UNSEATED","APN_BROKEN"]
assert branches==["REFUEL","RESEAT_SIM","RESET_APN_REBOOT"]

# Static source-level separation certificate:
# rows = task contexts, cols = full deterministic fix suffixes.
M=[
    [1,0,0], # exact +2 GB assertion makes REFUEL uniquely successful
    [0,1,0], # missing SIM remains missing under the other two programs
    [0,0,1], # BROKEN APN remains broken under REFUEL or RESEAT_SIM
]

a=audit_site(
    "stretto-telecom:check_apn_settings:task-success-three-faults",
    contexts,branches,M
)
assert a.beta==3
assert a.routing_bits_fixed_length==2
assert a.minimum_cover==branches
assert len([x for x in a.lower_bound_certificate["exhaustive_failures"]
            if len(x["candidate_continuations"])==2])==3

out={
  "schema":"task-success-beta3-static-certificate-v0.8",
  "specification":{
    "id":"TAU2_TASK_SUCCESS",
    "description":"The official task-family environment assertions / exact extra assertion are satisfied."
  },
  "matrix":{"rows":contexts,"columns":branches,"values":M},
  "audit":a.__dict__,
  "source_level_separation_facts":e["static_separation_facts"],
  "compiler_site_evidence":e["compiler_site"],
  "scope":e["scope"]
}
(ROOT/"results/tau2_task_beta3_v08.json").write_text(json.dumps(out,indent=2))
print(json.dumps({
  "site":a.site,"beta_task":a.beta,"routing_bits":a.routing_bits_fixed_length,
  "matrix":M,"minimum_cover":a.minimum_cover
},indent=2))
