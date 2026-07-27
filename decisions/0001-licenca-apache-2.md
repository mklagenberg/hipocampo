# 0001 — Licença Apache 2.0, não MIT

**Status:** Aceito

## Contexto

Hipocampo precisa de uma licença de código aberto para os repositórios públicos (`hipocampo`, `hipocampo-toolkit`). A escolha mais comum em projetos pequenos é MIT, por simplicidade.

## Decisão

Usar Apache License 2.0 nos dois repositórios públicos.

## Racional

Apache-2.0 tem três propriedades que MIT não tem e que importam aqui:

1. **Cláusula de marca explícita** (Seção 6 da licença) — protege o nome "Hipocampo" separado da liberdade de uso do código. MIT não distingue isso; qualquer um poderia usar o nome "Hipocampo" para um fork ou produto derivado sem violar a licença.
2. **Exigência de declarar mudanças em arquivos modificados** (Seção 4) — dá rastreabilidade a derivados: quem forka e altera precisa sinalizar isso, o que ajuda a distinguir a spec original de variações.
3. **Cláusula de patente com retaliação** (Seção 3) — protege contribuidores e usuários contra litígio de patente por quem contribuiu; custo zero de incluir, já que não há intenção de monetizar via patente.

## Alternativas descartadas

- **MIT** — mais simples, mas sem as três propriedades acima. Descartada porque a proteção de marca (item 1) é especificamente relevante: "Hipocampo" é o nome pessoal do método, e a intenção é que ele continue sendo identificável como tal mesmo em uso por terceiros.
- **Nenhuma licença (all rights reserved)** — descartada porque contradiz o objetivo de que a metodologia em si seja livremente adotável — só o nome/marca tem restrição, não o conteúdo da spec.
