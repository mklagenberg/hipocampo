# Hipocampo — Migrations

Guia de migração para cada salto MAJOR de versão (SemVer — ver SPEC.md, seção 9, e DISCLAIMER.md).

Migração MINOR e PATCH não exige ação — ver DISCLAIMER.md, seção "Versionamento e o que isso significa pra você". Este arquivo só documenta saltos MAJOR, que exigem migração ativa por definição.

## Como usar este documento

Cada instância declara, no próprio `CLAUDE.md`/README, a versão ou faixa de compatibilidade que implementa. Quando uma versão MAJOR nova é liberada, encontre aqui a seção correspondente ao salto que você precisa dar (por exemplo, "1.x → 2.0") antes de atualizar a declaração de versão da sua instância.

## Histórico de saltos MAJOR

Nenhum salto MAJOR ainda ocorreu. A versão inicial é 1.0.0 — não há migração a documentar até a primeira mudança incompatível.

Quando o primeiro salto MAJOR acontecer, a seção correspondente aqui vai seguir este formato:

```markdown
## 1.x → 2.0

**O que quebrou:** [resumo direto]
**Por quê:** [link pro Decision Record em decisions/ que motivou a mudança]
**Passo a passo:**
1. ...
2. ...
**Como saber se sua instância já pode migrar:** [checklist]
```
