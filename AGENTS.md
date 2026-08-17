# Instruções para agentes

Hipocampo é um repositório de metodologia, público. Este arquivo é o entry point canônico de agente pra quem contribui **na metodologia em si** — distinto do `AGENTS.md` que cada instância de conteúdo (vault) usa pra si mesma, e que o Hipocampo especifica pra outros (`SPEC.md`, seção 11). Se você chegou aqui tentando operar um vault (salvar conhecimento, rodar um ritual), o arquivo certo é o `AGENTS.md` daquele repositório de conteúdo, não este.

## Comece pelo mapa

Carregue só o contexto necessário pra tarefa atual:

1. Leia `README.md` pra identidade e navegação do repositório.
2. Leia `SPEC.md` pra especificação normativa completa.
3. Leia `moda.yaml` pra identidade legível por máquina e estado de conformidade com o MODA.
4. Leia a Decision Record relevante em `decisions/` antes de mudar qualquer regra já existente.
5. Leia `ROADMAP.md` quando a mudança afetar direção ou introduzir capacidade nova.
6. Leia `CHANGELOG.md` e `UPGRADE.md` antes de mudar comportamento já lançado.
7. Leia `conformance/moda.yaml` e a auditoria mais recente em `audits/moda/` antes de mudar estrutura que afete conformidade com o MODA.

Não transforme este arquivo numa enciclopédia. Conhecimento detalhado vive nos documentos linkados.

## Disclosure MODA

<!-- moda:disclosure:start -->
Este repositório está sendo estruturado e avaliado com o [MODA](https://github.com/mklagenberg/moda) — um framework aberto para organizar, desenhar, auditar, empacotar e evoluir metodologias agênticas.

Antes de mudar a estrutura da metodologia, leia `moda.yaml`, `conformance/moda.yaml`, e a auditoria mais recente em `audits/moda/`. Não alegue conformidade sem evidência produzida contra a versão declarada do MODA — hoje a relação declarada é `audited_against` (retrospectiva, `claim_stage: mapped`, `conformance_result: partial`), não `conforms_to`. Não migre estrutura silenciosamente.
<!-- moda:disclosure:end -->

## Regras de trabalho

- Preserve a distinção entre metodologia, framework, método, processo, procedimento, workflow, padrão, prompt, skill, toolkit e implementação (SPEC MODA, seção 3) — o próprio `SPEC.md` já usa essas distinções de forma consistente, mesmo sem as palavras-chave RFC 2119 explícitas do MODA.
- Trate o repositório como sistema de registro. Não trate uma conversa não registrada como única fonte de intenção durável — decisão estrutural sempre vira Decision Record.
- Aponte pra evidência; não copie regra normativa pra dentro de mapeamento de conformidade ou relatório de auditoria.
- Prefira validação determinística quando ela existir — hoje não existe nenhuma pro próprio repositório de metodologia (achado `major` da auditoria de 2026-08-17, `audits/moda/`); até isso ser resolvido (ver `ROADMAP.md`), toda mudança estrutural depende de revisão humana explícita.
- Exija direção humana pra intenção não resolvida, aceitação de risco, ação destrutiva, efeito colateral externo, fronteira de segurança, e migração incompatível — mesmo princípio do invariante 5 do `SPEC.md` (seção 8), aplicado aqui à metodologia em si, não só às instâncias que ela especifica.
- Nunca relate fonte, teste, link ou auditoria como checado quando não foi checado de fato.

## Protocolo de mudança

- Classifique o trabalho como editorial, operacional ou normativo antes de implementar (vocabulário do MODA). O mecanismo formal de Change Set (`changes/<id>/proposal.md` + `impact.yaml`) existe desde a Fase C (`docs/change-management.md`, `decisions/0031-mecanismo-de-change-set.md`) e é **obrigatório** pra mudança `operational`/`normative` a partir daquele ponto: um Change Set novo em `changes/<id>/`, acompanhando a Decision Record (quando envolve escolha estrutural) e as seções correspondentes de `SPEC.md`/`CHANGELOG.md`, todos atualizados na mesma PR. Mudança `editorial` não exige Change Set.
- Mude a especificação normativa (`SPEC.md`) primeiro quando a obrigação mudar.
- Use branch de vida curta e PR pra mudança normal; mantenha `main` como única branch de integração permanente.
- Atualize `CHANGELOG.md` pra mudança de comportamento ou contrato notável.
- Registre escolha estrutural durável em `decisions/`.
- Atualize `ROADMAP.md` quando a direção mudar; nunca use como backlog de tarefa ou changelog.
- Atualize `UPGRADE.md` pra ação de adoção exigida por release compatível pra trás.
- Atualize `MIGRATIONS.md` pra mudança incompatível.
- Quando operar só via MCP, sem capacidade de criar tag/release, forneça ao humano a tag exata, branch alvo, commit, título, descrição derivada do changelog, e classificação de release pra criação após aprovação — nunca alegue que a tag ou release existe. Ver `SPEC.md`, seção 9, e `decisions/0014-rotina-obrigatoria-de-release.md`.

## Versionamento

Hipocampo segue [SemVer](https://semver.org/lang/pt-BR/) — critério operacional completo em `SPEC.md`, seção 9, e `decisions/0023-criterio-operacional-escopo-semver.md`.

## Conclusão

Uma mudança só está completa quando:

- a intenção e o escopo estão explícitos;
- a Decision Record relevante (quando aplicável), o Change Set (quando `operational`/`normative`) e as seções correspondentes de `SPEC.md`/`CHANGELOG.md` estão sincronizados na mesma PR;
- nenhum achado crítico conhecido fica escondido;
- documentação afetada e disclosures gerados estão sincronizados;
- nenhuma alegação de conformidade MODA vai além do que a evidência em `conformance/moda.yaml` sustenta.
