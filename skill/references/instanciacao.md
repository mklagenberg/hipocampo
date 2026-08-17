# Instanciar um vault novo — a skill é o mecanismo

Não existe mais um botão "Use this template" (`hipocampo-toolkit` foi consolidado e arquivado, `decisions/0032`). O agente operando esta skill é o próprio mecanismo de instanciação — segue este procedimento em vez de apontar o usuário pro GitHub.

## Procedimento

1. **Escolha o profile.** `hipocampo/scaffold/profiles/pessoal.yaml` (domínio pessoal, `decisions/0002`) ou `hipocampo/scaffold/profiles/empresa.yaml` (domínio empresa). Se não estiver óbvio pelo pedido do usuário, pergunte.
2. **Colete os `inputs` declarados no profile** diretamente com o usuário — nome do repositório, `tier` (`confidencial` ou `público`, `decisions/0029`), e a identidade do titular (nome completo + `@usuario-github` no domínio pessoal; razão social no domínio empresa). Nunca assumir um valor que o profile marca como obrigatório.
3. **Apresente o plano completo antes de qualquer escrita** — todos os `outputs` que serão criados, com os valores que vão entrar em cada um (invariante 5, `SPEC.md` seção 8). Só prossiga depois de confirmação explícita.
4. **Crie o repositório** (privado — nunca público, invariante 1) e gere cada arquivo declarado em `outputs`, lendo o conteúdo-fonte de `hipocampo/scaffold/skeleton/` e `hipocampo/scaffold/license-templates/`, preenchendo os placeholders com os `inputs` coletados. Respeite a classe de ownership de cada output (`canonical-reference`/`generated-once`/`managed-structure`/`user-authored`, declarada no profile) — não é preciso decidir de novo o que cada arquivo é.
5. **Se algum output já existir no destino** (repositório reaproveitado, não vazio), pare e relate — nunca sobrescreva silenciosamente (`conflicts.default: stop-and-report`, mesmo comportamento em todos os profiles).
6. **Depois de gerar tudo, aponte o usuário pro `POS-INSTANCIACAO.md`** gerado na raiz do novo repositório — funciona agora como checklist de verificação (confirmar que cada passo saiu certo), não mais como passo a passo manual do zero.

## Exemplo

> Usuário: "cria um vault novo, corporativo, pra Gauge"
>
> Agente: profile `empresa.yaml`, tier a perguntar ("confidencial ou público?"). Usuário: "confidencial". Agente coleta razão social, apresenta o plano (nome do repo, `LICENSE-corporativo` preenchido, `AGENTS.md` com "Tipo de instância: corporativa", `hipocampo.yaml` com `domain: empresa`/`tier: confidencial`), aguarda confirmação, cria o repositório privado e os arquivos, depois aponta pro `POS-INSTANCIACAO.md` gerado pra revisão final.
