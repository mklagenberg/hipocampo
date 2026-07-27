# 0005 — `category: frameworks` e `type: framework` são eixos ortogonais

**Status:** Aceito

## Contexto

Dois campos do frontmatter usam a palavra "framework" de formas aparentemente sobrepostas: `category` (campo livre, string) pode valer `"frameworks"`, e `type` tem o valor `framework`. Era preciso decidir se isso é redundância a ser resolvida ou duas coisas genuinamente diferentes.

## Decisão

Manter os dois campos coexistindo, sem fundir. `category` decide onde o documento mora fisicamente (subpasta por tema, só existe com massa crítica). `type: framework` decide regime de autoria/titularidade (SPEC.md seção 3, DISCLAIMER.md), independente de pasta.

## Racional

Um documento pode ser `type: framework` (sujeito ao regime de titularidade de autor/proprietário) sem ainda ter `category: frameworks` — não ter atingido massa crítica de documentos do tema para justificar uma subpasta física não muda o regime de titularidade do conteúdo em si. Os dois campos respondem perguntas diferentes ("onde isso mora" vs. "quem é dono disso") que só coincidem de nome por acaso de vocabulário.

## Alternativas descartadas

- **Fundir os dois num campo só** — descartada porque um documento `type: framework` isolado (sem massa crítica de pasta) perderia a marcação de titularidade se `category` fosse o único campo, ou um documento em `category: frameworks` que não é sujeito a regime especial de autoria ganharia uma classificação incorreta se `type` fosse eliminado.
- **Renomear um dos dois pra evitar a coincidência de nome** — considerada, mas cada nome já é o mais descritivo pro que o campo faz; a nota explícita no SPEC.md (seção 4) resolve a confusão sem precisar inventar um nome pior.
