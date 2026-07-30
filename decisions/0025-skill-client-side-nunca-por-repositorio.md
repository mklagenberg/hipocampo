# 0025 — A skill roda client-side, por pessoa/ambiente de IA — nunca por repositório

**Status:** Aceito

## Contexto

Toda instância de conteúdo carregava uma pasta `skill/` própria, copiada automaticamente pelo mecanismo "Use this template" do GitHub a partir do `hipocampo-toolkit` — não por uma decisão deliberada de arquitetura. Essa cópia nunca teve efeito funcional: uma skill só existe operacionalmente quando instalada no ambiente de IA de quem opera (via `save_skill` ou mecanismo equivalente da ferramenta) — nenhum agente varre repositórios do GitHub em busca de um `SKILL.md` pra ativar automaticamente. A cópia dentro do repositório sempre foi um arquivo markdown inerte.

Essa duplicação gerou confusão real, levantada por Mau ao questionar diretamente: "isso vai gerar confusão, não? Se eu instalar a skill aqui no Cowork, ele também vai usar a skill lá do repo?" A resposta é não — mas o próprio `POS-INSTANCIACAO.md` já precisava avisar explicitamente pra não editar o arquivo dentro do repositório "como se isso já a ativasse", sintoma de que o desenho anterior convidava ao erro. Auditando os 4 repositórios de conteúdo reais (ver correções via `UPGRADE.md`), nenhum deles jamais teve uma skill de fato instalada — todos carregavam só o `SKILL-STUB.md` original do template, nunca substituído.

## Decisão

A skill Hipocampo tem exatamente **um** lugar onde existe de forma operante: o ambiente de IA da pessoa que opera a instância, instalada (personalizada, com roteador de repositórios preenchido) a partir do template canônico em `hipocampo-toolkit/skill/SKILL.md` + `references/`. Repositório de conteúdo **nunca** carrega cópia própria da skill — a pasta `skill/` deixa de fazer parte do escopo esperado de uma instância de conteúdo.

`hipocampo-toolkit/POS-INSTANCIACAO.md`, passo 3, passa a instruir: apagar a pasta `skill/` herdada do template logo após instanciar (é resíduo do "Use this template", nunca funcional), e instalar a skill personalizada diretamente a partir do `hipocampo-toolkit`, referenciando o repositório novo no roteador de repositórios.

O `hipocampo-toolkit` continua carregando `skill/SKILL.md` + `references/` na própria raiz — ali faz sentido, porque é a fonte canônica de distribuição, não uma instância de conteúdo.

## Racional

Manter uma cópia "decorativa" da skill em cada repositório de conteúdo tem só custos, nenhum benefício real: (1) sugere um modelo mental errado — "cada repo tem sua skill" — quando o modelo correto é "uma skill por pessoa/ambiente, operando sobre N repositórios via roteador"; (2) cria superfície de drift adicional (cópia no toolkit, cópia em cada repo, cópia instalada no client — três lugares em vez de dois); (3) na prática, levou ao mesmo resultado nos 4 repositórios reais auditados: a cópia nunca foi atualizada além do stub original, porque ninguém tinha motivo real pra mexer nela.

## Alternativas descartadas

- **Manter a cópia no repositório como "referência read-only" documentando qual versão da skill estava em uso quando o repo foi sincronizado.** Descartado: essa informação já é capturada pela declaração de versão do Hipocampo no `AGENTS.md` — não precisa de uma cópia inteira do `SKILL.md` só pra isso.
- **Adicionar aviso mais forte dentro do arquivo, em vez de remover a pasta.** Descartado: o aviso já existia (`POS-INSTANCIACAO.md`) e não impediu que os 4 repositórios reais nunca tivessem a skill instalada — o problema é estrutural, não de comunicação.
