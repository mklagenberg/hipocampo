# 0017 — Frontmatter audit: ritual determinístico que precede a consolidação REM

**Status:** Aceito

## Contexto

A checagem de staleness (SPEC.md seção 5) e o ritual REM (seção 5-A) dependem de saber quais documentos têm `ttl` vencido, campo obrigatório ausente, ou outra violação da norma de frontmatter (seção 2) — mas até a v1.9.0 não existe nenhum mecanismo formal que produza essa lista. Rodar essa checagem via agente de IA, documento por documento, é desperdício de token e sujeito ao mesmo risco de erro probabilístico que o DISCLAIMER.md já reconhece pra qualquer rotina de IA — quando a checagem é puramente mecânica (comparação de data, presença de campo), não precisa de julgamento de modelo nenhum.

## Decisão

Frontmatter audit é um ritual novo, determinístico (implementado como script, não como julgamento de agente de IA), com cadência recomendada diária, rodando **antes** da consolidação REM do mesmo dia. Ele varre todo o frontmatter de um repositório (sem ler o corpo dos documentos — seção 2-B já estabelece frontmatter-first) e produz um arquivo de fila, `meta/fila-de-manutencao.md`, listando: documentos com `ttl` vencido (por `temporality`), documentos com campo obrigatório ausente (seção 2), e qualquer outra violação mecanicamente detectável da norma de frontmatter.

O frontmatter audit nunca decide disposição (arquivar, superseder, revalidar) — só relata. A decisão de disposição é sempre do ritual REM (seção 5-A, função de "atualizar memórias antigas") ou de um humano, nunca do próprio audit.

## Racional

Separar detecção (determinística, sem ambiguidade, sem custo de julgamento) de decisão (que precisa de julgamento, e por isso é sempre supervisionada por humano, invariante 5) segue o mesmo espírito do DISCLAIMER.md: usar IA onde julgamento é necessário, não onde uma checagem mecânica já resolve. Rodar antes da REM, não depois, garante que a consolidação do dia já opera com a fila atualizada, em vez de trabalhar com informação potencialmente desatualizada sobre o que precisa de atenção.

## Alternativas descartadas

- **Deixar a checagem de staleness inteiramente a cargo do agente de IA, sem script:** descartada pelo custo de token (ler frontmatter de todo documento via agente, toda vez) e pelo risco de erro numa tarefa que é puramente mecânica.
- **Rodar o frontmatter audit depois da REM, não antes:** descartada porque a REM precisa da fila atualizada pra cumprir sua segunda função (atualizar memórias antigas) no mesmo ciclo diário — rodar depois adiaria o tratamento de qualquer pendência nova em um dia inteiro.
- **Um único arquivo de fila global, cross-repositório:** descartada porque os rituais de manutenção operam sempre no escopo de um repositório por vez (ver DR0016) — um arquivo por repositório evita ambiguidade sobre onde uma pendência mora.
