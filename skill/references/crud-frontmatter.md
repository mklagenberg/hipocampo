# Mecânica CRUD e leitura frontmatter-first

Referência completa: `hipocampo/SPEC.md`, seção 2-B (`decisions/0012`, `decisions/0018`).

## Regra de leitura

Ao operar sobre múltiplos documentos (busca, triagem, staleness), ler sempre o **frontmatter primeiro** — YAML, custo de token baixo, suficiente pra filtrar por `type`, `tags`, `status`, `temporality`, `related`. Só ler o **corpo completo** depois de decidir, pelo frontmatter, que aquele documento específico precisa. Não ler o corpo inteiro de todo candidato como padrão — é desperdício de token evitável, especialmente numa instância com muitos documentos.

## Validação em tempo de leitura (independente do frontmatter audit em lote)

Toda operação de READ — mesmo uma consulta pontual, fora de qualquer ritual agendado — valida o frontmatter do documento contra a norma (schema da seção 2) e a checagem de staleness (seção 5) **no momento da leitura**, independente de o frontmatter audit em lote (referência `rotinas.md`) já ter passado por aquele documento.

Se a validação encontrar problema, sinalizar explicitamente o quê e o que fazer. Nunca alterar `status` ou qualquer campo sozinho como parte dessa validação — só sinalizar. Casos concretos:

- **`ttl` vencido:** avisar que a informação pode estar defasada. Se `source: url`, sugerir revalidação por pesquisa (mesmo gatilho que aciona a skill `deep-research`) antes de tratar o conteúdo como atual.
- **Campo obrigatório ausente:** apontar qual campo falta, sem inventar um valor.
- **`temporality: contextual` com `context_anchor` apontando pra documento já `archived`/`superseded`:** sinalizar que o documento pode estar desatualizado mesmo com `ttl` ainda não vencido — a âncora mudou de estado antes do prazo.

## Exemplo

> Usuário: "o que a gente sabe sobre o fornecedor X?"
>
> Agente lê o frontmatter dos candidatos por `tags`/`type: company`. Encontra um documento com `ttl: 2026-03-01` (já vencido) e `source: url`. Resposta: "Achei um documento sobre o fornecedor X, mas o `ttl` venceu em março e a fonte original é uma URL — a informação pode estar desatualizada. Quer que eu revalide via pesquisa antes de responder, ou prefere ver o conteúdo como está, com essa ressalva?"

O CRUD em si (Create/Read/Update/Delete) mapeia o ciclo de vida do campo `status` (seção 2 do SPEC) — Delete é sempre mitigado pela invariante 3 (nunca apagar fisicamente), exceto pela exceção estreita da `decisions/0010`.
