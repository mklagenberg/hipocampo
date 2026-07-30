# 0024 — UPGRADE.md: checklist cumulativa e idempotente de atualização de instância

**Status:** Aceito

## Contexto

Um usuário com instância parada numa versão antiga da metodologia não tinha, até aqui, onde consultar o que fazer pra ficar aderente à versão atual. Os três documentos que tocam o assunto não resolvem: `CHANGELOG.md` é cronológico e exige garimpar manualmente release por release, decidindo sozinho o que é ação necessária; `MIGRATIONS.md` só cobre saltos MAJOR (nenhum ocorreu ainda entre v1.0.0 e v1.9.0, então o arquivo está vazio, o que não significa "nada a fazer"); `POS-INSTANCIACAO.md` só cobre instanciação nova, não atualização de instância existente.

Exercitado concretamente com um caso hipotético (4 repositórios parados em v1.3.0, metodologia em v1.9.0 + não lançado) e confirmado contra um caso real: o repositório `hipocampo-company-vault` (Gauge) está exatamente nessa situação — skill ainda no estágio "stub" (anterior à v1.7.0), `CLAUDE.md` nunca migrado pro `AGENTS.md`, `LICENSE` não verificado. Ninguém tinha um checklist pra aplicar contra ele.

## Decisão

Cria-se `hipocampo/UPGRADE.md`: checklist **cumulativa e idempotente** — "o que uma instância deveria ter, hoje, não importa de onde partiu" — organizada por área (arquivo canônico e skill; licenciamento; rituais de manutenção; privacidade), com cada item marcado **Obrigatório**, **Recomendado** ou **Informativo**, citando a versão em que apareceu e o Decision Record de origem.

Atualização do `UPGRADE.md` vira passo obrigatório da rotina de release (DR0014), na sequência: (1) classificar escopo (DR0023); (2) tag + GitHub Release publicados sempre juntos, no mesmo passo — nunca um sem o outro (fecha a assimetria real encontrada na v1.3.0, que tem tag mas nunca teve Release publicado); (3) mover `CHANGELOG.md` `[Não lançado]` pra seção numerada; (4) sincronizar `hipocampo-toolkit`; (5) atualizar `UPGRADE.md` — toda mudança MINOR que afete instância existente ganha uma linha nova; correção PATCH que revela um bug real de instância (ex.: herança indevida de `LICENSE`, skill nunca instalada) também.

A skill Hipocampo, na checagem de release nova (início de sessão), passa a apontar pro `UPGRADE.md` como próximo passo, em vez de tentar resumir o `CHANGELOG.md` na hora — evita reconstruir esse trabalho manual a cada sessão.

## Racional

Um documento organizado por delta-de-versão ("o que fazer pra ir de 1.3 para 1.4", depois "de 1.4 para 1.5"...) exigiria que o usuário soubesse sua versão exata de partida e navegasse por N seções concatenadas — frágil e cresce sem limite conforme a metodologia evolui. Uma checklist cumulativa e idempotente resolve isso: funciona pra qualquer ponto de partida, inclusive pra quem já fez parte do trabalho manualmente (só confirma o que falta), e não cresce em complexidade de leitura conforme mais versões saem — só cresce em número de itens, que o usuário pode marcar e nunca mais reler.

## Alternativas descartadas

- **Documento por delta de versão.** Descartado pelo motivo acima — frágil e não escala.
- **Deixar a checagem de release nova da skill resumir o `CHANGELOG.md` na hora, via leitura do agente.** Descartado: gera resultado inconsistente entre sessões diferentes (o agente pode resumir de formas diferentes cada vez) e refaz um trabalho de síntese que deveria ser feito uma vez, na release, não repetido a cada sessão de cada usuário.
