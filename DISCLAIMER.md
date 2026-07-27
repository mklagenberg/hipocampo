# Hipocampo — Disclaimer

Este documento existe separado da [LICENSE](LICENSE) porque resolve um problema diferente: a LICENSE diz o que você pode fazer legalmente com o código/spec; este documento diz o que a metodologia **é e não é**, na prática, antes de você depender dela para algo que importa.

## Objetivo

Hipocampo é uma metodologia de organização de conhecimento pessoal ou corporativo usando git, markdown e rituais conduzidos por agentes de IA. O objetivo é retrieval melhor e conhecimento vivo (não estático) ao longo do tempo — não é, e nunca teve a ambição de ser, um substituto para sistemas com garantias formais mais fortes.

## O que Hipocampo não é

- **Não é um banco de dados transacional.** Não há garantia de atomicidade, consistência sob concorrência, ou rollback automático além do que o próprio git oferece (que é versionamento, não transação).
- **`visibility` não é enforcement técnico.** O campo `visibility` no frontmatter (SPEC.md, seção 2) é uma convenção de leitura para humanos e agentes — não impede tecnicamente que alguém com acesso ao repositório leia um arquivo marcado `confidential`. Enforcement técnico real, quando necessário, é feito por permissão de repositório do GitHub (ver invariante 4 do SPEC.md), não por etiqueta dentro de um repositório compartilhado.
- **Não substitui compliance legal.** Nada neste repositório constitui parecer jurídico. Se sua instância guarda dado pessoal sensível, segredo industrial ou informação sujeita a regulação específica (LGPD, contratual, setorial), a adequação legal é responsabilidade de quem opera a instância — não algo que o Hipocampo resolve por desenho.
- **Rotinas de IA são probabilísticas.** Qualquer ritual conduzido por um agente (consolidação, staleness, classificação de `type`/`temporality`) pode errar. Hipocampo assume supervisão humana no laço — o invariante "o agente nunca escreve sem pedido explícito" (SPEC.md, seção 8) existe exatamente por isso, não é boilerplate.

## Cenários recomendados

- Conhecimento pessoal ou de equipe pequena, onde a pessoa/time consegue revisar o que o agente propõe.
- Conteúdo onde "provavelmente certo, revisável depois" é uma trade-off aceitável em troca de retrieval melhor.
- Organizações que já confiam em GitHub como plataforma de permissionamento (o modelo de privacidade do Hipocampo depende estruturalmente disso — ver `docs/FUNDAMENTOS.md`).

## Cenários não recomendados

- Registro que precisa de trilha de auditoria formal com garantias legais (esse é papel de sistema de compliance dedicado, não de second brain).
- Dado que não pode, sob nenhuma circunstância, ser processado por um modelo de IA de terceiro — mesmo com opt-out de treinamento, o conteúdo ainda passa pela inferência do provedor no momento do uso.
- Substituição de sistema com SLA formal de disponibilidade/integridade (git + markdown não tem esse tipo de garantia).

## Pressupostos técnicos

Hipocampo pressupõe: um host de git com permissionamento real por repositório (o modelo foi desenhado em torno do GitHub, mas o princípio se generaliza a qualquer host equivalente); um agente de IA capaz de ler/escrever markdown e seguir instrução estruturada; disposição do operador da instância de revisar o que o agente propõe, não só aceitar automaticamente.

## Versionamento e o que isso significa pra você

A metodologia segue SemVer (detalhe completo em SPEC.md, seção 9, e em `MIGRATIONS.md`). Na prática, para quem só usa:

- **PATCH** (1.0.x) — nada muda pra você. Clarificação de texto ou correção de erro de spec.
- **MINOR** (1.x.0) — capacidade nova opcional. Sua instância continua válida sem adotar nada; ignorar é uma opção legítima.
- **MAJOR** (x.0.0) — algo mudou de forma incompatível. Sua instância continua funcionando com a versão que ela declara seguir, mas migrar para a versão nova exige seguir o guia correspondente em `MIGRATIONS.md`. Migração nunca é automática nem silenciosa.

## Ponte pra LICENSE

Este disclaimer não altera nem substitui nada da [LICENSE](LICENSE) (Apache-2.0) ou do [NOTICE](NOTICE). Em caso de conflito de interpretação entre este documento e a LICENSE, a LICENSE prevalece como o documento juridicamente vinculante — este arquivo é orientação prática, não instrumento legal.
