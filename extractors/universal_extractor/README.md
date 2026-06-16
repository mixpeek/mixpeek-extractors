# Universal All-in-One (Gemini)

> One extractor for image, video, audio & documents — auto-detects modality and applies the right pipeline.

`universal_extractor` · `v1` · **🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF · 📝 Text** · 15 cr/image

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/universal?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor)** · ▶️ **[Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor)**

**Universal all-in-one extractor** — handles image, video, audio, and documents in a single extractor using Gemini APIs.

Automatically detects modality and applies the best processing strategy:
- **Image**: Embedding + description + OCR
- **Video**: Segment into clips → embedding + transcription + scene description per segment
- **Audio**: Transcription → embedding per segment
- **Document**: Page-level embedding + text extraction + OCR

All embeddings use Gemini Embedding 2 (3072-d) in a unified multimodal vector space, enabling cross-modal search (e.g., text query finds relevant video segments).

**Runs on Celery (no Ray startup delay)** — optimized for the Studio upload flow where files need to be searchable in seconds, not minutes.

**Model:** gemini-embedding-2 (Gemini Embedding 2, 3072-d)

**When to use:** Heterogeneous buckets where you don't want to wire a different extractor per file type.

## Embeddings produced

- `gemini-embedding-2`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `content` | `string` | ✅ | `—` | URL or path to the file to process. Populated from input_mappings. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `output_dimensionality` | `integer` | — | `3072` | Output embedding dimensions (Gemini Embedding 2 supports 256-3072). |
| `task_type` | `string` | — | `RETRIEVAL_DOCUMENT` | Embedding intent used as a text instruction for Gemini Embedding 2. Common values: RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY. |
| `generate_description` | `boolean` | — | `True` | Generate a text description of the content via Gemini vision/understanding. |
| `extract_text` | `boolean` | — | `True` | Extract text content (OCR for images/docs, transcription for audio/video). |
| `max_video_segments` | `integer` | — | `10` | Maximum number of 30s segments to process for video files. |
| `max_document_pages` | `integer` | — | `50` | Maximum number of pages to process for document files. |
| `max_file_download_mb` | `integer` | — | `500` | Maximum file download size in MB for Celery fast-path processing. |
| `max_concurrency` | `integer` | — | `4` | Maximum per-task object concurrency for Celery fast-path processing. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `universal_extractor_v1_embedding` | `array` | ✅ | `—` | Gemini Embedding 2 vector (3072-d) for the content. |
| `modality` | `string` | ✅ | `—` | Detected modality: image, video, audio, or document. |
| `text` | `string` | — | `—` | Extracted text (OCR, transcription, or document text). |
| `description` | `string` | — | `—` | AI-generated description of the content. |
| `segment_index` | `integer` | — | `—` | Segment index (for chunked content like video/audio/documents). |
| `segment_total` | `integer` | — | `—` | Total segments for this source object. |
| `page_number` | `integer` | — | `—` | Page number (documents only). |
| `start_time_s` | `number` | — | `—` | Segment start time in seconds (video/audio only). |
| `end_time_s` | `number` | — | `—` | Segment end time in seconds (video/audio only). |
| `duration_s` | `number` | — | `—` | Total file duration in seconds (video/audio only). |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/universal?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"universal_extractor","version":"v1","parameters":{"extract_text":true,"generate_description":true,"max_concurrency":4,"max_file_download_mb":500,"output_dimensionality":3072,"task_type":"RETRIEVAL_DOCUMENT"}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'universal_extractor', 'version': 'v1', 'parameters': {'extract_text': True, 'generate_description': True, 'max_concurrency': 4, 'max_file_download_mb': 500, 'output_dimensionality': 3072, 'task_type': 'RETRIEVAL_DOCUMENT'}}],
)
```

## Run it locally

Drive this extractor end-to-end from your machine with [`scripts/run_extractor.py`](../../scripts/run_extractor.py) — it creates a throwaway namespace (auto-expires in 6h), processes one object, and runs a search:

```bash
export MIXPEEK_API_KEY=sk_...   # https://studio.mixpeek.com
pip install -r scripts/requirements.txt
python scripts/run_extractor.py --extractor universal_extractor --input <your-asset-url>
```

---

<sub>Topics: universal extractor, any file embeddings, auto modality detection, gemini multimodal api</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/universal?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor) · [Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor) · [Get an API key](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=universal_extractor)</sub>
