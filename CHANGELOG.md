# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

## [1.8.0] — 2026-07-29

### Adicionado
- `docs/FUNDAMENTOS.md` — passo a passo concreto de "Use this template" (onde clicar, o que preencher), pra quem nunca usou GitHub.
- `docs/USO-MULTI-FERRAMENTA.md` — princípio comum de uso do Hipocampo (MCP do GitHub) e especificidades por ferramenta: Claude (Cowork, Code, API/Desktop), ChatGPT, Gemini, GitHub Copilot, Antigravity.

## [1.7.0] — 2026-07-29

### Adicionado
- `docs/MODELOS-DE-IA.md` — referência sobre o que importa (e o que não importa) num modelo/produto de IA pra operar o Hipocampo bem: janela de contexto e frontmatter-first, natureza probabilística das rotinas, MCP do GitHub como denominador comum entre ferramentas.
- `docs/PERFORMANCE-E-GRAFO.md` — como o modelo de retrieval/grafo do Hipocampo funciona, e comparação explícita com o OKF (Open Knowledge Format) da Google, publicado em junho de 2026.

### Alterado
- `GETTING-STARTED.md` — nova seção 0 com ordem de leitura recomendada pra quem está aprendendo a metodologia pela primeira vez; passo de instanciação atualizado com a troca de LICENSE (herdado incorretamente como Apache-2.0) e a personalização/instalação da skill real (`hipocampo-toolkit/skill/SKILL.md`); referências à skill "stub" removidas.

## [1.6.0] — 2026-07-29

### Adicionado
- Rotina obrigatória a cada release da metodologia (SPEC.md, seção 9): checagem de necessidade de migração (mesmo que a conclusão seja "nenhuma ação necessária") e sincronização do `hipocampo-toolkit` (CLAUDE.md e demais arquivos afetados). Primeira execução retroativa desta rodada: `hipocampo-toolkit/CLAUDE.md` corrigido de "^1.0.0" (desatualizado havia cinco releases) para "^1.5.0", e adicionados templates de LICENSE pros perfis pessoal/corporativo em `hipocampo-toolkit/license-templates/`, corrigindo a herança indevida do Apache-2.0 da metodologia em repositórios de conteúdo recém-instanciados. Ver `decisions/0014-rotina-obrigatoria-de-release.md`.

## [1.5.0] — 2026-07-29

### Adicionado
- Seção 2-B no SPEC.md: mecânica CRUD nomeada explicitamente (Create/Read/Update/Delete mapeados ao ciclo de vida já existente) e regra de leitura frontmatter-first para agentes (frontmatter primeiro, corpo completo só quando necessário — economia de tokens). Ver `decisions/0012-mecanica-crud-frontmatter-first.md`.
- Seção 10 no SPEC.md: migração de conteúdo pré-existente nunca copia arquivo direto — frontmatter sempre reescrito conforme o schema vigente, corpo ajustado conforme atomicidade/nomenclatura/privacidade vigentes. Ver `decisions/0011-migracao-nunca-copia-arquivo-direto.md`.
- Novo princípio no DISCLAIMER.md: dados de qualquer instância sempre human-readable (markdown + git), independente de produto de IA específico estar no ar. Ver `decisions/0013-dados-sempre-human-readable.md`.

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
