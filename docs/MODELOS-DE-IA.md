# Modelos de IA e o Hipocampo

Referência central, não específica de nenhuma instância — ver `hipocampo/decisions/0002` (replicação gera divergência silenciosa) sobre por que este conteúdo mora aqui e instâncias novas recebem só o link, não uma cópia.

Hipocampo é desenhado pra funcionar com qualquer agente de IA capaz de ler/escrever markdown via git — não depende de nenhum modelo ou produto específico (ver `DISCLAIMER.md`, "Dados sempre human-readable"). Ainda assim, algumas características de um modelo/produto importam pra operar a metodologia bem.

## O que importa, na prática

**Seguir instrução estruturada sem se desviar.** A metodologia depende de invariantes que não têm enforcement técnico automático (SPEC.md, seção 8) — o modelo precisa realmente seguir a regra "nunca escrever sem pedido explícito", não só quando conveniente. Isso é uma questão de instrução (skill bem escrita) mais do que de modelo específico, mas modelos mais capazes de seguir instrução longa e contextual sustentam isso com menos atrito.

**Janela de contexto e o motivo do frontmatter-first.** Nenhum modelo tem janela de contexto infinita, e mesmo os que têm janelas grandes cobram (em latência e em token) por usá-la inteira. A mecânica CRUD/frontmatter-first (SPEC.md, seção 2-B) existe exatamente pra isso: numa instância com muitos documentos, ler só o frontmatter de cada candidato antes de decidir ler o corpo completo é o que torna a metodologia viável em qualquer modelo, independente do tamanho da janela de contexto dele.

**Rotinas de IA são probabilísticas, não determinísticas.** Nenhum modelo — por mais capaz que seja — garante 0% de erro numa classificação de `type`/`temporality`, numa triagem de staleness, ou numa decisão de consolidação do ritual REM. É por isso que todo ritual da metodologia sempre apresenta o plano antes de executar (SPEC.md, seção 8) — a supervisão humana no laço não é uma camada de segurança contra um modelo ruim, é uma camada de segurança contra a natureza probabilística de qualquer modelo, inclusive os melhores disponíveis.

**MCP do GitHub como denominador comum.** A forma como o Hipocampo é operado — leitura/escrita de repositório via ferramentas — depende de o ambiente de IA em uso ter acesso a um MCP (ou mecanismo equivalente) de GitHub. Isso é o que torna a metodologia utilizável a partir de ferramentas diferentes (Claude Cowork, ChatGPT, Gemini, GitHub Copilot, Antigravity, entre outras) sem reescrever nada da metodologia em si — o princípio de operação é o mesmo em qualquer uma; o que muda é só a mecânica de cada ferramenta pra conectar esse MCP. Detalhe prático por ferramenta: ver `BEST-PRACTICES.md` e o guia multi-ferramenta da instância que você estiver seguindo.

## O que não importa

Não há modelo "oficialmente suportado" pelo Hipocampo, nem um mínimo de capacidade certificado. A metodologia não faz benchmark de modelo nenhum — ela assume, como pressuposto técnico (`DISCLAIMER.md`), só que o agente em uso é capaz de operar markdown estruturado e seguir instrução. Qual modelo/produto usar é decisão de quem opera a instância, não algo que a metodologia prescreve.
