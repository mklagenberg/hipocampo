# Change Set — 0032/0033: scaffolding consolidado e manifesto hipocampo.yaml por vault

## Resumo

Consolida o mecanismo de instanciação de vaults (antes `hipocampo-toolkit`, repositório GitHub separado) dentro de `hipocampo/scaffold/`, como scaffold declarativo conforme MODA; introduz o manifesto `hipocampo.yaml`, que todo vault gerado passa a carregar.

## Classe

**normative** — introduz um novo artefato normativo (o schema do `hipocampo.yaml`, `decisions/0033`) e uma mudança de mecanismo que afeta como todo vault futuro é criado (`decisions/0032`); não é só uma correção editorial nem uma operação isolada de rotina.

## Semver

**minor** (consistente com o restante do trabalho de adequação ao MODA nesta fase — o salto pra MAJOR/2.0.0 é acumulado ao final de todas as fases, não decidido fase a fase; mesma lógica de `decisions/0031`).

## Gatilhos disparados

| Gatilho | Disparado? | Nota |
|---|---|---|
| `regra_normativa` | Sim | `decisions/0032` e `decisions/0033` são normas novas. |
| `schema_frontmatter` | Não | Não altera o schema de frontmatter de documento — só introduz um manifesto de repositório, fora do escopo de frontmatter. |
| `mecanismo_cross_repositorio` | Não | `registry.md`/`$alias:` não são afetados. |
| `politica_dados_sensiveis` | Não | Não altera a política de dados sensíveis nem sua variante por tipo de instância. |
| `release` | Reservado | Avaliado no fechamento do release v2.0.0, não neste Change Set isolado. |

## Impacto

Ver `impact.yaml`.

## Status

`implemented` — as mudanças descritas aqui já foram executadas nesta mesma PR (Fase D), não é uma proposta futura.
