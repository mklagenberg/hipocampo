# 0029 — Taxonomia de tipo de repositório: domínio × tier de exposição

**Status:** Proposto

## Contexto

Hipocampo já opera, na prática, com repositórios de conteúdo organizados por dois critérios informais — titularidade (`decisions/0002`, pessoal vs. corporativo) e nível de restrição de acesso (vault confidencial vs. repositório mais aberto) — sem que esses dois critérios jamais tivessem sido nomeados formalmente. Isso ficou evidente ao começar a adequar a metodologia ao MODA: o contrato de scaffolding do MODA exige que todo profile de scaffold declare a variante legítima de instância que gera, e a auditoria (seção 4.14) aponta que perfis de instância mal definidos tendem a virar templates soltos sem contrato compartilhado. Precisamos de vocabulário formal pras variantes de repositório de conteúdo que o Hipocampo já produz — não de uma estrutura nova.

O ponto de partida foi uma proposta com cinco tiers nomeados: pessoal-confidencial, pessoal-público, empresa-confidencial, empresa-estruturante, empresa-público — "estruturante" descrito como "conhecimento a ser curado pelas lideranças", ao lado de "confidencial" descrito como "conhecimento que só as lideranças podem acessar". As duas descrições compartilham o mesmo público de acesso (lideranças); a diferença é de intenção (permanecer confidencial vs. ser candidato a publicação futura), não de quem pode ler.

## Decisão

Dois eixos ortogonais, ambos já existentes na prática, agora nomeados formalmente (`SPEC.md`, seção 2-C):

1. **Domínio de titularidade** (`decisions/0002`, sem mudança): `pessoal` ou `empresa`.
2. **Tier de exposição**, dentro de cada domínio: `confidencial` ou `público` — dois valores em ambos os domínios, sem terceiro tier.

Os quatro pares mapeiam, sem repositório novo, aos quatro repositórios de conteúdo reais que o Mau já opera:

| Domínio | Tier | Repositório |
|---|---|---|
| pessoal | confidencial | hipocampo-personal-vault |
| pessoal | público | hipocampo-concepts |
| empresa | confidencial | hipocampo-company-vault |
| empresa | público | hipocampo-company |

"Estruturante" não vira um quinto repositório físico. Vira um campo de frontmatter novo, opcional, relevante só dentro do repositório `empresa-confidencial`: `curation_status: staged | permanent` (`SPEC.md`, seção 2). `staged` marca um documento como candidato a eventualmente ser promovido pra `empresa-público`, depois de curadoria da liderança; `permanent` (default) marca conteúdo confidencial por natureza, sem expectativa de publicação futura. O comportamento de Promote em relação a esse campo é tratado à parte, em `decisions/0030`.

A declaração formal de qual domínio+tier um repositório específico implementa fica, por ora, no campo "tipo de instância" já existente do `AGENTS.md` (`decisions/0022`) combinado com o tier conhecido informalmente pelo operador — e será formalizada por um manifesto de instância quando a adequação da metodologia ao MODA incorporar o scaffolding (fase separada, ainda não executada).

## Racional

Reaproveitar os quatro repositórios reais em vez de propor um modelo teórico novo segue o mesmo princípio que motivou `decisions/0002` (não desenhar estrutura antes da necessidade real aparecer) e o item de `BEST-PRACTICES.md` ("`category` nasce depois, nunca antes" — mesmo raciocínio aplicado aqui a repositório em vez de pasta). "Estruturante" e "confidencial" descrevem o mesmo público de acesso — pelo invariante 4 (`SPEC.md`, seção 8: separação de acesso é sempre por repositório), só se justifica repositório novo quando o *acesso* muda, não quando só a *intenção* muda. Tratar isso como campo de frontmatter em vez de repositório evita gerar um repositório vazio, de baixo volume, só pra representar um estágio de ciclo de vida.

A ausência de um terceiro tier pessoal reflete uma assimetria real: "estruturante" só faz sentido quando quem decide publicar (a liderança) é estruturalmente diferente de quem escreveu (o colaborador) — situação exclusiva do domínio `empresa`. No domínio `pessoal`, autor e curador são a mesma pessoa; não existe um estágio de "aguardando curadoria de terceiro" a marcar.

## Alternativas descartadas

- **Quinto repositório físico pra "estruturante".** Descartada — mesmo público de acesso que `empresa-confidencial` hoje, sem diferença de enforcement real do GitHub que justifique separação (invariante 4); contraria o princípio de não estruturar antes da necessidade real.
- **Terceiro tier simétrico no domínio pessoal ("pessoal-estruturante").** Descartada — não existe hoje, no domínio pessoal, um curador estruturalmente diferente do autor que justifique um estágio de curadoria antes de liberar; sem caso de uso real, seria estrutura prematura.
- **Incorporar os tiers dentro do campo `visibility` existente.** Descartada — `visibility` já resolve um problema diferente e bem definido (o que, já tendo acesso ao repositório, pode ser usado sem restrição adicional); misturar os dois conceitos (tier de repositório vs. convenção de leitura intra-repositório) reduziria a clareza dos dois campos.
