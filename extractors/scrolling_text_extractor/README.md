# Scrolling/Marquee Text OCR

> Reads scrolling video text via phase-correlation band detection, panoramic stitching, and VLM OCR.

`scrolling_text_extractor` · `v1` · **🎬 Video** · 30 cr/minute

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/scrolling-text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor)** · ▶️ **[Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor)**

Extracts scrolling/marquee text from video using phase-correlation band detection, panoramic stitching, and VLM OCR.

**What it does:**
Detects text that scrolls across the screen — horizontally (R-to-L / L-to-R tickers, banners, promotions) or vertically (credits, disclaimers, terms). No single frame shows the full text; this extractor reconstructs the complete string by stitching frames together like a panorama photograph.

**Pipeline:**
1. Sample video frames at configurable FPS
2. Split frames into horizontal and vertical strips
3. Phase-correlate consecutive frames to detect per-strip pixel shift
4. Merge strips with consistent shift into scrolling bands
5. Panoramic-stitch each band into one wide/tall image
6. OCR the panorama via Gemini vision (VLM)
7. Deduplicate repeated marquee loops

**Use for:** Video ads with scrolling banners/tickers, news chyrons, scrolling disclaimers/T&Cs, credits sequences, live event info bars.

**Not for:** Static text overlays (use multimodal_extractor with run_ocr), spoken content (use multimodal_extractor with run_transcription), animated text with non-linear motion (fade, scale, rotate).

**Processing speed:** ~2-5x realtime depending on resolution and FPS.

**When to use:** News tickers, credits, marquees, and any on-screen text that moves across the frame.

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `video` | `string` | ✅ | `—` | URL or S3 path to a video file containing scrolling text. The extractor samples frames and uses phase correlation to detect which screen regions contain scrolling text, then stitches those regions into a panorama for OCR. Formats: MP4, MOV, AVI, MKV, WebM, FLV. Examples: 's3://bucket/ads/promo.mp4', 'https://cdn.example.com/video.mp4' |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `fps` | `number` | — | `5.0` | Frame sampling rate for analysis. Higher values improve detection accuracy for fast-scrolling text but increase processing time. 5 FPS works well for most video ads and tickers. |
| `strip_height` | `integer` | — | `40` | Height (in pixels) of each scanning strip used for phase correlation. Should roughly match the height of the scrolling text band. Smaller values detect narrower text bands; larger values are more robust but may miss thin tickers. 40px works for most standard video ads. |
| `min_shift_px` | `number` | — | `2.0` | Minimum pixel shift per frame to consider a strip as 'scrolling'. Lower values detect slower-moving text; higher values filter out noise. 2.0px is a good default for 5 FPS sampling. |
| `consistency_ratio` | `number` | — | `0.6` | Fraction of frame pairs that must show consistent shift for a band to be classified as scrolling. 0.6 means 60% of frames must agree. Lower values detect intermittent scrolling; higher values reduce false positives. |
| `pad` | `integer` | — | `8` | Pixel padding above/below detected band when cropping for stitching. |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `scrolling_text` | `string` | — | `—` | Full extracted scrolling text, combined from all detected bands. If multiple bands are found, their texts are joined with ' | '. Repeated marquee loops are automatically deduplicated. |
| `scroll_bands` | `array` | — | `—` | Per-band extraction details. Each entry contains: axis (horizontal/vertical), direction (right_to_left, etc.), shift_per_frame (px), and the extracted text for that band. |
| `bands_detected` | `integer` | — | `—` | Number of scrolling text bands detected in the video. |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/scrolling-text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"scrolling_text_extractor","version":"v1","parameters":{"description":"Standard video ad with scrolling banner","fps":5.0,"strip_height":40,"use_case":"Extract promotional text from video ad tickers"}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'scrolling_text_extractor', 'version': 'v1', 'parameters': {'description': 'Standard video ad with scrolling banner', 'fps': 5.0, 'strip_height': 40, 'use_case': 'Extract promotional text from video ad tickers'}}],
)
```

## Run it locally

Drive this extractor end-to-end from your machine with [`scripts/run_extractor.py`](../../scripts/run_extractor.py) — it creates a throwaway namespace (auto-expires in 6h), processes one object, and runs a search:

```bash
export MIXPEEK_API_KEY=sk_...   # https://studio.mixpeek.com
pip install -r scripts/requirements.txt
python scripts/run_extractor.py --extractor scrolling_text_extractor --input <your-asset-url>
```

---

<sub>Topics: video ocr api, scrolling text detection, marquee ocr, news ticker ocr, vlm ocr</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/scrolling-text?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor) · [Try in Studio](https://studio.mixpeek.com?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor) · [Get an API key](https://studio.mixpeek.com/namespaces/create?utm_source=github&utm_medium=cookbook&utm_campaign=extractors&utm_content=scrolling_text_extractor)</sub>
