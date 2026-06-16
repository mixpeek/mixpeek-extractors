# Face Identity (SCRFD + ArcFace)

> Production face recognition — detect, align, and embed faces to 512-D ArcFace vectors across image, video & PDF.

`face_identity_extractor` · `v1` · **🖼️ Image · 🎬 Video · 📄 PDF** · 5 cr/image, 5 cr/face

Production-grade face recognition using state-of-the-art models (SCRFD + ArcFace). Detects faces, aligns to canonical template, generates 512-dimensional embeddings with 99.8%+ verification accuracy (LFW benchmark). Supports images, videos, and PDFs.

**Pipeline Steps:**
1. Filter dataset to collection (if collection_id provided)
2. **Content Type Routing:**
   - **Images:** Direct to Step 3
   - **Videos:** Frame extraction (sampling at video_sampling_fps) → Step 3
   - **PDFs:** Page rendering → Step 3
   - **Mixed:** Branch by type, process separately, then union
3. Face detection using SCRFD
   - Detect all faces per image/frame/page
   - Extract 5-point facial landmarks (eyes, nose, mouth)
   - Filter by min_face_size and detection_threshold
4. 5-point affine face alignment
   - Warp face to canonical 112x112 template
   - Mandatory for consistent embeddings
5. ArcFace embedding generation (512D, L2 normalized)
   - arcface_r100 model
   - Cosine similarity for matching
6. **Conditional:** Quality scoring (if enable_quality_scoring=true)
   - Assess blur, size, landmark confidence
   - Filter by quality_threshold if specified
7. **Conditional:** Video deduplication (if video_deduplication=true AND video content)
   - Remove duplicate faces across frames
   - Threshold-based similarity matching
   - Track face timelines in video
8. Output validation
9. **Output:** Per-face documents with embeddings, bbox, landmarks, and quality scores

**Use for:** Employee verification, photo organization, face clustering, surveillance, identity systems.

**Not for:** General image search (use image_extractor), object detection (use multimodal_extractor).

**When to use:** Face search, person re-identification across footage, and cast/talent indexing.

## Embeddings produced

