# Web Scraper + Multimodal Embeddings

> Crawl sites (docs, job boards, news, SPAs) and extract text, code & image embeddings in one pass.

`web_scraper` · `v1` · **📝 Text** · 5 cr/page, 1 cr/extraction, 2 cr/image

📖 **[Documentation](https://mixpeek.com/docs/processing/extractors/web-scraper)** · ▶️ **[Try in Studio](https://studio.mixpeek.com)** · ⚙️ **[API reference](https://mixpeek.com/docs/api-reference)**

Crawls websites and extracts content with multimodal embeddings. Supports documentation sites, job boards, news sites, and SPAs.

**Embedding Types:**
- Text (E5-Large 1024D): Semantic search over page content
- Code (Jina Code 768D): Code similarity and API pattern matching
- Images (SigLIP 768D): Semantic visual search (what is shown)
- Images (DINOv2 768D): Visual structure comparison (how it looks)

**Use for:** Documentation freshness detection, knowledge base building, job board ingestion, API example indexing, curriculum validation.

**When to use:** Index a website or doc portal for search/RAG without building your own crawler.

## Embeddings produced

- `intfloat__multilingual_e5_large_instruct`
- `jinaai__jina_embeddings_v2_base_code`
- `google__siglip_base_patch16_224`
- `facebook__dinov2_base`

## Inputs

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | `string` | ✅ | `—` | REQUIRED. Seed URL to start crawling from. Example: 'https://docs.example.com/api/' |

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `max_depth` | `integer` | — | `2` | Maximum link depth to crawl. 0=seed page only, 1=seed+direct links, etc. Default: 2. Max: 10. |
| `max_pages` | `integer` | — | `50` | Maximum pages to crawl. Default: 50. Max: 500. |
| `crawl_timeout` | `integer` | — | `300` | Maximum total time for crawling in seconds. Default: 300 (5 minutes). Increase for large sites with many pages. Max: 3600 (1 hour). |
| `crawl_mode` | `CrawlMode` | — | `deterministic` | Crawl strategy. DETERMINISTIC: BFS all links (predictable). SEMANTIC: LLM-guided, prioritizes relevant pages (requires crawl_goal). |
| `crawl_goal` | `string` | — | `—` | Goal for semantic crawling. Only used when crawl_mode=SEMANTIC. Example: 'Find all S3 API documentation and examples' |
| `render_strategy` | `RenderStrategy` | — | `auto` | How to render pages. AUTO (default): tries static, falls back to JS. STATIC: fast HTTP fetch. JAVASCRIPT: Playwright browser for SPAs. |
| `include_patterns` | `array` | — | `—` | Regex patterns for URLs to include. Example: ['/docs/', '/api/'] |
| `exclude_patterns` | `array` | — | `—` | Regex patterns for URLs to exclude. Example: ['/blog/', '\.pdf$'] |
| `chunk_strategy` | `ChunkStrategy` | — | `none` | How to split page content. NONE: one chunk per page. SENTENCES/PARAGRAPHS: semantic boundaries. WORDS/CHARACTERS: fixed size chunks. |
| `chunk_size` | `integer` | — | `500` | Target size for each chunk (in units of chunk_strategy). |
| `chunk_overlap` | `integer` | — | `50` | Overlap between chunks to preserve context. |
| `document_id_strategy` | `DocumentIdStrategy` | — | `url` | How to generate document IDs. URL (default): stable across re-crawls. POSITION: order-based. CONTENT: deduplicates identical content. |
| `generate_text_embeddings` | `boolean` | — | `True` | Generate E5 embeddings for text content. |
| `generate_code_embeddings` | `boolean` | — | `True` | Generate Jina code embeddings for code blocks. |
| `generate_image_embeddings` | `boolean` | — | `True` | Generate SigLIP embeddings for images/figures. |
| `generate_structure_embeddings` | `boolean` | — | `True` | Generate DINOv2 visual structure embeddings for layout comparison. |
| `response_shape` | `string | object` | — | `—` | Optional structured extraction schema. Natural language or JSON schema. Example: 'Extract API version, deprecated methods, and example code' |
| `llm_provider` | `string` | — | `—` | LLM provider for structured extraction: openai, google, anthropic |
| `llm_model` | `string` | — | `—` | LLM model for structured extraction. |
| `llm_api_key` | `string` | — | `—` | API key for LLM operations (BYOK - Bring Your Own Key). Supports: - Direct key: 'sk-proj-abc123...' - Secret reference: '{{SECRET.openai_api_key}}'  When using secret reference, the key is loaded from your organization's secrets vault at runtime. Store secrets via POST /v1/organizations/secrets.  If not provided, uses Mixpeek's default API keys. |
| `max_retries` | `integer` | — | `3` | Maximum retry attempts for failed HTTP requests. Uses exponential backoff with jitter. Default: 3. |
| `retry_base_delay` | `number` | — | `1.0` | Base delay in seconds for retry backoff. Actual delay = base * 2^attempt + jitter. Default: 1.0. |
| `retry_max_delay` | `number` | — | `30.0` | Maximum delay in seconds between retries. Default: 30. |
| `respect_retry_after` | `boolean` | — | `True` | Respect Retry-After header from 429/503 responses. If False, uses exponential backoff instead. Default: True. |
| `proxies` | `array` | — | `—` | List of proxy URLs for rotation. Supports formats: 'http://host:port', 'http://user:pass@host:port', 'socks5://host:port'. Proxies rotate on errors or every N requests. |
| `rotate_proxy_on_error` | `boolean` | — | `True` | Rotate to next proxy when request fails. Default: True. |
| `rotate_proxy_every_n_requests` | `integer` | — | `0` | Rotate proxy every N requests (0 = disabled). Useful for avoiding IP-based rate limits. Default: 0 (disabled). |
| `captcha_service_provider` | `string` | — | `—` | Captcha solving service provider: '2captcha', 'anti-captcha', 'capsolver'. If not set, captcha pages are skipped gracefully. |
| `captcha_service_api_key` | `string` | — | `—` | API key for captcha solving service. Supports secret reference: '{{SECRET.captcha_api_key}}'. Required if captcha_service_provider is set. |
| `detect_captcha` | `boolean` | — | `True` | Detect captcha challenges (Cloudflare, reCAPTCHA, hCaptcha). If detected and no solver configured, page is skipped. Default: True. |
| `persist_cookies` | `boolean` | — | `True` | Persist cookies across requests within a crawl session. Useful for sites requiring authentication. Default: True. |
| `custom_headers` | `object` | — | `—` | Custom HTTP headers to include in all requests. Example: {'Authorization': 'Bearer token', 'X-Custom': 'value'} |
| `youtube_mode` | `string` | — | `auto` | YouTube channel fast path. 'auto' (default): detect YouTube channel URLs and hand off to yt-dlp; other URLs run normal BFS. 'off': never hand off. 'force': treat every URL as a YouTube channel (useful for explicit channel buckets). |
| `youtube_max_videos` | `integer` | — | `50` | Max videos to pull per channel enumeration. Default: 50. |
| `youtube_backfill_months` | `integer` | — | `6` | Skip videos older than this many months. Default: 6. |
| `youtube_show_filter` | `string` | — | `—` | Optional case-insensitive regex applied to video titles. Used when a channel hosts multiple shows and you only want one. |
| `youtube_download_videos` | `boolean` | — | `True` | If true (default), download each video file so downstream processors can read it from the `video_path` field. If false, only metadata + captions are emitted. |
| `youtube_format_ladder` | `string` | — | `b[height<=720]/bv*[height<=720]+ba/best` | yt-dlp format selector. Defaults to a muxed-first ladder that avoids breaking on YouTube's DASH n-challenge when the current EJS signature solver is stale. See BUILD_LOG.md in the greenroom folder for the rationale. |
| `youtube_cookies_path` | `string` | — | `—` | Optional path to a Netscape cookies file. Required for age-gated or members-only content. |
| `youtube_request_sleep` | `number` | — | `1.0` | Seconds to sleep between yt-dlp requests. Default: 1.0. |
| `delay_between_requests` | `number` | — | `0.0` | Delay in seconds between consecutive requests. Useful for polite crawling and avoiding rate limits. Default: 0 (no delay). |

## Output fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `content` | `string` | — | `—` | Extracted text content from the page or chunk. |
| `title` | `string` | — | `—` | Page title extracted from HTML. |
| `page_url` | `string` | — | `—` | URL of the source page. |
| `code_blocks` | `array` | — | `—` | Code blocks extracted from the page. |
| `images` | `array` | — | `—` | Images extracted from the page. |
| `asset_links` | `array` | — | `—` | Downloadable assets discovered on this page (PDFs, docs, archives). These links are captured for downstream processing by specialized extractors (e.g., PDF collection) but are NOT followed during crawling. Use this to build complete documentation coverage including non-HTML assets. |
| `intfloat__multilingual_e5_large_instruct` | `array` | — | `—` | E5 embedding for text content (1024D). Derived from intfloat/multilingual-e5-large-instruct. |
| `jinaai__jina_embeddings_v2_base_code` | `array` | — | `—` | Jina code embedding for code blocks (768D). Derived from jinaai/jina-embeddings-v2-base-code. |
| `google__siglip_base_patch16_224` | `array` | — | `—` | SigLIP embedding for images (768D). Derived from google/siglip-base-patch16-224. |
| `facebook__dinov2_base` | `array` | — | `—` | DINOv2 visual structure embedding (768D). Derived from facebook/dinov2-base. |
| `chunk_index` | `integer` | — | `—` | Index of this chunk within the page. |
| `total_chunks` | `integer` | — | `—` | Total chunks from this page. |
| `crawl_depth` | `integer` | — | `—` | Depth from seed URL (0=seed page). |
| `parent_url` | `string` | — | `—` | URL of the page that linked to this one. |

## Quickstart

**Fastest path:** create a collection with this extractor in [Mixpeek Studio](https://studio.mixpeek.com/namespaces/create), upload an object, and search — no code. Prefer the API? The extractor config below is generated from the live schema; see the [API reference](https://mixpeek.com/docs/api-reference) for the full request envelope, or the [extractor docs](https://mixpeek.com/docs/processing/extractors/web-scraper) for a full walkthrough.

```bash
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"my-collection","feature_extractors":[{"feature_extractor_name":"web_scraper","version":"v1","parameters":{"chunk_size":3,"chunk_strategy":"paragraphs","description":"Documentation site crawl","max_depth":3,"max_pages":100}}]}'
```

```python
from mixpeek import Mixpeek

client = Mixpeek(api_key="$MIXPEEK_API_KEY")
client.collections.create(
    collection_name="my-collection",
    feature_extractors=[{'feature_extractor_name': 'web_scraper', 'version': 'v1', 'parameters': {'chunk_size': 3, 'chunk_strategy': 'paragraphs', 'description': 'Documentation site crawl', 'max_depth': 3, 'max_pages': 100}}],
)
```

---

<sub>Topics: web scraper api, website embeddings, crawl and embed, rag website, documentation search</sub>

<sub>↩ Back to the [Extractor Catalog](../../README.md) · [Documentation](https://mixpeek.com/docs/processing/extractors/web-scraper) · [Try in Studio](https://studio.mixpeek.com) · [Get an API key](https://studio.mixpeek.com/namespaces/create)</sub>
