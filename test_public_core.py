
from residual_auditor import audit_site

cases=[
 ("b1",["x1","x2","x3"],["A","B"],[[1,1],[0,1],[1,1]],1,0),
 ("b2",["x","y"],["A","B"],[[1,0],[0,1]],2,1),
 ("b3",["x","y","z"],["A","B","C"],[[1,0,0],[0,1,0],[0,0,1]],3,2),
]
for site,ctx,cont,M,beta,bits in cases:
    a=audit_site(site,ctx,cont,M)
    assert a.beta==beta
    assert a.routing_bits_fixed_length==bits
print("PASS_PUBLIC_CORE_BETA_1_2_3")