- `insightface__arcface`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `image` | `string` | — | `—` | Image URL or S3 path containing faces. Formats: JPEG, PNG, WebP, BMP. Resolution: 640px+ recommended. |
| `video` | `string` | — | `—` | Video URL or S3 path. Subject to max_video_length limit. Formats: MP4, MOV, AVI, MKV, WebM. Sampling controlled by video_sampling_fps. |
| `video_frame` | `string` | — | `—` | Single video frame URL or S3 path. Treated as image. |
| `pdf` | `string` | — | `—` | PDF URL or S3 path containing faces in pages. Each page is converted to an image and processed for faces. Useful for ID documents, resumes, forms with photos. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `detection_model` | `string` | — | `scrfd_2.5g` | SCRFD model for face detection. 'scrfd_500m': Fastest (2-3ms). 'scrfd_2.5g': Balanced (5-7ms), recommended. 'scrfd_10g': Highest accuracy (10-15ms). |
| `min_face_size` | `integer` | — | `20` | Minimum face size in pixels to detect. 20px: Balanced. 40px: Higher quality. 10px: Maximum recall. |
| `detection_threshold` | `number` | — | `0.5` | Confidence threshold for face detection (0.0-1.0). |
| `max_faces_per_image` | `integer` | — | `—` | Maximum number of faces to process per image. None: Process all. |
| `normalize_embeddings` | `boolean` | — | `True` | L2-normalize embeddings to unit vectors (recommended). |
| `enable_quality_scoring` | `boolean` | — | `True` | Compute quality scores (blur, size, landmarks). Adds ~5ms per face. |
| `quality_threshold` | `number` | — | `—` | Minimum quality score to index faces. None: Index all faces. 0.5: Moderate filtering. 0.7: High quality only. |
| `max_video_length` | `integer` | — | `60` | Maximum video length in seconds. 60: Default. 10: Recommended for retrieval. 300: Maximum (extraction only). |
| `video_sampling_fps` | `number` | — | `1.0` | Frames per second to sample from video. 1.0: One frame per second (recommended). |
| `video_deduplication` | `boolean` | — | `True` | Remove duplicate faces across video frames (extraction only). Reduces 90-95% redundancy. NOT used in retrieval. |
| `video_deduplication_threshold` | `number` | — | `0.8` | Cosine similarity threshold for deduplication. 0.8: Conservative (default). |
| `output_mode` | `string` | — | `per_face` | 'per_face': One document per face (recommended). 'per_image': One doc per image with faces array. |
| `include_face_crops` | `boolean` | — | `True` | Include aligned 112×112 face crops as base64. Adds ~5KB per face. Required for LLM cluster labeling to see actual faces instead of hallucinating. |
| `include_source_frame_thumbnail` | `boolean` | — | `False` | Include resized source frame/image as base64 thumbnail (~15-30KB per face). Used for display with bounding box overlay. |
| `store_detection_metadata` | `boolean` | — | `True` | Store bbox, landmarks, detection scores. Recommended for debugging. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `face_identity_extractor_v1_embedding` | `array` | ✅ | `—` | ArcFace face embedding (512-d L2-normalized vector). Use cosine similarity for face matching. Similarity > 0.25-0.30 indicates same person. |
| `face_index` | `integer` | ✅ | `—` | Index of this face in source image (0-based) |
| `bbox` | `object` | ✅ | `—` | Face bounding box {x1, y1, x2, y2, width, height} |
| `detection_score` | `number` | ✅ | `—` | SCRFD detection confidence (0.0-1.0) |
| `landmarks` | `object` | ✅ | `—` | 5 facial landmarks for alignment |
| `quality_score` | `number` | — | `—` | Face quality score (0.0-1.0) |
| `quality_components` | `object` | — | `—` | Quality component scores |
| `face_crop_url` | `string` | — | `—` | S3 URL of aligned 112×112 face crop JPEG |
| `aligned_face_crop` | `string` | — | `—` | Base64 aligned 112×112 face crop |
| `source_frame_thumbnail` | `string` | — | `—` | Base64 resized source frame thumbnail for display with bbox overlay |
| `source_frame_width` | `integer` | — | `—` | Original source frame width in pixels |
| `source_frame_height` | `integer` | — | `—` | Original source frame height in pixels |
| `frame_number` | `integer` | — | `—` | Frame number in source video |
| `timestamp` | `number` | — | `—` | Timestamp in source video (seconds) |
| `page_number` | `integer` | — | `—` | Page number in source PDF (0-based) |
| `embedding_model` | `string` | ✅ | `—` | Embedding model used |
| `detection_model` | `string` | ✅ | `—` | Detection model used |
| `processing_time_ms` | `number` | ✅ | `—` | Processing time (milliseconds) |

## Try it

Attach this extractor to a collection, then upload an object and search. The extractor config below is generated from the live schema; see the [API reference](https://docs.mixpeek.com) for the full request envelope.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"face_identity_extractor","version":"v1","parameters":{"description":"Employee verification (high quality, 1:1 matching)","detection_model":"scrfd_2.5g","detection_threshold":0.7,"enable_quality_scoring":true,"max_faces_per_image":1,"min_face_size":40,"normalize_embeddings":true,"output_mode":"per_face","quality_threshold":0.5,"use_case":"Corporate access control, employee ID photos for badge matching"}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'face_identity_extractor', 'version': 'v1', 'parameters': {'description': 'Employee verification (high quality, 1:1 matching)', 'detection_model': 'scrfd_2.5g', 'detection_threshold': 0.7, 'enable_quality_scoring': True, 'max_faces_per_image': 1, 'min_face_size': 40, 'normalize_embeddings': True, 'output_mode': 'per_face', 'quality_threshold': 0.5, 'use_case': 'Corporate access control, employee ID photos for badge matching'}}],
)
```

---

<sub>Topics: face recognition api, arcface embeddings, face detection, scrfd, face search, person reidentification</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Docs](https://docs.mixpeek.com) · [Get an API key](https://mixpeek.com)</sub>
