#!/usr/bin/env python3
"""Run the supplied Day 2 reference checks without claiming learner review.

Install semantic-lab/scripts/requirements.txt first. This orchestrates the
teaching checks; it is not another ontology validator or approval mechanism.
It makes no requests and leaves all lesson inputs unchanged. JSON goes to stdout.
"""
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "episodes/files/fraser-coho-workshop"
LAB = KIT / "semantic-lab"

# Use the vocabulary check's explicit reference-inspection function. The
# learner CLI independently requires the existing human-preparation checkpoint.
sys.path.insert(0, str(LAB / "vocabulary"))
from check_vocabulary import validate_vocabulary

vocabulary = validate_vocabulary(LAB / "vocabulary/estimate-methods.ttl",
                                 LAB / "vocabulary/concepts-working.csv", KIT)
model_bridge = subprocess.run(
    [sys.executable, "semantic-lab/scripts/check_reference.py"],
    cwd=KIT, capture_output=True, text=True,
)
if model_bridge.stderr:
    print(model_bridge.stderr, file=sys.stderr, end="")
model_bridge.check_returncode()
report = {
    "status": "pass",
    "observed_at": datetime.now(timezone.utc).isoformat(),
    "scope": "Maintainer inspection of distributed Day 2 drafts; not learner completion, scientific approval, a full OWL DL check, or a release authorization.",
    "vocabulary": vocabulary,
    "model_and_bridge": json.loads(model_bridge.stdout),
    "checked_files": [
        {"path": p.relative_to(KIT).as_posix(),
         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(LAB.rglob("*"))
        if p.is_file() and p.suffix in {".ttl", ".py", ".R", ".csv", ".json", ".txt"}
        and "output" not in p.relative_to(LAB).parts
    ],
}
print(json.dumps(report, indent=2))
