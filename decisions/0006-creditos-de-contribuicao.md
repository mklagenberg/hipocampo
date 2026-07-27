# 0006 — Créditos de contribuição para conteúdo histórico

**Status:** Aceito

## Contexto

Conteúdo de trabalho migrado de sistemas anteriores ao Hipocampo nasceu de autoria coletiva nunca rastreada por indivíduo — equipes inteiras (diretoria, comercial, pré-vendas) produziram documentos sem que ninguém registrasse "quem escreveu esta frase". Forçar um `author` pessoal único por documento nesses casos seria arbitrário. O invariante "`author` é sempre uma pessoa" (SPEC.md, seção 8) não muda — falta um mecanismo pra quando a pessoa real não é recuperável da fonte.

## Decisão

Um arquivo `CONTRIBUTORS.md` (por instância, onde equipes fizerem sentido) define seções nomeadas e já datadas — por exemplo `## comercial-empresa-q1-2026` — cada uma com descrição curta de contexto/histórico e a lista de pessoas com sua posição. `author` e `contributors` no frontmatter podem referenciar essa seção diretamente por `@nome-da-secao` (ex.: `author: "@comercial-empresa-q1-2026"`), além de continuarem aceitando o formato de pessoa já existente (`"Nome Real - @usuario-github"`). A resolução temporal ("foto do momento") fica embutida no próprio nome da seção — quem redige o documento escolhe o nome já datado, sem algoritmo de resolução dinâmica.

**Escopo: só conteúdo histórico/migrado.** Documento novo, criado já dentro de uma instância Hipocampo, sempre tem `author` pessoa real (quem de fato escreveu ou está aprimorando aquele conhecimento) e `contributors` apurados por commit ou citação explícita — o mecanismo de equipe não se aplica a conteúdo novo.

## Racional

Reaproveita o padrão `@mention`, já familiar do próprio GitHub, em vez de inventar sintaxe nova. Elimina a necessidade de um pipeline de resolução dinâmica por data — a data já está no nome da seção, não num campo de intervalo que precisa ser computado. Tem precedente real fora do ecossistema Git: o sistema de créditos do Writers Guild of America distingue formalmente equipe que trabalhou junta ("&") de autoria separada no tempo ("and"); a tag `<collab>`/`<collab-wrap>` de JATS/Crossref resolve autoria coletiva em publicação científica; Schema.org aceita `Organization` como valor de `author`. O risco mais documentado desse tipo de mecanismo — diluição de accountability quando `author` é só um grupo genérico, convergente tanto na literatura de RACI quanto na de hiperautoria científica — fica mitigado pelo escopo: restrito ao estoque de conteúdo migrado, finito e decrescente conforme documentos são revisados, nunca recorrente em conteúdo novo.

## Alternativas descartadas

- **Unidade de crédito única com lista de períodos aninhada em YAML, resolvida por algoritmo de data em tempo de build.** Descartada por complexidade desproporcional ao estágio do projeto — Markdown simples, sem pipeline de CI/CD estabelecido.
- **Sintaxe `$alias:`** (já usada para `related`/`context_anchor` cross-repositório). Descartada para este caso: `@nome` é mais legível para uma referência dentro do mesmo repositório a uma seção de um arquivo, uso diferente do que `$alias:` resolve (documento inteiro em outro repositório).
- **Manter CRediT (Contributor Roles Taxonomy) como precedente direto.** Descartada como base do mecanismo — CRediT descreve o que cada autor fez (papel de contribuição), não quem conta como autor (identidade), eixo diferente do que este mecanismo resolve.
