# Roadmap

Última revisão: **2026-08-17**

Este roadmap comunica direção, não promessa de data. Só um plano de release aprovado ou marco formal cria compromisso de entrega. Trabalho detalhado vive em Decision Records e PRs; trabalho concluído vive no `CHANGELOG.md`.

## Agora

### Adequação da metodologia ao MODA — rumo à v2.0.0

**Resultado:** Hipocampo declara e sustenta com evidência real uma relação formal de conformidade com o [MODA](https://github.com/mklagenberg/moda) — hoje `audited_against`/`mapped`/`partial` (ver `moda.yaml`, `conformance/moda.yaml`), evoluindo pra `conforms_to` conforme os achados `major` da auditoria de 2026-08-17 (`audits/moda/`) forem endereçados.

**Status:** em andamento — taxonomia de tipo de repositório (`decisions/0029`/`0030`) e fundação declarativa (`moda.yaml`, `AGENTS.md`, este `ROADMAP.md`) já mescladas; mecanismo de Change Set, validação determinística, consolidação do `hipocampo-toolkit` em scaffolding, tradução pra inglês, e as dimensões de design ainda faltantes (falha/recuperação, qualidade/avaliação) seguem pendentes.

O trabalho inclui:

- mecanismo de Change Set (`changes/<id>/proposal.md` + `impact.yaml`), com backfill retroativo do PR #22 como primeiro exercício;
- validação determinística mínima (script + CI) da integridade estrutural do próprio repositório de metodologia;
- consolidação do `hipocampo-toolkit` dentro do `hipocampo` como scaffolding formal (perfis declarando engine version, inputs, outputs, classe de ownership de arquivo), incluindo a skill genérica;
- manifesto por vault (`hipocampo.yaml`) pra todo repositório de conteúdo instanciado, com estado de sincronização (`current`/`update-available`/etc.);
- tradução completa do repositório `hipocampo` (só a metodologia, não os vaults nem a cópia pessoal de skill) pra inglês, com stub de redirecionamento em todo caminho de `decisions/` traduzido;
- seção nova de comportamento sob falha (evidência insuficiente, contradição, ferramenta indisponível, interrupção, pedido inseguro, migração incompatível);
- cenários representativos mínimos de avaliação;
- casos de uso documentados;
- `MIGRATIONS.md` ganhando sua primeira entrada real ("1.x → 2.0") e corte da tag `v2.0.0`.

A release fica bloqueada até o gate de release da própria metodologia (`SPEC.md`, seção 9, e `decisions/0014`/`0021`/`0023`) passar e ser aprovado explicitamente por Mau.

## Depois

### Validação determinística contínua

**Resultado:** toda PR contra `main` roda automaticamente checagem de template de Decision Record, links internos, e consistência versão declarada ↔ `CHANGELOG.md`, sem depender de revisão manual pra achar esse tipo de erro.

**Status:** especificado como parte da v2.0.0 (ver "Agora"); implementação real ainda não começou.

## Mais tarde

### Auditoria periódica de instâncias reais

**Resultado:** os 4 repositórios de conteúdo do Mau (e qualquer instância futura de terceiro) têm uma cadência declarada de checagem de aderência ao `hipocampo.yaml`/`UPGRADE.md`, não só sob pedido explícito.

**Status:** hipótese.

## Não planejado

- Hospedar ou executar instância de conteúdo — Hipocampo especifica, não roda infraestrutura.
- Orquestração multi-agente — Hipocampo é desenhado pra um agente por vez, client-side (`decisions/0025`).
- Atualizar silenciosamente skill instalada ou conteúdo já gerado numa instância.
- Certificação externa de conformidade MODA — MODA 1.0 não oferece isso, e Hipocampo não pretende inventar a própria.
