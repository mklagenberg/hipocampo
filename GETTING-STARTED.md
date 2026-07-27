# Hipocampo — Getting Started

Guia prático para adotar a metodologia. Para a especificação normativa completa, ver [SPEC.md](SPEC.md). Para o que o Hipocampo não é e onde não se aplica, ver [DISCLAIMER.md](DISCLAIMER.md). Se você nunca usou git/GitHub, comece pelo [doc de fundamentos](docs/FUNDAMENTOS.md).

## 1. Entenda a arquitetura antes de criar nada

Hipocampo separa dois tipos de repositório:

| Camada | O que guarda | Visibilidade |
|---|---|---|
| Metodologia e ferramental (`hipocampo`, `hipocampo-toolkit`) | Spec, regras, template, skill — nunca conteúdo real | Pública |
| Base de conhecimento (qualquer repositório instanciado a partir do `hipocampo-toolkit`) | O conteúdo de fato — notas, decisões, projetos, pessoas | **Sempre privada, sem exceção** |

Você nunca edita `hipocampo` nem `hipocampo-toolkit` para guardar conhecimento próprio. Eles são a spec e o molde; seu conhecimento vive num repositório separado, privado, instanciado a partir do molde.

## 2. Instancie um repositório de conteúdo

1. No GitHub, acesse `hipocampo-toolkit` e use o botão **"Use this template"** para criar um repositório novo.
2. **Marque o novo repositório como privado.** Isso não é opcional — é o invariante que sustenta todo o modelo de `visibility` do SPEC.md (seção 8).
3. No `CLAUDE.md` gerado a partir do template, preencha o bloco "Extensões locais a Hipocampo vX.Y" com as decisões específicas dessa instância (subpastas de `category` que você já sabe que vai usar, `ttl` default por tipo de conteúdo, convenção de commit).
4. Declare a versão de compatibilidade (exemplo: "Segue Hipocampo ^1.0.0").

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

Hipocampo pressupõe rituais periódicos conduzidos por um agente de IA sob sua supervisão — não automação sem revisão. Dois rituais centrais:

- **Staleness** — verificação periódica de `ttl` vencido, comportamento diferente por `temporality` (SPEC.md, seção 5).
- **Consolidação** (inbox → conhecimento) — captura solta vira documento com frontmatter completo, sempre revisada por você antes de escrita definitiva (invariante 5 do SPEC.md — o agente nunca escreve sem pedido explícito).

A arquitetura específica de skill para rodar essas rotinas fica a cargo de cada adotante — o `hipocampo-toolkit` traz um stub como ponto de partida, não uma implementação fechada.

## 6. Antes de ativar

Leia o `DISCLAIMER.md` inteiro antes de tratar qualquer instância Hipocampo como fonte única de verdade para algo que importa (compliance, decisão financeira, avaliação de pessoa). A metodologia é um sistema de gestão de conhecimento sobre git + markdown + IA probabilística — não um banco de dados transacional nem um sistema de enforcement técnico de acesso além do que o próprio GitHub garante.
