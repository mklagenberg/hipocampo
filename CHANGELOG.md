# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

## [Não lançado]

Trabalho acumulado em `main`, ainda sem tag/release publicada — ver `decisions/0021-politica-de-cadencia-de-release.md`. Vira uma seção versionada de verdade quando a release for cortada.

### Adicionado
- SPEC.md, seção 5-B: **frontmatter audit** — ritual determinístico (script, não julgamento de IA), cadência recomendada diária, roda antes da REM, produz `meta/fila-de-manutencao.md`. Ver `decisions/0017-frontmatter-audit-ritual-deterministico.md`.
- SPEC.md, seção 5-C: **auditoria estrutural semanal** — atomicidade, posicionamento, e verificação de vazamento de dado sensível contra a política por tipo de instância (primeiro mecanismo de enforcement da DR0009). Ver `decisions/0019-auditoria-estrutural-semanal.md`.
- SPEC.md, seção 11: **AGENTS.md como arquivo canônico de instrução**, `CLAUDE.md` vira ponteiro fino. `AGENTS.md` também passa a declarar o **tipo de instância** (`corporativa`/`pessoal`), critério do qual variante da política de dados sensíveis (seção 2-A) se aplica ao repositório — nunca mais inferido pelo agente. Ver `decisions/0015-agents-md-arquivo-canonico-instrucao.md` e `decisions/0022-tipo-de-instancia-declarado-no-agents-md.md`.
- SPEC.md, seção 12: **identidade de autor multi-conta** — registro de contas de git equivalentes ao mesmo `author`, e regra de direção de convite (pessoal convida profissional pro second brain pessoal, nunca o inverso). Ver `decisions/0020-identidade-autor-multi-conta.md`.
- SPEC.md, seção 9: **critério operacional de escopo SemVer** — teste concreto pra classificar MAJOR/MINOR/PATCH ("quebra ou só fica atrasado?"), em vez de julgamento solto. Ver `decisions/0023-criterio-operacional-escopo-semver.md`.
- **`UPGRADE.md`** (novo) — checklist cumulativa e idempotente de atualização de instância: o que uma instância deveria ter, hoje, pra estar aderente à versão atual, não importa de qual versão antiga ela partiu. Diferente do `MIGRATIONS.md` (só saltos MAJOR). Exercitado contra um caso hipotético (instância parada em v1.3.0) e validado contra os 4 repositórios de conteúdo reais do Mau. Ver `decisions/0024-upgrade-md-checklist-cumulativa.md`.
- **`decisions/0025-skill-client-side-nunca-por-repositorio.md`** — a skill roda sempre no ambiente de IA de quem opera, por pessoa, nunca por repositório. A pasta `skill/` que todo repositório de conteúdo herdava do "Use this template" nunca teve efeito funcional (nenhum agente ativa uma skill automaticamente a partir de um arquivo num repositório) — deixa de fazer parte do escopo esperado de uma instância. Levantado por Mau ao questionar a arquitetura diretamente.
- `decisions/0016-memoria-curto-prazo-sanitizacao.md` — refina o modelo de camadas de memória (DR0008): curto prazo é estágio de sanitização (atomicidade, posicionamento), não só captura bruta; cada repositório tem seu próprio `inbox/`.
- `decisions/0018-validacao-frontmatter-tempo-de-leitura.md` — extensão da mecânica CRUD/READ (DR0012): toda leitura valida frontmatter contra a norma, sinaliza `ttl` vencido e sugere revalidação por pesquisa quando aplicável.
- `decisions/0021-politica-de-cadencia-de-release.md` — acumular trabalho antes de cortar release, hotfix/PATCH pra urgência genuína.
- `decisions/0022-tipo-de-instancia-declarado-no-agents-md.md` — fecha uma assimetria na auditoria estrutural (DR0019): a função de vazamento de dado sensível estava ancorada só na política genérica (seção 2-A), sem dizer onde o tipo de instância que a política referencia é declarado. Agora está explicitamente no `AGENTS.md`, mesmo artefato que já ancorava a função de posicionamento.
- `decisions/0023-criterio-operacional-escopo-semver.md` — ver acima.
- `decisions/0024-upgrade-md-checklist-cumulativa.md` — ver acima.

### Alterado
- SPEC.md, seção 5-A: ritual REM ganha segunda função ("atualizar memórias antigas", processando a fila do frontmatter audit) e cadência recomendada diária.
- SPEC.md, seção 2-B: READ agora inclui validação de frontmatter em tempo real, não só leitura frontmatter-first.
- SPEC.md, seção 2-A: nova frase de fechamento apontando pro campo "tipo de instância" do `AGENTS.md` como critério de qual variante da política se aplica (DR0022).
- SPEC.md, seção 5-C: função 3 (vazamento de dado sensível) reescrita pra citar o mesmo campo "tipo de instância" do `AGENTS.md`, no mesmo padrão já usado pela função 2 (posicionamento).
- SPEC.md, seção 9: reescrita — critério operacional de escopo (DR0023), regra de tag + Release sempre publicados juntos (fecha a assimetria real da v1.3.0, que tem tag sem Release), e rotina de release expandida pra incluir a atualização do `UPGRADE.md` (DR0024).
- SPEC.md, seção 11: nota final apontando pro `UPGRADE.md` como checklist completo de migração `CLAUDE.md` → `AGENTS.md`.
- `UPGRADE.md`: novo item obrigatório — repositório de conteúdo não tem pasta `skill/` própria (DR0025).
- Corrigido o cabeçalho de versão do SPEC.md, que estava desatualizado em "1.6.0" (não acompanhava os releases v1.7.0-v1.9.0, que não alteraram o SPEC.md em si) — agora reflete a versão atual, 1.9.0 + não lançado.

## [1.9.0] — 2026-07-29

### Adicionado
- `docs/FAQ-E-ERROS-COMUNS.md` — erros de instanciação já encontrados de verdade (skill não instalada pelo template, LICENSE herdado incorretamente, `CLAUDE.md` desatualizado, permissão de org, migração por cópia direta) e perguntas frequentes (apagamento físico, outage de produto de IA, necessidade da skill, licença metodologia vs. conteúdo, detecção de release nova, git host alternativo, visibilidade esquecida).

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
