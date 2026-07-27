# 0002 — Arquitetura multi-repositório, sem replicação

**Status:** Aceito

## Contexto

O desenho original considerava um modelo de "Contexto Global" replicado entre repositórios — cada instância teria uma cópia sincronizada de certas informações compartilhadas.

## Decisão

Adotar arquitetura de repositórios independentes, sem replicação de conteúdo entre eles. Duas camadas: metodologia e ferramental (`hipocampo`, `hipocampo-toolkit`, públicos) e base de conhecimento (repositórios de conteúdo instanciados do template, sempre privados). Referências entre repositórios de conteúdo são resolvidas por link/alias (`related` com prefixo `$alias:`, ver SPEC.md seção 6), nunca por cópia de dado.

## Racional

Replicação sem mecanismo de sincronização automática gera divergência silenciosa — a cópia em um repositório fica desatualizada em relação à origem sem que ninguém perceba, porque não há checagem automática de consistência entre as duas. Um documento que existe fisicamente em só um lugar (com outros repositórios apontando para ele por referência) não tem esse modo de falha: ou o link resolve pro documento certo, ou o link está quebrado — não existe estado intermediário de "cópia desatualizada mas presente".

## Alternativas descartadas

- **Contexto Global replicado** — descartada pelo risco de divergência sem mecanismo de sync, descrito acima.
- **Um repositório único para tudo** — descartada porque contradiz a exigência de que repositórios de conhecimento sejam sempre privados enquanto `hipocampo`/`hipocampo-toolkit` sejam sempre públicos — permissão real do GitHub é por repositório, não por pasta dentro de um repositório compartilhado (mesmo princípio do invariante de `visibility`, SPEC.md seção 2).
