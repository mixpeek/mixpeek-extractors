# Multi-File Object Embeddings (Gemini)

> Embed ALL files of an object (images, PDFs, video, audio, text) into one 3072-D Gemini vector.

`gemini_multifile_extractor` · `v1` · **🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF · 📝 Text** · 10 cr/image

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/gemini-multifile?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor)** · ▶️ **[Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor)**

**Multi-file object embedding using Gemini Embedding 2** (gemini-embedding-2, 3072-d).

Embeds ALL files of an object (images, PDFs, video, audio, text) into a SINGLE unified vector in one Gemini API call. Use when you want object-level search where similarity is based on the combined content of all an object's blobs — not individual file-level search.

**Configure with array input_mappings:**
```json
{"files": ["hero_image", "spec_sheet", "description"]}
```

**When to use:**
- Product catalogs: embed image + spec PDF + description together
- Medical records: embed scan + report + notes together
- Legal documents: embed contract + exhibits + summary together
- E-commerce: embed product photo + manual + label together

**Output:** One 3072-d embedding per object (not per file).
**Model:** gemini-embedding-2 (Gemini Embedding 2)

**When to use:** Objects that bundle several files (a product with photos + spec sheet + demo clip) you want represented as one searchable entity.

## Embeddings produced

- `gemini-embedding-2`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `files` | `array` | ✅ | `—` | List of blob field values (URLs or text) to embed together. Populated automatically from array input_mappings — not set directly by users. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `output_dimensionality` | `integer` | — | `3072` | Output embedding dimensions. Gemini Embedding 2 supports 3072 (default), 768, or 256 via truncation. Lower dimensions reduce storage cost at slight quality loss. |
| `task_type` | `string` | — | `RETRIEVAL_DOCUMENT` | Embedding intent used as a text instruction for Gemini Embedding 2. Common values: RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION. |
| `input_key` | `string` | — | `files` | The input_mappings key whose value is the list of blob fields to embed together. Must match the key used in input_mappings (e.g., 'files'). Default: 'files'. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `gemini_multifile_extractor_v1_embedding` | `array` | ✅ | `—` | Gemini Embedding 2 vector (3072-d by default) for all input files combined. |
| `source_blob_count` | `integer` | ✅ | `—` | Number of blobs that were embedded together. |
| `source_blob_properties` | `array` | — | `—` | Blob property names that contributed to this embedding. |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/gemini-multifile?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"gemini_multifile_extractor","version":"v1","parameters":{"input_key":"files","output_dimensionality":3072,"task_type":"RETRIEVAL_DOCUMENT"}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'gemini_multifile_extractor', 'version': 'v1', 'parameters': {'input_key': 'files', 'output_dimensionality': 3072, 'task_type': 'RETRIEVAL_DOCUMENT'}}],
)
```

## Run it locally

Drive this extractor end-to-end from your machine with [`scripts/run_extractor.py`](../../scripts/run_extractor.py) — it creates a throwaway namespace (auto-expires in 6h), processes one object, and runs a search:

```bash
export MIXPEEK_API_KEY=sk_...   # https://studio.mixpeek.com
pip install -r scripts/requirements.txt
python scripts/run_extractor.py --extractor gemini_multifile_extractor --input <your-asset-url>
```

---

<sub>Topics: multi file embeddings, gemini embedding, object embeddings, document embeddings api</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/gemini-multifile?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor) · [Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor) · [Get an API key](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=gemini_multifile_extractor)</sub>
