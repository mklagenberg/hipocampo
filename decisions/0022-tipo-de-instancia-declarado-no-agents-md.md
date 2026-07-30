# 0022 — Tipo de instância (corporativa/pessoal) declarado explicitamente no AGENTS.md

**Status:** Aceito

## Contexto

A política de dados sensíveis por tipo de instância (seção 2-A, DR0009) diferencia o que uma instância *corporativa* pode armazenar do que uma instância *pessoal* pode. A auditoria estrutural semanal (seção 5-C, DR0019) tem, entre suas três funções, verificar vazamento de dado sensível "contra a política por tipo de instância" — mas nunca especifica onde esse tipo de instância está declarado.

Na mesma seção 5-C, a função de posicionamento resolve isso corretamente: está explicitamente ancorada no escopo declarado no `AGENTS.md` (seção 11, DR0015). A função de vazamento de dado sensível não tem o mesmo ancoramento — funciona hoje só porque o agente infere contextualmente qual repositório é qual, o que é exatamente o tipo de decisão que a seção 8 do SPEC.md diz que nunca deve ficar implícita ("sempre documentado, nunca implícito"). Levantado por Mau ao revisar o desenho da auditoria estrutural antes da reescrita da skill (G2).

## Decisão

O `AGENTS.md` de toda instância declara explicitamente, dentro do bloco "Escopo do repositório" (seção 11), o **tipo de instância**: `corporativa` ou `pessoal`. Esse campo é o critério que a auditoria estrutural (seção 5-C, função 3) e qualquer leitura/escrita de documento novo usam pra saber qual variante da política de dados sensíveis (seção 2-A) se aplica àquele repositório — nunca inferido implicitamente pelo agente a partir do nome do repositório ou do contexto da conversa.

SPEC.md, seção 2-A, ganha uma frase de fechamento apontando pra esse campo. SPEC.md, seção 5-C, tem a função 3 reescrita pra citar o mesmo campo, no mesmo padrão já usado pela função 2 (posicionamento).

## Racional

Fecha uma assimetria real dentro da própria seção 5-C: duas das três funções (posicionamento e, agora, vazamento de dado sensível) ficam ancoradas no mesmo artefato declarado (`AGENTS.md`), em vez de uma delas depender de inferência do agente. Reaproveita um campo que já é obrigatório preencher (seção 11) em vez de criar um mecanismo novo — o tipo de instância já era, na prática, uma decisão implícita de qual repositório existe (`-company`/`-vault` vs. `-personal-vault`); este DR só torna essa decisão um campo lido, não presumido.

## Alternativas descartadas

- **Inferir o tipo de instância pelo nome do repositório (sufixo `-company`, `-personal-vault`, etc.).** Descartado: depende de convenção de nomenclatura nunca formalizada como regra, e quebra silenciosamente se algum dia um repositório for renomeado ou um usuário escolher nome diferente do padrão.
- **Criar um campo de frontmatter novo em vez de usar o `AGENTS.md`.** Descartado: o tipo de instância é uma propriedade do repositório inteiro, não de documento individual — frontmatter já tem `owner` cumprindo parte desse papel por documento; duplicar a informação em cada arquivo seria redundante e sujeito a divergência.
