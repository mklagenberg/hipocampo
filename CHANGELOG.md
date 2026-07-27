# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

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
