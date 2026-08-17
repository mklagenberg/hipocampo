# Hipocampo — Getting Started

Guia prático para adotar a metodologia. Para a especificação normativa completa, ver [SPEC.md](SPEC.md). Para o que o Hipocampo não é e onde não se aplica, ver [DISCLAIMER.md](DISCLAIMER.md). Se você nunca usou git/GitHub, comece pelo [doc de fundamentos](docs/FUNDAMENTOS.md).

## 0. Se você está aprendendo a metodologia pela primeira vez

Antes de instanciar qualquer coisa, uma ordem de leitura que evita voltar atrás:

1. **[DISCLAIMER.md](DISCLAIMER.md)** — o que o Hipocampo é e não é, antes de depender dele pra algo que importa.
2. **Este documento, do início ao fim** — a mecânica prática.
3. **[BEST-PRACTICES.md](BEST-PRACTICES.md)** — julgamento do dia a dia, privacidade, adoção em equipe — depois que a mecânica já fez sentido.
4. Sob demanda, quando a dúvida aparecer: **[SPEC.md](SPEC.md)** (a norma completa), **[docs/MODELOS-DE-IA.md](docs/MODELOS-DE-IA.md)** (o que importa num agente de IA pra operar isso bem) e **[docs/PERFORMANCE-E-GRAFO.md](docs/PERFORMANCE-E-GRAFO.md)** (como o retrieval funciona, e a relação com o OKF da Google).

Se você já instanciou um repositório e só quer o passo a passo imediato de configuração, pule pra seção 2 abaixo e para o `POS-INSTANCIACAO.md` gerado pelo agente dentro do seu repositório novo (fonte-modelo: `scaffold/skeleton/POS-INSTANCIACAO.md`).

## 1. Entenda a arquitetura antes de criar nada

Hipocampo separa dois tipos de repositório:

| Camada | O que guarda | Visibilidade |
|---|---|---|
| Metodologia e ferramental (`hipocampo`, incluindo `scaffold/` e `skill/`) | Spec, regras, scaffold, skill — nunca conteúdo real | Pública |
| Base de conhecimento (qualquer repositório instanciado pelo agente a partir do scaffold em `hipocampo/scaffold/`) | O conteúdo de fato — notas, decisões, projetos, pessoas | **Sempre privada, sem exceção** |

Você nunca edita `hipocampo` pra guardar conhecimento próprio. Ele é a spec e o scaffold; seu conhecimento vive num repositório separado, privado, instanciado a partir do scaffold.

## 2. Instancie um repositório de conteúdo

Não existe mais um botão "Use this template" — a instanciação é executada por um agente de IA operando a skill Hipocampo (ver `skill/references/instanciacao.md`), a partir de um profile declarado em `scaffold/profiles/` (`pessoal.yaml` ou `empresa.yaml`, `decisions/0032`).

1. Peça ao agente pra instanciar um repositório novo, informando: nome do repositório, tipo de instância (`corporativa`/`pessoal`), titular do conteúdo (pessoa física ou empresa), e nível de curadoria (`conteudo` ou `vault` — ver `SPEC.md`, seção 2-C).
2. O agente lê o profile correspondente, coleta qualquer input que faltar, e **apresenta o plano completo antes de escrever qualquer coisa** (invariante 5, `SPEC.md` seção 8) — repositório a criar, cada arquivo a gerar, LICENSE escolhido.
3. Depois de você confirmar, o agente cria o repositório (**privado — não é opcional**, invariante 1) e gera cada output declarado no profile: `AGENTS.md` e `hipocampo.yaml` já preenchidos com os inputs coletados, `LICENSE` já a partir do template certo (`scaffold/license-templates/`), `CLAUDE.md`, `POS-INSTANCIACAO.md`, `registry.md`, `example/exemplo-nota.md`.
4. O repositório novo **não** recebe uma pasta `skill/` — a skill roda sempre no seu ambiente de IA, por pessoa, nunca por repositório (`decisions/0025`). Se ainda não tiver, instale sua própria cópia personalizada a partir de [`skill/SKILL.md`](skill/SKILL.md) + `skill/references/*.md` (este repositório, fonte canônica), preenchendo o roteador de repositórios (`references/personalizacao.md` da sua cópia) — inclusive com este repositório novo.
5. Depois de gerado, siga o `POS-INSTANCIACAO.md` do repositório novo — agora um checklist de **verificação**, não um passo a passo manual: confirma que o agente gerou tudo certo antes de você guardar qualquer conhecimento real.

Detalhe operacional completo (quem faz o quê, em que ordem, o que apresentar antes de escrever): `skill/references/instanciacao.md`.

## 3. Escreva seu primeiro documento

Todo documento é um `.md` com o frontmatter do SPEC.md (seção 2). Um exemplo mínimo, de uma nota nova:

```yaml
---
title: "Nome do documento"
date: "2026-07-27"
updated: "2026-07-27"
source: "conversa"
tags: []
type: "note"
temporality: "evergreen"
ttl: "2028-07-27"
status: "active"
related: []
revision: 1
visibility: "internal"
author: "Seu Nome - @seu-usuario-github"
---
```

Preencha `type` (seção 3 do SPEC) e `temporality` (seção 5) pensando no propósito real do documento — não force um valor só porque parece o mais comum. Se nenhum `type` existente encaixa, releia a regra de expansão antes de criar um novo valor.

## 4. Referências entre repositórios

Se você mantém mais de um repositório de conteúdo (por exemplo, um pessoal e um de trabalho), use `related: ["$alias:path.md"]` para apontar de um para o outro, e mantenha um `registry.md` no repositório menos restrito de cada escopo. Detalhe completo: SPEC.md, seção 6.

## 5. Rotinas

Hipocampo pressupõe rituais periódicos conduzidos por um agente de IA sob sua supervisão — não automação sem revisão. Dois rituais centrais, ambos já cobertos pela skill Hipocampo (`skill/SKILL.md`, depois de personalizada):

- **Staleness** — verificação periódica de `ttl` vencido, comportamento diferente por `temporality` (SPEC.md, seção 5).
- **Consolidação** (inbox → conhecimento) — captura solta vira documento com frontmatter completo, sempre revisada por você antes de escrita definitiva (invariante 5 do SPEC.md — o agente nunca escreve sem pedido explícito).

A skill também checa, no início de sessão, se há uma versão nova da metodologia publicada em `hipocampo` e avisa você — nunca aplica a atualização sozinha.

## 6. Antes de ativar

Leia o `DISCLAIMER.md` inteiro antes de tratar qualquer instância Hipocampo como fonte única de verdade para algo que importa (compliance, decisão financeira, avaliação de pessoa). A metodologia é um sistema de gestão de conhecimento sobre git + markdown + IA probabilística — não um banco de dados transacional nem um sistema de enforcement técnico de acesso além do que o próprio GitHub garante.
