# Hipocampo — Boas Práticas

Este guia é para quem já leu o [Getting Started](GETTING-STARTED.md) e quer usar o Hipocampo bem — não só corretamente, mas de um jeito que segure o teste do tempo. Ele nasceu de erros reais cometidos numa migração de centenas de documentos (não de teoria) — cada recomendação aqui já foi testada, quebrada, ou aprendida do jeito difícil por alguém antes de você.

Se você quer o texto normativo completo, ele está no [SPEC.md](SPEC.md). Aqui é o "e na prática, o que eu faço?".

## 1. Usando bem no dia a dia

**Nem toda decisão precisa de um Decision Record.** Se a dúvida é "por que esse cliente foi pro cofre e não pro repositório geral", isso é uma decisão da sua instância — vira um documento comum com `type: decision`, do lado do conteúdo. Um Decision Record de verdade (pasta `decisions/` do `hipocampo`) é reservado pra mudança na metodologia em si — schema, regra, comportamento do agente. Confundir os dois deixa o `hipocampo` inchado com decisões que não interessam a mais ninguém fora da sua instância.

**`related` vazio quase sempre é preguiça, não ausência de conexão.** Se o texto de um documento cita outro pelo nome, isso é uma conexão que merece entrar no campo `related` — não custa nada e economiza uma busca manual depois. A lição mais repetida durante a migração de conteúdo real foi exatamente essa: dezenas de documentos citavam uns aos outros no corpo do texto sem nenhum link estruturado.

**`category` nasce depois, nunca antes.** Não crie uma subpasta `crm/` ou `financeiro/` só porque você imagina que um dia vai precisar. Espere acumular alguns documentos do mesmo tema e só então promova pra subpasta — o mesmo raciocínio vale pra criar um novo valor de `type`. Estrutura demais, cedo demais, é tão ruim quanto estrutura nenhuma.

**`type: framework` é para metodologia sua, não para todo documento bem escrito.** Esse tipo existe porque ele muda quem é dono do conteúdo (você, mesmo que aplicado em contexto de trabalho — ver `DISCLAIMER.md`). Se o documento é só um bom guia técnico, sem essa questão de titularidade em jogo, ele é `reference`, não `framework`.

**Migrando conteúdo antigo? Três armadilhas garantidas:**
- O documento-índice de uma pasta antiga quase nunca deve ser copiado literalmente — ele normalmente acumula nomes, links e contexto que não pertencem ao lugar novo. Reescreva como um `README.md` limpo.
- Um documento genérico que virou vários documentos mais específicos precisa virar um "tombstone": `status: superseded`, com `superseded_by` listando todos os filhos — nunca dois documentos ativos dizendo a mesma coisa.
- Se o acervo antigo não tinha campo `date`, não invente — puxe a data do primeiro commit real do arquivo (histórico do git), é mais confiável que qualquer estimativa.

**Autoria de conteúdo migrado sem dono claro (equipe inteira, sem registro individual) tem um mecanismo próprio** (`CONTRIBUTORS.md` + `@nome-da-secao`, ver `decisions/0006`) — mas isso é só para o passado. Documento novo, escrito hoje, sempre tem um autor de verdade: a pessoa que escreveu ou dirigiu a escrita. Não force esse mecanismo em conteúdo novo só porque parece mais neutro.

## 2. Privacidade não é feature, é fundação

O Hipocampo não trata privacidade como uma etiqueta a mais no frontmatter — trata como parte do desenho. Vale entender por quê, porque isso muda como você deveria pensar ao escrever qualquer documento novo em instância de trabalho.

**O que nunca entra num repositório corporativo, resumido:** contrato ou NDA, avaliação de desempenho de alguém identificável, qualquer anotação de saúde (sua ou de terceiro), dado pessoal (senha, endereço, telefone/e-mail pessoal, nome de parente), e valor de salário, fornecedor ou projeto — com uma única exceção: o resultado de negócio entregue a um cliente num case (quanto de receita gerou, quanto de custo evitou) pode ficar como número real, porque é o próprio produto do trabalho, não exposição financeira interna. Nome, cargo e contato profissional de colega ou cliente são permitidos, sempre com o ano da referência ao lado — é uma fotografia datada, nunca um estado presumido atual. O detalhe completo está em `decisions/0009`.

