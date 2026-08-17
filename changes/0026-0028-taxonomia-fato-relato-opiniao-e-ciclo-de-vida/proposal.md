# Taxonomia fato/relato/opinião/lembrança + ciclo de vida cross-repositório (Promote/Depromote/Redbutton)

**Nota:** Change Set retroativo (backfill), criado depois da implementação e do merge (PR #22, 2026-08-17) — primeiro exercício do mecanismo de Change Set adotado em `decisions/0031`. O trabalho real já foi revisado e mesclado antes deste documento existir; ele reconstrói a proposta e o impacto pra validar o template, não pra reabrir a decisão.

## Problema

Hipocampo não tinha vocabulário formal pra distinguir informação verificada de opinião/lembrança pessoal dentro de um documento de instância corporativa — risco de responsabilização pessoal indevida sem sinalização clara. Também não existia mecanismo formal pra mover ou remover conteúdo entre repositórios de uma mesma pessoa/organização (reclassificação pessoal↔corporativo, correção de nível de confidencialidade, remediação de violação de política) — só o CRUD de um único repositório (seção 2-B).

## Contrato atual

`SPEC.md` seção 2 não distinguia tipo de informação dentro do corpo de um documento. Seção 8 cobria só o CRUD de um repositório único; não existia ação formal pra mover conteúdo entre repositórios do mesmo titular, nem pra apagar fisicamente conteúdo que violasse a política de dados sensíveis (seção 2-A) fora do gatilho estreito de solicitação legal (`decisions/0010`).

## Contrato proposto

- Taxonomia de quatro tipos de informação (**Fato**, **Relato**, **Opinião**, **Lembrança**) + campo `contains_subjective_content`, com gate de confirmação explícita antes de gravar Opinião/Lembrança nova em instância corporativa (`decisions/0026`).
- Três ações de ciclo de vida cross-repositório — Promote (pessoal → corporativo, dois caminhos), Depromote (downgrade intra-domínio), Redbutton (remediação de violação de política) — complementares ao CRUD existente (`decisions/0027`).
- Gatilho de apagamento físico (`decisions/0010`) ampliado pra também cobrir violação confirmada da política de dados sensíveis identificada por auditoria estrutural ou pelo operador, não só solicitação legal formal (`decisions/0028`).

## Alternativas

- **Tratar Opinião/Lembrança como Fato sem distinção.** Descartada — perde o sinal de risco de responsabilização pessoal que motivou a mudança.
- **Resolver reclassificação cross-repo com edição manual ad-hoc, sem ação nomeada.** Descartada — sem `related`/`superseded_by` consistente, quebra rastreabilidade e a disciplina de "documento nunca apagado fisicamente" (invariante 3).
- **Gatilho de apagamento restrito só à solicitação legal formal.** Descartada — deixava violação de política encontrada por auditoria sem remediação formal, mesmo sem pedido do titular.

## Riscos

- Confusão entre `contains_subjective_content` e `visibility`: mitigado por texto explícito em `SPEC.md` seção 2 distinguindo os dois campos.
- Uso indevido de Redbutton pra remover conteúdo só incômodo, não violador: mitigado por decisão humana sempre explícita e escopo estreito (reservado a violação real de política ou risco legal).

## Critério de aceitação

- [x] `SPEC.md` seção 2 documenta a taxonomia de quatro tipos e `contains_subjective_content`.
- [x] `SPEC.md` seção 13 documenta Promote/Depromote/Redbutton.
- [x] `SPEC.md` seção 8 documenta o gatilho ampliado de apagamento físico.
- [x] `CHANGELOG.md` registra as três mudanças em `[Não lançado]`.
- [x] `decisions/0026`, `0027`, `0028` mescladas.

## Compatibilidade e migração

Aditivo — nenhuma instância existente fica formalmente incompatível sem essas ações (teste da `decisions/0023`). Escopo MINOR isoladamente; entra no pacote de mudanças acumuladas rumo à v2.0.0 por decisão de acúmulo (`decisions/0021`), não porque force MAJOR sozinho.

## Recuperação

Reverter os três commits de decision + as seções correspondentes de `SPEC.md`/`CHANGELOG.md` seria a via de rollback, caso necessário — não há adopter migrado dependendo disso ainda (trabalho recente, não lançado).
