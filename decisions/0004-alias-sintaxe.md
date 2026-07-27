# 0004 — Sintaxe de alias cross-repositório: `$nome`, não `{{nome}}`

**Status:** Aceito

## Contexto

O campo `related` (e `context_anchor`) precisa de uma sintaxe para diferenciar referência ao mesmo repositório de referência a um repositório diferente (SPEC.md, seção 6).

## Decisão

Usar prefixo `$alias:` (exemplo: `$concepts:path.md`) para referência cross-repositório, resolvido por um arquivo `registry.md`.

## Racional

A alternativa mais óbvia, `{{nome}}`, é a sintaxe padrão de motores de template como Jinja e Mustache. Se um arquivo Hipocampo algum dia passar por um pipeline que usa um desses motores (geração de site estático, processamento em lote), `{{nome}}` corre o risco real de ser interpretado como uma variável de template a ser substituída, corrompendo a referência silenciosamente. `$` não tem significado especial em YAML puro nem nos motores de template mais comuns nesse contexto — sintaxe sem ambiguidade conhecida.

## Alternativas descartadas

- **`{{nome}}`** — descartada pelo risco de colisão com sintaxe de motor de template, descrito acima.
- **URL completa do GitHub** — descartada por verbosidade e por acoplar a referência ao nome atual do repositório; renomear um repositório quebraria toda referência existente, em vez de só uma linha no `registry.md`.
