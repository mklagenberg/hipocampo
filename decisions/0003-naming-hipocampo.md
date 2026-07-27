# 0003 — Naming: prefixo `hipocampo-*`, "company" como nome literal

**Status:** Aceito

## Contexto

A convenção de nomenclatura anterior usava prefixo `second-brain-*`. Era preciso decidir também como nomear o repositório de conteúdo corporativo sem amarrar o nome a uma empresa específica.

## Decisão

Todo repositório da metodologia usa prefixo `hipocampo-*`. A palavra "company" é usada literalmente (não como placeholder a ser substituído) nos nomes de repositório corporativo — `hipocampo-company` e `hipocampo-company-vault` — porque o org do GitHub em que o repositório vive já desambigua qual empresa é. O sufixo `-vault` é genérico, usado para conteúdo sensível/identificável, generalizado a partir da ideia original de um sufixo `-leadership` (que descrevia só a audiência, não o conteúdo).

## Racional

`second-brain-*` foi descartado pelo nome da metodologia em si ter mudado para Hipocampo — manter o prefixo antigo criaria uma inconsistência de marca logo na largada. "company" literal evita a armadilha de um placeholder que precisa ser lembrado de substituir (risco de nome esquecido/errado ao instanciar); o org do GitHub já resolve a ambiguidade de "qual empresa" sem precisar repetir isso no nome do repositório. "-vault" generaliza melhor que "-leadership": o critério real de separação é sensibilidade/identificabilidade do conteúdo, não quem tem permissão de ler — a audiência pode mudar (quem é "liderança" varia por organização), mas "conteúdo sensível separa em vault" é estável.

## Alternativas descartadas

- **Manter `second-brain-*`** — descartada por inconsistência de marca com o nome novo da metodologia.
- **`-leadership` como sufixo** — descartada por descrever só quem acessa, não o que o conteúdo é; "vault" descreve a propriedade do conteúdo que motiva a separação.
- **Placeholder genérico tipo `hipocampo-{empresa}`** — descartada por criar um passo manual de substituição sem necessidade, já que o org do GitHub já desambigua.
