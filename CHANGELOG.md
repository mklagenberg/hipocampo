# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

## [1.4.0] — 2026-07-29

### Adicionado
- `BEST-PRACTICES.md` — guia de boas práticas de uso da metodologia, em tom acessível: operação do dia a dia, postura de privacidade/compliance, e adoção por times/empresas novas.
- Exceção formal e estreita ao Invariante 3 (SPEC.md, seção 8): apagamento físico do conteúdo pessoal específico é permitido quando acionado por uma solicitação legítima de eliminação de dado pessoal (LGPD Art. 16 / GDPR Art. 17), sempre com decisão humana explícita e substituição por um registro mínimo do fato ("tombstone"). Ver `decisions/0010-excecao-apagamento-obrigacao-legal.md`.

## [1.3.0] — 2026-07-28

### Adicionado
- Seção 2-A no SPEC.md: política de dados sensíveis por tipo de instância. Instância corporativa nunca armazena contrato/NDA, avaliação de desempenho, anotação de saúde, dado pessoal (senha, endereço/contato pessoal, nome de parente), ou valor de salário/fornecedor/projeto — exceto valor de resultado de negócio num `type: case`. Nome completo, cargo e contato profissional são permitidos com citação de ano. Detalhe técnico de vulnerabilidade/exploração ativa nunca é registrado verbatim, em nenhuma instância. Ver `decisions/0009-politica-de-privacidade-por-instancia.md`.

## [1.2.0] — 2026-07-28

### Adicionado
- Seção 5-A no SPEC.md: ritual REM e modelo de quatro estações de memória (sensorial → gate de atenção → curto prazo → consolidação REM → longo prazo), capacidade opcional por instância. Formaliza como um item novo (captura bruta) entra no sistema e vira documento consolidado — complementa a seção 5 (que trata de como um documento já existente envelhece). Ver `decisions/0008-ritual-rem-e-camadas-de-memoria.md`.

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
