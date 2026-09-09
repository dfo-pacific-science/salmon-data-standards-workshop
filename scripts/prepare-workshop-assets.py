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

    steps = [("See the journey", "Publication, contribution and local stewardship"),
             ("Draw relationships", "Nodes, edges, row meaning"),
             ("Describe and review", "Dictionary and decomposition"),
             ("Build the package", "Human work into SDP files"),
             ("Map and evaluate AI", "Evidence and recorded decisions"),
             ("Document codes", "Methods and local/shared gaps"),
             ("Validate and rehearse", "EML and KNB test only"),
             ("Choose the semantic route", "Reuse, local meaning or shared contribution"),
             ("Build a controlled vocabulary", "SKOS concepts, sources and stewardship"),
             ("Formalize the human graph", "RDF, OWL and limited reasoning checks"),
             ("Build and assess bridges", "Typed mappings, evidence and consequences"),
             ("Prepare a contribution", "Term request, clarification and review plan")]
    figures = ROOT / "episodes/fig"
    figures.mkdir(exist_ok=True)
    mermaid = ["flowchart TB", '  subgraph day1["Day 1: beginner route to publication - 6 hours"]']
    for i, (name, _) in enumerate(steps, 1):
        if i == 8:
            mermaid.extend(["  end", '  subgraph day2["Day 2: build and connect meanings - 6 hours"]'])
        mermaid.append(f'  s{i}["{i}. {name}"]')
        if i > 1 and i != 8:
            mermaid.append(f"  s{i-1} --> s{i}")
    mermaid.extend(["  end", "  s7 --> s8"])
    (figures / "workflow.mmd").write_text("\n".join(mermaid) + "\n")
    for active in range(1, len(steps) + 1):
        # Use full-width stacked rows so the two-day map remains readable.
        # The editable Mermaid source and chapter tables provide text equivalents.
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="840" viewBox="0 0 760 840" role="img" aria-labelledby="title desc">',
                 f'<title id="title">Workshop workflow: chapter {active}</title>',
                 '<desc id="desc">Twelve chapters over two six-hour days. Day 1: human diagram, dictionary and peer review before package creation, AI review and KNB test publication. Day 2: routing, SKOS vocabulary, OWL model, bridges and contribution drafts. No production publication or official term creation.</desc>',
                 '<rect width="760" height="840" fill="#ffffff"/>',
                 '<text x="20" y="25" font-family="sans-serif" font-size="20" font-weight="bold" fill="#172b3a">Day 1 · Beginner route to publication · 6 hours</text>',
                 '<text x="20" y="494" font-family="sans-serif" font-size="20" font-weight="bold" fill="#172b3a">Day 2 · Build and connect meanings · 6 hours</text>']
        for i, (name, detail) in enumerate(steps, 1):
            y = 38 + (i-1)*62 + (36 if i >= 8 else 0)
            fill, stroke, label = ("#e2f0eb", "#17624d", "Current chapter") if i == active else ("#f4f5f6", "#687582", "")
            parts += [f'<rect x="20" y="{y}" width="720" height="54" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{3 if i == active else 1}"/>',
                      f'<text x="40" y="{y+23}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#172b3a">{i}. {html.escape(name)}</text>',
                      f'<text x="40" y="{y+43}" font-family="sans-serif" font-size="16" fill="#334755">{html.escape(detail)}</text>',
                      f'<text x="715" y="{y+23}" text-anchor="end" font-family="sans-serif" font-size="15" fill="#17624d">{label}</text>']
            if i < len(steps) and i != 7:
                parts.append(f'<path d="M 380 {y+55} v 6 m -3 -3 l 3 3 l 3 -3" fill="none" stroke="#334755" stroke-width="2"/>')
        parts.append('</svg>')
        (figures / f"workflow-{active}.svg").write_text("\n".join(parts) + "\n")
    print("Pinned source files and twelve two-day workflow figures prepared.")


if __name__ == "__main__":
    main()
