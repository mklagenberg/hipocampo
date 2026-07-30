# Hipocampo — Guia de atualização de instância

Checklist **cumulativa e idempotente**: o que uma instância deveria ter, hoje, pra estar aderente à versão atual da metodologia — não importa de qual versão antiga ela partiu. Diferente do `CHANGELOG.md` (histórico cronológico do que mudou) e do `MIGRATIONS.md` (só passos de mudança MAJOR, que quebram compatibilidade), este documento é a lista prática "o que fazer agora", sempre relativa ao presente. Ver `decisions/0024-upgrade-md-checklist-cumulativa.md`.

## Como usar

1. Abra o `AGENTS.md` (ou `CLAUDE.md`, se a instância ainda não migrou) e confira a versão declarada.
2. Percorra a lista abaixo, item por item. Cada um diz se é **Obrigatório** (invariante ou segurança — raro), **Recomendado** (funcional, mas nada quebra sem ele) ou **Informativo** (leitura, sem ação no repositório).
3. Repita para cada repositório que você opera — atualização é sempre por instância, nunca "global" (mesmo se você tiver vários repositórios, cada um avança na hora que fizer sentido pra ele).

Este documento é atualizado a cada release da metodologia (passo obrigatório da rotina de release, `decisions/0014` + `decisions/0024`) — sempre cumulativo, nunca reescrito do zero.

## Checklist

### Arquivo canônico e skill

- [ ] **[Recomendado, desde a seção 11 do SPEC]** `AGENTS.md` é o arquivo canônico de instrução da instância — não `CLAUDE.md`. Se sua instância ainda usa só `CLAUDE.md`, crie `AGENTS.md` com o conteúdo completo (invariantes, escopo, extensões locais) e deixe `CLAUDE.md` como ponteiro fino de poucas linhas. Ver `decisions/0015-agents-md-arquivo-canonico-instrucao.md`.
- [ ] **[Recomendado, desde a seção 11 + 2-A do SPEC]** O bloco "Escopo deste repositório" no `AGENTS.md` declara o **Tipo de instância** (`corporativa` ou `pessoal`) — critério que a auditoria estrutural usa pra saber qual variante da política de dados sensíveis se aplica. Ver `decisions/0022-tipo-de-instancia-declarado-no-agents-md.md`.
- [ ] **[Recomendado, desde a v1.7.0]** A skill instalada no seu ambiente de IA é a versão real e personalizada (`hipocampo-toolkit/skill/SKILL.md` + `references/`) — não o "stub" de versões anteriores à v1.7.0. Reinstale via `save_skill` (ou mecanismo equivalente da sua ferramenta) se sua cópia for antiga.
- [ ] **[Recomendado, desde a seção 11 do SPEC / v1.9 não lançado]** O roteador de repositórios (`skill/references/personalizacao.md` da sua cópia pessoal da skill) lista **todos** os repositórios que você opera — inclusive os que raramente são tocados. É a lista que qualquer auditoria de versão futura vai usar.
- [ ] **[Recomendado, se aplicável — seção 12 do SPEC]** Se você opera mais de uma conta de git resolvendo pro mesmo autor humano (ex.: pessoal e vinculada a empregador), essa relação está registrada no `AGENTS.md` da instância pessoal e no roteador da skill personalizada — nunca na cópia genérica. Ver `decisions/0020-identidade-autor-multi-conta.md`.

### Licenciamento

- [ ] **[Obrigatório]** O `LICENSE` do repositório não é o Apache-2.0 herdado do template — é o `LICENSE-pessoal` ou `LICENSE-corporativo` de `hipocampo-toolkit/license-templates/`. Bug comum em instâncias antigas — ver `docs/FAQ-E-ERROS-COMUNS.md`.

### Rituais de manutenção

- [ ] **[Recomendado, desde a seção 5-B do SPEC / v1.9 não lançado]** Frontmatter audit (diário, determinístico) rodando antes do ritual REM do mesmo ciclo — cadência declarada no `AGENTS.md`, seção "Rituais de manutenção". Ver `decisions/0017-frontmatter-audit-ritual-deterministico.md`.
- [ ] **[Recomendado, desde a seção 5-A do SPEC]** Ritual REM (diário, duas funções: consolidar `inbox/` + atualizar memórias antigas) — mesma seção do `AGENTS.md`. Ver `decisions/0008-ritual-rem-e-camadas-de-memoria.md` e `decisions/0016-memoria-curto-prazo-sanitizacao.md`.
- [ ] **[Recomendado, desde a seção 5-C do SPEC / v1.9 não lançado]** Auditoria estrutural (semanal: atomicidade, posicionamento, vazamento de dado sensível) — mesma seção do `AGENTS.md`. Ver `decisions/0019-auditoria-estrutural-semanal.md`.

### Privacidade

- [ ] **[Informativo]** Existe uma exceção formal e estreita ao invariante "documento nunca é apagado fisicamente", pra obrigação legal de eliminação de dado pessoal (LGPD Art. 16 / GDPR Art. 17) — decisão sempre humana, nunca do agente. Ver `decisions/0010-excecao-apagamento-obrigacao-legal.md`. Nenhuma ação necessária a menos que o caso ocorra de verdade.

## Leitura recomendada, sem ação necessária no repositório

`BEST-PRACTICES.md`, `docs/MODELOS-DE-IA.md`, `docs/PERFORMANCE-E-GRAFO.md`, `docs/USO-MULTI-FERRAMENTA.md`, `docs/FAQ-E-ERROS-COMUNS.md`, `DISCLAIMER.md` — contexto e boas práticas que não mudam nada estruturalmente numa instância existente.

## Mudanças que quebram compatibilidade (MAJOR)

Nenhuma até o momento. Quando uma mudança MAJOR for aceita (critério em `decisions/0023-criterio-operacional-escopo-semver.md`), o passo a passo obrigatório de migração vai para `MIGRATIONS.md`, não para este arquivo.
