#!/usr/bin/env python3
"""Export readable reference pages, inventory bytes, and build the teaching ZIP.

Run from the repository root after building the reference checkpoints.
Only generated HTML, inventory and ZIP files are overwritten.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "episodes/files/fraser-coho-workshop"
ZIP = KIT.with_suffix(".zip")
generated = [KIT / "README.md", KIT / "raw_data/PROVENANCE.md"]
for folder in ("reference", "ai", "publication", "validation"):
    generated.extend(sorted((KIT / folder).glob("*.md")))
generated.extend(sorted((KIT / "semantic-lab").rglob("*.md")))
generated_sources = {path.resolve() for path in generated}
for source in generated:
    # These are generated reading views. Markdown/CSV remain the editable source.
    # Markdown authoring links need to reach the generated reading companions.
    # The downloadable originals remain unchanged; Pandoc transforms this view.
    markdown = source.read_text()
    def reading_link(match):
        original = match.group(0)
        url = urlsplit(original)
        if url.scheme or url.netloc:
            return original
        target = (source.parent / url.path).resolve()
        return original[:-3] + ".html" if target in generated_sources else original
    markdown = re.sub(r'(?<=\]\()[^\s)]+\.md(?=[#)])', reading_link, markdown)
    subprocess.run(["pandoc", "--standalone", "--from=gfm", "--to=html5",
                    "--metadata", "title=" + source.stem.replace("-", " "),
                    "--output", str(source.with_suffix(".html"))], input=markdown, text=True, check=True)


def included(path):
    parts = path.relative_to(KIT).parts
    return (path.is_file() and not any(p.startswith(".") or p == "__pycache__" for p in parts)
            and "output" not in parts and path.suffix != ".pyc")


inventory = KIT / "validation/kit-files.json"
inventory.parent.mkdir(exist_ok=True)
files = sorted(p for p in KIT.rglob("*") if included(p) and p != inventory)
inventory.write_text(json.dumps({
    "description": "SHA-256 inventory of included teaching files; this inventory excludes itself.",
    "files": [{"path": p.relative_to(KIT).as_posix(), "bytes": p.stat().st_size,
               "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
}, indent=2) + "\n")
files = sorted(files + [inventory])
with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in files:
        info = zipfile.ZipInfo("fraser-coho-workshop/" + path.relative_to(KIT).as_posix(),
                               date_time=(2026, 9, 8, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, path.read_bytes())
print(f"Built {ZIP.relative_to(ROOT)}: {len(files)} files, {ZIP.stat().st_size} bytes")
