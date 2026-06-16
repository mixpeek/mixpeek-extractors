# Document Layout Graph

> Decompose PDFs into spatial blocks — paragraphs, tables, forms, headers — with layout classification & confidence.

`document_graph_extractor` · `v1` · **📄 PDF** · 5 cr/page, 20 cr/extraction

Extracts spatial blocks from PDFs with layout classification and confidence scoring. Decomposes documents into paragraphs, tables, forms, lists, headers, footers, figures, and handwritten content. Includes optional VLM correction for low-confidence blocks. Best for archival documents, scanned files, and documents requiring spatial understanding.

**Pipeline Steps:**
1. Filter dataset to collection (if collection_id provided)
2. Find and resolve PDF URL from row data
3. **Layout Detection Mode Fork:**
   - **If use_layout_detection=true (NEW - ML-based):**
     a. PaddleOCR layout detection (finds ALL elements: text, images, tables)
     b. Skip to Step 4 (object_type already set by detector)
   - **If use_layout_detection=false (LEGACY - Text-only):**
     a. PyMuPDF span extraction (text with bounding boxes)
     b. Spatial clustering (group nearby spans into logical blocks)
     c. Layout classification (rule-based: paragraph, table, form, etc.)
4. Confidence scoring (A/B/C/D tags based on extraction quality)
5. Text cleaning (remove OCR artifacts, normalize whitespace)
6. **Conditional:** Page rendering (if generate_thumbnails=true OR use_vlm_correction=true)
   - Full page and segment thumbnails at configured DPI
7. **Conditional:** VLM correction (if use_vlm_correction=true AND not fast_mode AND confidence C/D)
   - Gemini/OpenAI/Anthropic vision models correct low-confidence text
8. **Conditional:** Text embedding (if run_text_embedding=true)
   - E5-Large embeddings (1024D) for semantic search
9. **Output:** Block-level documents with text, layout type, bbox, confidence, and embeddings

**Use for:** Archival documents, scanned PDFs, forms processing, structured extraction, document understanding.

**Not for:** Simple text extraction (use text_extractor), images (use image_extractor).

**When to use:** Document understanding, layout-aware RAG, table/form extraction, and structured PDF parsing.

## Embeddings produced

