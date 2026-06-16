# Image Embeddings (SigLIP)

> Dense 768-D image embeddings with Google SigLIP — text-to-image search in one contrastive space.

`image_extractor` · `v1` · **🖼️ Image · 📄 PDF** · 2 cr/image

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/image?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor)** · ▶️ **[Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor)**

Image embedding extractor using Google SigLIP (768D). Generates dense vector embeddings for images and PDFs, with text query support in the same contrastive latent space. Optimized for visual similarity search, product matching, and text-to-image search.

**When to use:** Visual similarity search, text→image retrieval, product/image dedup, and PDF-page visual search.

## Embeddings produced

- `google_siglip_base_v1`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `image` | `string` | ✅ | `—` | Image or PDF URL or S3 path for embedding generation. |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `enable_thumbnails` | `boolean` | — | `True` | Whether to generate thumbnail images. |
| `use_cdn` | `boolean` | — | `False` | Whether to use CloudFront CDN for thumbnail delivery. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `image_extractor_v1_embedding` | `array` | ✅ | `—` | SigLIP image embedding (768-d). |
| `processing_time_ms` | `number` | ✅ | `—` | Processing time in milliseconds |
| `thumbnail_url` | `string` | — | `—` | S3 URL of the thumbnail image |
| `page_number` | `integer` | — | `—` | Page number for PDF sources (1-indexed) |
| `total_pages` | `integer` | — | `—` | Total number of pages in the PDF |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/image?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"image_extractor","version":"v1","parameters":{"enable_thumbnails":true,"use_cdn":false}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'image_extractor', 'version': 'v1', 'parameters': {'enable_thumbnails': True, 'use_cdn': False}}],
)
```

---

<sub>Topics: image embeddings api, siglip, text to image search, visual search, image similarity, clip alternative</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/image?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor) · [Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor) · [Get an API key](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=image_extractor)</sub>
