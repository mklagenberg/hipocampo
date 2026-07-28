# 0008 — Ritual REM e modelo de três camadas de memória

**Status:** Aceito

## Contexto

O SPEC.md (seção 5) formaliza como um documento já existente envelhece (`temporality`/`ttl`/rotina de staleness), mas não formaliza como um item novo — captura bruta, ainda não curada — entra no sistema e vira documento consolidado. Sem isso explícito na metodologia, cada instância reinventa (ou não tem) seu próprio pipeline de captura→consolidação. Uma instância anterior ao Hipocampo já opera esse pipeline sob o nome de ritual REM — nome que é, aliás, a origem conceitual do próprio nome "Hipocampo" (consolidação de memória de curto pra longo prazo, no cérebro, via hipocampo durante o sono REM).

## Decisão

O Hipocampo adota um modelo de quatro estações de memória e um ritual de consolidação entre elas (SPEC.md, nova seção 5-A):

1. **Memória sensorial** — buffer bruto de percepção (ex.: a janela de conversa). Alta perda por design; não é papel do Hipocampo reter isso.
2. **Gate de atenção** — mecanismo explícito que decide o que atravessa da sensorial pra curto prazo (ex.: um "check-in"/dump de sessão). Só entra no sistema canônico o que passa pelo gate.
3. **Memória de curto prazo** — item já capturado no sistema canônico (git), ainda não curado. Mínimo viável: uma pasta `inbox/` versionada no próprio repositório — infraestrutura de nuvem (fila, banco de estado) é "Extensão local" opcional, nunca linha de base.
4. **Ritual REM (consolidação)** — lê só da memória de curto prazo, nunca direto da sensorial. Roda periodicamente ou sob pedido. Para cada item pendente, decide entre virar documento novo, fundir com um existente, ou descartar. O plano completo é sempre apresentado antes de qualquer execução (mesmo invariante de "agente nunca escreve sem pedido explícito", seção 8, aplicado a este ritual).
5. **Memória de longo prazo** — documento atômico, curado, frontmatter completo. É o corpo principal de qualquer repositório de conteúdo Hipocampo já existente desde a v1.0.0 — não é capacidade nova.

Regras adicionais: atomicidade (documento consolidado = um conceito só; material bruto com N ideias vira N documentos); `memory.md` de harness de agente e snapshot de transferência não são memória sensorial nem passam pelo ritual REM (mecanismos distintos); evolução de schema é reativa, só cresce por massa crítica (reforça o princípio já geral da seção 4).

## Racional

Formaliza um padrão que já opera de fato numa instância, em vez de deixá-lo implícito e sujeito a reinvenção divergente por instância nova. É estritamente aditivo — nenhuma instância existente quebra por causa disso; adotar o ritual é opcional, como o resto da rotina de staleness na prática já é. Fecha o círculo conceitual entre o nome do projeto e a metáfora que o originou.

## Alternativas descartadas

- **Manter como convenção implícita, não documentada no SPEC.** Descartado — é exatamente o problema que motivou este DR: conhecimento operacional real preso numa instância, não reutilizável como metodologia.
- **Trazer a infraestrutura de nuvem (fila/banco de estado) como parte obrigatória do modelo.** Descartado — quebra o invariante de simplicidade do escopo ("git + markdown + rituais de IA", seção 1). Fica só como exemplo de Extensão local possível.
- **Formalizar só a rotina de staleness (já existente) como suficiente.** Descartado — staleness cobre envelhecimento de documento já consolidado, não resolve captura→consolidação.