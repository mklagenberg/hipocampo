# Performance and Hipocampo's graph model

Central reference — see `hipocampo/decisions/0002` for why this content lives here and new instances receive only the link, not a copy.

## How retrieval works, under the hood

Every Hipocampo document is a node: the frontmatter (SPEC.md, section 2) carries the metadata that allows filtering without reading the body (`type`, `tags`, `status`, `temporality`, `related`) — CRUD/frontmatter-first mechanic, `decisions/0012`. The graph's edges are the `related` field, both local (`"path.md"`) and cross-repository (`"$alias:path.md"`, resolved via `registry.md` — SPEC.md, section 6). This is, in practice, a knowledge graph navigable with native git/markdown tools alone — no dedicated graph database is required as a baseline.

## Comparison with Google's OKF (Open Knowledge Format)

In June 2026, Google Cloud published the [Open Knowledge Format (OKF)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) — an open, vendor-neutral specification for storing knowledge as a directory of markdown files with YAML frontmatter, designed to be shareable across different agents, LLMs, and tools. The conceptual kinship with Hipocampo is real and not a coincidence: both designs arrive at the same conclusion — markdown + YAML + tags forming a graph is the simplest format that sustains knowledge readable by both humans and agents at once.

The difference lies in the depth of the schema:

| | OKF | Hipocampo |
|---|---|---|
| Required field | only `type` | `title`, `date`, `updated`, `source`, `type`, `temporality`, `ttl`, `status`, `visibility`, `author`, `revision`, among others |
| Recommended fields | `title`, `description`, `resource`, `tags`, `timestamp` | — |
| Access governance | not the spec's focus | `visibility`/`license` derived mechanically, multi-repo architecture for real separation (`decisions/0002`, `decisions/0007`) |
| Document lifecycle | not specified | `draft`→`active`→`stale`→`archived`→`superseded`, never physically deleted (invariant 3, with the narrow exception in `decisions/0010`) |
| Privacy by instance type | not the spec's focus | explicit policy on what never enters a corporate instance (`decisions/0009`) |

In spirit, Hipocampo can be read as "OKF plus a layer of governance, lifecycle, and privacy" — not a competing alternative, but a superset designed specifically for sensitive knowledge (personal or corporate), where "who can see what" and "what should never be stored" matter as much as the graph's structure itself.

## What this means in practice

A simple OKF bundle is, in general, compatible in spirit with a Hipocampo document — both are markdown + YAML + tags. Migrating from one to the other is never a direct copy (same principle as `decisions/0011`, SPEC.md section 10): Hipocampo's richer schema requires filling in the lifecycle, visibility, and license fields that OKF doesn't require.
