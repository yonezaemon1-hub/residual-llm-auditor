
from residual_auditor import audit_site
from specification_beta import verify_specification_monotonicity

# Strict: identity matrix -> beta=3.
strict=[[1,0,0],[0,1,0],[0,0,1]]
# Weak: continuation A also succeeds on second and third contexts -> beta=1.
weak=[[1,0,0],[1,1,0],[1,0,1]]

assert verify_specification_monotonicity(strict,weak)
bs=audit_site("strict",["x","y","z"],["A","B","C"],strict).beta
bw=audit_site("weak",["x","y","z"],["A","B","C"],weak).beta
assert bs==3 and bw==1 and bs>=bw
print("PASS_SPEC_MONOTONICITY beta_strict=3 beta_weak=1")
