# 0023 — Critério operacional de escopo SemVer (MAJOR/MINOR/PATCH)

**Status:** Aceito

## Contexto

SPEC.md, seção 9, define MAJOR/MINOR/PATCH em termos abstratos (quebra compatibilidade / capacidade nova compatível / clarificação-correção), mas nunca ofereceu um teste prático pra aplicar essa definição a uma mudança concreta — cada release decidia o escopo por julgamento solto. Isso ficou evidente ao exercitar, pela primeira vez, um guia de atualização real (ver DR0024): pra classificar cada mudança entre v1.3.0 e v1.9.0 como "ação necessária" ou "só informativo", foi preciso aplicar um teste que não estava escrito em lugar nenhum — só existia informalmente na cabeça de quem decidia.

## Decisão

Toda mudança aceita na metodologia é classificada por este teste, antes de entrar na rotina de release (DR0014):

- **MAJOR:** uma instância existente, sem nenhuma ação, passa a estar formalmente **incompatível** com a versão nova (campo obrigatório renomeado/removido, mecanismo eliminado, regra que a instância já seguia deixa de ser válida).
- **MINOR:** capacidade nova, aditiva — uma instância existente **continua válida sem nenhuma ação**, ainda que fique "atrasada" em relação à capacidade nova disponível (exemplo real: a seção 11, `AGENTS.md` como arquivo canônico, é MINOR — nenhuma instância que ainda usa só `CLAUDE.md` está quebrada por isso).
- **PATCH:** clarificação ou correção que não muda schema nem introduz comportamento novo (exemplo real: DR0022, que fecha uma lacuna de rastreabilidade sem criar capacidade nova).

Este teste é aplicado como primeiro passo da rotina obrigatória de release (DR0014), antes de qualquer outro passo — a classificação de escopo determina, entre outras coisas, se a mudança precisa de entrada no `MIGRATIONS.md` (só MAJOR) e/ou no `UPGRADE.md` (MINOR/PATCH com ação recomendada, ver DR0024).

## Racional

Classificação inconsistente de escopo entre releases diferentes propaga erro adiante: se uma mudança MINOR for tratada como MAJOR, gera trabalho de migração desproporcional; se uma mudança que deveria gerar uma recomendação de atualização for tratada como "só informativa", ela nunca chega ao `UPGRADE.md` e nenhuma instância existente fica sabendo que deveria adotá-la. O teste "quebra ou só fica atrasado?" é simples o suficiente pra aplicar de forma consistente sem exigir julgamento caso a caso.

## Alternativas descartadas

- **Manter em aberto, decidir caso a caso.** Descartado — foi exatamente essa ambiguidade que motivou o levantamento que originou este DR.
- **Um quarto nível de escopo (ex.: "MINOR forte" vs. "MINOR fraco") pra capturar a diferença entre capacidades novas triviais e estruturais (como o `AGENTS.md`).** Descartado por ora: o SemVer de três níveis já é suficiente desde que o `UPGRADE.md` (DR0024) carregue a granularidade de "quão recomendado" cada item é — não precisa de um quarto nível formal no versionamento em si.
