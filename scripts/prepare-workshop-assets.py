#!/usr/bin/env python3
"""Refresh pinned teaching sources and render the shared workflow figures.

Run from the lesson repository. Source data is copied from the released R
package, never from mutable generated checkpoints. No inference or deposit.
"""
from pathlib import Path
import hashlib
import html
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "episodes/files/fraser-coho-workshop"
UPSTREAM = ROOT.parent / "metasalmon"
TAG = "v0.5.0"


def released(path):
    return subprocess.check_output(["git", "show", f"{TAG}:{path}"], cwd=UPSTREAM)


def main():
    destinations = {
        "inst/extdata/nuseds-fraser-coho-2023-2024.csv": "raw_data/nuseds-fraser-coho-2023-2024.csv",
        "inst/extdata/nuseds-fraser-coho-2023-2024-column_dictionary.csv": "raw_data/source-column-dictionary.csv",
        "inst/extdata/example-data-README.md": "raw_data/upstream-example-data-README.md",
        "data-raw/nuseds_fraser_coho_examples.R": "raw_data/upstream-derivation.R",
    }
    records = []
    commit = subprocess.check_output(["git", "rev-parse", f"{TAG}^{{commit}}"], cwd=UPSTREAM, text=True).strip()
    for source, target in destinations.items():
        content = released(source)
        path = KIT / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        records.append({"path": target, "sha256": hashlib.sha256(content).hexdigest(),
                        "source_url": f"https://raw.githubusercontent.com/salmon-data-mobilization/metasalmon/{commit}/{source}"})
    (KIT / "raw_data/source-manifest.json").write_text(json.dumps({
        "package": "metasalmon", "version": TAG, "commit": commit,
        "original_catalog": "https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6",
        "files": records,
    }, indent=2) + "\n")

    steps = [("See the journey", "Raw data to test catalog"),
             ("Draw relationships", "Nodes, edges, row meaning"),
             ("Describe and review", "Dictionary and decomposition"),
             ("Build the package", "Human work into SDP files"),
             ("Map and evaluate AI", "Evidence and recorded decisions"),
             ("Document codes", "Methods and local/shared gaps"),
             ("Validate and rehearse", "EML and KNB test only")]
    figures = ROOT / "episodes/fig"
    figures.mkdir(exist_ok=True)
    mermaid = ["flowchart LR"]
    for i, (name, _) in enumerate(steps, 1):
        mermaid.append(f'  s{i}["{i}. {name}"]')
        if i > 1:
            mermaid.append(f"  s{i-1} --> s{i}")
    (figures / "workflow.mmd").write_text("\n".join(mermaid) + "\n")
    for active in range(1, 8):
        # A vertical figure remains legible in the mobile lesson layout.
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="590" viewBox="0 0 760 590" role="img" aria-labelledby="title desc">',
                 f'<title id="title">Workshop workflow: chapter {active}</title>',
                 '<desc id="desc">Seven stages. Human diagram, dictionary and peer review precede package creation and AI. Publication uses KNB test only.</desc>',
                 '<rect width="760" height="590" fill="#ffffff"/>']
        for i, (name, detail) in enumerate(steps, 1):
            y = 12 + (i-1)*80
            fill, stroke, label = ("#e2f0eb", "#17624d", "Current chapter") if i == active else ("#f4f5f6", "#687582", "")
            parts += [f'<rect x="20" y="{y}" width="720" height="65" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{3 if i == active else 1}"/>',
                      f'<text x="40" y="{y+27}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#172b3a">{i}. {html.escape(name)}</text>',
                      f'<text x="40" y="{y+49}" font-family="sans-serif" font-size="16" fill="#334755">{html.escape(detail)}</text>',
                      f'<text x="715" y="{y+28}" text-anchor="end" font-family="sans-serif" font-size="15" fill="#17624d">{label}</text>']
            if i < 7:
                parts.append(f'<path d="M 380 {y+66} v 12 m -4 -4 l 4 4 l 4 -4" fill="none" stroke="#334755" stroke-width="2"/>')
        parts.append('</svg>')
        (figures / f"workflow-{active}.svg").write_text("\n".join(parts) + "\n")
    print("Pinned source files and seven workflow figures prepared.")


if __name__ == "__main__":
    main()
