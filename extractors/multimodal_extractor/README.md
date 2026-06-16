# Multimodal Video/Audio/Image (Vertex v1 · Gemini v2)

> Unified embeddings for video, audio, image & text — FFmpeg scene/silence chunking, Whisper transcription, thumbnails.

`multimodal_extractor` · `v2` · **🎬 Video · 🖼️ Image · 🔊 Audio · 📝 Text** · 50 cr/minute, 5 cr/image, 2 cr/1k_tokens

**Multimodal extractor v2** using **Gemini Embedding 2** (3072D) for unified embeddings.

Same pipeline as v1 (FFmpeg chunking, Whisper transcription, thumbnails, Gemini vision) but with upgraded embedding model:
- **v1**: Vertex Multimodal Embedding (1408D)
- **v2**: Gemini Embedding 2 (3072D, configurable: 1536/768)

Gemini Embedding 2 is Google's first natively multimodal embedding model, mapping text, images, video (up to 120s), audio, and PDFs into a unified space.

**Pipeline Steps:**
1. FFmpeg chunking (time/scene/silence)
2. Whisper transcription (optional)
3. E5 transcription embeddings (optional, 1024D)
4. **Gemini Embedding 2** multimodal embeddings (3072D)
5. Thumbnail generation (optional)
6. Gemini visual description/OCR (optional)

**Use for:** Unified multimodal search with higher-dimensional embeddings and native multimodal understanding.

**When to use:** Video search, scene-level retrieval, ad/creative analysis, and any mixed-media corpus that needs one searchable space.

## Embeddings produced

- `gemini-embedding-2`
- `multilingual_e5_large_instruct_v1`

## Versions

| Version | Embeddings | Modalities |
|---|---|---|
| `v1` | `vertex_multimodal_embedding`, `multilingual_e5_large_instruct_v1` | 🎬 Video · 🖼️ Image · 🔊 Audio · 📝 Text |
| `v2` *(latest)* | `gemini-embedding-2`, `multilingual_e5_large_instruct_v1` | 🎬 Video · 🖼️ Image · 🔊 Audio · 📝 Text |

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `video` | `string` | — | `—` | URL or S3 path to video file. Decomposed into segments. |
| `image` | `string` | — | `—` | URL or S3 path to image file. Embedded directly. |
| `text` | `string` | — | `—` | Plain text content. Embedded directly. |
| `gif` | `string` | — | `—` | URL or S3 path to GIF file. Treated as video. |
| `custom_thumbnail` | `string` | — | `—` | Optional custom thumbnail URL. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `split_method` | `SplitMethod` | — | `time` | Video splitting strategy. |
| `description_prompt` | `string` | — | `Watch this video segment carefully and describe exactly what you see. Do not make up or infer details that are not visible in the footage. Include: who is shown (gender, appearance, actions), what they are doing, the setting/location, and any products, text, or branding visible on screen.` | Prompt for description generation. |
| `time_split_interval` | `integer` | — | `10` | Interval in seconds for 'time' splitting. |
| `silence_db_threshold` | `integer` | — | `—` | Decibel threshold for silence detection. Recommended: -40. |
| `scene_detection_threshold` | `number` | — | `—` | Scene detection threshold (0.0-1.0). Recommended: 0.5. |
| `run_transcription` | `boolean` | — | `False` | Run Whisper transcription on segments. |
| `transcription_language` | `string` | — | `en` | Transcription language code. |
| `run_video_description` | `boolean` | — | `False` | Generate Gemini descriptions for segments. |
| `run_transcription_embedding` | `boolean` | — | `False` | Generate E5 embeddings for transcriptions (1024D). |
| `run_multimodal_embedding` | `boolean` | — | `True` | Generate Gemini Embedding 2 multimodal embeddings (3072D). Creates unified embeddings across video, image, text, audio, and GIF content. |
| `run_ocr` | `boolean` | — | `False` | Extract text from video frames via Gemini OCR. |
| `max_segment_duration` | `number` | — | `30.0` | Maximum duration in seconds for any single segment. Scene/silence segments longer than this are subdivided. Set to None to disable. Default: 30s. |
| `sensitivity` | `string` | — | `low` | Scene detection sensitivity. |
| `enable_thumbnails` | `boolean` | — | `True` | Generate thumbnail images for segments. |
| `use_cdn` | `boolean` | — | `False` | Use CloudFront CDN for thumbnail delivery. |
| `generation_config` | `GenerationConfig` | — | `—` |  |
| `output_dimensionality` | `integer` | — | `3072` | Output embedding dimensions. Gemini Embedding 2 supports Matryoshka dimension reduction: 3072 (full), 1536, or 768. |
| `task_type` | `string` | — | `RETRIEVAL_DOCUMENT` | Embedding task type hint. Options: RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION. |
| `response_shape` | `string | object` | — | `—` | Custom structured output schema for Gemini extraction. String for natural language prompt, dict for explicit JSON schema. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `start_time` | `number` | ✅ | `—` | Start time of the segment in seconds |
| `end_time` | `number` | ✅ | `—` | End time of the segment in seconds |
| `start_frame` | `integer` | — | `—` | Start frame number of the segment (start_time * fps) |
| `end_frame` | `integer` | — | `—` | End frame number of the segment (end_time * fps) |
| `fps` | `number` | — | `—` | Frame rate of the video at the time of splitting |
| `source_fps` | `number` | — | `—` | Original source video frame rate before preprocessing (e.g. 29.97, 30, 23.976) |
| `duration` | `number` | — | `—` | Total source video duration in seconds |
| `transcription` | `string` | — | `—` | Transcription of audio |
| `description` | `string` | — | `—` | Generated segment description |
| `ocr_text` | `string` | — | `—` | OCR text from video frames |
| `json_output` | `object` | — | `—` | Raw JSON from underlying models |
| `thumbnail_url` | `string` | — | `—` | Thumbnail image URL |
| `source_video_url` | `string` | — | `—` | Original source video URL |
| `video_segment_url` | `string` | — | `—` | Video segment URL |
| `multimodal_extractor_v2_multimodal_embedding` | `array` | — | `—` | Dense vector embeddings (3072D) via Gemini Embedding 2 for multimodal content. |
| `multimodal_extractor_v2_transcription_embedding` | `array` | — | `—` | Dense vector embeddings (1024D) for transcription text via E5-Large. |
| `internal_metadata` | `object` | — | `—` | Internal processing metadata |

## Try it

Attach this extractor to a collection, then upload an object and search. The extractor config below is generated from the live schema; see the [API reference](https://docs.mixpeek.com) for the full request envelope.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"multimodal_extractor","version":"v2","parameters":{"description":"Standard video processing with Gemini Embedding 2","enable_thumbnails":true,"output_dimensionality":3072,"run_multimodal_embedding":true,"split_method":"time","time_split_interval":10}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'multimodal_extractor', 'version': 'v2', 'parameters': {'description': 'Standard video processing with Gemini Embedding 2', 'enable_thumbnails': True, 'output_dimensionality': 3072, 'run_multimodal_embedding': True, 'split_method': 'time', 'time_split_interval': 10}}],
)
```

---

<sub>Topics: video embeddings api, multimodal embeddings, video scene detection, video search api, whisper transcription, gemini embedding 2</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Docs](https://docs.mixpeek.com) · [Get an API key](https://mixpeek.com)</sub>
