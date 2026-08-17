# 0031 — Adoção do mecanismo de Change Set (MODA)

**Status:** Proposto

## Contexto

Achado major 5 da auditoria MODA de 2026-08-17 (`audits/moda/2026-08-17-v1.0.0-self-audit.md`): Hipocampo não tinha nenhum mecanismo formal de proposta+impacto antes de implementar mudança operacional/normativa — `decisions/0014` (rotina de release), `decisions/0021` (cadência), `decisions/0023` (critério SemVer) cobrem cadência e classificação de escopo, mas não declaram gatilhos, superfícies afetadas, ou validação por mudança individual antes de implementar. O próprio MODA formaliza esse mecanismo (`docs/change-management.md` deles, `changes/<id>/`) como parte do contrato de repositório (SPEC MODA, seções 4.16 e 5.5).

## Decisão

Adotar o mecanismo de Change Set do MODA, adaptado ao Hipocampo em `docs/change-management.md`: classes `editorial`/`operational`/`normative` (vocabulário do MODA, mantido em inglês — ver racional); Change Set obrigatório em `changes/<change-id>/` (`proposal.md` + `impact.yaml`) pra mudança `operational`/`normative`; tabela de gatilhos adaptada ao vocabulário real do Hipocampo (`regra_normativa`, `schema_frontmatter`, `mecanismo_cross_repositorio`, `politica_dados_sensiveis`, `release`) em vez de copiar literalmente os gatilhos do MODA — `package_contract`, por exemplo, não tem equivalente real no Hipocampo hoje, porque não existe conceito de pacote empacotado e distribuído neste repositório ainda.

Change Set não substitui Decision Record — os dois continuam coexistindo com escopos diferentes (Change Set = impacto desta mudança específica; DR = a escolha durável em si, mesma distinção de propósito já em uso entre Decision Record e `type: decision`, `SPEC.md` seção 7).

Primeiro exercício do mecanismo: backfill retroativo de `changes/0026-0028-taxonomia-fato-relato-opiniao-e-ciclo-de-vida/` cobrindo o PR #22 (já mesclado antes deste mecanismo existir) — valida o template contra trabalho real já revisado, antes de exigi-lo prospectivamente. PRs #23 e #24 (também mesclados antes deste mecanismo existir) não recebem backfill — só o PR #22 serve como exercício de validação do template, proporcional ao objetivo de validar o mecanismo, não de reescrever retroativamente todo o histórico recente.

## Racional

Fechar o achado major 5 sem inventar um mecanismo próprio do zero — reaproveitar o desenho do MODA (que já resolveu exatamente esse problema, com trigger rules e status de impacto testados na própria adoção deles) é mais barato e mais consistente do que desenhar algo novo. Adaptar (não copiar) a tabela de gatilhos evita declarar superfícies que não existem no Hipocampo hoje (`schemas/`, `scripts/`, `skill/` como pastas do próprio repositório — a skill vive em `hipocampo-toolkit`, fora deste repositório, até a Fase D consolidar).

## Alternativas descartadas

- **Mecanismo próprio, desenhado do zero.** Descartada — reinventaria um problema que o MODA já resolveu, sem ganho real; o vocabulário do MODA (`editorial`/`operational`/`normative`) já é preciso o suficiente.
- **Traduzir as classes pro português.** Descartada — "operacional"/"normativo" traduzem bem, mas "editorial" em português carrega conotação de opinião/parecer que não existe no termo original (mudança de wording/formatação); manter o termo técnico em inglês evita esse ruído, mesmo com o resto do repositório em português (será revisitado quando a Fase E traduzir o repositório inteiro).
- **Backfill retroativo de todos os PRs mesclados até aqui (#22, #23, #24).** Descartada — desproporcional ao objetivo de validar o template; só o PR #22 foi explicitamente escolhido como exercício no plano de release 2.0.0.
