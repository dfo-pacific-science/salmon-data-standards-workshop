#!/usr/bin/env python3
"""Independently read a completed KNB TEST deposit, without any credential.

Usage: python3 scripts/verify-test-record.py PACKAGE NEW_RECEIPT.json
Never uploads. A dry-run manifest is rejected before any HTTP request.
Browser rendering still needs a separate signed-out visual inspection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("package", type=Path)
parser.add_argument("receipt", type=Path)
args = parser.parse_args()
if args.receipt.exists():
    parser.error("Receipt already exists; use a new filename.")
manifest = json.loads((args.package / "publication/test/knb-manifest.json").read_text())
if manifest.get("knb_environment") != "test" or manifest.get("node_id") != "urn:node:mnTestKNB":
    parser.error("Only the KNB test environment is permitted.")
if manifest.get("status") not in {"complete", "published_pending_catalog"}:
    parser.error("A completed upload manifest is required; a plan is not a public record.")
if manifest.get("public") is not True:
    parser.error("Expected the separately prepared public workshop record.")

BASE = "https://dev.nceas.ucsb.edu"
MN = BASE + "/knb/d1/mn/v2"
receipt = {"observed_utc": datetime.now(timezone.utc).isoformat(),
           "knb_environment": "test", "authenticated": False,
           "metadata_pid": manifest["metadata_pid"], "objects": [],
           "browser_rendering": "requires separate signed-out visual inspection"}


def read(url):
    # No Authorization header, environment token or stored cookie is consulted.
    with urllib.request.urlopen(urllib.request.Request(url, headers={
        "User-Agent": "SalmonWorkshopAnonymousVerification/1.0"}), timeout=25) as response:
        if response.status != 200:
            raise ValueError(f"Unexpected HTTP status {response.status}")
        return response.read()


try:
    resource_map = None
    for obj in manifest["objects"]:
        pid = urllib.parse.quote(obj["pid"], safe="")
        body = read(f"{MN}/object/{pid}")
        digest = hashlib.sha256(body).hexdigest()
        if digest != obj["sha256"] or len(body) != obj["size"]:
            raise ValueError(f"Object bytes do not match the plan: {obj['path']}")
        sysmeta = ET.fromstring(read(f"{MN}/meta/{pid}"))
        public = any(any(c.tag.rsplit("}", 1)[-1] == "subject" and c.text == "public" for c in allow)
                     and any(c.tag.rsplit("}", 1)[-1] == "permission" and c.text == "read" for c in allow)
                     for allow in sysmeta.iter() if allow.tag.rsplit("}", 1)[-1] == "allow")
        if not public:
            raise ValueError(f"Public-read policy not found: {obj['path']}")
        receipt["objects"].append({"pid": obj["pid"], "path": obj["path"],
                                   "bytes": len(body), "sha256": digest, "public_read": True})
        if obj["role"] == "resource_map":
            resource_map = ET.fromstring(body)
    if resource_map is None:
        raise ValueError("Resource map missing from manifest.")
    # DataONE serializes member identifiers inside resolver URLs; decode those
    # RDF object IRIs before matching each manifest identifier exactly.
    aggregated = {urllib.parse.unquote(e.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", ""))
                  for e in resource_map.iter() if e.tag == "{http://www.openarchives.org/ore/terms/}aggregates"}
    for obj in manifest["objects"]:
        if obj["role"] != "resource_map" and not any(u == obj["pid"] or u.endswith("/" + obj["pid"]) for u in aggregated):
            raise ValueError(f"Object missing from resource map: {obj['path']}")
    receipt["resource_membership"] = "pass"
    query = urllib.parse.urlencode({"q": 'id:"' + manifest["metadata_pid"] + '"', "wt": "json"})
    search = json.loads(read(MN + "/query/solr/?" + query))
    docs = search.get("response", {}).get("docs", [])
    if len(docs) != 1 or docs[0].get("id") != manifest["metadata_pid"]:
        raise ValueError("Exact metadata record is not yet anonymously indexed.")
    title = docs[0].get("title", "")
    if title != "Workshop demonstration: NuSEDS Fraser Coho — KNB Test Node":
        raise ValueError("Indexed title does not match the workshop record.")
    receipt["catalog_indexing"] = "pass"
    receipt["indexed_title"] = title
    receipt["catalog_url"] = BASE + "/view/" + urllib.parse.quote(manifest["metadata_pid"], safe="")
    read(receipt["catalog_url"])
    receipt["catalog_http"] = 200
    receipt["status"] = "anonymous-machine-checks-passed-browser-review-pending"
except Exception as error:
    receipt["status"] = "failed"
    receipt["error"] = str(error)
finally:
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
print(receipt["status"])
raise SystemExit(1 if receipt["status"] == "failed" else 0)
