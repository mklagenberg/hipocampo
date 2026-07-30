# 0021 — Política de cadência de release: acumular antes de lançar, hotfix pra urgência

**Status:** Aceito

## Contexto

A rotina obrigatória de release (DR0014, v1.6.0) já define o que precisa acontecer a cada nova versão (checagem de migração, sincronização do toolkit), mas não diz nada sobre a frequência com que novas versões deveriam ser cortadas. Na prática, entre 2026-07-27 e 2026-07-29, a metodologia publicou dez versões (v1.0.0 a v1.9.0) num intervalo de poucas horas de trabalho contínuo — cada MINOR bump imediatamente virou tag e release publicados. Isso teve uma consequência concreta e já observada: instâncias de conteúdo reais (`hipocampo-company`, `hipocampo-concepts`, `hipocampo-personal-vault`) ficaram presas em `^1.0.0` por nove versões inteiras, porque acompanhar esse ritmo de publicação não é realista pra quem só consome a metodologia.

## Decisão

Trabalho na metodologia (novo Decision Record, mudança de SPEC.md, novo doc) acumula em `main` via PR normal, sem necessariamente virar tag/release imediatamente. Só se corta uma release (tag + GitHub Release publicados) quando houver massa crítica acumulada, ou numa pausa natural de trabalho, a critério de quem mantém a metodologia. `CHANGELOG.md` ganha uma seção `[Não lançado]` no topo, que acumula entradas até o momento da release — só então essas entradas viram uma seção versionada de verdade.

Mudança genuinamente urgente (correção de erro que atrapalha uso corrente, não capacidade nova) sai como PATCH, fora do ciclo normal de acúmulo — release imediata, sem esperar a próxima janela de publicação.

## Racional

SemVer comunica pra quem consome se algo mudou de um jeito que precisa de atenção — isso pressupõe que uma versão publicada teve alguma vida antes da próxima existir. Publicar dez versões em poucas horas não dá esse sinal; dá o sinal oposto (mudança tão rápida que acompanhar é inviável), e isso já causou o problema real de instâncias desatualizadas. Reservar o caminho de PATCH pra urgência genuína preserva a capacidade de corrigir rápido quando precisa, sem exigir que toda mudança pequena vire uma release isolada.

## Alternativas descartadas

- **Manter o ritmo de tag a cada mudança:** descartada pela evidência concreta já observada (nove versões de atraso em instâncias reais).
- **Só permitir release manual, sem nenhum caminho de urgência:** descartada — criaria fricção desnecessária pra correção de erro real que não pode esperar o próximo lote acumulado.
