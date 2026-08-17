# Hipocampo — Changelog

Histórico de versões da metodologia em si. Segue [SemVer](https://semver.org/lang/pt-BR/) — ver SPEC.md, seção 9.

## [Não lançado]

Trabalho acumulado em `main`, ainda sem tag/release publicada — ver `decisions/0021-politica-de-cadencia-de-release.md`. Vira uma seção versionada de verdade quando a release for cortada.

### Adicionado
- **`scaffold/`** (novo) — mecanismo de instanciação de vaults consolidado a partir do antigo repositório `hipocampo-toolkit`, como scaffold declarativo conforme MODA (`docs/composition-scaffolding-and-distribution.md`): dois profiles por domínio (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`, com `tier` como input), `scaffold/skeleton/` com o conteúdo-fonte de cada output, `scaffold/license-templates/` migrado sem alteração de conteúdo jurídico. Ver `decisions/0032-consolidacao-toolkit-em-scaffolding.md`.
- **`skill/`** (migrado pra dentro de `hipocampo`) — a skill operacional da metodologia, antes hospedada só em `hipocampo-toolkit`, agora vive em `hipocampo/skill/` (`SKILL.md` + `references/crud-frontmatter.md`, `invariantes.md`, `personalizacao.md`, `rotinas.md`, e o novo `references/instanciacao.md`). A pasta `skill/` deixa de ser copiada pra dentro de repositórios de conteúdo novos — nunca teve efeito funcional ali (`decisions/0025`).
- **`skill/manifest.yaml`** (novo) — manifesto de máquina da skill, seguindo o padrão `skill-manifest.yaml` do MODA, adaptado honestamente: sem versão independentemente empacotada/distribuída ainda (só a cópia pessoal client-side, `decisions/0025`).
- **`skill/references/instanciacao.md`** (novo) — procedimento completo de instanciação agent-driven de um vault novo: escolha de profile, coleta de inputs, apresentação do plano antes de escrever (invariante 5), geração dos outputs, comportamento em conflito.
- **`hipocampo.yaml`** (novo formato, por vault) — manifesto machine-readable que todo vault gerado pelo scaffold passa a carregar na raiz: proveniência (profile, commit-fonte, versão do engine), `instance.domain`/`instance.tier`, `state`. Ver `decisions/0033-manifesto-hipocampo-yaml-por-vault.md`. Divergência de vocabulário entre `instance.domain` (`pessoal`/`empresa`) e o campo "Tipo de instância" do `AGENTS.md` (`pessoal`/`corporativa`) é registrada como pendência conhecida, não harmonizada nesta fase.
- **`changes/0032-0033-scaffolding-e-manifesto-vault/`** (novo) — Change Set prospectivo cobrindo `decisions/0032` e `decisions/0033`, primeiro exercício do mecanismo (`decisions/0031`) fora do modo backfill.
- `moda.yaml`: componente `personal-skill` passa de lifecycle `independent` (hospedado em `hipocampo-toolkit`) pra `embedded`; novos componentes `vault-scaffold` e `vault-manifest`; novos pacotes locais `skill` e `scaffold` em `packages`.
- `conformance/moda.yaml`: controle `packaging_and_synchronization` reavaliado à luz do `skill/manifest.yaml` e do `hipocampo.yaml` por vault (segue `partial` — nenhum vault real existente foi retroativamente atualizado ainda); controle `specification_driven_change_control` ganha segunda evidência (Change Set prospectivo, não só backfill); controles `distribution_of_agency`, `contracts` e `repository_contract` ganham evidência nova referente ao scaffold.
- `README.md`, `GETTING-STARTED.md` (seções 1 e 2), `UPGRADE.md`: todos os pontos de referência a `hipocampo-toolkit` atualizados pra apontar pro `scaffold/` consolidado; `GETTING-STARTED.md` seção 2 reescrita do zero pro modelo agent-driven (sem botão "Use this template"); `UPGRADE.md` ganha itens novos de checklist (`hipocampo.yaml`, `skill/manifest.yaml`, divergência de vocabulário `domain`/"Tipo de instância").
- **`docs/change-management.md`** (novo) — mecanismo de Change Set adotado do MODA e adaptado ao vocabulário do Hipocampo: classes `editorial`/`operational`/`normative`, estrutura `changes/<change-id>/` (`proposal.md` + `impact.yaml`), tabela de gatilhos própria. Passa a ser obrigatório pra mudança `operational`/`normative` a partir de agora. Ver `decisions/0031-mecanismo-de-change-set.md`.
- **`changes/0026-0028-taxonomia-fato-relato-opiniao-e-ciclo-de-vida/`** (novo) — Change Set retroativo (backfill) do PR #22, primeiro exercício de validação do template.
- **`moda.yaml`** (novo, raiz) — declaração formal de conformidade retrospectiva com o [MODA](https://github.com/mklagenberg/moda): `relationship: audited_against`, `adoption_mode: retrospective`, `claim_stage: mapped`, `conformance_result: partial`. Primeiro artefato da adequação da metodologia ao MODA rumo à v2.0.0.
- **`conformance/moda.yaml`** (novo) — mapeamento controle-a-controle contra as dimensões de design do MODA (SPEC MODA, seção 4) e o contrato de repositório (seção 5), refletindo os achados da auditoria de 2026-08-17.
- **`audits/moda/2026-08-17-v1.0.0-self-audit.md`** (novo) — auditoria de conformidade MODA congelada como evidência imutável.
- **`AGENTS.md`** (novo, raiz) — entry point de agente pra contribuição na metodologia em si, distinto do `AGENTS.md` que cada instância de conteúdo usa pra si mesma (SPEC.md, seção 11). Fecha achado major 2 da auditoria.
- **`ROADMAP.md`** (novo, raiz) — direção por resultado, sem duplicar backlog (`decisions/`) nem changelog. Fecha achado major 3 da auditoria.
- `README.md`: disclosure MODA (seção 5.1 do SPEC MODA) — perfil de artefato, compatibilidade, relação de adoção, links pro manifesto/perfil de conformidade/auditoria.
- SPEC.md, seção 2-C (nova): **taxonomia de tipo de repositório** — dois eixos ortogonais, domínio de titularidade (`pessoal`/`empresa`, já em uso via `decisions/0002`) e tier de exposição (`confidencial`/`público`), mapeando sem repositório novo aos quatro repositórios de conteúdo reais. Novo campo de frontmatter `curation_status` (seção 2), relevante só em repositório `empresa-confidencial` — `staged` (candidato a promoção futura) ou `permanent` (default). Ver `decisions/0029-taxonomia-tipo-de-repositorio.md`.
- SPEC.md, seção 13 (Promote): generalizada pra cobrir também graduação dentro do mesmo domínio de titularidade (documento `empresa-confidencial` com `curation_status: staged` sendo promovido pra `empresa-público`), sempre pelo caminho elegante — o caminho literal continua exclusivo do caso cross-domain, porque só ali há transferência de titularidade real em jogo. Ver `decisions/0030-promote-graduacao-mesmo-dominio.md`.
- SPEC.md, seção 2: campos `contributors` (adicionado à listagem central do schema — já existia via `decisions/0006`, mas nunca aparecia na listagem principal) e `contains_subjective_content` (novo, relevante só quando `owner` preenchido). Taxonomia de quatro tipos de informação — **Fato**, **Relato**, **Opinião**, **Lembrança** — usada como rótulo inline em documento misto; `contains_subjective_content` cobre só Opinião/Lembrança, as duas categorias com risco de responsabilização pessoal. `@handle` inline só quando há mais de um contribuidor. Grava Opinião/Lembrança nova em instância corporativa só mediante confirmação explícita do usuário — sem isso, vai pra instância pessoal. Aplica-se também à função de consolidação do ritual REM (seção 5-A) e à ação Promote (seção 13). Ver `decisions/0026-relato-vs-opiniao-em-instancia-corporativa.md`.
- SPEC.md, seção 13 (nova): **Promote, Depromote, Redbutton** — ações de ciclo de vida cross-repositório. Promote (pessoal → corporativo) com dois caminhos (derivação elegante via `decisions/0011`, ou transferência literal com aviso explícito de titularidade per `decisions/0007`); Depromote (descida de nível dentro do mesmo domínio de titularidade); Redbutton (remediação de violação da política 2-A). `superseded_by` (seção 2/6) passa a aceitar sintaxe `$alias:` cross-repositório. Ver `decisions/0027-promote-depromote-redbutton.md`.
- SPEC.md, seção 8: gatilho da exceção ao invariante 3 (`decisions/0010`) ampliado pra também cobrir violação da política 2-A identificada por auditoria estrutural ou pelo operador, sem exigir solicitação formal do titular. Ver `decisions/0028-gatilho-ampliado-remediacao-2a.md`.
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
- `decisions/0026-relato-vs-opiniao-em-instancia-corporativa.md` — ver acima.
- `decisions/0027-promote-depromote-redbutton.md` — ver acima.
- `decisions/0028-gatilho-ampliado-remediacao-2a.md` — ver acima.
- `decisions/0029-taxonomia-tipo-de-repositorio.md` — ver acima.
- `decisions/0030-promote-graduacao-mesmo-dominio.md` — ver acima.
- `decisions/0031-mecanismo-de-change-set.md` — ver acima.
- `decisions/0032-consolidacao-toolkit-em-scaffolding.md` — ver acima.
- `decisions/0033-manifesto-hipocampo-yaml-por-vault.md` — ver acima.

### Alterado
- SPEC.md, seção 5-A: ritual REM ganha segunda função ("atualizar memórias antigas", processando a fila do frontmatter audit) e cadência recomendada diária.
- SPEC.md, seção 2-B: READ agora inclui validação de frontmatter em tempo real, não só leitura frontmatter-first.
- SPEC.md, seção 2-A: nova frase de fechamento apontando pro campo "tipo de instância" do `AGENTS.md` como critério de qual variante da política se aplica (DR0022).
- SPEC.md, seção 5-C: função 3 (vazamento de dado sensível) reescrita pra citar o mesmo campo "tipo de instância" do `AGENTS.md`, no mesmo padrão já usado pela função 2 (posicionamento).
- SPEC.md, seção 9: reescrita — critério operacional de escopo (DR0023), regra de tag + Release sempre publicados juntos (fecha a assimetria real da v1.3.0, que tem tag sem Release), e rotina de release expandida pra incluir a atualização do `UPGRADE.md` (DR0024).
- SPEC.md, seção 11: nota final apontando pro `UPGRADE.md` como checklist completo de migração `CLAUDE.md` → `AGENTS.md`.
- `UPGRADE.md`: novo item obrigatório — repositório de conteúdo não tem pasta `skill/` própria (DR0025); e, nesta rodada, itens novos de manifesto `hipocampo.yaml`, `skill/manifest.yaml` e divergência de vocabulário (DR0033); caminhos `hipocampo-toolkit/*` corrigidos pra `scaffold/*` (DR0032).
- Corrigido o cabeçalho de versão do SPEC.md, que estava desatualizado em "1.6.0" (não acompanhava os releases v1.7.0-v1.9.0, que não alteraram o SPEC.md em si) — agora reflete a versão atual, 1.9.0 + não lançado.
- `README.md`, `GETTING-STARTED.md`: pontos de referência a `hipocampo-toolkit` (instanciação via "Use this template", caminho da skill genérica) reescritos pro modelo agent-driven baseado em `scaffold/` (DR0032).

### Removido
- Referência ao repositório `hipocampo-toolkit` como template GitHub separado — consolidado dentro de `hipocampo` (`scaffold/` + `skill/`). O repositório em si é arquivado no GitHub como ação manual (nenhuma ferramenta disponível neste processo automatiza esse passo), recebendo antes um aviso de redirecionamento no próprio `README.md` dele.

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
