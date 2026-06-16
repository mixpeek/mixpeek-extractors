# Audio Fingerprinting (CLAP)

> 512-D audio embeddings with CLAP — content-based audio search and matching from files or video tracks.

`audio_fingerprint_extractor` · `v1` · **🔊 Audio · 🎬 Video** · 3 cr/extraction

Audio fingerprinting using CLAP (Contrastive Language-Audio Pretraining).

Extracts 512-dimensional embeddings from audio files or audio tracks extracted from video. Uses laion/clap-htsat-tiny model.

**Pipeline Steps:**
1. Audio extraction from video (if video input, via FFmpeg)
2. Audio segmentation (configurable window + hop)
3. CLAP embedding generation (512-d per segment)
4. L2 normalization
5. Output validation

**Use for:** Sound mark detection, audio similarity search, music/jingle identification, audio deduplication.

**Not for:** Speech-to-text (use omnilingual_asr), general audio classification (use dedicated classifiers).

**When to use:** Music/sound similarity, audio dedup, and text→audio search.

## Embeddings produced

- `laion__clap_htsat_tiny`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `audio` | `string` | — | `—` | Audio URL or S3 path. Formats: MP3, WAV, FLAC, OGG, M4A.  |
| `video` | `string` | — | `—` | Video URL or S3 path. Audio track is extracted via FFmpeg. Formats: MP4, MOV, AVI, MKV, WebM. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `segment_duration_sec` | `number` | — | `5.0` | Duration of each audio segment in seconds. 5.0: Recommended for sound mark matching. Shorter segments increase recall but reduce per-segment context. |
| `segment_hop_sec` | `number` | — | `2.5` | Hop size between segments in seconds. 2.5: 50% overlap (recommended). Set equal to segment_duration_sec for no overlap. |
| `sample_rate` | `integer` | — | `48000` | Target sample rate for audio. 48000: CLAP default (recommended). Audio is resampled to this rate before embedding. |
| `normalize_embeddings` | `boolean` | — | `True` | L2-normalize embeddings to unit vectors (recommended for cosine similarity). |
| `max_audio_length_sec` | `number` | — | `120.0` | Maximum audio length to process in seconds. 120: Default (2 minutes). Audio beyond this is truncated. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `audio_fingerprint_extractor_v1_embedding` | `array` | ✅ | `—` | CLAP audio embedding (512-d, L2-normalized). Use cosine similarity for audio matching. |
| `segment_index` | `integer` | ✅ | `—` | Index of this segment in the source audio (0-based) |
| `start_time_sec` | `number` | ✅ | `—` | Start time of this segment in the source audio (seconds) |
| `end_time_sec` | `number` | ✅ | `—` | End time of this segment in the source audio (seconds) |
| `duration_sec` | `number` | ✅ | `—` | Duration of this segment (seconds) |
| `total_duration_sec` | `number` | — | `—` | Total duration of the source audio (seconds) |
| `sample_rate` | `integer` | ✅ | `—` | Sample rate used for processing |
| `audio_source_type` | `string` | ✅ | `—` | Source type: 'audio' or 'video' |
| `embedding_model` | `string` | — | `laion/clap-htsat-tiny` | CLAP model used for embedding |
| `processing_time_ms` | `number` | ✅ | `—` | Processing time for this segment (milliseconds) |

## Try it

Attach this extractor to a collection, then upload an object and search. The extractor config below is generated from the live schema; see the [API reference](https://docs.mixpeek.com) for the full request envelope.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"audio_fingerprint_extractor","version":"v1","parameters":{"description":"Sound mark detection (IP safety)","normalize_embeddings":true,"sample_rate":48000,"segment_duration_sec":5.0,"segment_hop_sec":2.5}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'audio_fingerprint_extractor', 'version': 'v1', 'parameters': {'description': 'Sound mark detection (IP safety)', 'normalize_embeddings': True, 'sample_rate': 48000, 'segment_duration_sec': 5.0, 'segment_hop_sec': 2.5}}],
)
```

---

<sub>Topics: audio fingerprint api, clap embeddings, audio search, sound similarity, content based audio retrieval</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Docs](https://docs.mixpeek.com) · [Get an API key](https://mixpeek.com)</sub>
