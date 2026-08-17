# 0027 — Promote, Depromote e Redbutton: ações de ciclo de vida cross-repositório

**Status:** Proposto

## Contexto

O CRUD (seção 2-B) opera dentro de um único repositório. Mas conteúdo legitimamente precisa mudar de repositório ao longo do tempo — conhecimento pessoal que amadurece e vale a pena virar conhecimento corporativo, conteúdo corporativo compartilhado além do necessário que precisa ser restringido, ou conteúdo que viola a política de dados sensíveis (seção 2-A) e precisa ser removido mesmo sem uma solicitação formal de titular. Hoje não existe mecanismo formal pra nenhum dos três casos — o risco é ad hoc: copiar e colar manualmente (reintroduzindo o problema de divergência silenciosa que `decisions/0002` já rejeitou), ou não ter caminho nenhum pra remediar conteúdo mal colocado além do que `decisions/0010` cobre (só solicitação do titular).

A primeira linha de proteção contra conteúdo mal colocado continua sendo a curadoria do próprio ritual REM (seção 5-A, função Consolidar) — decidir na entrada se um item nasce pessoal ou corporativo. As ações desta decisão são o complemento: pra quando a curadoria de entrada falha, ou quando um documento já existente precisa mudar de classificação deliberadamente, depois do fato.

## Decisão

Três ações novas, documentadas normativamente em `SPEC.md`, seção 13:

### 1. Promote (pessoal → corporativo)

Dois caminhos, sempre apresentados juntos antes de qualquer escrita (invariante 5):

- **Elegante (recomendado por padrão):** cria documento novo no repositório corporativo, seguindo a disciplina de `decisions/0011` — frontmatter reescrito do zero pro schema/política do destino, nunca copiado verbatim; corpo despersonalizado conforme necessário; checagem de conformidade com a política de dados sensíveis (seção 2-A) antes de escrever; `author` corrigido pra identidade corporativa (`decisions/0020`); rótulos de tipo de informação (`decisions/0026`) reavaliados no novo contexto. O documento pessoal de origem **não muda de `status`** — continua ativo, ganha só um `related` novo (`$alias:`) apontando pro documento corporativo, com `revision_note` registrando data e natureza da derivação. O documento corporativo aponta de volta pro pessoal do mesmo jeito. Os dois evoluem de forma independente dali em diante — não é replicação no sentido vetado por `decisions/0002`, porque nunca houve expectativa de sincronia entre os dois.

- **Literal (raro):** o documento pessoal é de fato transferido — `status: superseded`, `superseded_by: $alias:destino`, `temporality: historical`, conteúdo preservado como estava no momento da promoção. Antes de qualquer escrita nesse caminho, o agente explica explicitamente: (a) isso transfere titularidade do conteúdo pra empresa, conforme `decisions/0007` — o `LICENSE` do repositório corporativo declara a empresa como titular; (b) isso não é reversível de forma trivial. Só prossegue com confirmação explícita depois desse aviso.

### 2. Depromote (descida de nível, mesmo domínio de titularidade)

Move conteúdo entre repositórios do mesmo titular (ex.: `empresa-público` → `empresa-confidencial`, ou entre variantes pessoais) sem cruzar a fronteira pessoal/corporativo — por isso não carrega a questão de titularidade do Promote literal, e não precisa do mesmo aviso explícito. Mecânica: `status: superseded` na origem, `superseded_by: $alias:destino`. Reversão literal do Promote (corporativo → pessoal, cruzando a fronteira de titularidade de volta) fica fora do escopo desta ação — não é automatizada; é decisão caso a caso do humano responsável, fora do fluxo normal do Hipocampo, no mesmo espírito do `DISCLAIMER.md` ("não substitui compliance legal").

### 3. Redbutton (remediação de violação da política 2-A)

Extensão do gatilho de `decisions/0010` — ver `decisions/0028` pro detalhe completo. Resumo: o mesmo mecanismo de apagamento físico + tombstone de `0010` passa a ser acionável também quando a auditoria estrutural (5-C) ou o operador da instância identifica conteúdo que viola a política de dados sensíveis (seção 2-A), mesmo sem solicitação formal do titular.

### 4. `superseded_by` cross-repositório

`superseded_by`, usado por Promote (caminho literal) e por Depromote, passa a aceitar formalmente a mesma sintaxe `$alias:` já documentada pra `related` (seção 6) — necessário pras duas ações apontarem pra um documento em outro repositório.

## Racional

Promote elegante evita reintroduzir o problema que `decisions/0002` já resolveu (replicação com risco de divergência silenciosa) ao tratar a derivação como um Create novo com proveniência documentada, não uma cópia com expectativa de sincronia. O caminho literal existe porque às vezes a intenção real é mesmo transferir — mas a decisão de fazer isso, sabendo que muda quem é dono legal do conteúdo (`decisions/0007`), precisa ser do humano, informada, nunca assumida pelo agente. Depromote fica deliberadamente mais simples que Promote porque não cruza a mesma fronteira de titularidade — tratar os dois com o mesmo peso seria fricção desproporcional ao risco real do caso comum (correção de superexposição dentro da mesma empresa).

## Alternativas descartadas

- **Move/Copy/Delete genéricos, sem distinção de direção.** Descartada: "Copy" como duplicata mantida solto colide com `decisions/0002`; um "Move" único não captura a assimetria de risco entre cruzar a fronteira pessoal/corporativo (questão de titularidade real) e mover dentro do mesmo domínio (reclassificação de acesso, sem questão de titularidade).
- **Promote com um caminho só (literal).** Descartada: esconde do usuário a opção de baixo risco (derivação, sem transferência) atrás da única opção de alto risco (transferência de titularidade), quando na prática a maioria dos casos de promoção não precisa ser transferência de fato.
- **Depromote como reversão automatizada e simétrica do Promote.** Descartada: a reversão cruzando de volta pro domínio pessoal enfrenta a mesma questão de titularidade do Promote literal, só que sem base legal clara equivalente — não é uma ação de rotina que o agente deveria automatizar.
