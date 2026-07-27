# 0007 — Licenciamento dos repositórios de conteúdo

**Status:** Aceito

## Contexto

`decisions/0001` cobre a licença Apache-2.0 de `hipocampo`/`hipocampo-toolkit` — a metodologia em si, pública. Os repositórios de conteúdo (`hipocampo-concepts`, `hipocampo-personal-vault`, `hipocampo-company`, `hipocampo-company-vault`) não tinham nenhum tratamento de licença — o plano original previa "License: Nenhuma". Isso deixa uma lacuna: sem arquivo de licença, o conteúdo fica sob copyright restrito por padrão, sem cláusula explícita de titularidade nem efeito diferenciado por grau de `visibility`. Uma instância anterior ao Hipocampo (Second Brain Pessoal do titular) já havia resolvido esse mesmo problema de forma equivalente.

## Decisão

Todo repositório de conteúdo Hipocampo ganha um arquivo `LICENSE` na raiz, modelo proprietário/confidencial — nunca uma licença aberta —, com titular explícito: a pessoa física, em `hipocampo-concepts`/`hipocampo-personal-vault`; a empresa, em `hipocampo-company`/`hipocampo-company-vault`. Campo novo no frontmatter, `license` (SPEC.md, seção 2), **sempre derivado mecanicamente de `visibility`, nunca definido à mão**, usando o padrão SPDX `LicenseRef-<idstring>` — identificador curto embutido no documento, texto legal completo só no `LICENSE`. Quatro valores possíveis, um por grau de `visibility`: `LicenseRef-<Instância>-Public`, `-Internal`, `-Confidential`, `-Restricted`.

## Racional

Bases de conhecimento privadas pedem um modelo proprietário confidencial, não uma licença aberta — licença aberta introduziria risco de vazamento e obrigação de disponibilização que não se aplica a repositórios de conteúdo que, por invariante (SPEC.md, seção 8), nunca são públicos. Derivar `license` mecanicamente de `visibility` evita divergência entre as duas camadas sem duplicar a granularidade operacional da camada de confidencialidade na camada jurídica. Embutir o identificador no frontmatter garante que o documento carregue seu próprio efeito jurídico mesmo se copiado isoladamente, fora do contexto do repositório de origem.

## Alternativas descartadas

- **Manter "License: Nenhuma" nos repositórios de conteúdo**, plano original. Descartada: sem arquivo de licença, o padrão legal é copyright restrito, sem cláusula explícita de titularidade nem tratamento diferenciado por `visibility` — exatamente a lacuna que motivou esta decisão.
- **`license` como campo de valor livre, preenchido à mão.** Descartada pela mesma razão que impede preencher `visibility`→efeito legal à mão: risco de divergência entre os dois campos sem ganho real de expressividade.
- **Uma licença única para todos os repositórios de conteúdo, independente de titular.** Descartada — `hipocampo-company`/`hipocampo-company-vault` têm titular diferente (a empresa) de `hipocampo-concepts`/`hipocampo-personal-vault` (a pessoa física), então o `LICENSE` de cada repositório precisa declarar isso explicitamente, não pode ser um texto único compartilhado.
