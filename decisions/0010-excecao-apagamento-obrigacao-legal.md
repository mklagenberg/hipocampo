# 0010 — Exceção de apagamento físico por obrigação legal

**Status:** Aceito

## Contexto

O Invariante 3 existe pra garantir auditabilidade total — nenhuma decisão de conteúdo desaparece sem deixar rastro, mesmo quando o documento vira `archived` ou `superseded`. Isso é uma força real do Hipocampo. Mas essa mesma força colide com uma obrigação legal: se um documento contém dado pessoal de alguém identificável (um colega, um contato de cliente) e essa pessoa exerce o direito de eliminação previsto em lei, "nunca apagar fisicamente" não é uma opção válida — é descumprimento.

Duas coisas reduzem a frequência prática desse problema, sem eliminá-lo:

1. **A política de privacidade por instância (`decisions/0009`) já bane a maior parte do dado pessoal sensível** de instância corporativa (saúde, contato pessoal, avaliação de desempenho, valor de salário/fornecedor). O que sobra permitido — nome completo, cargo, contato profissional, com citação de ano — ainda é dado pessoal sob a lei, só que de severidade bem mais baixa. Esta exceção deve ser vista como cobertura pro resíduo, não pro grosso do conteúdo.
2. **LGPD Art. 4º, I** exclui do escopo da lei o "tratamento de dados pessoais realizado por pessoa natural para fins exclusivamente particulares e não econômicos" — o que provavelmente tira uma instância pessoal privada e sem propósito econômico do escopo da lei por definição, não só na prática. A exposição real e recorrente fica concentrada em instância corporativa, onde a lei incide de fato e o `owner` (a organização) atua como Controlador.

## Decisão

O Invariante 3 continua valendo para o ciclo de vida normal do conhecimento — nada é apagado só porque ficou desatualizado, errado, ou foi substituído; isso continua resolvido por `archived`/`superseded`, sem exceção.

Cria-se uma exceção formal, estreita e documentada: **apagamento físico do conteúdo pessoal específico é permitido quando, e somente quando, acionado por uma solicitação legítima de eliminação de um titular de dado identificável, com base legal real** (LGPD Art. 16 / GDPR Art. 17). Não é uma porta aberta para "limpar" o repositório por conveniência — é resposta a um direito exercido.

Quando essa exceção é acionada:

1. **O agente nunca decide sozinho.** Mesmo princípio do Invariante 5 e da `decisions/0009`: a legitimidade do pedido (é mesmo um direito de eliminação válido, ou existe base legal que autoriza manter o dado — cumprimento de obrigação legal, processo em curso, etc.) é avaliada pelo humano responsável pela instância, não pelo agente.
2. **O conteúdo pessoal específico é substituído por um "tombstone"** — um registro mínimo que preserva só o fato de que uma remoção ocorreu, a data, a base legal invocada, e uma descrição genérica do tipo de conteúdo removido (ex.: "nome e cargo de indivíduo removidos a pedido do titular, LGPD art. 16, em YYYY-MM-DD"), nunca o dado em si. Isso preserva a auditabilidade do fato da remoção, sem preservar o que foi removido.
3. **Limitação técnica reconhecida, não escondida:** substituir o conteúdo no estado atual do repositório (HEAD) resolve o caso de uso comum (quem lê o repositório hoje não vê mais o dado). Mas o histórico do git, por padrão, ainda contém o conteúdo original nos commits antigos — qualquer pessoa com acesso ao repositório pode checar um commit anterior e ver o dado removido. Se a solicitação exigir remoção completa também do histórico, isso requer uma segunda etapa manual e explícita (reescrita de histórico via `git filter-repo`/BFG), fora do fluxo normal do Hipocampo, decidida caso a caso pelo humano responsável — nunca automática, porque reescrever histórico é uma operação destrutiva e rara, com efeito colateral em qualquer clone existente do repositório.

## Racional

Sem essa exceção, o Invariante 3 obriga o Hipocampo a descumprir uma lei real sempre que um titular de dado exercer um direito legítimo — isso não é uma hipótese remota, é um risco jurídico direto pra qualquer instância corporativa. A exceção é desenhada pra ser o menor desvio possível do invariante original: não abre uma porta geral de apagamento, mantém o registro do fato (preservando o espírito de auditabilidade), e reconhece honestamente a diferença entre "sumir do estado atual" e "sumir do histórico completo" — no mesmo espírito do `DISCLAIMER.md`, que já assume abertamente que `visibility` não é enforcement técnico. Fingir que o problema não existe seria pior do que documentá-lo com uma solução parcial e honesta.

## Alternativas descartadas

- **Manter o Invariante 3 sem exceção nenhuma.** Descartado: coloca qualquer instância corporativa em situação de descumprimento legal automático diante de uma solicitação válida.
- **Permitir apagamento livre, por qualquer motivo, revertendo o Invariante 3 de forma geral.** Descartado: destrói a auditabilidade que é a principal força do método — abriria espaço pra apagar decisão incômoda, não só cumprir direito legal.
- **Reescrever automaticamente o histórico do git toda vez que a exceção for acionada.** Descartado: é uma operação destrutiva e rara demais pra automatizar; decidir se vale a pena (e coordenar com quem tem clones do repositório) precisa ser humano, caso a caso.
- **Criar um novo valor de `status` (ex.: `erased`) só pra esse caso.** Descartado por ora — reaproveitar `revision_note` pra registrar o motivo e a base legal já é suficiente e evita inflar o enum de `status` por um caso raro (mesma regra de expansão reativa das seções 3/4 do SPEC.md).
