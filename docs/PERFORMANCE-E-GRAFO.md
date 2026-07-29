# Performance e o modelo de grafo do Hipocampo

Referência central — ver `hipocampo/decisions/0002` sobre por que este conteúdo mora aqui e instâncias novas recebem só o link, não uma cópia.

## Como o retrieval funciona, no fundo

Cada documento Hipocampo é um nó: o frontmatter (SPEC.md, seção 2) carrega os metadados que permitem filtrar sem ler o corpo (`type`, `tags`, `status`, `temporality`, `related`) — mecânica CRUD/frontmatter-first, `decisions/0012`. As arestas do grafo são o campo `related`, tanto local (`"path.md"`) quanto cross-repositório (`"$alias:path.md"`, resolvido via `registry.md` — SPEC.md, seção 6). Isso é, na prática, um grafo de conhecimento navegável só com ferramentas nativas de git/markdown — nenhum banco de grafo dedicado é necessário como linha de base.

## Comparação com o OKF (Open Knowledge Format) da Google

A Google Cloud publicou em junho de 2026 o [Open Knowledge Format (OKF)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) — uma especificação aberta e vendor-neutral pra guardar conhecimento como um diretório de arquivos markdown com frontmatter YAML, pensada pra ser compartilhável entre agentes, LLMs e ferramentas diferentes. O parentesco conceitual com o Hipocampo é real e não é coincidência: os dois desenhos chegam à mesma conclusão — markdown + YAML + tags formando um grafo é o formato mais simples que sustenta conhecimento legível por humano e por agente ao mesmo tempo.

A diferença está na profundidade do schema:

| | OKF | Hipocampo |
|---|---|---|
| Campo obrigatório | só `type` | `title`, `date`, `updated`, `source`, `type`, `temporality`, `ttl`, `status`, `visibility`, `author`, `revision`, entre outros |
| Campos recomendados | `title`, `description`, `resource`, `tags`, `timestamp` | — |
| Governança de acesso | não é o foco da spec | `visibility`/`license` derivados mecanicamente, arquitetura multi-repo pra separação real (`decisions/0002`, `decisions/0007`) |
| Ciclo de vida do documento | não especificado | `draft`→`active`→`stale`→`archived`→`superseded`, nunca apagado fisicamente (invariante 3, com exceção estreita da `decisions/0010`) |
| Privacidade por tipo de instância | não é o foco da spec | política explícita do que nunca entra numa instância corporativa (`decisions/0009`) |

Em espírito, o Hipocampo pode ser lido como "OKF mais uma camada de governança, ciclo de vida e privacidade" — não uma alternativa concorrente, um superconjunto pensado especificamente pra conhecimento sensível (pessoal ou corporativo), onde "quem pode ver o quê" e "o que nunca deveria ser guardado" importam tanto quanto a estrutura do grafo em si.

## O que isso significa na prática

Um bundle OKF simples é, em geral, compatível em espírito com um documento Hipocampo — os dois são markdown + YAML + tags. Migrar de um pra outro nunca é cópia direta (mesmo princípio da `decisions/0011`, seção 10 do SPEC.md): o schema mais rico do Hipocampo exige preencher os campos de ciclo de vida, visibilidade e licença que o OKF não obriga.
