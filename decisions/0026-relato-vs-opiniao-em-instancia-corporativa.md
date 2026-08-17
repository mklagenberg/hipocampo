# 0026 — Relato vs. opinião em instância corporativa

**Status:** Proposto

## Contexto

Instância corporativa hoje não distingue fato relatado/observável de julgamento subjetivo do autor. Frontmatter já resolve *quem* responde por um documento (`author`, invariante 2) e, para documento novo, *quem mais* contribuiu (`contributors`, `decisions/0006`) — mas nenhum dos dois resolve *que tipo* de afirmação está sendo feita dentro do corpo.

Exemplo real: `org-gauge/gauge-latam-observacoes.md`, em `hipocampo-company`, mistura observação ("LATAM orça errado — revisar, com olhar de tech e opec") e recomendação sobre pessoa nomeada ("Fábio ser coordenador") num documento `confidential`, nunca revisado desde a migração, sob nome de pessoa real, num repositório que colegas acessam. Não existe hoje gate que pergunte se aquele julgamento deveria estar ali, nem marcação que diferencie do relato factual ao lado (ex.: `org-gauge/modelo-matricial-gauge-e-papel-do-principal.md`, que já rotula organicamente trechos como "relatado", sem que isso seja convenção formal).

## Decisão

1. Novo campo opcional de frontmatter, `contains_opinion: true|false` (default `false`), relevante quando `owner` está preenchido (instância corporativa). Sinaliza que o corpo contém ao menos um trecho marcado como opinião pessoal do autor (ou de um contribuidor), permitindo que o frontmatter audit (seção 5-B) e a auditoria estrutural semanal (seção 5-C) encontrem esses documentos sem ler corpo inteiro de todo candidato (mantém o princípio frontmatter-first, seção 2-B).

2. Convenção de corpo: documento que mistura relato e opinião rotula os trechos relevantes com prefixo **Relato:** / **Opinião:**. Documento inteiramente relato ou inteiramente opinião não precisa rotular frase a frase — só o `contains_opinion` correto já basta (evita estrutura desproporcional ao caso comum, mesmo princípio de `BEST-PRACTICES.md`, item 1).

3. O `@handle` só é anexado ao rótulo quando o documento tem `contributors` preenchido (`decisions/0006`) — sinal de que mais de uma pessoa contribuiu conteúdo àquele documento específico, tornando `author` sozinho insuficiente pra saber de quem é cada trecho. Documento de autor único (sem `contributors`) dispensa o handle inline; `author` do frontmatter já resolve a atribuição sem redundância.

4. Gate de escrita: antes de qualquer Create/Update gravar opinião (`contains_opinion` passando a `true`) numa instância corporativa, o agente pergunta explicitamente se aquele julgamento deve ficar ali marcado, ou ir pra instância pessoal do autor/contribuidor responsável. Sem confirmação explícita de "sim, fica", vai pra pessoal — nunca adivinha (mesmo princípio do roteador de repositórios). Aplica-se também na função de consolidação do ritual REM (seção 5-A) ao triar `inbox/` com destino a instância corporativa.

5. `SPEC.md`, seção 2 (schema unificado): `contributors` passa a constar explicitamente na listagem central de campos — já existia e já está em uso real (`decisions/0006`, `CONTRIBUTORS.md` de instâncias corporativas), mas nunca apareceu na listagem principal do schema, só na Decision Record que o instituiu. Correção de lacuna documental, não capacidade nova.

## Racional

`author` é sempre pessoa real, nunca a IA (invariante 2) — isso já cria risco de exposição quando o conteúdo é subjetivo, não factual, num repositório que sobrevive ao tempo de empresa de quem escreveu e que outras pessoas com acesso ao repositório podem ler. Relato é, em princípio, verificável contra um evento ou decisão; opinião não é — trocando de autor, a conclusão pode divergir. Isso não conflita com `type: decision` (seção 7): aquilo é julgamento sobre a arquitetura da própria instância, categoria já sancionada e distinta de opinião sobre negócio, estratégia ou pessoas de terceiros. Reaproveitar `contributors` em vez de criar mecanismo de atribuição paralelo evita duplicar um campo que já resolve exatamente essa pergunta ("quem mais escreveu isso").

## Alternativas descartadas

- **Marcar `@handle` em toda frase, sempre, independente de autor único.** Rejeitada: redundante quando `author` já resolve sozinho, e contraria o princípio de não impor estrutura desproporcional cedo demais.
- **Banir opinião de repositório corporativo.** Rejeitada: às vezes a opinião registrada é a decisão institucional que vale preservar com atribuição — o problema não é opinião existir lá, é existir sem ser explícita e sem opt-in do autor.
- **Novo valor de `type` (`type: opinion`) em vez de flag de frontmatter.** Rejeitada: viola a regra de expansão de `type` (seção 3, exige massa crítica) e não resolve o caso comum, que é documento misto — não inteiramente opinativo.
- **Campo `contributors` novo, paralelo ao existente.** Rejeitada após checagem: `decisions/0006` já resolve exatamente essa necessidade pra documento novo; criar um segundo mecanismo duplicaria schema sem ganho.
