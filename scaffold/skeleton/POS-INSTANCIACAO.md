# Pós-instanciação — checklist de verificação

Este repositório foi gerado por um agente de IA operando a skill Hipocampo, seguindo o profile de scaffold declarado (`hipocampo/scaffold/profiles/pessoal.yaml` ou `empresa.yaml`) — ver `hipocampo/skill/references/instanciacao.md`. O agente já apresentou o plano completo antes de escrever qualquer arquivo (invariante 5) e gerou os outputs declarados no profile. Este checklist existe pra você confirmar que a geração ficou correta antes de guardar qualquer conhecimento real — não é mais um passo a passo manual de instanciação.

## 1. Confirme que o repositório está privado

Não é opcional. É o invariante que sustenta todo o modelo de `visibility` da metodologia (`hipocampo/SPEC.md`, seção 8, invariante 1). O agente deveria ter criado o repositório já como privado — confirme.

## 2. Confirme o LICENSE

O agente deveria ter gerado o `LICENSE` já a partir do template certo (pessoal ou corporativo, `hipocampo/scaffold/license-templates/`), com os placeholders preenchidos a partir dos inputs que você forneceu. Abra o arquivo e confira:

1. Nome/handle (pessoal) ou razão social (corporativo) preenchidos corretamente.
2. Se este repositório for de nível "vault" (só recebe `visibility: confidential`/`restricted`), confirme que só as seções (c) e (d) do template foram mantidas, conforme a nota de ajuste do próprio template.

## 3. Confirme a instalação da skill no seu ambiente de IA

Este repositório de conteúdo **não** carrega uma pasta `skill/` — a skill roda sempre no seu ambiente de IA (Cowork, Claude Code, etc.), por pessoa, nunca por repositório (`hipocampo/decisions/0025-skill-client-side-nunca-por-repositorio.md`). O scaffold nunca gera essa pasta.

1. Confirme que sua cópia pessoal da skill (fonte canônica: [`hipocampo/skill/SKILL.md`](https://github.com/mklagenberg/hipocampo/blob/main/skill/SKILL.md) + `skill/references/*.md`) está instalada no seu ambiente de IA.
2. Confirme que a tabela de roteador de repositórios em `references/personalizacao.md` da sua cópia já inclui **este repositório novo** — o agente deveria ter pedido essa atualização como parte do plano de instanciação; se não pediu, atualize agora.
3. Se você opera mais de uma conta de git que resolvem pro mesmo autor humano, confirme também a tabela de identidade multi-conta no mesmo arquivo — só na sua cópia pessoal, nunca na genérica (`hipocampo/SPEC.md`, seção 12).

## 4. Confirme o AGENTS.md

`AGENTS.md` já deveria ter sido preenchido pelo agente a partir dos inputs coletados antes da geração — não `[preencher: ...]` genérico. Confira:

- **Escopo deste repositório** — os dois campos obrigatórios preenchidos: o **tipo de instância** (`corporativa` ou `pessoal`) e o que deve/não deve ser armazenado aqui.
- **Identidade de autor multi-conta**, se aplicável.
- **Extensões locais a Hipocampo vX.Y** — se não houver nada pra declarar ainda, deve estar registrado como "nenhum ainda", não em branco.
- **Rituais de manutenção** — cadência confirmada (default ou ajuste real desta instância).

## 5. Confirme a versão de compatibilidade

No mesmo `AGENTS.md`, confira a linha "Versão do Hipocampo seguida por esta instância" — deve refletir a versão atual do `hipocampo/SPEC.md` no momento da instanciação, não um valor desatualizado.

## 6. Confirme o manifesto `hipocampo.yaml`

Este repositório deve ter um `hipocampo.yaml` na raiz, gerado pelo agente a partir do profile de scaffold usado — ver `hipocampo/decisions/0033-manifesto-hipocampo-yaml-por-vault.md`. Confira que `instance.domain`, `instance.tier` e `scaffold.profile` refletem corretamente esta instância.

## 7. Apague ou adapte o exemplo

`example/exemplo-nota.md` existe só pra ilustrar o frontmatter — não é conteúdo real. Apague ou adapte antes do primeiro documento de verdade.

## Pronto

A partir daqui, siga `hipocampo/GETTING-STARTED.md` (seções 3 em diante) pra escrever seu primeiro documento e configurar as rotinas (frontmatter audit, REM, auditoria estrutural), já cobertas pela skill que você confirmou no passo 3.
