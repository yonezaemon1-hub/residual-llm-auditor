
from residual_auditor import audit_site
from candidate_relative_beta import candidate_extension_monotonicity, context_extension_monotonicity

# Candidate extension can only help (or leave beta unchanged).
old=[[1,0],[0,1]]
new=[[1,0,1],[0,1,1]]
assert candidate_extension_monotonicity(old,new)
b_old=audit_site("old",["x","y"],["A","B"],old).beta
b_new=audit_site("new",["x","y"],["A","B","UNIVERSAL"],new).beta
assert b_old==2 and b_new==1 and b_new<=b_old

# Context extension can only hurt (or leave beta unchanged).
small=[[1,0,0],[0,1,0]]
large=[[1,0,0],[0,1,0],[0,0,1]]
assert context_extension_monotonicity(small,large)
b_small=audit_site("small",["x","y"],["A","B","C"],small).beta
b_large=audit_site("large",["x","y","z"],["A","B","C"],large).beta
assert b_small==2 and b_large==3 and b_large>=b_small

print("PASS_CANDIDATE_EXTENSION_MONOTONICITY 2->1")
print("PASS_CONTEXT_EXTENSION_MONOTONICITY 2->3")
