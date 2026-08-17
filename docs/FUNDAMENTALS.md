# Hipocampo — git and GitHub fundamentals (for those who've never used them)

This document doesn't assume any prior knowledge of git or GitHub. If you already use both day to day, you can skip straight to [GETTING-STARTED.md](../GETTING-STARTED.md).

## Why git + markdown, and not something else

Hipocampo stores knowledge as plain text files (`.md`, markdown) inside a git repository. Two practical reasons:

- **Markdown is plain text.** It doesn't depend on any specific program to open — any text editor can read it. This means knowledge never gets locked into a proprietary format.
- **Git versions by nature.** Every change is recorded with author, date, and what changed — without needing a separate history system.

**Parallel with Obsidian:** if you already use Obsidian (or Notion, Logseq, etc.), the idea of "notes in markdown linked by reference" is already familiar. Hipocampo is compatible with Obsidian, not a competitor — an Obsidian vault is, structurally, a folder of markdown files, and so is a Hipocampo repository. You can open a Hipocampo repository as an Obsidian vault with no conflict at all; what Hipocampo adds on top is structured frontmatter (SPEC.md) and git/GitHub versioning/permissioning, which Obsidian alone doesn't offer.

## Basic glossary

| Term | What it is |
|---|---|
| **Git** | The system that records the change history of a set of files. Runs locally, doesn't depend on internet access to work. |
| **Repository (repo)** | A folder of files with git history. It's the unit that GitHub permissions — whoever has access to a repository sees everything inside it. |
| **Commit** | A "save point" in the history — a set of changes, with author, date, and a message describing what changed. |
| **Branch** | A parallel line of development within the same repository — allows proposing a change without affecting the "official" version until it's accepted. |
| **Pull Request (PR)** | A formal request to "merge the changes from this branch into the main branch," usually reviewed before being accepted. |
| **GitHub** | A service that hosts git repositories in the cloud and adds permissioning, a web interface, and automation on top of plain git. |
| **Template** | A repository marked as a "model" — using it creates a new repository with the same starting files, without inheriting the original's commit history. |
| **Organization (org)** | A GitHub account that represents a group/company, not a person. Corporate repositories usually live in an org, not in anyone's personal account. |

## Step by step: creating a repository from a template

This is what you do to instantiate Hipocampo from `hipocampo-toolkit` (see `GETTING-STARTED.md`, section 2). With no assumption of prior knowledge:

1. Go to the `hipocampo-toolkit` repository page on GitHub (`github.com/mklagenberg/hipocampo-toolkit`).
2. Near the top of the page, to the right of the repository name, there's a green **"Use this template"** button. Click it and choose **"Create a new repository"** from the menu that appears.
3. You'll land on a new repository creation screen. Fill in:
   - **Owner** — your personal account, or the company organization, if you have permission to create repositories there (see "Organization" in the glossary above).
   - **Repository name** — the name of your content repository (e.g., `my-second-brain` or whatever name your instance will use).
   - **Visibility** — choose **Private**. This is mandatory under the methodology (see `SPEC.md`, section 8) — never choose Public here.
4. Click the green **"Create repository from template"** button. Within a few seconds you'll have a new repository, with the same files as `hipocampo-toolkit`, but without its commit history — it's a clean copy, starting from zero.
5. From here, follow `hipocampo-toolkit/POST-INSTANTIATION.md` — the template doesn't leave anything ready to use on its own; there's a mandatory first-setup checklist (swapping the inherited license, installing your own copy of the skill, among other steps).

**If the repository needs to live inside an organization (e.g., a company) and you don't see the organization in the "Owner" list:** you probably don't have permission to create repositories there — ask whoever administers the organization to create the repository, or to grant you that permission.

## Why GitHub specifically

Hipocampo's privacy model depends structurally on GitHub's actual per-repository permissioning — it's not a matter of convenience. `visibility` in the frontmatter (SPEC.md, section 2) is a reading convention; what actually prevents unauthorized access is the repository's "private" setting on GitHub. This is what makes the invariant "no knowledge repository is public" (SPEC.md, section 8) a real technical guarantee, not just a promise of good conduct.

## Privacy of a private repository on GitHub

A repository marked as **private** is only visible to whoever the owner has explicitly invited (or, in the case of an organization, to whoever has permission within that org). This is different from "not indexed" or "hard to find" — it's actual access control, enforced by GitHub itself, not by obscurity.

**What changes when AI tools enter the picture:** when using Copilot (or any AI assistant integrated with GitHub) inside a private repository, it's worth checking that tool's data-use policy specifically — it can differ from the repository's visibility policy itself. Finding verified on `docs.github.com` as of this writing (July 27, 2026): since April 24, 2026, for **Copilot Free, Pro, Pro+, and Max** plans, GitHub may use the user's interactions with Copilot features (inputs, outputs, code snippets, and associated context) to train and improve AI models, with an **opt-out** option available in personal Copilot settings. For **Copilot Business and Copilot Enterprise**, customer data is not used to train models — it's protected by GitHub's Data Protection Agreement. This is the kind of policy that changes over time — before assuming a specific plan doesn't train on your data, check the current page at `docs.github.com` (Copilot → Privacy section), don't rely solely on this paragraph.

**General principle, regardless of the policy of the day:** if this policy changes materially (for example, paid plans starting to train by default without opt-out, or the scope of collected data expanding), the privacy guarantee that the Hipocampo method assumes needs to be reassessed — it's not something decided once and never checked again.

## Privacy of AI engines in general

The same care applies to the AI agent used to operate the Hipocampo instance (Claude, ChatGPT, Copilot, or another) — model training policy varies by provider and by plan, and changes over time. Instead of a fixed table (which goes stale), use this checklist of questions before connecting an AI agent to a Hipocampo repository with sensitive content:

1. Does the plan I'm using (free/individual vs. team/enterprise/API) train the model on my content by default?
2. Is there an opt-out option, and is it enabled?
3. If it's a team/enterprise/API plan, is there an explicit contractual guarantee of non-training (not just a claim on a marketing page)?
4. Where is the official, current page for this policy — and when was the last time I checked it?

The pattern observed among the main providers (Claude, ChatGPT, Copilot), as of this writing: consumer/free plans tend to train by default with an opt-out option; Team/Enterprise/API plans tend not to train by default, with a contractual guarantee. Treat this pattern as a starting point for research, not as a fixed fact — confirm it in each provider's official documentation before deciding what to connect to sensitive content.
