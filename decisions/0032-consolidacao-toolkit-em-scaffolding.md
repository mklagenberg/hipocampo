# 0032 — Consolidação do hipocampo-toolkit em scaffolding declarativo

**Status:** Aceito

## Contexto

O repositório `hipocampo-toolkit` existia como template GitHub separado ("Use this template"), carregando o esqueleto de arquivos que um repositório de conteúdo novo precisa (`AGENTS.md`, `CLAUDE.md`, `POS-INSTANCIACAO.md`, `LICENSE`, `registry.md`, `example/`, e uma cópia da skill dentro de `skill/`) além dos templates de `LICENSE`. Essa topologia — metodologia normativa (`hipocampo`) e mecanismo de distribuição/scaffold (`hipocampo-toolkit`) em repositórios distintos — nunca foi avaliada contra o MODA.

O MODA normatiza scaffold e distribuição em `docs/composition-scaffolding-and-distribution.md`, exigindo que qualquer mecanismo de scaffold declare, por profile: versão do engine, inputs, outputs com classe de propriedade (`canonical-reference`/`generated-once`/`managed-structure`/`user-authored`), comportamento em conflito e comportamento de upgrade. Isso é exatamente o que faltava no `hipocampo-toolkit` — ele funcionava, mas via um mecanismo totalmente implícito (o botão nativo do GitHub), sem nenhuma dessas declarações.

Adicionalmente, o próprio `hipocampo-toolkit` continha um problema estrutural conhecido: a pasta `skill/` copiada por "Use this template" pra dentro de cada repositório de conteúdo novo nunca teve efeito nenhum (a skill roda client-side, por pessoa — `decisions/0025`) — e o próprio `POS-INSTANCIACAO.md` do toolkit já instruía o usuário a apagá-la manualmente. Era ruído estrutural que o próprio processo reconhecia como erro, mas nunca corrigia na origem.

## Decisão

Consolidar o conteúdo do `hipocampo-toolkit` dentro do próprio repositório `hipocampo`, em `scaffold/`, como um scaffold declarativo conforme MODA:

- **Dois profiles por domínio** (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`), não por tier — o esqueleto gerado não difere por tier (`conteudo`/`vault`), só o `LICENSE` recebe um ajuste documentado (seções mantidas). `tier` é um input declarado no profile, não um profile separado.
- **`scaffold/skeleton/`** guarda o conteúdo-fonte de cada output declarado, migrado do toolkit com dois ajustes: (a) a pasta `skill/` deixa de ser gerada — não existe mais esse resíduo; (b) `POS-INSTANCIACAO.md` é reformulado de passo-a-passo manual para checklist de verificação pós-geração (ver racional).
- **A skill (`skill/`, antes só no toolkit) migra pra dentro do próprio `hipocampo`**, como componente de metodologia — deixa de ter lifecycle `independent` no `moda.yaml` (era um componente hospedado num repositório GitHub separado) e passa a `embedded`.
- **Sem o botão "Use this template"** (consequência de arquivar o toolkit), a instanciação de um vault novo passa a ser **executada pelo agente**: a skill lê o profile, coleta os inputs do usuário, apresenta o plano completo antes de escrever (invariante 5), cria o repositório novo e gera cada output declarado — sem nenhum mecanismo de templating nativo do GitHub envolvido. Procedimento completo: `skill/references/instanciacao.md`.
- **`hipocampo-toolkit` é arquivado** no GitHub (repositório real, ação manual — nenhuma ferramenta disponível neste ambiente automatiza esse passo) e recebe, antes do arquivamento, um `README.md` de redirecionamento apontando pra `hipocampo/scaffold/`.
- Todos os pontos de referência existentes que citavam `hipocampo-toolkit` (`README.md`, `GETTING-STARTED.md`, `UPGRADE.md`, `AGENTS.md`, `moda.yaml`) são atualizados pra apontar pro novo `scaffold/`.

## Racional

Consolidar resolve dois problemas de uma vez: (1) alinha o mecanismo de scaffold ao contrato declarativo do MODA, tornando explícito o que hoje era implícito no clique de um botão; (2) remove o ruído estrutural da pasta `skill/` residual, que nunca funcionou e cujo próprio checklist manual já reconhecia como erro.

A perda do botão "Use this template" é uma consequência operacional real, não cosmética — mas a alternativa de manter um repositório template mínimo separado só pra preservar o clique reintroduziria o mesmo problema de fundo (mecanismo implícito, sem declaração de inputs/outputs/conflitos) que este DR busca eliminar. Optar por agente executando o scaffold, em vez de manter um clique nativo ou de exigir um checklist manual completo, foi decisão explícita do Mau (não do agente) diante desse trade-off.

`POS-INSTANCIACAO.md` deixa de ser passo-a-passo porque o agente já executa os passos que antes eram manuais (marcar privado, trocar LICENSE, preencher AGENTS.md) como parte da própria geração — o arquivo sobra como checklist de verificação humana do que o agente gerou, não como instrução de execução.

## Alternativas descartadas

- **Manter `hipocampo-toolkit` como está, só documentando-o no `moda.yaml`.** Descartada: não resolve o problema de fundo (mecanismo de scaffold implícito, pasta `skill/` residual) — só declara formalmente uma lacuna que o MODA pede pra ser fechada.
- **Criar um repositório template mínimo novo, sem a pasta `skill/`, mantendo dois repositórios.** Descartada nesta rodada: preservaria o clique nativo do GitHub, mas ainda deixaria o scaffold sem declaração de inputs/outputs/conflitos — o problema normativo persistiria, só a superfície visível (a pasta `skill/`) seria corrigida.
- **Checklist manual completo, sem agente executando nada.** Descartada por decisão explícita do Mau — o agente já tem acesso ao GitHub MCP e já executa esse tipo de operação em outros contextos (criação de branches, push de arquivos, PRs); exigir um checklist manual joga fora essa capacidade sem necessidade.
