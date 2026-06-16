# Mixpeek Extractors — Multimodal Feature Extraction for Video, Image, Audio, Text & PDFs

[![Extractors](https://img.shields.io/badge/extractors-11-6c5ce7)](#catalog) [![Docs](https://img.shields.io/badge/docs-mixpeek.com-0984e3)](https://docs.mixpeek.com) [![License](https://img.shields.io/badge/license-MIT-2d3436)](LICENSE)

**Extractors** are Mixpeek's processing pipelines: point one at your objects (video, images, audio, PDFs, text, or whole multi-file bundles) and it produces **searchable vector embeddings** plus structured metadata — video scene detection, Whisper transcription, SigLIP/Gemini/E5 embeddings, OCR, face identity, audio fingerprinting, document layout graphs, and more. This repo is the runnable catalog.

> 🔁 **Auto-generated from the live registry** — every parameter, input field, embedding model and credit cost below is rendered straight from the API's extractor definitions, so it never drifts from production. [Get an API key →](https://mixpeek.com)

## Catalog

| Extractor | What it does | Modalities | Embeddings | Credits |
|---|---|---|---|---|
| **[Audio Fingerprinting (CLAP)](extractors/audio_fingerprint_extractor/README.md)** | 512-D audio embeddings with CLAP — content-based audio search and matching from files or video tracks. | 🔊 Audio · 🎬 Video | `laion__clap_htsat_tiny` | 3 cr/extraction |
| **[Document Layout Graph](extractors/document_graph_extractor/README.md)** | Decompose PDFs into spatial blocks — paragraphs, tables, forms, headers — with layout classification & confidence. | 📄 PDF | `intfloat__multilingual_e5_large_instruct` | 5 cr/page, 20 cr/extraction |
| **[Face Identity (SCRFD + ArcFace)](extractors/face_identity_extractor/README.md)** | Production face recognition — detect, align, and embed faces to 512-D ArcFace vectors across image, video & PDF. | 🖼️ Image · 🎬 Video · 📄 PDF | `insightface__arcface` | 5 cr/image, 5 cr/face |
| **[Image Embeddings (SigLIP)](extractors/image_extractor/README.md)** | Dense 768-D image embeddings with Google SigLIP — text-to-image search in one contrastive space. | 🖼️ Image · 📄 PDF | `google_siglip_base_v1` | 2 cr/image |
| **[Multi-File Object Embeddings (Gemini)](extractors/gemini_multifile_extractor/README.md)** | Embed ALL files of an object (images, PDFs, video, audio, text) into one 3072-D Gemini vector. | 🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF · 📝 Text | `gemini-embedding-2` | 10 cr/image |
| **[Multimodal Video/Audio/Image (Vertex v1 · Gemini v2)](extractors/multimodal_extractor/README.md)** | Unified embeddings for video, audio, image & text — FFmpeg scene/silence chunking, Whisper transcription, thumbnails. | 🎬 Video · 🖼️ Image · 🔊 Audio · 📝 Text | `gemini-embedding-2` | 50 cr/minute, 5 cr/image, 2 cr/1k_tokens |
| **[Universal All-in-One (Gemini)](extractors/universal_extractor/README.md)** | One extractor for image, video, audio & documents — auto-detects modality and applies the right pipeline. | 🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF · 📝 Text | `gemini-embedding-2` | 15 cr/image |
| **[Text Embeddings (E5-Large)](extractors/text_extractor/README.md)** | Multilingual dense text embeddings with E5-Large — semantic search & RAG out of the box. | 📝 Text | `multilingual_e5_large_instruct_v1` | 1 cr/1k_tokens |
| **[Passthrough (Storage Only)](extractors/passthrough_extractor/README.md)** | Store and canonicalize objects with zero ML — metadata-only ingestion. | 📝 Text · 🖼️ Image · 🎬 Video · 🔊 Audio · 📄 PDF | — | 1 cr/extraction |
| **[Scrolling/Marquee Text OCR](extractors/scrolling_text_extractor/README.md)** | Reads scrolling video text via phase-correlation band detection, panoramic stitching, and VLM OCR. | 🎬 Video | — | 30 cr/minute |
| **[Web Scraper + Multimodal Embeddings](extractors/web_scraper/README.md)** | Crawl sites (docs, job boards, news, SPAs) and extract text, code & image embeddings in one pass. | 📝 Text | `intfloat__multilingual_e5_large_instruct` | 5 cr/page, 1 cr/extraction, 2 cr/image |

## Browse by use case

- **🎬 Video search & scene retrieval** — [Multimodal Video/Audio/Image (Vertex v1 · Gemini v2)](extractors/multimodal_extractor/README.md), [Scrolling/Marquee Text OCR](extractors/scrolling_text_extractor/README.md)
- **🖼️ Image & visual search** — [Image Embeddings (SigLIP)](extractors/image_extractor/README.md), [Face Identity (SCRFD + ArcFace)](extractors/face_identity_extractor/README.md)
- **📝 Semantic text search & RAG** — [Text Embeddings (E5-Large)](extractors/text_extractor/README.md), [Web Scraper + Multimodal Embeddings](extractors/web_scraper/README.md)
- **🔊 Audio search & matching** — [Audio Fingerprinting (CLAP)](extractors/audio_fingerprint_extractor/README.md), [Multimodal Video/Audio/Image (Vertex v1 · Gemini v2)](extractors/multimodal_extractor/README.md)
- **📄 Document understanding** — [Document Layout Graph](extractors/document_graph_extractor/README.md), [Multi-File Object Embeddings (Gemini)](extractors/gemini_multifile_extractor/README.md)
- **🧩 Mixed / any file type** — [Universal All-in-One (Gemini)](extractors/universal_extractor/README.md), [Multi-File Object Embeddings (Gemini)](extractors/gemini_multifile_extractor/README.md), [Passthrough (Storage Only)](extractors/passthrough_extractor/README.md)

## Quickstart

```bash
export MIXPEEK_API_KEY=sk_...        # https://mixpeek.com
export MIXPEEK_NAMESPACE=my-namespace

# 1. Create a collection that runs an extractor over a bucket
curl -X POST https://api.mixpeek.com/v1/collections \
  -H "Authorization: Bearer $MIXPEEK_API_KEY" \
  -H "X-Namespace: $MIXPEEK_NAMESPACE" \
  -H "Content-Type: application/json" \
  -d '{"collection_name":"demo","feature_extractors":[{"feature_extractor_name":"text_extractor","version":"v1"}]}'
```

Full walkthrough in the [docs](https://docs.mixpeek.com).

## How it fits together

```
Bucket (your objects)  →  Collection (runs an extractor)  →  Documents + vectors  →  Retriever (search)
```

---

<sub>**Topics:** any file embeddings · arcface embeddings · audio fingerprint api · audio search · auto modality detection · clap embeddings · clip alternative · content based audio retrieval · crawl and embed · document embeddings api · document graph · document understanding api · documentation search · e5 large · face detection · face recognition api · face search · gemini embedding · gemini embedding 2 · gemini multimodal api · image embeddings api · image similarity · layout analysis · marquee ocr · metadata only ingestion · multi file embeddings · multilingual embeddings · multimodal embeddings · news ticker ocr · no embedding extractor · object embeddings · object storage api · pdf layout extraction · person reidentification · rag embeddings · rag website · scrfd · scrolling text detection · semantic search · siglip · sound similarity · table extraction · text embeddings api · text to image search · universal extractor · vector search · video embeddings api · video ocr api · video scene detection · video search api · visual search · vlm ocr · web scraper api · website embeddings · whisper transcription</sub>

<sub>Mixpeek is a multimodal data platform: ingest video, images, audio, documents and text; extract embeddings and metadata; search with hybrid retrievers. [mixpeek.com](https://mixpeek.com) · [docs](https://docs.mixpeek.com)</sub>
