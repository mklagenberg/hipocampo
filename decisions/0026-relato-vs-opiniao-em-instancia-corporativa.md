# 0026 — Taxonomia de tipo de informação em instância corporativa

**Status:** Proposto

## Contexto

Instância corporativa hoje não distingue tipos de afirmação dentro de um documento — tudo é tratado com o mesmo peso epistêmico, seja um fato confirmado, algo que alguém relatou sem verificação, um julgamento subjetivo do autor, ou uma lembrança pessoal reconstrutiva. Frontmatter já resolve *quem* responde por um documento (`author`, invariante 2) e, para documento novo, *quem mais* contribuiu (`contributors`, `decisions/0006`) — mas nenhum dos dois resolve *que tipo* de afirmação está sendo feita dentro do corpo.

Exemplo real: `org-gauge/gauge-latam-observacoes.md`, em `hipocampo-company`, mistura observação ("LATAM orça errado — revisar, com olhar de tech e opec") e recomendação sobre pessoa nomeada ("Fábio ser coordenador") num documento `confidential`, nunca revisado desde a migração, sob nome de pessoa real, num repositório que colegas acessam. Não existe hoje gate que pergunte se aquele julgamento deveria estar ali, nem marcação que diferencie do relato factual ao lado.

Precedente orgânico, já presente no próprio corpus antes desta decisão existir: `org-gauge/modelo-matricial-gauge-e-papel-do-principal.md` já rotula trechos como "relatado" e fecha com "fatos internos relatados na origem e devem ser confirmados antes de serem usados como dados institucionais oficiais" — distinguindo relato de fato confirmado organicamente, sem convenção formal. Isso é evidência de que um binário relato/opinião não é suficiente — falta pelo menos um terceiro estado (fato confirmado) e um quarto categoricamente diferente dos outros três (lembrança pessoal).

## Decisão

1. Corpo de documento que mistura mais de um tipo de afirmação rotula os trechos relevantes com um destes quatro prefixos:
   - **Fato:** afirmação verificada/confirmada — pode ser tratada como dado institucional com confiança.
   - **Relato:** o que foi dito ou observado, ainda não confirmado — uma fotografia do que foi reportado, não necessariamente verdade estabelecida.
   - **Opinião:** julgamento de valor do autor ou de um contribuidor — trocando de autor, a conclusão pode divergir.
   - **Lembrança:** recordação pessoal reconstrutiva — sujeita a viés e erosão de memória; categoricamente diferente de relato (não é o que alguém contou) e de opinião (não é julgamento de valor, é reconstrução de um evento vivido). Nome escolhido deliberadamente diferente de "memória" pra não colidir com o conceito já estabelecido de "camadas de memória" (SPEC.md, seção 5-A — sensorial/curto prazo/longo prazo), que é sobre estágio de processamento de um item entrando no sistema, não sobre confiabilidade de uma afirmação.

   Documento inteiramente de um só tipo não precisa rotular frase a frase — a rotulagem existe só pra documento misto (mesmo princípio de não impor estrutura desproporcional ao caso comum, `BEST-PRACTICES.md`, item 1).

2. Campo de frontmatter `contains_subjective_content: true|false` (default `false`), relevante quando `owner` está preenchido (instância corporativa). Cobre só **Opinião** e **Lembrança** — as duas categorias com risco real de responsabilização pessoal, já que `author` é sempre uma pessoa real (invariante 2) e ambas são subjetivas, não independentemente verificáveis. **Fato** e **Relato** não acionam esse campo — carregam risco de precisão, não de responsabilização pessoal de quem escreveu. Permite que o frontmatter audit (seção 5-B) e a auditoria estrutural semanal (seção 5-C) encontrem esses documentos sem ler corpo inteiro de todo candidato (mantém o princípio frontmatter-first, seção 2-B).

