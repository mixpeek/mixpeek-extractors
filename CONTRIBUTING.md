# Contributing

This catalog is **auto-generated** — please don't hand-edit `README.md` or any
`extractors/<name>/README.md`. They are rendered from Mixpeek's live extractor
registry (the same `FeatureExtractorModel` definitions the API serves), so the
docs can never silently drift from the product.

## What's generated vs. editable

| Path | Source of truth | Edit here? |
|---|---|---|
| `README.md` | registry → generator | ❌ generated |
| `extractors/*/README.md` | registry → generator | ❌ generated |
| Per-extractor **curated copy** (title, tagline, "when to use", SEO keywords) | `CURATED` dict in the generator | ✅ in the monorepo generator |
| `LICENSE`, `CONTRIBUTING.md`, `REPO_SETUP.md`, `.github/` | this repo | ✅ |

## Regenerating

The generator lives in the Mixpeek monorepo (it imports the engine, so it can't
run from this public repo):

```bash
# in mixpeek/server
make cookbook        # = python scripts/devrel/generate_extractor_cookbook.py
```

It writes into this repo's `README.md` + `extractors/`. A monorepo CI job runs
the generator and fails if the committed cookbook is stale, so a new/changed
extractor forces a regenerate. To improve a tagline or add keywords for an
extractor, edit the `CURATED` dict in
`server/scripts/devrel/generate_extractor_cookbook.py` and regenerate.

## Publishing

This repo is **published automatically** from the Mixpeek monorepo. On every
change to `extractors-cookbook/` on `main`, a monorepo CI job
(`.github/workflows/publish-extractor-cookbook.yml`) mirrors the directory here.
You don't push to this repo directly — change the source in the monorepo
(`make cookbook` for content, the `CURATED` dict for copy) and it flows through.

## Found a bug in an example?

Open an issue — but note the *extractor config* blocks are generated from the
schema, so if a parameter looks wrong it's most likely a registry change that
hasn't been regenerated yet. Ping us and we'll re-run the generator.
