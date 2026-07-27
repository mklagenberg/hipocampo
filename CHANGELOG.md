# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

## [1.1.0] — 2026-07-27

### Adicionado
- Campo `license` no frontmatter (SPEC.md, seção 2), sempre derivado mecanicamente de `visibility`, nunca definido à mão — padrão SPDX `LicenseRef-<idstring>`, texto legal completo no arquivo `LICENSE` da raiz de cada repositório de conteúdo. Ver `decisions/0007-licenciamento-repos-de-conteudo.md`.
- Mecanismo de créditos para conteúdo histórico/migrado sem autoria individual rastreável: arquivo `CONTRIBUTORS.md` por instância, com seções nomeadas e datadas; `author`/`contributors` podem referenciar uma seção via `@nome-da-secao`. Escopado só a conteúdo migrado — documento novo sempre usa autor pessoa real. Ver `decisions/0006-creditos-de-contribuicao.md`.

## [1.0.0] — 2026-07-27

Versão inicial pública da metodologia.

### Adicionado
- `SPEC.md` — schema de frontmatter unificado (`type`, `category`, `temporality`, `ttl`, `context_anchor`, `related`, `visibility`, `author`/`owner`, entre outros), mecanismo de Registry para `related` cross-repositório, distinção entre Decision Record e `type: decision`, invariantes e hierarquia de precedência do agente.
- `GETTING-STARTED.md` — guia prático de adoção.
- `DISCLAIMER.md` — escopo, limites e cenários recomendados/não recomendados.
- `MIGRATIONS.md` — estrutura pronta para os futuros saltos MAJOR.
- `decisions/` — Decision Records fundacionais (licenciamento, arquitetura multi-repositório, naming, sintaxe de alias, `category` vs. `type: framework`).
- `docs/FUNDAMENTOS.md` — introdução a git/GitHub para quem nunca usou, com paralelo a Obsidian e checklist de privacidade.
- `NOTICE` — carve-out de marca do nome "Hipocampo", complementar à LICENSE Apache-2.0.
