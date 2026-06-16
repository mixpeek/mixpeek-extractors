#!/usr/bin/env python3
"""Run any Mixpeek extractor end-to-end against the API.

Extractors run on Mixpeek's hosted infrastructure (Ray / GPU / Vertex), so
"running locally" means driving the hosted extractor from your machine: this
script creates a throwaway namespace, bucket, object, and collection, processes
one object through the extractor you pick, then builds a retriever and runs a
search — printing the result. The namespace is created with a short TTL so it
cleans itself up.

The API flow mirrors Mixpeek's own staging E2E test (the tested source of truth),
and the search feature URI is auto-detected from the collection metadata, so this
stays correct as models change.

Usage:
    export MIXPEEK_API_KEY=sk_...
    # text-based extractors run with a built-in sample:
    python run_extractor.py --extractor text_extractor
    # media extractors need a public URL (or s3:// / gs://) to your asset:
    python run_extractor.py --extractor image_extractor --input https://example.com/cat.jpg
    python run_extractor.py --extractor multimodal_extractor --input https://example.com/clip.mp4 --query "a person speaking"

Env:
    MIXPEEK_API_KEY   required
    MIXPEEK_BASE_URL  optional (default https://api.mixpeek.com)
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import requests  # pip install requests

# Per-extractor wiring: the input key the extractor declares, and the modality
# that drives the bucket field type / blob type. `sample` is a built-in default
# for the text-shaped extractors; media extractors require --input <url>.
EXTRACTORS = {
    "text_extractor": {"input_key": "text", "modality": "text",
                       "sample": "Wireless noise-cancelling headphones with 30-hour battery life."},
    "web_scraper": {"input_key": "url", "modality": "text", "sample": "https://docs.mixpeek.com"},
    "passthrough_extractor": {"input_key": "content", "modality": "text", "sample": "an example object to store"},
    "image_extractor": {"input_key": "image", "modality": "image", "sample": None},
    "face_identity_extractor": {"input_key": "image", "modality": "image", "sample": None},
    "document_graph_extractor": {"input_key": "pdf", "modality": "pdf", "sample": None},
    "multimodal_extractor": {"input_key": "video", "modality": "video", "sample": None},
    "scrolling_text_extractor": {"input_key": "video", "modality": "video", "sample": None},
    "audio_fingerprint_extractor": {"input_key": "audio", "modality": "audio", "sample": None},
    "gemini_multifile_extractor": {"input_key": "files", "modality": "image", "sample": None},
    "universal_extractor": {"input_key": "content", "modality": "image", "sample": None},
}

# modality -> (bucket field type, blob type). The retriever always queries with
# TEXT (the universal, simplest query for the contrastive text↔media models).
MODALITY = {
    "text": ("text", "text"),
    "image": ("image", "image"),
    "video": ("video", "video"),
    "audio": ("audio", "audio"),
    "pdf": ("pdf", "pdf"),
}

FIELD = "content"  # the single bucket field this quickstart uses


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--extractor", required=True, choices=sorted(EXTRACTORS), help="extractor to run")
    ap.add_argument("--version", default="v1")
    ap.add_argument("--input", help="text, or a public/s3/gs URL for media extractors")
    ap.add_argument("--query", default="example", help="search query to run after processing")
    ap.add_argument("--timeout", type=int, default=600, help="seconds to wait for processing")
    args = ap.parse_args()

    api_key = os.environ.get("MIXPEEK_API_KEY")
    if not api_key:
        sys.exit("ERROR: set MIXPEEK_API_KEY (get one at https://studio.mixpeek.com)")
    base = os.environ.get("MIXPEEK_BASE_URL", "https://api.mixpeek.com").rstrip("/")

    spec = EXTRACTORS[args.extractor]
    data = args.input or spec["sample"]
    if not data:
        sys.exit(f"ERROR: {args.extractor} needs a {spec['modality']} input — pass --input <url>")
    field_type, blob_type = MODALITY[spec["modality"]]
    name = args.extractor

    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {api_key}"

    def post(path, json, **kw):
        r = s.post(f"{base}{path}", json=json, timeout=60, **kw)
        r.raise_for_status()
        return r.json()

    def get(path):
        r = s.get(f"{base}{path}", timeout=60)
        r.raise_for_status()
        return r.json()

    print(f"→ creating namespace, bucket, object, and a {name} collection …")
    ns = post("/v1/namespaces", {
        "namespace_name": f"cookbook-{name}-{int(time.time())}",
        "feature_extractors": [{"feature_extractor_name": name, "version": args.version}],
        "ttl_seconds": 21600,  # auto-clean after 6h
    })
    s.headers["X-Namespace"] = ns["namespace_id"]

    bucket = post("/v1/buckets", {
        "bucket_name": "cookbook",
        "bucket_schema": {"properties": {FIELD: {"type": field_type}}},
    })
    bucket_id = bucket["bucket_id"]

    obj = post(f"/v1/buckets/{bucket_id}/objects", {
        FIELD: data,
        "blobs": [{"property": FIELD, "type": blob_type, "data": data}],
    })
    object_id = obj["object_id"]

    col = post("/v1/collections", {
        "collection_name": "cookbook",
        "source": {"type": "bucket", "bucket_ids": [bucket_id]},
        "feature_extractor": {
            "feature_extractor_name": name,
            "version": args.version,
            "input_mappings": {spec["input_key"]: FIELD},
            "parameters": {},
            "field_passthrough": [FIELD],
        },
    })
    col_id = col["collection_id"]

    print("→ submitting a batch …")
    batch = post(f"/v1/buckets/{bucket_id}/batches", {
        "batch_name": "cookbook", "object_ids": [object_id], "collection_ids": [col_id],
    })
    submit = post(f"/v1/buckets/{bucket_id}/batches/{batch['batch_id']}/submit",
                  {"collection_ids": [col_id]})
    task_id = submit["task_id"]

    print(f"→ processing (task {task_id}) …", end="", flush=True)
    deadline = time.time() + args.timeout
    while True:
        status = (get(f"/v1/tasks/{task_id}").get("status") or "").lower()
        if status in ("completed", "completed_with_errors"):
            print(f" {status}")
            break
        if status in ("failed", "canceled"):
            sys.exit(f"\nERROR: task {status}")
        if time.time() > deadline:
            sys.exit("\nERROR: timed out waiting for processing")
        print(".", end="", flush=True)
        time.sleep(10)

    # Auto-detect the feature URI from the collection (don't hardcode the model).
    meta = get(f"/v1/collections/{col_id}")
    indexes = meta.get("vector_indexes") or meta.get("required_vector_indexes") or []
    if not indexes:
        sys.exit("ERROR: collection has no vector index to search")
    feature_uri = indexes[0].get("feature_uri") or indexes[0].get("name")

    print("→ building a retriever and searching …")
    ret = post("/v1/retrievers", {
        "retriever_name": "cookbook",
        "collection_identifiers": [col_id],
        "stages": [{
            "stage_name": "search",
            "stage_type": "filter",
            "config": {"stage_id": "feature_search", "parameters": {
                "searches": [{
                    "feature_uri": feature_uri,
                    "query": {"input_mode": "text", "text": "{{INPUT.query}}"},
                    "top_k": 10,
                }],
                "final_top_k": 5,
                "fusion": "rrf",
                "collection_identifiers": [col_id],
            }},
        }],
        "input_schema": {"query": {"type": "string", "description": "Search query"}},
    })
    results = post(f"/v1/retrievers/{ret['retriever_id']}/execute", {"inputs": {"query": args.query}})
    docs = results.get("documents") or results.get("results") or []
    print(f"\n✅ {name} processed 1 object and returned {len(docs)} search result(s) for {args.query!r}:")
    for d in docs[:5]:
        score = d.get("score")
        print(f"   - document_id={d.get('document_id')} score={score}")
    print(f"\nNamespace {ns['namespace_id']} auto-expires in 6h. Docs: "
          f"https://mixpeek.com/docs/processing/feature-extractors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
