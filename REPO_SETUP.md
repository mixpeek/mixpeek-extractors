# Repo setup — discoverability checklist

One-time settings to make this repo rank and get found. Do these in the GitHub
UI when the repo is created (they can't be set from the file tree).

## 1. Repo name

`mixpeek-extractors` — keyword-first, matches what people search. (Avoid
`cookbook`/`examples`-only names; they bury the product term.)

## 2. About → Description

> Multimodal extractors for video, image, audio, text & PDF — turn any file
> into searchable vector embeddings (SigLIP, Gemini, E5, CLAP, ArcFace).

(Catalog count is shown by the auto-generated badge in the README; don't
hardcode a number here that will go stale.)

## 3. About → Website

`https://mixpeek.com`

## 4. About → Topics (GitHub topics drive search + the Topics pages)

Add all of these:

```
multimodal, embeddings, vector-search, video-search, semantic-search, rag,
image-embeddings, video-embeddings, audio-embeddings, ocr, face-recognition,
siglip, gemini, whisper, clip, vector-database, machine-learning, ai, mixpeek,
feature-extraction
```

## 5. Social preview image

Settings → Social preview → upload a 1280×640 card (logo + "Multimodal
Extractors" + the modality icons). This is what renders in Twitter/LinkedIn/
Slack unfurls and drives click-through.

## 6. Pin it

Pin the repo on the Mixpeek org profile, and link it from:
- the homepage footer / "Developers" nav
- the docs site ("Extractor catalog")
- the README of the main SDK repos

## 7. README hygiene (already done by the generator)

- H1 leads with the product + the searched terms.
- A catalog **table** (every row is keyword-rich and individually indexable).
- "Browse by use case" cross-links (internal link graph = better ranking).
- Per-extractor pages each target a long-tail query (e.g. "video ocr api").
- Keyword footer (`<sub>Topics: …`) on every page.

## 8. Keep it alive

A stale showcase reads as a stale product. The monorepo CI regenerates on every
extractor change and fails if this repo is out of date — so the catalog count
and parameters track production automatically. Don't let that job be skipped.
