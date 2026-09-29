
#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from residual_auditor import audit_site

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("matrix_json")
    ap.add_argument("--out", default=None)
    a=ap.parse_args()
    p=Path(a.matrix_json)
    d=json.loads(p.read_text(encoding="utf-8"))

    result=audit_site(
        site=d["site"],
        context_names=d["contexts"],
        continuation_names=d["continuations"],
        matrix=d["matrix"],
        observable_feature_values=d.get("feature_values"),
        feature_to_continuation=d.get("feature_to_continuation"),
    )
    out={
        "source_matrix":str(p),
        "audit":result.__dict__,
        "claim_boundary":d.get("claim_boundary","finite certification set only")
    }
    text=json.dumps(out,indent=2)
    if a.out:
        Path(a.out).write_text(text,encoding="utf-8")
    print(text)

if __name__=="__main__":
    main()
