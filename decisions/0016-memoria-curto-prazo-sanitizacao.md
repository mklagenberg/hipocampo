# 0016 — Memória de curto prazo como estágio de sanitização, não só captura bruta

**Status:** Aceito

## Contexto

A seção 5-A do SPEC.md (v1.2.0, DR0008) já descreve quatro estações de memória — sensorial, gate de atenção, curto prazo, consolidação REM, longo prazo — mas define curto prazo de forma rasa: "item já capturado no sistema canônico (git), ainda não curado", com `inbox/` como mínimo viável. Na prática (relatado em 2026-07-30), consolidar direto do inbox pro longo prazo, repetidamente, ao longo da evolução de um mesmo assunto, vai bagunçando a estrutura: atomicidade se perde, posicionamento de arquivo fica inconsistente, sem nenhum estágio intermediário que force uma sanitização antes da promoção final.

## Decisão

Curto prazo passa a ser explicitamente um estágio de sanitização, não só um buffer de captura. Definição revisada das três camadas relevantes pra operação do dia a dia (a memória sensorial e o gate de atenção continuam como já descritos):

1. **Sensorial:** vive fora de qualquer repositório Hipocampo — a conversa/sessão em si, notas no Google Keep, documentos no Google Drive, arquivo anexado. Nunca versionado em git.
2. **Curto prazo:** já vive dentro do repositório (`inbox/`), já passou pelo gate de atenção, mas ainda não é atômico nem está necessariamente no lugar certo — precisa de sanitização (dividir por conceito, reclassificar `category`/`visibility`, corrigir nomenclatura) antes de virar documento de longo prazo.
3. **Longo prazo:** documento atômico, curado, frontmatter completo, corretamente posicionado — sem mudança na definição já existente.

Cada repositório de conteúdo tem seu próprio `inbox/` — os rituais de manutenção (REM, frontmatter audit, auditoria estrutural) operam sempre dentro do escopo de um repositório por vez, não globalmente entre os repositórios de uma pessoa/organização.

## Racional

Sem um estágio intermediário reconhecido, toda consolidação nova é uma decisão isolada sobre onde/como estruturar aquele pedaço de conhecimento — sem nenhum momento formal de reavaliar se a estrutura acumulada ainda faz sentido. Nomear curto prazo como estágio de sanitização dá um lugar explícito pra essa reavaliação acontecer antes da promoção a longo prazo, em vez de depois (quando já virou documento "oficial" e mexer nele tem mais fricção).

## Alternativas descartadas

- **Manter a definição rasa de curto prazo (só "não curado ainda"):** descartada porque não endereça o problema relatado — não diz o que precisa acontecer entre a captura e a curadoria.
- **Sanitização acontecer só dentro da consolidação REM, sem nomear curto prazo como estágio à parte:** descartada porque dilui a responsabilidade — sem um nome e um lugar (`inbox/`) reconhecidos, fica implícito, e o que é implícito na metodologia tende a não ser seguido de forma consistente (mesmo princípio já aplicado a "nunca deixar implícito" nas extensões locais, SPEC.md seção 8).
