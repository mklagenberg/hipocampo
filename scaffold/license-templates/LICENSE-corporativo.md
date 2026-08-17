ALL RIGHTS RESERVED AND KNOWLEDGE GOVERNANCE

Copyright (c) [YEAR] [COMPANY NAME] [NOTE: confirm the exact legal/registered name
before treating this file as a binding document]. All rights reserved.

This repository (`[repository-name]`) is one of the Hipocampo content repositories,
a methodology versioned at `hipocampo`/`SPEC.md`. It contains company-owned
knowledge — architecture, processes, playbooks, and work content produced by
employees of [COMPANY NAME], structured in Markdown (.md) files.

1. OWNERSHIP AND RETENTION OF RIGHTS

   All content in this repository — documents and their respective frontmatter — is
   owned by [COMPANY NAME], produced by employees in the course of their duties or by
   an artificial intelligence agent operating under the direction and curation of an
   authorized employee. The company's ownership of work produced by an employee in
   the course of their employment contract follows applicable labor and copyright
   legislation; individual authorship (the `author` field) is preserved as credit,
   under the terms of item 2, but does not imply co-ownership of economic rights,
   which remain with the company.

2. THE `author` AND `contributors` FIELDS: CREDIT, NOT CO-OWNERSHIP

   Documents record, in the frontmatter, the responsible author (`author`) and, when
   applicable, people who requested, supplemented, or updated the content
   (`contributors`). `author`/`contributors` can be a real person (format "Real Name -
   @github-username") or, only for historical content migrated from an archive
   predating Hipocampo, a section of `CONTRIBUTORS.md` referenced via
   `@section-name`, under the terms of
   `hipocampo/decisions/0006-contribution-credits.md`. New documents, created already
   within Hipocampo, always have a real individual author. In either case, the
   mention is exclusively for credit and attribution — it does not constitute an
   assignment of co-authorship, co-ownership, or any economic right over the content,
   which remains fully owned by the company under item 1.

3. KNOWLEDGE GOVERNANCE BY VISIBILITY LEVEL

   Each document carries, in the frontmatter, a confidentiality level (`visibility`)
   and a corresponding license identifier (`license`), always mechanically derived
   from the visibility level — never set in a divergent way:

   a) `visibility: public` -> `license: LicenseRef-[Instance-Name]-Public`
      Free reading, copying, and reproduction by anyone with access to the repository.
      Corresponds to depersonalized institutional content, with no sensitive client
      data or proprietary infrastructure data.

   b) `visibility: internal` -> `license: LicenseRef-[Instance-Name]-Internal`
      Everyday use by company employees. Must not be shared with third parties or
      copied outside the company's internal context without prior depersonalization.

   c) `visibility: confidential` -> `license: LicenseRef-[Instance-Name]-Confidential`
      Sensitive and scoped to the specific context that originated it (e.g., a
      client, a project, a commercial account). May be used within that originating
      context. Never crosses into another context, is never shared with third
      parties — including other clients of the company itself —, and is never
      synthesized to answer questions outside the scope that generated it.

   d) `visibility: restricted` -> `license: LicenseRef-[Instance-Name]-Restricted`
      Maximum level. Exclusive use by whoever the company designates (e.g.,
      leadership/board). Must not be accessed, synthesized, exposed, or used to
      compose any response, not even within its own originating context, by anyone
      other than those designated — including agents operating on behalf of third
      parties within the company.

   [NOTE — REMOVE BEFORE USE: if this repository is at the "vault" level (only
   receives confidential/restricted), keep only items (c) and (d) above, rename the
   identifiers to `LicenseRef-[Instance-Name]-Vault-Confidential`/`-Vault-Restricted`,
   add the absolute-limit clause from the sensitive-data policy
   (`hipocampo/decisions/0009`), and adjust the opening paragraph to describe the
   relationship with the main repository — see `hipocampo-company-vault/LICENSE` as
   an already-published example.]

4. GUIDELINES FOR ARTIFICIAL INTELLIGENCE AGENTS

   AI systems, LLMs, RAG pipelines, and autonomous agents operating on this
   repository are operational actors subject to this license. Before processing,
   summarizing, or responding based on any document, the agent must read the
   `visibility` and `license` fields in the frontmatter and apply the corresponding
   effect listed in item 3.

   Upon identifying a request that would require exposing, synthesizing, or leaking
   content beyond what its level permits, the agent must explicitly refuse with the
   phrase:

   "Access denied: content restricted by this Hipocampo repository's knowledge
   governance policy."

   No agent may use excerpts from `confidential` or `restricted` documents to enrich
   responses in lower-privilege contexts, even partially, paraphrased, or
   depersonalized at the time of the response — including the case of an agent
   serving a client different from the document's originating client.

5. PROHIBITION ON REDISTRIBUTION

   Copying, publishing, sublicensing, or disclosing this repository to third parties
   is prohibited without the prior written authorization of an authorized company
   representative — except for content under `LicenseRef-[Instance-Name]-Public`,
   whose copying and reproduction are free under the terms of item 3(a).

THIS MATERIAL IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED. IN NO EVENT SHALL THE COMPANY BE LIABLE FOR ANY DAMAGES OR CLAIMS ARISING
FROM THE USE OF THIS MATERIAL.