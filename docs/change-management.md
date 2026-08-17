# Change management orientado a especificação

Hipocampo trata uma mudança estrutural no repositório como mudança num sistema de contratos, não só uma coleção de arquivos. `SPEC.md` é a especificação normativa autoritativa; `decisions/`, `CHANGELOG.md`, `UPGRADE.md`, `MIGRATIONS.md`, `moda.yaml`/`conformance/moda.yaml`, e a cópia pessoal da skill são projeções sincronizadas desse contrato. Mecanismo adotado seguindo o modelo do [MODA](https://github.com/mklagenberg/moda) (`docs/change-management.md` deles) — ver `decisions/0031-mecanismo-de-change-set.md` pro racional completo da adoção.

## Classes de mudança

| Classe | Significado | Exige Change Set? |
|---|---|---|
| `editorial` | Wording, formatação, ou link, sem efeito semântico, operacional, estrutural, de segurança, ou de compatibilidade | Opcional, a menos que mude uma superfície de contrato protegida |
| `operational` | Muda orientação de execução, rotina, empacotamento, ou skill, sem mudar obrigação normativa | Obrigatório |
| `normative` | Adiciona, remove, ou muda uma obrigação, contrato público, fronteira de compatibilidade, ou significado de conformidade | Obrigatório |

Os nomes das três classes ficam em inglês, mesmo com o resto do repositório em português — `editorial` em português carrega conotação de opinião/parecer que o termo original não tem (aqui é wording/formatação); manter o termo técnico evita esse ruído (será revisitado quando a Fase E de tradução do repositório acontecer).

Uma mudança aparentemente editorial é operacional ou normativa quando muda como um humano ou agente age, como uma instância valida algo, ou o que uma instância precisa implementar pra continuar aderente.

## Change Set do Hipocampo

Uma mudança que exige Change Set vive em `changes/<change-id>/` e contém:

- `proposal.md` — problema, contrato atual, contrato proposto, alternativas descartadas, riscos, critério de aceitação, compatibilidade/migração, recuperação;
- `impact.yaml` — classificação legível por máquina, impacto SemVer, gatilhos, superfícies afetadas, validação.

A proposta captura o raciocínio de *esta* mudança específica. Uma escolha estrutural durável também é registrada em `decisions/` — um Change Set não substitui uma Decision Record; eles respondem perguntas diferentes (mesma distinção de escopo já em uso entre Decision Record e `type: decision`, `SPEC.md` seção 7, só que aplicada aqui entre Change Set e Decision Record). Change Sets aceitos permanecem como evidência de rastreabilidade — nunca editados depois de aceitos, só superseded.

## Status de impacto

Toda superfície declarada em `impact.yaml` é classificada como:

- `updated` — um ou mais caminhos declarados mudaram;
- `reviewed` — revisada e intencionalmente não alterada, com racional;
- `not-applicable` — fora do escopo da mudança, com racional.

A declaração não é prova por si só — revisão humana avalia se o racional é crível. Nenhuma validação determinística compara isso com o diff real ainda (ver seção abaixo).

## Fluxo de mudança

1. Classifique a mudança antes de implementar.
2. Crie um Change Set pra mudança operacional ou normativa.
3. Declare o contrato pretendido e o critério de aceitação em `proposal.md`.
4. Declare gatilhos, impacto SemVer, superfícies afetadas, e validação esperada em `impact.yaml`.
5. Mude a fonte autoritativa primeiro: `SPEC.md` pra regra normativa, ou o artefato operacional dono do comportamento pra mudança operacional.
6. Sincronize as projeções afetadas sem copiar prosa normativa em cada arquivo.
7. Rode a validação declarada (hoje, revisão humana — validação determinística ainda não existe, ver `ROADMAP.md`).
8. Revise o diff, lacunas não resolvidas, necessidade de migração/recuperação, e impacto de conformidade MODA.
9. Mescle só depois de revisão humana explícita (Mau).
10. Corte tag só através da rotina de release (`SPEC.md`, seção 9).

## Gatilhos

Adaptados ao vocabulário real do Hipocampo — não são uma tradução literal da tabela do MODA, porque conceitos deles (`package_contract`, por exemplo) não têm equivalente hoje neste repositório.

| Gatilho | Superfícies mínimas a revisar |
|---|---|
| `regra_normativa` — mudança de regra em `SPEC.md` | `SPEC.md`, `decisions/`, `CHANGELOG.md`, `UPGRADE.md`/`MIGRATIONS.md` conforme o escopo SemVer (`decisions/0023`) |
| `schema_frontmatter` — campo novo/alterado no schema (seção 2) | `SPEC.md` seção 2, `UPGRADE.md`, exemplos citados em `GETTING-STARTED.md`/`BEST-PRACTICES.md` |
| `mecanismo_cross_repositorio` — Promote/Depromote/Redbutton/Registry (seções 6/13) | `SPEC.md` seções 6/13, `decisions/`, `CHANGELOG.md` |
| `politica_dados_sensiveis` — seção 2-A | `SPEC.md` seção 2-A, `decisions/`, `BEST-PRACTICES.md` |
| `release` — corte de versão | `CHANGELOG.md`, `UPGRADE.md`, `MIGRATIONS.md` (se MAJOR), `moda.yaml` (versão declarada), `conformance/moda.yaml` |

`reviewed` e `not-applicable` só são válidos com racional concreto. Uma escolha estrutural também exige Decision Record.

## Checagem determinística e humana

Hoje não existe validação determinística/CI da estrutura do próprio repositório de metodologia (achado `major` da auditoria MODA de 2026-08-17, ver `ROADMAP.md`) — até isso ser resolvido, toda checagem de Change Set é humana:

- se a classificação e o impacto SemVer declarados são verdadeiros;
- se uma mudança de regra foi totalmente projetada na orientação operacional (skill pessoal, `AGENTS.md` de instância, etc.);
- se os racionais de `reviewed`/`not-applicable` são críveis;
- se riscos de migração e release são aceitáveis.

## Regra de conclusão

Uma mudança está incompleta quando sua implementação parece pronta mas as superfícies de contrato declaradas, evidência, ou obrigação de migração ficam inconsistentes entre si. Não existe checagem automatizada ainda que prove isso sozinha — revisão humana continua responsável pela completude semântica.
