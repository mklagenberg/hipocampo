# 0015 — AGENTS.md como arquivo canônico de instrução, CLAUDE.md como ponteiro fino

**Status:** Aceito

## Contexto

Hipocampo desde o início defende operação multi-ferramenta (Claude, ChatGPT, Gemini, GitHub Copilot, Antigravity — ver `docs/USO-MULTI-FERRAMENTA.md`), mas toda instância até a v1.9.0 usa `CLAUDE.md` como o arquivo de instrução operacional primário — nome específico de uma ferramenta, não do padrão. Nesse meio tempo, `AGENTS.md` se consolidou como um padrão aberto real e amplamente adotado: formalizado como especificação em agosto/2025 com participação de OpenAI, Google, Cursor e Factory; doado à Agentic AI Foundation da Linux Foundation em dezembro/2025; mais de 60 mil repositórios e 20+ ferramentas de IA o suportam. Manter só `CLAUDE.md` como fonte de instrução contradiz o próprio princípio de neutralidade de ferramenta que o Hipocampo já defende.

## Decisão

`AGENTS.md` passa a ser o arquivo canônico de instrução operacional de qualquer instância Hipocampo — mesmo papel que `CLAUDE.md` ocupava até a v1.9.0 (invariantes, extensões locais, referência de frontmatter, escopo do repositório). `CLAUDE.md` continua existindo, mas vira um ponteiro fino: poucas linhas, remetendo o agente pra `AGENTS.md` como fonte de verdade. Isso segue o mesmo princípio de divulgação progressiva já usado em outros lugares da metodologia (ex.: skill vs. documento de referência) — o essencial num arquivo pequeno sempre carregado, o resto sob demanda, sem duplicar conteúdo em dois lugares que podem divergir.

Todo repositório de conteúdo (instanciado a partir do `hipocampo-toolkit`) passa a ter `AGENTS.md` como arquivo obrigatório; `CLAUDE.md` continua obrigatório também, mas só como ponteiro. Migração retroativa das instâncias já existentes é responsabilidade de quem opera cada uma — não é automática (mesmo princípio de qualquer mudança MINOR, ver DISCLAIMER.md).

## Racional

Duplicar a instrução operacional em `CLAUDE.md` e `AGENTS.md` recriaria o mesmo risco já identificado no precedente do Second Brain Pessoal (decisão de separar skill de framework, antes do Hipocampo existir): duas fontes da mesma verdade divergem silenciosamente assim que uma é editada e a outra não. Eleger uma delas como canônica e a outra como ponteiro elimina esse risco por construção. `AGENTS.md` é a escolha certa como canônica porque é o padrão que não pressupõe nenhuma ferramenta específica — exatamente o que o Hipocampo já pede de si mesmo.

## Alternativas descartadas

- **Manter só `CLAUDE.md`, sem `AGENTS.md`:** descartada por contradizer o princípio de multi-ferramenta já estabelecido — instâncias operadas por ferramentas que reconhecem `AGENTS.md` nativamente (mais de 20, incluindo várias fora do ecossistema Claude) ficariam sem instrução alguma se o agente não soubesse abrir `CLAUDE.md` por convenção própria.
- **Ter os dois arquivos com conteúdo completo e independente:** descartada pelo risco de divergência silenciosa já descrito.
- **`CLAUDE.md` como canônico, `AGENTS.md` como ponteiro:** descartada — inverteria a lógica de neutralidade de ferramenta; o arquivo tool-specific deveria ser o mais fino dos dois, não o contrário.
