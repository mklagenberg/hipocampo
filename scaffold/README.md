# scaffold/ — mecanismo de instanciação de vaults

Este diretório é o scaffold da metodologia Hipocampo: os profiles, o esqueleto de arquivos e os templates de LICENSE que um agente usa pra instanciar um repositório de conteúdo novo. Consolidado aqui a partir do antigo repositório `hipocampo-toolkit` (arquivado, `hipocampo/decisions/0032`) — não existe mais um repositório GitHub "template" separado nem o botão "Use this template".

- **`profiles/pessoal.yaml`** / **`profiles/empresa.yaml`** — contrato declarativo de cada instanciação: inputs a coletar, outputs a gerar (com classe de propriedade — `hipocampo/docs/composition-scaffolding-and-distribution.md`), comportamento em conflito, comportamento de upgrade.
- **`skeleton/`** — conteúdo-fonte de cada output declarado nos profiles (`AGENTS.md`, `CLAUDE.md`, `POS-INSTANCIACAO.md`, `registry.md`, `example/exemplo-nota.md`, `hipocampo.yaml`). O agente lê estes arquivos, preenche os placeholders com os inputs coletados, e grava no repositório novo — nunca copia literalmente sem preencher.
- **`license-templates/`** — os dois templates de `LICENSE` (pessoal/corporativo) e a lógica de escolha, migrados do toolkit sem alteração de conteúdo jurídico.

Procedimento operacional completo (quem executa, em que ordem, o que apresentar ao usuário antes de escrever): `hipocampo/skill/references/instanciacao.md`.
