# 0014 — Rotina obrigatória a cada release da metodologia

**Status:** Aceito

## Contexto

Até esta rodada, releases da metodologia (v1.0.0 até v1.5.0) sempre atualizaram `SPEC.md`/`CHANGELOG.md`/`README.md`, mas o `hipocampo-toolkit` nunca foi sincronizado — seu `CLAUDE.md` ainda declarava "Versão do Hipocampo seguida: ^1.0.0" mesmo cinco releases MINOR depois. Além disso, `MIGRATIONS.md` nunca ganhou conteúdo real correspondente a nenhuma dessas releases — todas foram MINOR, que não exige migração ativa, mas não há registro de que essa checagem tenha sido feita conscientemente a cada vez, só o fato de nenhuma delas ter sido MAJOR até agora. Sem uma rotina formal, ambos os passos ficam dependentes de alguém lembrar manualmente — e, na prática, isso já falhou uma vez (o `CLAUDE.md` do toolkit).

## Decisão

Toda vez que uma nova versão do `SPEC.md` for publicada, antes de considerar o release completo:

1. **Checagem de migração.** Se a versão for MAJOR: `MIGRATIONS.md` ganha uma entrada nova com o guia de migração da versão anterior para essa. Se for MINOR ou PATCH: confirmar explicitamente — mesmo que a conclusão seja "nenhuma ação necessária" — que não há necessidade de migração ativa, e registrar essa conclusão no próprio PR/commit do release, não pular a checagem silenciosamente.
2. **Sincronização do `hipocampo-toolkit`.** Revisar e atualizar `CLAUDE.md` (compatibilidade declarada, ex. "^1.5.0") e qualquer outro arquivo do toolkit afetado por invariante novo, seção nova, ou convenção default nova do `SPEC.md`.
3. **Tag/release de git.** Criar a tag correspondente à nova versão — hoje um passo manual do responsável pela metodologia, fora do alcance das ferramentas de escrita disponíveis via MCP.

## Racional

Um release da metodologia que não sincroniza o toolkit deixa quem instancia um repositório novo com uma declaração de compatibilidade desatualizada desde o primeiro commit da instância — exatamente o que aconteceu nesta rodada. Formalizar a checagem, mesmo para o caso "nenhuma ação necessária", evita que o hábito de pular a checagem se instale silenciosamente; é mais barato registrar uma checagem negativa do que descobrir, várias versões depois, que ninguém andou checando nada.

## Alternativas descartadas

- **Deixar como está, checagem ad hoc.** Descartada: gerou exatamente a divergência que motivou esta decisão — `CLAUDE.md` do toolkit parado em "^1.0.0" por cinco releases MINOR seguidas.
- **Automatizar completamente via CI/webhook.** Descartada por ora: está fora do escopo do ferramental disponível hoje (as ferramentas de escrita via MCP não criam tags nem workflows de CI), e decisões sobre o que precisa propagar para o toolkit a cada release ainda exigem julgamento — não são puramente mecânicas a ponto de dispensar revisão.
