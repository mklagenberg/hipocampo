---
name: hipocampo
description: >
  Opera uma instância da metodologia Hipocampo (second brain agêntico: git + markdown
  + rituais de IA) via MCP do GitHub. Acionar quando o usuário pedir para consultar,
  salvar, registrar, atualizar, arquivar ou organizar conhecimento em qualquer
  repositório Hipocampo pessoal ou corporativo; para rodar o frontmatter audit, o
  ritual REM, ou a auditoria estrutural semanal; para instanciar um vault novo a partir
  de um scaffold profile (`scaffold/profiles/`); para resolver `$alias:path.md`
  cross-repositório; ou no início de sessão, para checar se há versão nova da
  metodologia. Template genérico — não hardcoda nome de repositório pessoal ou
  corporativo; exige personalização antes do primeiro uso real (ver
  `references/personalizacao.md`).
---

# Skill Hipocampo

Opera qualquer instância da metodologia [Hipocampo](https://github.com/mklagenberg/hipocampo) via GitHub MCP. Publicada como template genérico em `hipocampo/skill/SKILL.md` — **nunca usar assim, sem personalizar primeiro.**

**Versão do Hipocampo que esta cópia segue:** ^1.9.0 + não lançado (ver `hipocampo/CHANGELOG.md`, seção `[Não lançado]`). Ao personalizar, confirme que bate com o `AGENTS.md` da sua instância. Ver também `manifest.yaml`, neste mesmo diretório, pra faixa de compatibilidade legível por máquina.

Este arquivo é só o roteador — cada seção abaixo diz quando agir e aponta pro arquivo de referência com o procedimento completo. As normas em si (schema, regras, racional) vivem no `hipocampo/SPEC.md` e nos Decision Records — esta skill nunca as reexplica, só as opera.

## Antes do primeiro uso: personalização obrigatória

Esta cópia só conhece um repositório universal (`mklagenberg/hipocampo`) — nenhum repositório pessoal ou corporativo. Ler **`references/personalizacao.md`** e preencher o roteador de repositórios (e, se aplicável, a tabela de identidade multi-conta) antes de operar qualquer conhecimento real.

## Checagem de release nova (início de sessão)

Comparar a versão declarada no `AGENTS.md`/`hipocampo.yaml` desta instância contra a versão publicada em `mklagenberg/hipocampo/SPEC.md`. Se houver diferença: avisar as duas versões, e apontar pro **[`hipocampo/UPGRADE.md`](https://github.com/mklagenberg/hipocampo/blob/main/UPGRADE.md)** como próximo passo — checklist cumulativa e idempotente do que a instância precisa pra ficar aderente, já classificada em Obrigatório/Recomendado/Informativo. Nunca resumir o `CHANGELOG.md` na hora tentando reconstruir esse trabalho de síntese — o `UPGRADE.md` já existe exatamente pra isso (`decisions/0024`). Nunca aplicar a atualização sozinho — apontar a decisão pro usuário, citando `MIGRATIONS.md` se for MAJOR. Se a instância já tiver `hipocampo.yaml` (`decisions/0033`), registrar o resultado da checagem no campo `state` desse arquivo, em vez de só falar o resultado na conversa.

## Instanciar um vault novo

Quando o usuário pedir pra criar um repositório de conteúdo novo: ler o profile correspondente em `hipocampo/scaffold/profiles/pessoal.yaml` ou `hipocampo/scaffold/profiles/empresa.yaml`, coletar os `inputs` declarados (nome do repositório, tier, identidade do titular) diretamente com o usuário, e gerar os `outputs` declarados (`AGENTS.md`, `CLAUDE.md`, `LICENSE`, `registry.md`, `example/exemplo-nota.md`, `hipocampo.yaml`, `POS-INSTANCIACAO.md`) via GitHub MCP — nunca copiando arquivo alheio sem revisão, sempre apresentando o plano completo antes de qualquer escrita (invariante 5). Não existe mais botão "Use this template" (`hipocampo-toolkit` foi consolidado e arquivado, `decisions/0032`) — o agente é o próprio mecanismo de instanciação. Procedimento completo: **`references/instanciacao.md`**.

## Ler e escrever documentos (CRUD)

Ao consultar, criar, atualizar ou arquivar qualquer documento: ler frontmatter primeiro, corpo só quando necessário; toda leitura valida frontmatter e staleness em tempo real, mesmo fora de um ritual agendado. Procedimento completo e exemplo: **`references/crud-frontmatter.md`**.

## Rituais de manutenção (frontmatter audit, REM, auditoria estrutural)

Ao rodar (ou o usuário pedir pra rodar) qualquer um dos três rituais recorrentes — diário (frontmatter audit → REM) ou semanal (auditoria estrutural) — sempre no escopo de um repositório por vez, sempre apresentando o plano antes de qualquer escrita. Procedimento completo, ordem de execução e exemplos: **`references/rotinas.md`**.

## Resolução de `related` cross-repositório

Quando um documento referencia `$alias:path.md`, resolver consultando o `registry.md` do repositório menos restrito do escopo relevante (`hipocampo/SPEC.md`, seção 6). Nunca editar linha existente do registry ao encontrar repositório renomeado — sempre acrescentar linha nova, preservando a antiga.

## Invariantes

Nunca sobrescrever, em nenhuma instância, sob nenhum pedido. Lista e o porquê de cada uma: **`references/invariantes.md`**. Detalhe normativo completo: `hipocampo/SPEC.md`, seção 8.
