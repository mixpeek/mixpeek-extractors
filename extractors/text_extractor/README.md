# Text Embeddings (E5-Large)

> Multilingual dense text embeddings with E5-Large — semantic search & RAG out of the box.

`text_extractor` · `v1` · **📝 Text** · 1 cr/1k_tokens

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor)** · ▶️ **[Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor)**

Extracts dense vector embeddings from text using E5-Large multilingual model. Optimized for semantic search, RAG applications, and general-purpose text retrieval. Supports text chunking/decomposition with multiple splitting strategies. With source_type='youtube', resolves YouTube URLs to caption text before embedding. Fast (5ms/doc) and supports 100+ languages.

**When to use:** Semantic search, RAG retrieval, clustering, and multilingual text matching.

## Embeddings produced

- `multilingual_e5_large_instruct_v1`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | `string` | ✅ | `—` | Text content to process into embeddings. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `source_type` | `string` | — | `text` | Source content type. Use 'youtube' to resolve YouTube URLs to caption text before embedding. Default: 'text' (plain text input). |
| `split_by` | `TextSplitStrategy` | — | `none` | Strategy for splitting text into multiple documents. |
| `chunk_size` | `integer` | — | `1000` | Target size for each chunk. |
| `chunk_overlap` | `integer` | — | `0` | Number of units to overlap between consecutive chunks. |
| `segment_length_seconds` | `integer` | — | `120` | Length of each transcript segment in seconds (for time_segments split strategy). Shorter segments give more precise search results but more documents. |
| `language` | `string` | — | `en` | Preferred language code for YouTube captions (when source_type='youtube'). |
| `extract_captions` | `boolean` | — | `True` | Extract auto-captions or manual subtitles from YouTube videos (when source_type='youtube'). Falls back to video description if False. |
| `response_shape` | `string | object` | — | `—` | Define custom structured output using LLM extraction. |
| `llm_provider` | `string` | — | `—` | LLM provider for structured extraction (openai, google, anthropic). |
| `llm_model` | `string` | — | `—` | Specific LLM model for structured extraction. |
| `llm_api_key` | `string` | — | `—` | API key for LLM operations (BYOK - Bring Your Own Key). Supports: - Direct key: 'sk-proj-abc123...' - Secret reference: '{{SECRET.openai_api_key}}'  When using secret reference, the key is loaded from your organization's secrets vault at runtime. Store secrets via POST /v1/organizations/secrets.  If not provided, uses Mixpeek's default API keys. |
| `embedding_model` | `EmbeddingModel` | — | `—` | Embedding model to use. Defaults to the current TEXT modality default in the central embedding registry. Changing this on an existing namespace requires a migration — dimensions are fixed at namespace creation. |
| `embedding_task` | `string` | — | `—` | Embedding task hint for instruction-aware models (E5, Gemini). Prefer setting this at collection level (embedding_task on the collection) rather than here. Collection-level overrides this value. Defaults to 'retrieval_document'. Values: retrieval_document, retrieval_query, semantic_similarity, classification, clustering. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | `string` | — | `—` | The processed text content for this document. |
| `text_extractor_v1_embedding` | `array` | — | `—` | Dense vector embedding. Dimensionality is determined by the selected embedding_model (see shared.models.embeddings registry). |
| `video_id` | `string` | — | `—` | YouTube video ID. |
| `title` | `string` | — | `—` | Video title. |
| `channel` | `string` | — | `—` | YouTube channel name. |
| `video_url` | `string` | — | `—` | Source YouTube video URL. |
| `duration_seconds` | `integer` | — | `—` | Total video duration in seconds. |
| `publish_date` | `string` | — | `—` | Video publish date (ISO format). |
| `start_ms` | `integer` | — | `—` | Segment start time in milliseconds. |
| `end_ms` | `integer` | — | `—` | Segment end time in milliseconds. |
| `segment_index` | `integer` | — | `—` | Index of this segment within the video (0-based). |
| `total_segments` | `integer` | — | `—` | Total number of segments from this video. |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"text_extractor","version":"v1","parameters":{"chunk_overlap":0,"chunk_size":1000,"split_by":"none"}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'text_extractor', 'version': 'v1', 'parameters': {'chunk_overlap': 0, 'chunk_size': 1000, 'split_by': 'none'}}],
)
```

---

<sub>Topics: text embeddings api, e5 large, semantic search, rag embeddings, multilingual embeddings, vector search</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor) · [Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor) · [Get an API key](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=text_extractor)</sub>
