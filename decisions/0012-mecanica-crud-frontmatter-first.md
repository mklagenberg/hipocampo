# 0012 — Mecânica CRUD e leitura frontmatter-first

**Status:** Aceito

## Contexto

O ciclo de vida de um documento Hipocampo (`draft`→`active`→`stale`→`archived`→`superseded`, SPEC.md seção 2) já implementa, na prática, as quatro operações de um CRUD (Create, Read, Update, Delete): Create é a criação do documento com frontmatter completo; Read é a consulta por um agente ou humano; Update é a edição de conteúdo com incremento de `revision`; Delete é mitigado pelo invariante 3 (nunca apagar fisicamente, só `archived`/`superseded`, com exceção estreita da `decisions/0010`). Essa mecânica nunca foi nomeada explicitamente como "CRUD" no SPEC.md, o que dificulta comunicar o modelo a quem já conhece o termo de outros contextos técnicos (bancos de dados, APIs). Além disso, a forma como um agente de IA deveria consumir tokens ao operar essa mecânica nunca foi especificada: hoje nada impede um agente de ler o corpo inteiro de todo documento candidato numa busca, o que é caro e desnecessário quando o frontmatter já contém metadado suficiente pra filtrar (`type`, `tags`, `status`, `temporality`, `related`).

## Decisão

Nomear explicitamente a mecânica de ciclo de vida como CRUD (SPEC.md, nova subseção 2-B), mapeando Create/Read/Update/Delete às operações já existentes. Adicionar uma regra de leitura recomendada ao agente: ao operar sobre múltiplos documentos (busca, triagem, staleness), ler sempre o frontmatter primeiro — YAML, custo de token baixo, suficiente pra filtrar e decidir relevância —; só ler o corpo completo do documento depois de decidir, pelo frontmatter, que aquele documento específico precisa de leitura completa. Isso não é uma regra nova de comportamento — é a formalização de uma prática eficiente que já deveria ser óbvia, mas nunca foi escrita.

## Racional

Nomear a mecânica como CRUD aproveita um vocabulário já conhecido de quem vem de outras áreas técnicas, facilitando comunicação sem inventar terminologia nova. A regra de frontmatter-first é puramente uma questão de eficiência de custo (tokens), que se torna cada vez mais relevante à medida que uma instância cresce — uma instância com centenas de documentos não deveria custar centenas de leituras completas só para decidir quais três são relevantes para uma pergunta.

## Alternativas descartadas

- **Não nomear a mecânica, deixar implícita.** Descartada: dificulta explicar a metodologia a quem já conhece o termo CRUD de outro contexto, sem nenhum ganho em não nomear.
- **Exigir leitura completa sempre, sem estágio de frontmatter-first.** Descartada: desperdiça tokens em qualquer instância com volume razoável de documentos, sem necessidade — o frontmatter já carrega metadado suficiente pra filtrar na maioria dos casos.
