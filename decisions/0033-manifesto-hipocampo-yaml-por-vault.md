# 0033 — Manifesto `hipocampo.yaml` por vault

**Status:** Aceito

## Contexto

O `moda.yaml`, introduzido na Fase B da adequação ao MODA, declara a relação de `hipocampo` (a metodologia) com o MODA — não diz nada sobre a relação entre um vault individual (ex.: `hipocampo-personal-vault`) e a versão do `hipocampo` que ele segue. Essa informação hoje vive só na linha "Versão do Hipocampo seguida por esta instância" do `AGENTS.md` de cada vault — texto livre, sem schema, não consultável por máquina.

Com a consolidação do scaffold em `hipocampo/scaffold/` (`decisions/0032`), cada vault passa a ser gerado por um profile declarado (`pessoal` ou `empresa`) a partir de um commit específico de `hipocampo`. Essa proveniência — qual profile, qual versão do engine, qual commit-fonte — também não tinha onde ser registrada.

## Decisão

Todo vault gerado pelo scaffold recebe, na raiz, um manifesto `hipocampo.yaml`, no mesmo espírito do `moda.yaml` da metodologia mas com escopo de instância:

```yaml
hipocampo:
  manifest_version: "1.0"
  compatibility: "^1.9.0"
  verified_against: "<versão do SPEC.md no momento da instanciação>"
  verified_commit: "<commit de hipocampo/main usado como fonte>"

instance:
  repository: "<URL deste repositório>"
  domain: "pessoal | empresa"
  tier: "conteudo | vault"

scaffold:
  profile: "pessoal | empresa"
  profile_version: "..."
  engine_version: "..."
  source_repository: "https://github.com/mklagenberg/hipocampo"
  source_commit: "<mesmo commit de hipocampo.verified_commit>"

skill:
  generated_by_version: "<versão da skill pessoal que executou a instanciação>"

state: "current"
```

`instance.domain` usa o vocabulário mais recente (`pessoal`/`empresa`, `decisions/0029`) — não o vocabulário original do campo "Tipo de instância" do `AGENTS.md` (`pessoal`/`corporativa`). Essa divergência é conhecida e deliberadamente **não** resolvida por este DR (ver racional).

Consequência: como todo vault existente precisa, eventualmente, ganhar esse manifesto pra se manter aderente à metodologia (`UPGRADE.md` ganha um item novo), esta é mais uma peça que reforça o caráter MAJOR do salto pra v2.0.0.

## Racional

O manifesto separa duas coisas que hoje estão misturadas em texto livre no `AGENTS.md`: a declaração operacional que um humano lê e edita (escopo, extensões locais, rituais) e a proveniência que idealmente uma ferramenta consultaria (de qual commit este vault veio, qual profile, compatível com qual versão). Machine-readable também é o que o MODA já pede de `hipocampo` mesmo — replicar o padrão pra dentro de cada vault é consistente.

A divergência de vocabulário (`domain: pessoal|empresa` vs. "Tipo de instância: pessoal|corporativa") é intencionalmente deixada como está, não harmonizada agora: mudar o campo do `AGENTS.md` obrigaria editar todos os `AGENTS.md` existentes (`hipocampo-personal-vault`, `hipocampo-concepts`, `hipocampo-company`, `hipocampo-company-vault`), uma operação de escopo maior que esta Fase D não se propôs a cobrir. Preferível nomear o problema aqui — explicitamente, por escrito — a resolvê-lo silenciosamente só na metade dos lugares onde aparece.

## Alternativas descartadas

- **Guardar essa informação só no `AGENTS.md`, sem manifesto separado.** Descartada: mistura texto operacional (editado por humano) com proveniência (deveria ser gerado e, no limite, verificado por máquina) — o mesmo argumento que já levou o `moda.yaml` a existir separado do `README.md`/`AGENTS.md` da metodologia.
- **Harmonizar o vocabulário agora, editando todos os `AGENTS.md` existentes.** Descartada nesta rodada: escopo maior do que Fase D se propôs, e arriscado editar quatro repositórios de conteúdo reais como efeito colateral de uma mudança de manifesto. Fica registrado como pendência conhecida.
- **Chamar o campo de `kind` em vez de `domain`.** Descartada: `kind` já é usado com outro sentido em `moda.yaml` (`artifact.kind`, metodologia vs. framework) — reutilizar o nome pra um conceito diferente dentro do próprio ecossistema Hipocampo/MODA geraria confusão.