**"Despersonalizar" um documento não é só trocar o nome.** Antes de considerar um documento seguro pra publicar, pergunte três coisas, na ordem de uma técnica real de anonimização (não inventamos isso, é o padrão usado por reguladores europeus):

1. **Isolamento** — mesmo sem o nome, dá pra isolar esse registro como sendo de uma pessoa/empresa específica, só de olhar pro resto do documento?
2. **Vinculação** — dá pra cruzar esse documento com outro que você já tem e juntar as peças?
3. **Inferência** — dá pra deduzir quem é, com alta probabilidade, só pelo contexto (setor, porte, época, projeto)?

Se a resposta for sim pra qualquer uma das três, a despersonalização não pegou de verdade — troque mais detalhe, não só o nome próprio.

**Às vezes alguém tem o direito de pedir que o próprio nome saia do repositório de vez.** Isso é raro (o item acima já reduz bastante quando acontece), mas quando é um pedido legítimo de eliminação de dado pessoal, o Hipocampo tem um processo pra isso (`decisions/0010`): o conteúdo pessoal específico é substituído por um registro mínimo do que aconteceu (sem repetir o dado), nunca simplesmente ignorado.

**`visibility` é uma convenção de leitura, não um cadeado.** Marcar um documento como `confidential` não impede tecnicamente ninguém com acesso ao repositório de abrir o arquivo — quem protege de verdade é a permissão do próprio GitHub no nível do repositório. É por isso que a arquitetura do Hipocampo separa pessoal, pessoal-sigiloso, corporativo e corporativo-sigiloso em **repositórios diferentes**, não em pastas dentro do mesmo repositório: permissão real do GitHub é por repositório, então a separação física é a única coisa que garante que quem não deveria ver, realmente não vê.

**Nunca escreva verbatim o "como" de uma falha de segurança.** Se você documentar que uma vulnerabilidade foi encontrada, registre o quê e quando — nunca o payload, a query, ou qualquer coisa que reproduza o ataque pra quem ler depois.

## 3. Adotando o Hipocampo num time ou empresa novo

**Comece pensando em quantos repositórios você precisa, não em quantas pastas.** O desenho de referência é quatro: um pessoal e um pessoal-sigiloso (pra quem adota sozinho), um do time/empresa e um sigiloso do time/empresa (pra quem adota em grupo). Nem todo mundo precisa dos quatro desde o primeiro dia — mas pense na separação de *quem tem acesso a quê* antes de escrever o primeiro documento, porque mudar isso depois significa mover conteúdo entre repositórios, não só reclassificar uma etiqueta.

**O repositório sigiloso ("vault") não é "o lugar mais confidencial de tudo" — é o lugar pra um tipo específico de sensibilidade.** Depois que você aplicar a política de dados sensíveis (item 2 acima), o que sobra candidato ao vault normalmente é sensibilidade competitiva qualitativa — pipeline comercial em negociação, avaliação interna de parceria, postura de negociação —, não financeiro nem avaliação de pessoa (isso já está banido antes de chegar na pergunta "vault ou não").

**Nomeie categorias conforme elas nascem, não com um plano de pastas pronto no dia 1.** Mesma lógica do item 1, só que agora em escala de organização inteira.

**Não ligue nada de verdade até ter certeza.** Construa a instância nova em paralelo, sem apontar rotina, skill ou colega pra ela até você mesmo confirmar que está pronta. É mais fácil adiar uma ativação do que desfazer uma confusão de dois sistemas rodando ao mesmo tempo.

**Duas pegadinhas mecânicas do GitHub que todo adotante encontra mais cedo ou mais tarde:**
- **"Use this template" só cria repositório novo** — não existe forma de aplicar um template retroativamente a um repositório que você já criou vazio. E ele também copia a LICENSE do template de origem, mesmo quando isso não faz sentido no destino — remova-a depois, é esperado.
- **Instalar um app de IA (como o conector do GitHub) num repositório de organização é diferente de autorizá-lo na sua conta pessoal.** São duas permissões separadas: quem autoriza (sua identidade) e quem instala (acesso ao repositório em si). Se sua conta pessoal não for administradora da organização, você vai precisar de uma segunda conta que seja, só pra fazer a instalação — a autorização da sua conta pessoal continua igual, não precisa refazer nada nela.

---

*Este documento é vivo — se você encontrar um erro comum que não está listado aqui, ele provavelmente merece uma linha nova.*
