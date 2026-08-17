# 0030 — Promote: generalização pra graduação dentro do mesmo domínio

**Status:** Proposto

## Contexto

`decisions/0027` definiu Promote como uma ação cross-domain (pessoal → corporativo) e Depromote como downgrade dentro do mesmo domínio de titularidade. `decisions/0029` introduz o campo `curation_status: staged`, aplicável a documentos `empresa-confidencial` candidatos a eventualmente virar `empresa-público`. O movimento de um documento `staged` de `empresa-confidencial` pra `empresa-público` não é coberto por nenhuma das duas ações existentes: não é Promote (não cruza a fronteira pessoal/corporativo) e não é Depromote (Depromote é definida especificamente como downgrade — direção oposta a essa graduação).

Mesmo padrão já usado por `decisions/0028` ao ampliar o gatilho de `decisions/0010`: registrar a extensão como decisão satélite, sem editar a decisão original, preservando rastreabilidade de qual pergunta cada Decision Record resolve.

## Decisão

A ação Promote (`decisions/0027`, `SPEC.md` seção 13) passa a cobrir dois casos:

1. **Cross-domain** (já existente, sem mudança): pessoal → corporativo, com os dois caminhos (elegante e literal) já definidos.
2. **Graduação dentro do mesmo domínio** (novo): um documento `empresa-confidencial` com `curation_status: staged` sendo promovido pra `empresa-público`.

O caso 2 usa sempre o **caminho elegante** de Promote — cria documento novo no destino, seguindo a disciplina de `decisions/0011`, com `related` bidirecional e `revision_note` documentando a graduação. O caminho literal nunca se aplica a esse caso: como origem e destino estão no mesmo domínio de titularidade (`empresa`) o tempo todo, não há transferência de titularidade nova em jogo (`decisions/0007` não muda), então o aviso obrigatório de irreversibilidade e transferência de titularidade do caminho literal seria falso — seu conteúdo simplesmente não se aplica aqui.

Documento de origem não é apagado nem tem `status` alterado — o agente atualiza `curation_status` pra `permanent` (encerrando o candidatismo) ou mantém `staged` com `related` apontando pro novo documento público, a critério de quem confirma a ação no momento da promoção.

**Pré-condição:** só documento com `curation_status: staged` é elegível a essa variante. Documento `permanent` (ou sem o campo preenchido, que usa o mesmo default) precisa de reclassificação explícita de `curation_status` antes — decisão humana separada da decisão de promover, para evitar que uma promoção "resolva" silenciosamente uma classificação de confidencialidade que ninguém revisou de propósito.

## Racional

Reaproveitar Promote em vez de criar uma quarta ação evita duplicar um mecanismo que já existe e já funciona (o caminho elegante). A única variável real entre os dois casos de Promote é se a titularidade muda — e isso já é exatamente o que determina, dentro da própria ação, se o caminho literal fica disponível (só no caso cross-domain) ou não (nunca no caso intra-domain). Adicionar uma ação nova só pra nomear essa distinção criaria superfície conceitual sem ganho de comportamento.

## Alternativas descartadas

- **Quarta ação nova ("Publish"/"Graduate").** Descartada — duplicaria o mecanismo do caminho elegante de Promote sem diferença real de comportamento, só de nome; aumenta a superfície que qualquer pessoa operando o Hipocampo precisa lembrar, sem necessidade.
- **Tratar como Depromote invertido.** Descartada — Depromote é definida especificamente como downgrade (`decisions/0027`); inverter seu comportamento pra cobrir também upgrade confundiria o nome da ação com o que ela de fato faz.
- **Permitir o caminho literal também no caso intra-domain.** Descartada — o caminho literal existe especificamente pra avisar sobre transferência de titularidade (`decisions/0007`); como titularidade não muda dentro do mesmo domínio, apresentar esse aviso seria falso e confundiria quem está confirmando a ação.
