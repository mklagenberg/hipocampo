# hipocampo

Metodologia de second brain agêntico: git + markdown + rituais de IA. Este repositório é spec e ferramental — nunca guarda conteúdo real de nenhuma instância.

- [SPEC.md](SPEC.md) — especificação normativa: schema de frontmatter, regras de retrieval, versionamento.
- [GETTING-STARTED.md](GETTING-STARTED.md) — guia prático de adoção.
- [DISCLAIMER.md](DISCLAIMER.md) — o que a metodologia é e não é, cenários recomendados e não recomendados.
- [BEST-PRACTICES.md](BEST-PRACTICES.md) — boas práticas de uso: do dia a dia, postura de privacidade/compliance, e adoção por times/empresas novas.
- [MIGRATIONS.md](MIGRATIONS.md) — guia de migração por salto MAJOR de versão.
- [CHANGELOG.md](CHANGELOG.md) — histórico de versões da metodologia.
- [ROADMAP.md](ROADMAP.md) — direção atual, sem compromisso de data.
- [decisions/](decisions/) — Decision Records: por que cada regra estrutural é o que é.
- [skill/SKILL.md](skill/SKILL.md) — skill operacional da metodologia (fonte canônica genérica; cada pessoa instala e personaliza sua própria cópia).
- [scaffold/README.md](scaffold/) — mecanismo declarativo de instanciação de repositórios de conteúdo novos (profiles, esqueleto de arquivos, templates de LICENSE).
- [docs/FUNDAMENTOS.md](docs/FUNDAMENTOS.md) — introdução a git/GitHub pra quem nunca usou, com paralelo a Obsidian e checklist de privacidade.
- [docs/MODELOS-DE-IA.md](docs/MODELOS-DE-IA.md) — o que importa num modelo/produto de IA pra operar o Hipocampo bem.
- [docs/PERFORMANCE-E-GRAFO.md](docs/PERFORMANCE-E-GRAFO.md) — como o retrieval/grafo funciona, e a relação com o OKF da Google.
- [docs/USO-MULTI-FERRAMENTA.md](docs/USO-MULTI-FERRAMENTA.md) — princípio comum e especificidades de uso em Claude, ChatGPT, Gemini, Copilot, Antigravity.
- [docs/FAQ-E-ERROS-COMUNS.md](docs/FAQ-E-ERROS-COMUNS.md) — erros de instanciação já encontrados de verdade e perguntas frequentes.

Para instanciar um repositório de conteúdo a partir desta metodologia, peça pro agente que opera sua cópia da skill Hipocampo pra executar o scaffold declarado em [scaffold/](scaffold/) — não existe mais um botão "Use this template" separado (o antigo `hipocampo-toolkit` foi consolidado aqui, `decisions/0032`). Procedimento operacional completo: [skill/references/instanciacao.md](skill/references/instanciacao.md).

Agentes devem começar por [AGENTS.md](AGENTS.md).

## Adequação ao MODA

<!-- moda:disclosure:start -->
Este repositório está sendo avaliado e adequado ao [MODA](https://github.com/mklagenberg/moda) — um framework aberto para organizar, desenhar, auditar, empacotar e evoluir metodologias agênticas.

- Perfil de artefato: `methodology`
- Compatibilidade MODA: `^1.0.0`
- Relação de adoção: `audited_against` (retrospectiva) — evoluindo pra `conforms_to` conforme os achados da auditoria forem endereçados
- Manifesto: [`moda.yaml`](moda.yaml)
- Perfil de conformidade: [`conformance/moda.yaml`](conformance/moda.yaml)
- Última auditoria: [`audits/moda/2026-08-17-v1.0.0-self-audit.md`](audits/moda/2026-08-17-v1.0.0-self-audit.md)
<!-- moda:disclosure:end -->

Versão atual: **1.9.0** ([SemVer](https://semver.org/lang/pt-BR/)).