3. O `@handle` só é anexado ao rótulo quando o documento tem `contributors` preenchido (`decisions/0006`) — sinal de que mais de uma pessoa contribuiu conteúdo àquele documento específico, tornando `author` sozinho insuficiente pra saber de quem é cada trecho. Documento de autor único (sem `contributors`) dispensa o handle inline; `author` do frontmatter já resolve a atribuição sem redundância.

4. Gate de escrita: antes de qualquer Create/Update gravar Opinião ou Lembrança nova (`contains_subjective_content` passando a `true`) numa instância corporativa, o agente pergunta explicitamente se aquele conteúdo deve ficar ali marcado, ou ir pra instância pessoal do autor/contribuidor responsável. Sem confirmação explícita de "sim, fica", vai pra pessoal — nunca adivinha (mesmo princípio do roteador de repositórios). Aplica-se também na função de consolidação do ritual REM (seção 5-A) ao triar `inbox/` com destino a instância corporativa, e à ação Promote (seção 13, `decisions/0027`) ao reavaliar rótulos no novo contexto.

5. `SPEC.md`, seção 2 (schema unificado): `contributors` passa a constar explicitamente na listagem central de campos — já existia e já está em uso real (`decisions/0006`, `CONTRIBUTORS.md` de instâncias corporativas), mas nunca apareceu na listagem principal do schema, só na Decision Record que o instituiu. Correção de lacuna documental, não capacidade nova.

## Racional

`author` é sempre pessoa real, nunca a IA (invariante 2) — isso já cria risco de exposição quando o conteúdo é subjetivo, não factual, num repositório que sobrevive ao tempo de empresa de quem escreveu e que outras pessoas com acesso ao repositório podem ler. Relato é, em princípio, verificável contra um evento ou decisão; opinião e lembrança não são — trocando de autor, ou revisitando a memória, a conclusão pode divergir. Fato, uma vez confirmado, pode ser tratado como dado institucional sem essa ressalva. Isso não conflita com `type: decision` (seção 7): aquilo é julgamento sobre a arquitetura da própria instância, categoria já sancionada e distinta de opinião sobre negócio, estratégia ou pessoas de terceiros. Reaproveitar `contributors` em vez de criar mecanismo de atribuição paralelo evita duplicar um campo que já resolve exatamente essa pergunta ("quem mais escreveu isso").

## Alternativas descartadas

- **Manter o binário relato/opinião original desta decisão.** Rejeitada: o próprio corpus já demonstra a necessidade de um terceiro estado (fato confirmado, ver `modelo-matricial-gauge-e-papel-do-principal.md`) e de um quarto categoricamente distinto (lembrança pessoal, reconstrutiva por natureza, diferente de relato de terceiro e de julgamento de valor).
- **Um campo de frontmatter por categoria (`contains_fact`, `contains_relato`, etc.).** Rejeitada: só Opinião e Lembrança carregam risco de responsabilização pessoal que justifica descoberta via frontmatter sem ler o corpo; Fato e Relato não precisam desse tratamento, então um único campo (`contains_subjective_content`) cobrindo as duas categorias de risco é suficiente, sem inflar o schema.
- **Marcar `@handle` em toda frase, sempre, independente de autor único.** Rejeitada: redundante quando `author` já resolve sozinho, e contraria o princípio de não impor estrutura desproporcional cedo demais.
- **Banir opinião/lembrança de repositório corporativo.** Rejeitada: às vezes o julgamento ou a lembrança registrada é a decisão institucional que vale preservar com atribuição — o problema não é existir lá, é existir sem ser explícita e sem opt-in do autor.
- **Novo valor de `type` (`type: opinion`) em vez de flag de frontmatter.** Rejeitada: viola a regra de expansão de `type` (seção 3, exige massa crítica) e não resolve o caso comum, que é documento misto.
- **Campo `contributors` novo, paralelo ao existente.** Rejeitada após checagem: `decisions/0006` já resolve exatamente essa necessidade pra documento novo; criar um segundo mecanismo duplicaria schema sem ganho.
