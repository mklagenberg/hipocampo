# Hipocampo — SPEC

Versão: 1.9.0 · Segue [SemVer](https://semver.org/lang/pt-BR/)

Este documento é a especificação normativa da metodologia Hipocampo: o schema de frontmatter, as regras de retrieval e as convenções que qualquer instância (repositório de conteúdo) precisa seguir para ser considerada compatível com uma versão do Hipocampo. Não é um manual de uso — para isso, ver [GETTING-STARTED.md](GETTING-STARTED.md). Não é um documento de limitações — para isso, ver [DISCLAIMER.md](DISCLAIMER.md). Não é um guia de boas práticas — para isso, ver [BEST-PRACTICES.md](BEST-PRACTICES.md).

## 1. Escopo

Hipocampo é uma metodologia de second brain agêntico: git + markdown + rituais de IA. Este repositório (`hipocampo`) e o `hipocampo-toolkit` são os únicos dois repositórios públicos da metodologia — carregam spec e ferramental, nunca conteúdo real. Toda base de conhecimento que implementa o Hipocampo vive em repositórios privados, sem exceção (ver invariantes, seção 8).

## 2. Frontmatter — schema unificado

Todo documento de uma instância Hipocampo é um arquivo `.md` com este frontmatter YAML:

```yaml
---
title: ""
date: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
source: "url | conversa | interno"
tags: []
type: "note | reference | decision | project | person | case | framework | company"
category: ""                      # opcional, só quando a área já tem subpasta física por tema
temporality: "evergreen | ephemeral | contextual | historical"
ttl: "YYYY-MM-DD"                 # sempre data concreta — nunca o literal "evergreen"
context_anchor: ""                # obrigatório só quando temporality: contextual
status: "draft | active | stale | archived | superseded"
related: []                       # "path/local.md" ou "$alias:path.md"
superseded_by: ""
revision: 1
revision_note: ""
visibility: "public | internal | confidential | restricted"
author: "Nome Real - @usuario-github"    # sempre pessoa, nunca a IA — ou @nome-da-secao de CONTRIBUTORS.md, só em conteúdo histórico (ver decisions/0006)
owner: ""                                 # nome da empresa, só quando nasce em contexto de trabalho
license: ""                               # sempre derivado de `visibility`, nunca preenchido à mão (ver decisions/0007)
---
```

### title, date, updated, source, tags
Uso descritivo padrão. `source` diferencia conhecimento que entrou por pesquisa externa (`url`), por diálogo (`conversa`) ou produzido internamente (`interno`).

### status
Ciclo de vida do documento: `draft` (ainda não é conhecimento consolidado) → `active` (em uso) → `stale` (sinalizado pela rotina de staleness, precisa revisão) → `archived` (retirado de circulação, mas preservado) → `superseded` (substituído por outro documento, ver `superseded_by`). Documento nunca é apagado fisicamente — só transita para `archived` ou `superseded` (invariante, ver seção 8).

### revision, revision_note
Cada edição de conteúdo (não wording trivial) incrementa `revision` e registra o motivo em `revision_note`. Histórico de por quê o documento mudou, não só quando.

### visibility
Resolve **só** quem, já tendo acesso ao repositório, pode usar o conteúdo sem restrição adicional: `public` (sem restrição, inclusive fora do repo), `internal` (uso interno da organização dona do repo), `confidential` (uso restrito a quem precisa saber, mesmo dentro do repo), `restricted` (uso individualizado, caso a caso). `visibility` **nunca decide exposição à internet** — isso é resolvido estruturalmente pela regra de que nenhum repositório de conhecimento é público (invariante, seção 8). Uma etiqueta `confidential` num repositório que o time inteiro acessa não impede ninguém desse time de ler o arquivo — permissão real do GitHub é granularidade de repositório, não de arquivo dentro de um repositório compartilhado. Conteúdo que precisa de enforcement técnico de fato vai para um repositório separado com permissão de acesso restrita, não para uma etiqueta `visibility` dentro de um repositório mais aberto.

### author / owner
`author` é sempre uma pessoa (`Nome Real - @usuario-github`), nunca a IA — mesmo quando um agente escreve o texto sob direção de alguém, o autor é quem dirigiu. Campo obrigatório em qualquer documento, qualquer `visibility`. Exceção escopada só a conteúdo histórico/migrado, sem autoria individual rastreável na origem: `author`/`contributors` podem referenciar uma seção nomeada e datada de um arquivo `CONTRIBUTORS.md` via `@nome-da-secao`, em vez de uma pessoa — documento novo nunca usa essa exceção (ver `decisions/0006-creditos-de-contribuicao.md`). `owner` é sempre o nome de uma empresa, preenchido só quando o documento nasce em contexto de trabalho — ver a distinção completa de papéis e o que cada um pode fazer com o conteúdo no `DISCLAIMER.md` e nos Decision Records de licenciamento em `decisions/`. Ver também seção 12 para o caso de uma pessoa operar mais de uma conta de git.

### license
Sempre derivado mecanicamente de `visibility`, nunca definido à mão — evita divergência entre a camada de confidencialidade (`visibility`) e a camada jurídica (`license`). Usa o padrão SPDX `LicenseRef-<idstring>`, com o texto legal completo no arquivo `LICENSE` da raiz do repositório, nunca reescrito por documento. Ver `decisions/0007-licenciamento-repos-de-conteudo.md`.

## 2-A. Política de dados sensíveis por tipo de instância

Instância corporativa (`owner` preenchido com o nome de uma organização) nunca armazena, em nenhum nível de `visibility` — mesmo `restricted`: conteúdo de contrato ou NDA; avaliação de desempenho de indivíduo identificável; anotação de saúde de qualquer pessoa (titular da instância ou terceiro); dado pessoal (senha, endereço pessoal, telefone ou e-mail pessoal, nome de parente); valor de salário, valor pago a fornecedor, ou valor de projeto/contrato. Exceção única pra valor absoluto: resultado de negócio entregue a um cliente num `type: case` (receita gerada, custo evitado) é o próprio produto do case, não exposição financeira interna. Aprendizado interno quantificado (ex.: economia de processo) é registrado como variação percentual, nunca valor absoluto.

Dado financeiro sobre terceiro que não é fornecedor/parceiro comercial direto (ex.: inteligência de mercado sobre concorrente, extraída de fonte pública) não é abrangido por essa restrição — desde que a fonte pública seja citada explicitamente no documento.

Nome completo, cargo, e-mail profissional, telefone ou endereço profissional — de colega ou de contato de cliente — são permitidos em instância corporativa, sempre acompanhados de citação de ano/data: o registro é uma fotografia datada, nunca um estado presumido atual.

Questão pessoal de qualquer indivíduo (saúde, situação financeira pessoal) nunca vai pra instância corporativa — sempre pra instância pessoal do titular relevante, se existir uma.

Detalhe técnico de vulnerabilidade ou exploração ativa (payload de ataque, query/dork que revela o comprometimento, credencial, endpoint explorável) nunca é registrado verbatim, em nenhuma instância, mesmo confidencial/restricted — registra-se o fato (existência da falha, categoria, data do achado) e a resposta dada, nunca o material que reproduziria ou confirmaria o ataque.

Quando um documento inteiro depende estruturalmente de um tipo de dado banido (não dá pra adaptar removendo só o trecho problemático), o agente não decide sozinho entre publicar mesmo assim ou descartar — sinaliza a violação ao humano responsável pela instância e aguarda decisão explícita. Ver `decisions/0009-politica-de-privacidade-por-instancia.md`. A auditoria estrutural semanal (seção 5-C) é o mecanismo periódico que verifica o cumprimento desta política.

## 2-B. Mecânica CRUD e leitura frontmatter-first

O ciclo de vida do documento (seção 2, campo `status`) implementa as quatro operações de um CRUD: **Create** (criação com frontmatter completo), **Read** (consulta por agente ou humano), **Update** (edição de conteúdo com incremento de `revision`), **Delete** (mitigado pelo invariante 3 — nunca apagar fisicamente, só `archived`/`superseded`, com exceção estreita da `decisions/0010`). Ver `decisions/0012-mecanica-crud-frontmatter-first.md`.

Regra de leitura recomendada ao agente: ao operar sobre múltiplos documentos (busca, triagem, staleness), ler sempre o **frontmatter primeiro** — YAML, custo de token baixo, suficiente pra filtrar por `type`, `tags`, `status`, `temporality`, `related` e decidir relevância. Só ler o **corpo completo** depois de decidir, pelo frontmatter, que aquele documento específico precisa de leitura completa. Numa instância com muitos documentos, isso evita custo de token desnecessário — ler o corpo inteiro de todo candidato só pra descartar a maioria não é o padrão de acesso default.

Além disso, toda operação de READ inclui uma validação leve do frontmatter contra a norma desta seção 2 e a checagem de staleness da seção 5 — independente de o frontmatter audit (seção 5-B, ritual em lote) já ter passado por aquele documento especificamente. Se a validação encontrar problema, o agente sinaliza explicitamente o que está errado e o que precisa ser feito; no caso de `ttl` vencido, deixa claro que a informação é defasada e sugere revalidação por pesquisa quando o documento for `source: url`. Esta validação nunca altera `status` ou qualquer campo sozinha — só sinaliza. Ver `decisions/0018-validacao-frontmatter-tempo-de-leitura.md`.

## 3. `type` — enum e critério de expansão

| Valor | Uso |
|---|---|
| `note` | observação atômica que não é nenhum dos outros |
| `reference` | conceito despersonalizado e reutilizável (absorve o que seria "generic") |
| `decision` | decisão de conteúdo/arquitetura de uma instância específica — distinto do Decision Record da metodologia, ver seção 7 |
| `project` | iniciativa em andamento |
| `person` | pessoa nomeada |
| `company` | empresa nomeada (cliente, parceiro, concorrente, a própria empresa) |
| `case` | case de cliente/trabalho entregue, com resultado quantificado |
| `framework` | metodologia sujeita a regime de autoria/titularidade (ver DISCLAIMER.md) |

`context` foi avaliado e descartado como valor de `type` — sobreposição grande com `reference`/`company`. Quando fizer sentido, vira tag (`contexto`), não classificação de retrieval.

**Regra de expansão:** só criar um valor novo de `type` quando houver massa crítica de documentos que não encaixam em nenhum valor existente — o mesmo princípio que já se aplica às subpastas de `category` (seção 4). Um enum pequeno e sem sobreposição é o que sustenta a melhora de retrieval que motiva ter `type` como campo estruturado.

## 4. `category`

Campo opcional, string livre. Só é preenchido quando a área temática já acumulou massa crítica de documentos a ponto de justificar uma subpasta física dedicada — não é obrigatório desde o primeiro documento de um tema.

**`category: frameworks` e `type: framework` coexistem e não são redundantes.** São eixos diferentes: `category` é sobre onde o documento mora fisicamente no repositório (só existe quando a área já tem massa crítica de subpastas); `type: framework` é sobre regime de autoria/titularidade, independente de pasta. Um documento pode ser `type: framework` sem `category: frameworks` — não ter atingido massa crítica pra virar subpasta física não muda o regime de titularidade do conteúdo. Ver `decisions/0005-category-vs-type-framework.md`.

## 5. `temporality` e o ciclo de staleness

Campo ortogonal a `type` — controla como a rotina de staleness (verificação periódica de conhecimento desatualizado) trata cada documento.

| Valor | `ttl` sugerido | Comportamento da rotina de staleness |
|---|---|---|
| `evergreen` | data concreta, longa (+24 meses) | Checagem leve — "ainda é verdade?" |
| `ephemeral` | data concreta, curta (+30 a 90 dias) | Agressiva — vencido sem renovação já entra pré-marcado "sugestão: arquivar/superseder", não só "revisar" |
| `contextual` | data concreta, de segurança (+90 a 180 dias) | Dupla checagem: pelo `ttl` de segurança E pelo status do documento em `context_anchor` — se a âncora mudar para `archived`/`superseded`, o documento contextual é flaggeado imediatamente, independente do `ttl` ainda não ter vencido |
| `historical` | data concreta, irrelevante na prática (pode ser bem longa) | Pulado por completo pela rotina de staleness — só sai desse estado via `superseded_by` |

`ttl` é **sempre uma data concreta**, nunca o literal `"evergreen"` — isso é papel exclusivo de `temporality`. Um documento com `ttl: "evergreen"` no valor do campo é um erro de preenchimento, não uma convenção válida.

`context_anchor` é obrigatório só quando `temporality: contextual`. Usa a mesma sintaxe de `related` (`path.md` local ou `$alias:path.md` cross-repo, ver seção 6), mas é valor único, não lista — precisa ser inequívoco qual documento governa a expiração.

Precedentes: `evergreen`/`ephemeral` seguem Andy Matuschak, "Evergreen notes" (evergreen vs. transient). `contextual` segue a prática de records management (event-based retention vs. time-based retention). `historical` formaliza a convenção já em uso do sufixo "(histórico)" no título.

## 5-A. Ritual REM e camadas de memória

A seção 5 formaliza como um documento *já existente* envelhece. Esta seção formaliza como um item *novo* — captura bruta, ainda não curada — entra no sistema e vira documento consolidado. Capacidade opcional por instância (ver `decisions/0008-ritual-rem-e-camadas-de-memoria.md`, refinada por `decisions/0016-memoria-curto-prazo-sanitizacao.md`).

Três camadas relevantes pro dia a dia:

1. **Memória sensorial** — vive fora de qualquer repositório Hipocampo: a conversa/sessão em si, notas soltas (ex.: Google Keep), documento externo (ex.: Google Drive), arquivo anexado. Nunca versionada em git; alta perda por design.
2. **Memória de curto prazo** — já vive dentro do repositório, em `inbox/`, já passou pelo gate de atenção (ex.: um "check-in"/dump de sessão), mas ainda não é atômica nem está necessariamente no lugar certo. É um estágio de **sanitização**, não só um buffer de captura — precisa de trabalho (dividir por conceito, corrigir `category`/nomenclatura/`visibility`) antes de virar memória de longo prazo.
3. **Memória de longo prazo** — documento atômico, curado, frontmatter completo, corretamente posicionado. Corpo principal de qualquer repositório Hipocampo.

**Ritual REM (consolidação):** cadência recomendada diária, rodando depois do frontmatter audit do mesmo ciclo (seção 5-B). Duas funções:

1. **Consolidar** — ler `inbox/` (memória de curto prazo, nunca a sensorial direto), decidir pra cada item pendente entre virar documento novo, fundir com um existente, ou descartar.
2. **Atualizar memórias antigas** — ler `meta/fila-de-manutencao.md` (produzida pelo frontmatter audit, seção 5-B) e decidir disposição de cada item sinalizado: revalidar (inclusive via pesquisa externa, quando `source: url`), arquivar, superseder, ou corrigir campo.

O plano completo (de qualquer uma das duas funções) é sempre apresentado antes de qualquer execução — mesmo invariante de pedido explícito (seção 8) aplicado a este ritual. Rituais de manutenção operam sempre no escopo de um repositório por vez — cada repositório tem seu próprio `inbox/` e sua própria fila.

Regras adicionais (sem mudança desde a v1.2.0): atomicidade (documento consolidado = um conceito só; material bruto com N ideias vira N documentos); um `memory.md` de harness de agente (satélite pequeno e durável do próprio agente) e um snapshot de transferência (export imutável pra migração) não são memória sensorial nem passam pelo ritual REM — mecanismos distintos, não confundir; evolução de schema é reativa, só cresce por massa crítica (mesmo princípio da seção 4).

## 5-B. Frontmatter audit

Ritual novo, **determinístico** (script, não julgamento de agente de IA) — cadência recomendada diária, rodando antes da consolidação REM do mesmo ciclo (seção 5-A). Varre o frontmatter (nunca o corpo — frontmatter-first, seção 2-B) de todo documento de um repositório, e produz `meta/fila-de-manutencao.md`, listando: `ttl` vencido (por `temporality`, seção 5), campo obrigatório ausente (seção 2), e qualquer outra violação mecanicamente detectável da norma de frontmatter.

Frontmatter audit nunca decide disposição — só relata. Decisão de disposição é sempre da função "atualizar memórias antigas" do ritual REM (seção 5-A), ou de pedido humano explícito. Ver `decisions/0017-frontmatter-audit-ritual-deterministico.md`.

## 5-C. Auditoria estrutural semanal

Ritual novo, cadência recomendada semanal, com três funções: (1) revisar atomicidade de documentos já consolidados; (2) revisar posicionamento — se a estrutura de `category`/pastas ainda faz sentido, se um documento está fora do escopo do repositório onde vive (ver seção 11, escopo declarado no `AGENTS.md`); (3) verificar vazamento de dado sensível contra a política por tipo de instância (seção 2-A). É o primeiro mecanismo periódico de verificação dessa política, que existe como regra desde a v1.3.0 sem nenhuma checagem formal até aqui.

Qualquer achado é sempre apresentado ao humano responsável antes de qualquer ação — mover, dividir ou remover documento nunca acontece sozinho (invariante 5). Ver `decisions/0019-auditoria-estrutural-semanal.md`.

## 6. `related` entre repositórios — o Registry

Um documento em qualquer instância Hipocampo pode referenciar outro documento no mesmo repositório ou em um repositório diferente da mesma pessoa/organização. A sintaxe distingue os dois casos:

- Sem prefixo (`"path/local.md"`) = mesmo repositório.
- Com prefixo `$alias:` (`"$alias:path.md"`) = repositório diferente, resolvido via um arquivo `registry.md`.

`$nome`, não `{{nome}}` — `{{nome}}` corre o risco de ser interpretado como sintaxe de motor de template (Jinja/Mustache) se o arquivo algum dia passar por um pipeline desse tipo; `$` não tem significado especial em YAML puro. Ver `decisions/0004-alias-sintaxe.md`.

`registry.md` mora no repositório menos restrito de cada escopo (por exemplo, o repositório de conceitos de um escopo pessoal, ou o repositório principal de um escopo corporativo). Formato:

```markdown
| Alias | Repositório atual | Válido desde | Nota |
|---|---|---|---|
| $alias-exemplo | dono/repo-atual | YYYY-MM-DD | — |
```

**Nunca editar uma linha existente do registry.** Renomear um repositório = acrescentar linha nova com o nome novo e a data, preservando a linha antiga — o mesmo princípio de `superseded_by` (seção 2), aplicado a nome de repositório em vez de documento.

Um documento `type: framework` isento de titularidade de empresa (ver DISCLAIMER.md) nunca migra entre repositórios — nesse sentido específico, `related` para ele nunca precisa de sintaxe cross-repo, porque ele não muda de endereço. O inverso é esperado e correto: um documento em qualquer repositório de conteúdo pode (e deve) ter `related` cross-repo apontando **para** um desses frameworks isentos. A isenção impede a cópia/duplicação do framework, não a referência a ele.

## 7. Decision Record vs. `type: decision`

Dois mecanismos com escopos diferentes — não confundir:

- **Decision Record** (`decisions/NNNN-slug.md`) — só existe no repositório `hipocampo`. Decisão sobre a metodologia em si: schema, regra, rotina. Template: Contexto (dúvida central) → Decisão (escolha) → Racional (porquê) → Alternativas descartadas → Status.
- **`type: decision`** — documento comum, existe em qualquer repositório de conteúdo. Decisão sobre conteúdo/arquitetura daquela instância específica (por exemplo, "por que esse cliente ficou em tal repositório e não em outro").

O `CHANGELOG.md` de cada instância de conteúdo é estreito de escopo: só registra decisão estrutural local daquela instância. Mudança de regra/schema do Hipocampo em si vira uma linha de referência ("atualizado para Hipocampo vX.Y, ver CHANGELOG do hipocampo") em vez de reexplicada.

## 8. Extensão/personalização e precedência do agente

**Invariantes** — nenhuma instância sobrescreve, sob nenhuma circunstância:

1. Nenhum repositório de conhecimento é público à internet.
2. `author` é sempre uma pessoa, nunca a IA (ver exceção escopada da seção 2 para conteúdo histórico).
3. Documento nunca é apagado fisicamente — só arquivado ou superseded.
4. Separação de acesso é sempre por repositório, nunca por etiqueta dentro de um repositório compartilhado.
5. O agente nunca escreve sem pedido explícito do usuário.

O invariante 3 tem uma exceção formal e estreita, documentada em `decisions/0010-excecao-apagamento-obrigacao-legal.md`: apagamento físico do conteúdo pessoal específico é permitido quando, e somente quando, acionado por uma solicitação legítima de eliminação de dado pessoal de um titular identificável, com base legal real (LGPD Art. 16 / GDPR Art. 17). A legitimidade do pedido é sempre avaliada pelo humano responsável pela instância, nunca decidida pelo agente sozinho, e o conteúdo removido é substituído por um registro mínimo do fato ocorrido ("tombstone") — nunca simplesmente apagado sem rastro, e nunca uma porta aberta para apagamento por conveniência.

**Ajustável por instância** — sempre documentado, nunca implícito, num bloco "Extensões locais a Hipocampo vX.Y" no `AGENTS.md` daquele repositório (ver seção 11): subpastas de `category`, `ttl` default sugerido por tipo de conteúdo, rituais extras específicos (incluindo se/como o ritual REM da seção 5-A é adotado), nomenclatura de commit/branch.

**Hierarquia de precedência do agente**, do mais específico para o mais geral:

1. Pedido explícito do usuário na conversa atual — dentro dos limites dos invariantes.
2. Extensão/override documentado localmente na instância.
3. Regra base deste `SPEC.md`.
4. Convenção default do `hipocampo-toolkit`, na ausência de tudo o resto.

Nenhuma camada sobrescreve um invariante. Se um pedido violar um invariante, o agente segue o invariante e avisa isso explicitamente — nunca obedece nem recusa em silêncio.

## 9. Versionamento

A metodologia em si segue [SemVer](https://semver.org/lang/pt-BR/): MAJOR para mudança que quebra compatibilidade (exige migração ativa, ver `MIGRATIONS.md`), MINOR para capacidade nova compatível com o que já existe, PATCH para clarificação ou correção que não muda comportamento. Cada versão liberada é marcada com uma tag de git. Cada instância declara, no próprio `AGENTS.md`/`CLAUDE.md`, a versão ou faixa de compatibilidade que implementa (exemplo: "Segue Hipocampo ^1.0.0").

Toda nova versão segue uma rotina obrigatória antes de ser considerada completa — checagem de necessidade de migração e sincronização do `hipocampo-toolkit`. Ver `decisions/0014-rotina-obrigatoria-de-release.md`.

Corte de release (tag + GitHub Release publicados) não precisa acontecer a cada mudança aceita — trabalho acumula em `main` até massa crítica ou pausa natural, ver `decisions/0021-politica-de-cadencia-de-release.md`. Mudança urgente (correção, não capacidade nova) sai como PATCH, fora do ciclo normal de acúmulo.

## 10. Migração de conteúdo pré-existente

Trazer conteúdo de fora do Hipocampo (sistema legado, export de outra ferramenta) ou de uma versão anterior da metodologia nunca copia o arquivo original diretamente para o repositório de destino. O frontmatter é sempre reescrito do zero, conforme o schema vigente (seção 2); o corpo é ajustado conforme as regras vigentes de atomicidade, nomenclatura e privacidade (seção 2-A), documentando em `revision_note` o que foi preservado verbatim e o que foi alterado, e por quê. Ver `decisions/0011-migracao-nunca-copia-arquivo-direto.md`.

## 11. Arquivo de instrução: AGENTS.md e CLAUDE.md

`AGENTS.md` é o arquivo canônico de instrução operacional de qualquer instância Hipocampo — invariantes, extensões locais (seção 8), referência de frontmatter, e o **escopo do repositório**: o que deve e o que não deve ser armazenado ali, e pra onde vai o que não pertence. Este último item é obrigatório, nunca implícito — mesmo princípio das extensões locais — e é a fonte que os rituais de manutenção (REM, seção 5-A; auditoria estrutural, seção 5-C) consultam pra decidir se um documento pertence ao repositório onde está.

`CLAUDE.md` continua existindo em toda instância, mas como ponteiro fino — poucas linhas, remetendo pra `AGENTS.md` como fonte de verdade, sem duplicar conteúdo. Ver `decisions/0015-agents-md-arquivo-canonico-instrucao.md`.

Instâncias já existentes antes desta seção (v1.6.0 e anteriores, quando `CLAUDE.md` ainda era o arquivo canônico) migram na próxima vez que forem tocadas — não é automático (mesmo princípio de qualquer mudança MINOR, ver DISCLAIMER.md).

## 12. Identidade de autor multi-conta

Quando a pessoa por trás de `author` opera mais de uma conta de git (ex.: pessoal e vinculada a empregador) que precisam resolver pro mesmo `author` humano (invariante 2), essa relação é registrada no `AGENTS.md` do repositório pessoal menos restrito — nunca no `hipocampo`/`hipocampo-toolkit` públicos — e no roteador de repositórios da skill personalizada (nunca na cópia genérica).

Entre instância pessoal e instância corporativa da mesma pessoa, convite de acesso (colaborador de repositório) sempre parte da conta pessoal convidando a profissional pro second brain **pessoal** — nunca o inverso. A identidade pessoal é sempre a âncora de confiança; a organização empregadora nunca tem posição de conceder ou negar acesso ao conhecimento pessoal de alguém. Ver `decisions/0020-identidade-autor-multi-conta.md`.

## Histórico de versões

Ver [CHANGELOG.md](CHANGELOG.md).
