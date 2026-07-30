# 0018 — Validação de frontmatter em tempo de leitura (extensão da mecânica CRUD/READ)

**Status:** Aceito

## Contexto

A seção 2-B do SPEC.md (DR0012) já estabelece que READ deve ler frontmatter primeiro, por economia de token — mas não diz que READ deve *validar* esse frontmatter contra a norma vigente antes de entregar o conteúdo. Hoje, um documento com `ttl` vencido é lido e usado como se fosse informação corrente, a menos que o frontmatter audit (DR0017) já tenha passado por ele e alguém tenha visto a fila. Isso deixa uma janela onde informação defasada é consumida sem sinalização, entre um audit e o próximo.

## Decisão

Toda operação de READ da mecânica CRUD (seção 2-B) passa a incluir uma validação leve do frontmatter lido contra a norma da seção 2, além da checagem de staleness da seção 5 — independente de o frontmatter audit (ritual em lote, DR0017) já ter passado por aquele documento especificamente. Se a validação encontrar problema, o agente sinaliza explicitamente ao usuário o que está errado e o que precisa ser feito, antes ou junto da resposta baseada naquele conteúdo. No caso específico de `ttl` vencido: o agente deixa explícito que a informação é defasada, e sugere revalidação por pesquisa quando o documento for `source: url` (fato do mundo externo) — mesmo mecanismo já coberto pela skill `deep-research`, agora acionado também por este gatilho, não só por pedido explícito.

Esta validação em tempo de leitura nunca altera `status` ou qualquer campo do documento sozinha — só sinaliza. Mudança de `status` continua exigindo o mesmo processo já estabelecido (ritual REM ou pedido explícito, invariante 5).

## Racional

Frontmatter audit (ritual em lote, diário) e validação em tempo de leitura (mecânica, a cada READ) são complementares, não redundantes: o audit garante cobertura completa e periódica, mesmo de documentos que ninguém acessa por acaso; a validação em tempo de leitura garante que ninguém consome informação defasada na janela entre um audit e o próximo, exatamente quando o documento é de fato usado. Ter as duas cobre tanto o caso "documento esquecido" quanto o caso "documento acessado logo depois de vencer, antes do próximo audit".

## Alternativas descartadas

- **Confiar só no frontmatter audit em lote, sem checagem em tempo de leitura:** descartada pela janela de exposição entre execuções do audit, especialmente relevante pra documentos `ephemeral` com `ttl` curto.
- **READ recusar retornar conteúdo com `ttl` vencido, em vez de sinalizar e retornar mesmo assim:** descartada — o conteúdo ainda é geralmente útil (é a melhor informação disponível até revalidação), e recusar completamente atrapalharia mais do que ajudaria; sinalizar com clareza é suficiente pra manter a decisão de uso com o humano.
