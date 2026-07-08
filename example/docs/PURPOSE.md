# Purpose: ADD LLM Wiki

**Source material:**
- `docs/requirements/REQ-001-llm-wiki-cli.md` — refined LLM-wiki requirements and user clarifications
- `docs/requirements/llm-wiki.md` — Karpathy LLM-wiki pattern source
- `README.md` — staged delivery and hexagonal design baseline

**Date:** 2026-07-01
**Status:** Draft

---

## Thesis

ADD LLM Wiki is a local-first tool that lets a knowledge worker turn an existing Obsidian vault into a persistent, compounding LLM-maintained wiki without surrendering ownership of the raw notes.

## The job it does

A knowledge worker with a populated Obsidian vault hires the tool to read selected markdown sources, maintain structured wiki pages, answer questions from that wiki, and surface wiki health issues while keeping raw source notes read-only and human-curated.

## North-star outcome

The user can rely on the wiki as a durable second layer of knowledge: initialized, ingested, queried, linted, browsed in Obsidian, and improved over time without modifying source notes.

## Trade-off rule

When goals conflict, optimize for **durable, inspectable knowledge artifacts under user control** over **maximum automation or query-time convenience**.

This keeps the product aligned with the LLM-wiki pattern: the wiki is the compounding artifact. Automation is useful only when it preserves user confirmation, readable markdown, and source immutability.

## Anti-thesis

- A transient chat or RAG wrapper that answers questions without improving the persistent wiki.
- A tool that rewrites or reorganizes the user's raw Obsidian notes.
- A schema-only demo that cannot initialize, ingest, query, and lint a real vault.
- A monolithic CLI whose logic would have to be rewritten for an Obsidian plugin.
- A fully autonomous curator that files or fixes wiki pages without user confirmation where the requirements call for review.

## Success signals

- A real vault can be initialized with `wiki/SCHEMA.md`, `wiki/index.md`, and `wiki/log.md` while all non-wiki markdown stays untouched.
- Ingested sources produce durable wiki page updates, index entries, log entries, and `.ingested.json` records.
- Queries read the wiki, answer with wiki citations, and only file answers after user confirmation.
- Lint reports contradictions, stale claims, orphan pages, and missing links without silently rewriting pages.
- Stage 1 works as a Cursor-first daily driver before the Python CLI exists.
- Stage 2 exposes the same behavior through a hexagonal Python core so a future Obsidian plugin can reuse use cases and ports.

## Open purpose questions

- [ ] Packaging/distribution for users to install Stage 1 commands outside this repository remains a later design concern.

## Links

- Related requirements: `docs/requirements/REQ-001-llm-wiki-cli.md`
- Related domain model: `docs/DOMAIN.md`

---

*Created: 2026-07-01 | Modeled by: modeler in Purpose Mode*
