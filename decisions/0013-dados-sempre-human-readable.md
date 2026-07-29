# 0013 — Dados sempre human-readable, independente de produto de IA

**Status:** Aceito

## Contexto

A metodologia Hipocampo já é, por desenho, git + markdown — mas a razão de ser desse desenho nunca foi articulada como princípio explícito. Instabilidades reais de produtos de IA reforçam por que isso importa na prática, não só em teoria: o Claude Cowork teve múltiplos outages em julho de 2026 (6, 14, 21 e 25/07). Se o conhecimento de uma instância só pudesse ser lido através de uma interface ou produto específico, um outage desse produto deixaria o usuário sem acesso ao próprio conhecimento — não só sem a conveniência de operá-lo com IA.

## Decisão

Formalizar como princípio explícito (DISCLAIMER.md, nova seção): todo dado de uma instância Hipocampo deve permanecer legível e navegável por um humano usando só as ferramentas nativas do repositório — o visualizador de markdown do próprio GitHub, um editor de texto qualquer, `git log`/`git show` —, sem depender de nenhum produto de IA específico estar no ar. Isso não é uma limitação da metodologia — é a mesma característica que já garante, na seção 2 (`visibility`) e no `DISCLAIMER.md`, que permissão de acesso é sempre resolvida no nível do GitHub, nunca de um produto de terceiro por cima dele.

## Racional

Vendor lock-in é um risco real e crescente à medida que mais funcionalidade é construída em cima de produtos de IA específicos (skills, MCPs, agentes). Um outage, uma descontinuação de produto, ou uma mudança de precificação não deveriam nunca colocar em risco o acesso ao conhecimento em si. O outage do Claude Cowork em julho de 2026 é usado aqui como validação factual de um risco genérico, não como razão específica contra aquele produto — o mesmo argumento valeria para qualquer outro.

## Alternativas descartadas

- **Não formalizar, deixar implícito no desenho já existente (markdown + git).** Descartada: o mesmo raciocínio da `decisions/0012` — um princípio que já existe na prática, mas nunca foi escrito, corre o risco de ser erodido por uma decisão futura que pareça razoável isoladamente (por exemplo, guardar algum dado só em formato binário/proprietário "porque é mais eficiente").
- **Formalizar citando o outage do Cowork como motivação central e específica.** Descartada: amarraria o princípio a um incidente e um produto específico, quando o risco é genérico a qualquer produto de IA — o outage é evidência de que o risco é real, não a causa do princípio.
