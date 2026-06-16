# Passthrough (Storage Only)

> Store and canonicalize objects with zero ML — metadata-only ingestion.

`passthrough_extractor` · `v1` · **📝 Text · 🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF** · 1 cr/extraction

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/passthrough)** · ▶️ **[Try in Studio](https://studio.mixpeek.com)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference)**

Minimal passthrough extractor for simple object storage. No ML processing - just canonicalization and data preservation. Use when you need to store objects without feature extraction.

**When to use:** You want Mixpeek's object/bucket model and metadata filtering without paying for embeddings.

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `content` | `string` | — | `—` | URL or path to content (any type supported). |
| `data` | `object` | — | `—` | Direct data payload to store. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `preserve_metadata` | `boolean` | — | `True` | Preserve source object metadata in output document. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `content_url` | `string` | — | `—` | Canonicalized URL of stored content. |
| `content_type` | `string` | — | `—` | Detected content type. |
| `size_bytes` | `integer` | — | `—` | Content size in bytes. |
| `metadata` | `object` | — | `—` | Preserved metadata from source object. |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/passthrough) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"passthrough_extractor","version":"v1"}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'passthrough_extractor', 'version': 'v1'}],
)
```

---

<sub>Topics: object storage api, metadata only ingestion, no embedding extractor</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/passthrough) · [Try in Studio](https://studio.mixpeek.com) · [Get an API key](https://studio.mixpeek.com/namespaces/create)</sub>
