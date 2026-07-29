# Hipocampo — SPEC

Versão: 1.6.0 · Segue [SemVer](https://semver.org/lang/pt-BR/)

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
`author` é sempre uma pessoa (`Nome Real - @usuario-github`), nunca a IA — mesmo quando um agente escreve o texto sob direção de alguém, o autor é quem dirigiu. Campo obrigatório em qualquer documento, qualquer `visibility`. Exceção escopada só a conteúdo histórico/migrado, sem autoria individual rastreável na origem: `author`/`contributors` podem referenciar uma seção nomeada e datada de um arquivo `CONTRIBUTORS.md` via `@nome-da-secao`, em vez de uma pessoa — documento novo nunca usa essa exceção (ver `decisions/0006-creditos-de-contribuicao.md`). `owner` é sempre o nome de uma empresa, preenchido só quando o documento nasce em contexto de trabalho — ver a distinção completa de papéis e o que cada um pode fazer com o conteúdo no `DISCLAIMER.md` e nos Decision Records de licenciamento em `decisions/`.

### license
Sempre derivado mecanicamente de `visibility`, nunca definido à mão — evita divergência entre a camada de confidencialidade (`visibility`) e a camada jurídica (`license`). Usa o padrão SPDX `LicenseRef-<idstring>`, com o texto legal completo no arquivo `LICENSE` da raiz do repositório, nunca reescrito por documento. Ver `decisions/0007-licenciamento-repos-de-conteudo.md`.

## 2-A. Política de dados sensíveis por tipo de instância

Instância corporativa (`owner` preenchido com o nome de uma organização) nunca armazena, em nenhum nível de `visibility` — mesmo `restricted`: conteúdo de contrato ou NDA; avaliação de desempenho de indivíduo identificável; anotação de saúde de qualquer pessoa (titular da instância ou terceiro); dado pessoal (senha, endereço pessoal, telefone ou e-mail pessoal, nome de parente); valor de salário, valor pago a fornecedor, ou valor de projeto/contrato. Exceção única pra valor absoluto: resultado de negócio entregue a um cliente num `type: case` (receita gerada, custo evitado) é o próprio produto do case, não exposição financeira interna. Aprendizado interno quantificado (ex.: economia de processo) é registrado como variação percentual, nunca valor absoluto.

Dado financeiro sobre terceiro que não é fornecedor/parceiro comercial direto (ex.: inteligência de mercado sobre concorrente, extraída de fonte pública) não é abrangido por essa restrição — desde que a fonte pública seja citada explicitamente no documento.

Nome completo, cargo, e-mail profissional, telefone ou endereço profissional — de colega ou de contato de cliente — são permitidos em instância corporativa, sempre acompanhados de citação de ano/data: o registro é uma fotografia datada, nunca um estado presumido atual.

Questão pessoal de qualquer indivíduo (saúde, situação financeira pessoal) nunca vai pra instância corporativa — sempre pra instância pessoal do titular relevante, se existir uma.

Detalhe técnico de vulnerabilidade ou exploração ativa (payload de ataque, query/dork que revela o comprometimento, credencial, endpoint explorável) nunca é registrado verbatim, em nenhuma instância, mesmo confidencial/restricted — registra-se o fato (existência da falha, categoria, data do achado) e a resposta dada, nunca o material que reproduziria ou confirmaria o ataque.

Quando um documento inteiro depende estruturalmente de um tipo de dado banido (não dá pra adaptar removendo só o trecho problemático), o agente não decide sozinho entre publicar mesmo assim ou descartar — sinaliza a violação ao humano responsável pela instância e aguarda decisão explícita. Ver `decisions/0009-politica-de-privacidade-por-instancia.md`.

## 2-B. Mecânica CRUD e leitura frontmatter-first

O ciclo de vida do documento (seção 2, campo `status`) implementa as quatro operações de um CRUD: **Create** (criação com frontmatter completo), **Read** (consulta por agente ou humano), **Update** (edição de conteúdo com incremento de `revision`), **Delete** (mitigado pelo invariante 3 — nunca apagar fisicamente, só `archived`/`superseded`, com exceção estreita da `decisions/0010`). Ver `decisions/0012-mecanica-crud-frontmatter-first.md`.

Regra de leitura recomendada ao agente: ao operar sobre múltiplos documentos (busca, triagem, staleness), ler sempre o **frontmatter primeiro** — YAML, custo de token baixo, suficiente pra filtrar por `type`, `tags`, `status`, `temporality`, `related` e decidir relevância. Só ler o **corpo completo** depois de decidir, pelo frontmatter, que aquele documento específico precisa de leitura completa. Numa instância com muitos documentos, isso evita custo de token desnecessário — ler o corpo inteiro de todo candidato só pra descartar a maioria não é o padrão de acesso default.

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

A seção 5 formaliza como um documento *já existente* envelhece. Esta seção formaliza como um item *novo* — captura bruta, ainda não curada — entra no sistema e vira documento consolidado. Capacidade opcional por instância (ver decisions/0008-ritual-rem-e-camadas-de-memoria.md).

Quatro estações e um ritual de consolidação:

1. **Memória sensorial** — buffer bruto de percepção (ex.: a janela de conversa). Alta perda por design; não é papel do Hipocampo reter isso.
2. **Gate de atenção** — mecanismo explícito que decide o que atravessa da sensorial pra curto prazo (ex.: um "check-in"/dump de sessão). Só entra no sistema canônico o que passa pelo gate.
3. **Memória de curto prazo** — item já capturado no sistema canônico (git), ainda não curado. Mínimo viável: uma pasta `inbox/` versionada no próprio repositório — infraestrutura de nuvem (fila, banco de estado) é Extensão local opcional (seção 8), nunca linha de base.
4. **Ritual REM (consolidação)** — lê só da memória de curto prazo, nunca direto da sensorial. Roda periodicamente ou sob pedido. Para cada item pendente, decide entre virar documento novo, fundir com um existente, ou descartar. O plano completo é sempre apresentado antes de qualquer execução (mesmo invariante "agente nunca escreve sem pedido explícito", seção 8, aplicado a este ritual).
5. **Memória de longo prazo** — documento atômico, curado, frontmatter completo. É o corpo principal de qualquer repositório de conteúdo Hipocampo, já descrito desde a v1.0.0 — não é capacidade nova.

Regras adicionais: atomicidade (documento consolidado = um conceito só; material bruto com N ideias vira N documentos); um `memory.md` de harness de agente (satélite pequeno e durável do próprio agente) e um snapshot de transferência (export imutável pra migração) não são memória sensorial nem passam pelo ritual REM — mecanismos distintos, não confundir; evolução de schema é reativa, só cresce por massa crítica (mesmo princípio da seção 4).

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

**Ajustável por instância** — sempre documentado, nunca implícito, num bloco "Extensões locais a Hipocampo vX.Y" no `CLAUDE.md`/README daquele repositório: subpastas de `category`, `ttl` default sugerido por tipo de conteúdo, rituais extras específicos (incluindo se/como o ritual REM da seção 5-A é adotado), nomenclatura de commit/branch.

**Hierarquia de precedência do agente**, do mais específico para o mais geral:

1. Pedido explícito do usuário na conversa atual — dentro dos limites dos invariantes.
2. Extensão/override documentado localmente na instância.
3. Regra base deste `SPEC.md`.
4. Convenção default do `hipocampo-toolkit`, na ausência de tudo o resto.

Nenhuma camada sobrescreve um invariante. Se um pedido violar um invariante, o agente segue o invariante e avisa isso explicitamente — nunca obedece nem recusa em silêncio.

## 9. Versionamento

A metodologia em si segue [SemVer](https://semver.org/lang/pt-BR/): MAJOR para mudança que quebra compatibilidade (exige migração ativa, ver `MIGRATIONS.md`), MINOR para capacidade nova compatível com o que já existe, PATCH para clarificação ou correção que não muda comportamento. Cada versão liberada é marcada com uma tag de git. Cada instância declara, no próprio `CLAUDE.md`/README, a versão ou faixa de compatibilidade que implementa (exemplo: "Segue Hipocampo ^1.0.0").

Toda nova versão segue uma rotina obrigatória antes de ser considerada completa — checagem de necessidade de migração e sincronização do `hipocampo-toolkit`. Ver `decisions/0014-rotina-obrigatoria-de-release.md`.

## 10. Migração de conteúdo pré-existente

Trazer conteúdo de fora do Hipocampo (sistema legado, export de outra ferramenta) ou de uma versão anterior da metodologia nunca copia o arquivo original diretamente para o repositório de destino. O frontmatter é sempre reescrito do zero, conforme o schema vigente (seção 2); o corpo é ajustado conforme as regras vigentes de atomicidade, nomenclatura e privacidade (seção 2-A), documentando em `revision_note` o que foi preservado verbatim e o que foi alterado, e por quê. Ver `decisions/0011-migracao-nunca-copia-arquivo-direto.md`.

## Histórico de versões

Ver [CHANGELOG.md](CHANGELOG.md).
