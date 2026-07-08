<!--
Purpose artifact contract:
- This file is produced or updated by /define-purpose (modeler in Purpose mode).
- Save it to the configured purpose path (default `docs/PURPOSE.md`).
- Purpose is canonical for product intent. Requirements, design, domain modeling, stories, reviews, and QA must not contradict it silently.
- Keep this artifact short enough for every later agent and human gate to read. If it becomes a requirements document, it has stopped doing its job.
- Unresolved purpose-level questions are listed under `Open purpose questions` and block downstream work for the affected scope.
-->

# Purpose: {Product name}

**Source material:** {bullet list of files, transcripts, notes, or user answers used in this purpose pass}
**Date:** {YYYY-MM-DD}
**Status:** Draft | Approved | Superseded (link to replacement)

---

## Thesis

{One sentence stating what this product fundamentally is and the value it exists to deliver. This is the center of gravity for trade-offs.}

## The job it does

{One short paragraph naming the primary actor, their context, the job they hire this product to do, and why the job matters.}

## North-star outcome

{The single outcome that, if true, means the product succeeded. Prefer an observable outcome over an internal implementation milestone.}

## Trade-off rule

When goals conflict, optimize for **{primary value}** over **{secondary value}**.

{Explain why this ordering reflects the product's purpose. This rule is what later agents use when requirements pull in different directions.}

## Anti-thesis

{Tempting but wrong shapes for this product. These are not generic non-goals; they are forms that would satisfy some attributes while betraying the intent.}

- ...

## Success signals

{A short list of signals a human could use to recognize that the shipped product is true to the thesis.}

- ...

## Open purpose questions

{Questions whose answers could change the thesis, job, north-star outcome, trade-off rule, or anti-thesis. These are blocking for affected downstream work.}

- [ ] ...

## Links

- Related requirements: {REQ-NNN ...}
- Related domain model: {configured domain model path, default `docs/DOMAIN.md`}
- Supersedes / superseded by: {if applicable}

---

*Created: {YYYY-MM-DD} | Modeled by: modeler in Purpose Mode*
