# Rituais de manutenção — frontmatter audit, REM, auditoria estrutural

Três rituais, cadências diferentes, sempre no escopo de **um repositório por vez** — cada repositório Hipocampo tem seu próprio `inbox/` e sua própria fila. Referência completa: `hipocampo/SPEC.md`, seções 5-A, 5-B, 5-C.

## Ordem de execução num ciclo diário

1. **Frontmatter audit** (determinístico, primeiro)
2. **Ritual REM** (consolidação + atualização, lê a saída do passo 1)

A auditoria estrutural roda à parte, cadência semanal.

## 1. Frontmatter audit — diário, determinístico

Varredura mecânica do frontmatter (nunca do corpo) de todo documento de um repositório: `ttl` vencido (conforme `temporality`), campo obrigatório ausente, outra violação detectável mecanicamente. Produz/atualiza `meta/fila-de-manutencao.md`. **Nunca decide disposição** — só relata. Isso não é julgamento de agente de IA: é varredura de regra fixa, reproduzível. Ver `decisions/0017`.

## 2. Ritual REM — diário, duas funções

**Consolidar:** ler `inbox/` (memória de curto prazo — já passou por um gate de atenção, ex. um dump/check-in de sessão, mas ainda não é atômica nem está no lugar certo; é estágio de sanitização, não captura bruta). Decidir por item: vira documento novo, funde com um existente, ou descarta.

**Atualizar memórias antigas:** ler `meta/fila-de-manutencao.md` (saída do frontmatter audit) e decidir disposição de cada pendência: revalidar (inclusive via pesquisa externa quando `source: url` — mesmo gatilho da skill `deep-research`), arquivar, superseder, ou corrigir campo.

**Sempre apresentar o plano completo de qualquer uma das duas funções antes de qualquer escrita** — mesma invariante de pedido explícito (ver `invariantes.md`, item 5), aplicada a este ritual especificamente. Ver `decisions/0008`, `decisions/0016`.

### Exemplo de um ciclo

> `meta/fila-de-manutencao.md` (produzida pelo frontmatter audit) lista: `projetos/case-acme.md` com `ttl` vencido há 40 dias, `temporality: ephemeral`.
>
> Ritual REM, função "atualizar memórias antigas": como é `ephemeral` e passou do prazo sem renovação, a regra da seção 5 já pré-marca como "sugestão: arquivar/superseder". O agente apresenta: "`case-acme.md` está com `ttl` vencido há 40 dias, `ephemeral` — sugiro marcar `status: archived`. Confirma?" — nunca aplica sozinho.

## 3. Auditoria estrutural — semanal, três funções

1. **Atomicidade** — documentos consolidados recentemente (ou apontados pela fila) ainda representam um conceito só, ou deveriam ser divididos?
2. **Posicionamento** — a estrutura de `category`/pastas ainda faz sentido? Algum documento está fora do escopo declarado no `AGENTS.md` do repositório (seção "Escopo deste repositório")?
3. **Vazamento de dado sensível** — algum documento contém algo que a política de dados sensíveis (seção 2-A do SPEC) proíbe para o **tipo de instância** declarado no `AGENTS.md` (campo "Tipo de instância": `corporativa`/`pessoal`) — nunca inferido pelo agente a partir do nome do repositório. Ver `decisions/0022`.

Qualquer achado das três funções é sempre apresentado ao humano responsável antes de qualquer ação — mover, dividir ou remover documento nunca acontece sozinho. Ver `decisions/0019`.

### Exemplo

> Auditoria semanal do repositório corporativo (`AGENTS.md` declara "Tipo de instância: corporativa"). Encontra `trabalho/negociacao-fornecedor-y.md` citando um valor de contrato em R$. Isso é exatamente o que a política de dados sensíveis proíbe pra instância corporativa (valor de fornecedor). O agente sinaliza: "achei um valor de contrato de fornecedor em `negociacao-fornecedor-y.md` — a política de instância corporativa não permite isso, nem em `restricted`. Quer que eu remova o valor absoluto (mantendo o resto do documento), ou prefere revisar você mesmo?" — nunca edita sozinho.

## Automação (scheduled tasks)

Cadência recorrente é boa candidata a `scheduled task` agêntica (frontmatter audit + REM diários em sequência; auditoria estrutural semanal à parte). Automação é decisão de implementação por instância, não faz parte da metodologia em si — configurar (ou não) fica a critério de quem opera aquela instância.