- `intfloat__multilingual_e5_large_instruct`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `pdf` | `string` | ✅ | `—` | REQUIRED. URL or S3 path to PDF file for processing. PDF will be decomposed into spatial blocks with layout classification. Supports any PDF version, both digital and scanned documents. Examples: 's3://bucket/document.pdf', 'https://example.com/report.pdf' |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `use_layout_detection` | `boolean` | — | `True` | Enable ML-based layout detection to find ALL document elements (text, images, tables, figures). When enabled, uses the configured layout_detector to detect and extract both text regions AND non-text elements (scanned images, figures, charts) as separate documents. **Recommended for**: Scanned documents, image-heavy PDFs, mixed content documents. **When disabled**: Falls back to text-only extraction (faster but misses images). Default: True (detects all elements including images). |
| `layout_detector` | `string` | — | `pymupdf` | Layout detection engine to use when use_layout_detection=True. 'pymupdf': Fast, rule-based detection using PyMuPDF heuristics (~15 pages/sec). 'docling': SOTA ML-based detection using IBM Docling with DiT model (~3-8 sec/doc). **Docling advantages**: Better semantic type detection (section_header vs paragraph), true table structure extraction (rows/cols), more accurate figure detection. **PyMuPDF advantages**: Much faster, lower memory usage, simpler dependencies. Default: 'pymupdf' for speed. Use 'docling' for accuracy-critical applications. |
| `vertical_threshold` | `number` | — | `15.0` | Maximum vertical gap (in points) between lines to be grouped in same block. Increase for looser grouping, decrease for tighter blocks. Default 15pt works well for standard documents. |
| `horizontal_threshold` | `number` | — | `50.0` | Maximum horizontal distance (in points) for overlap detection. Affects column detection and block merging. Increase for wider columns, decrease for narrow layouts. |
| `min_text_length` | `integer` | — | `20` | Minimum text length (characters) to keep a block. Blocks with less text are filtered out. Helps remove noise and tiny fragments. |
| `base_confidence` | `number` | — | `0.85` | Base confidence score for embedded (native) text. Penalties are subtracted for OCR artifacts, encoding issues, etc. |
| `min_confidence_for_vlm` | `number` | — | `0.6` | Confidence threshold below which VLM correction is triggered. Blocks with confidence < this value get sent to VLM for correction. Only applies when use_vlm_correction=True. |
| `use_vlm_correction` | `boolean` | — | `True` | Enable VLM (Vision Language Model) correction for low-confidence blocks. Uses Gemini/GPT-4V to correct OCR errors by analyzing the page image. Significantly slower (~1 page/sec) but improves accuracy for degraded docs. |
| `fast_mode` | `boolean` | — | `False` | Skip VLM correction entirely for maximum throughput (~15 pages/sec). Overrides use_vlm_correction. Use when speed is more important than accuracy. |
| `vlm_provider` | `string` | — | `google` | LLM provider for VLM correction. Options: 'google' (Gemini), 'openai' (GPT-4V), 'anthropic' (Claude). Google recommended for best vision quality. |
| `vlm_model` | `string` | — | `gemini-2.5-flash` | Specific model for VLM correction. Examples: 'gemini-2.5-flash', 'gpt-4o', 'claude-3-5-sonnet'. |
| `llm_api_key` | `string` | — | `—` | API key for VLM correction (BYOK - Bring Your Own Key). Supports: - Direct key: 'sk-proj-abc123...' - Secret reference: '{{SECRET.openai_api_key}}'  When using secret reference, the key is loaded from your organization's secrets vault at runtime. Store secrets via POST /v1/organizations/secrets.  If not provided, uses Mixpeek's default API keys. |
| `run_text_embedding` | `boolean` | — | `True` | Generate text embeddings for semantic search over block content. Uses E5-Large (1024-dim) for multilingual support. |
| `render_dpi` | `integer` | — | `150` | DPI for page rendering (used for VLM correction). 72: Fast, lower quality. 150: Balanced (recommended). 300: High quality, slower. |
| `generate_thumbnails` | `boolean` | — | `True` | Generate thumbnail images for blocks. Useful for visual previews and UI display. |
| `thumbnail_mode` | `string` | — | `both` | Thumbnail generation mode. 'full_page': Low-res thumbnail of entire page. 'segment': Cropped thumbnail of just the block's bounding box. 'both': Generate both types (recommended for flexibility). |
| `thumbnail_dpi` | `integer` | — | `72` | DPI for thumbnail generation. Lower DPI = smaller files. 72: Standard web quality. 36: Very small thumbnails. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `page_number` | `integer` | ✅ | `—` | Page number in original PDF (1-indexed) |
| `object_type` | `ObjectType` | ✅ | `—` | Classified type of this block. PARAGRAPH: Regular text. TABLE: Tabular data. FORM: Form fields. LIST: Bulleted/numbered lists. HEADER/FOOTER: Page headers/footers. FIGURE: Images/diagrams. HANDWRITTEN: Handwritten content. |
| `block_index` | `integer` | ✅ | `—` | Block index within the page (0-indexed) |
| `bbox` | `BoundingBox` | ✅ | `—` | Bounding box coordinates for this block on the page |
| `text_raw` | `string` | ✅ | `—` | Original extracted text from the block (before cleaning) |
| `text_corrected` | `string` | — | `—` | Cleaned and/or VLM-corrected text. Contains cleaned text for high-confidence blocks, VLM-corrected text for low-confidence blocks (if enabled). |
| `overall_confidence` | `number` | ✅ | `—` | Extraction confidence score (0.0-1.0) |
| `confidence_tag` | `ConfidenceTag` | ✅ | `—` | Confidence category. A: >=0.85 (high). B: >=0.70 (medium). C: >=0.50 (low, may need verification). D: <0.50 (very low, needs VLM). |
| `document_graph_extractor_v1_text_embedding` | `array` | — | `—` | Dense vector embedding for text content (1024-dim E5) |
| `thumbnail_url` | `string` | — | `—` | URL to full page thumbnail (low-res image of entire page) |
| `segment_thumbnail_url` | `string` | — | `—` | URL to segment thumbnail (cropped to block's bounding box) |
| `total_pages` | `integer` | — | `—` | Total pages in source PDF |
| `source_file` | `string` | — | `—` | Original source file name |

## Try it

Attach this extractor to a collection, then upload an object and search. The extractor config below is generated from the live schema; see the [API reference](https://docs.mixpeek.com) for the full request envelope.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"document_graph_extractor","version":"v1","parameters":{"description":"Fast processing mode (no VLM, maximum throughput)","fast_mode":true,"generate_thumbnails":true,"layout_detector":"pymupdf","run_text_embedding":true,"use_case":"High-volume document ingestion where speed matters more than perfect accuracy","use_layout_detection":true}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'document_graph_extractor', 'version': 'v1', 'parameters': {'description': 'Fast processing mode (no VLM, maximum throughput)', 'fast_mode': True, 'generate_thumbnails': True, 'layout_detector': 'pymupdf', 'run_text_embedding': True, 'use_case': 'High-volume document ingestion where speed matters more than perfect accuracy', 'use_layout_detection': True}}],
)
```

---

<sub>Topics: pdf layout extraction, document understanding api, table extraction, document graph, layout analysis</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Docs](https://docs.mixpeek.com) · [Get an API key](https://mixpeek.com)</sub>
