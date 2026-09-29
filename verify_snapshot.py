#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS.json"

TESTS = [
    "test_public_core.py",
    "test_v07_public.py",
    "test_v08.py",
    "test_specification_beta.py",
    "test_candidate_relative_monotonicity.py",
]

REGENERATORS = {
    "audit_stretto_beta3.py": "results/stretto_beta3_trace_exact_v07.json",
    "audit_stretto_corrected.py": "results/stretto_5session_corrected_v08.json",
    "audit_stretto_beta4.py": "results/stretto_reach_beta4_v08.json",
    "audit_tau2_task_beta3.py": "results/tau2_task_beta3_v08.json",
    "audit_stretto_beta4_candidate_relative.py": "results/stretto_beta4_candidate_relative_v09.json",
    "audit_tau2_task_beta3_candidate_relative.py": "results/tau2_task_beta3_candidate_relative_v09.json",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_hashes() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    for rel, expected in sorted(manifest.items()):
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"MISSING {rel}")
            continue
        got = sha256(path)
        if got != expected:
            failures.append(f"HASH {rel} expected={expected} got={got}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS_SHA256 {len(manifest)} files")


def run_script(work: Path, script: str) -> None:
    cp = subprocess.run(
        [sys.executable, script],
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if cp.returncode:
        raise SystemExit(f"FAIL_SCRIPT {script}\n{cp.stdout}")
    lines = [line for line in cp.stdout.splitlines() if line.strip()]
    tail = lines[-1] if lines else "PASS"
    print(f"PASS_SCRIPT {script}: {tail[:160]}")


def compare_json(a: Path, b: Path, label: str) -> None:
    left = json.loads(a.read_text(encoding="utf-8"))
    right = json.loads(b.read_text(encoding="utf-8"))
    if left != right:
        raise SystemExit(f"FAIL_REGENERATED_JSON {label}")
    print(f"PASS_REGENERATED_JSON {label}")


def main() -> None:
    check_hashes()
    with tempfile.TemporaryDirectory(prefix="residual-llm-auditor-") as td:
        work = Path(td) / "repo"
        shutil.copytree(
            ROOT,
            work,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo"),
        )
        snapshots = {
            result: json.loads((ROOT / result).read_text(encoding="utf-8"))
            for result in REGENERATORS.values()
        }
        for script, result in REGENERATORS.items():
            run_script(work, script)
            regenerated = json.loads((work / result).read_text(encoding="utf-8"))
            if regenerated != snapshots[result]:
                raise SystemExit(f"FAIL_REGENERATED_JSON {result}")
            print(f"PASS_REGENERATED_JSON {result}")
        for script in TESTS:
            run_script(work, script)
    print("PASS_PUBLIC_SNAPSHOT")


if __name__ == "__main__":
    main()
