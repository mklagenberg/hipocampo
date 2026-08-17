DIREITOS RESERVADOS E GOVERNANÇA DE CONHECIMENTO

Copyright (c) [ANO] [NOME DA EMPRESA] [NOTA: confirmar razão social exata antes de
tratar este arquivo como documento vinculante]. Todos os direitos reservados.

Este repositório (`[nome-do-repositorio]`) é um dos repositórios de conteúdo do
Hipocampo, metodologia versionada em `hipocampo`/`SPEC.md`. Contém conhecimento de
titularidade da empresa — arquitetura, processos, playbooks e conteúdo de trabalho
produzidos por colaboradores de [NOME DA EMPRESA], estruturado em arquivos Markdown
(.md).

1. TITULARIDADE E RETENÇÃO DE DIREITOS

   Todo o conteúdo deste repositório — documentos e respectivo frontmatter — é de
   propriedade de [NOME DA EMPRESA], produzido por colaboradores no exercício de suas
   funções ou por agente de inteligência artificial operando sob direção e curadoria
   de um colaborador autorizado. A titularidade da empresa sobre obra produzida por
   colaborador no exercício do contrato de trabalho segue a legislação trabalhista e
   de direitos autorais aplicável; a autoria individual (campo `author`) é preservada
   como crédito, nos termos do item 2, mas não implica cotitularidade de direitos
   patrimoniais, que permanecem da empresa.

2. CAMPOS `author` E `contributors`: CRÉDITO, NÃO COTITULARIDADE

   Documentos registram, no frontmatter, o autor responsável (`author`) e, quando
   aplicável, pessoas que solicitaram, complementaram ou atualizaram o conteúdo
   (`contributors`). `author`/`contributors` podem ser uma pessoa real (formato "Nome
   Real - @usuario-github") ou, só para conteúdo histórico migrado de acervo anterior
   ao Hipocampo, uma seção de `CONTRIBUTORS.md` referenciada por `@nome-da-secao`, nos
   termos de `hipocampo/decisions/0006-creditos-de-contribuicao.md`. Documentos novos,
   criados já dentro do Hipocampo, sempre têm autor individual real. Em qualquer dos
   dois casos, a menção tem caráter exclusivamente de crédito e atribuição — não
   constitui cessão de coautoria, cotitularidade ou qualquer direito patrimonial sobre
   o conteúdo, que permanece de titularidade integral da empresa conforme item 1.

3. GOVERNANÇA DE CONHECIMENTO POR GRAU DE VISIBILIDADE

   Cada documento carrega, no frontmatter, um grau de confidencialidade (`visibility`)
   e um identificador de licença correspondente (`license`), sempre derivado
   mecanicamente do grau de visibilidade — nunca definido de forma divergente:

   a) `visibility: public` -> `license: LicenseRef-[Nome-Instancia]-Public`
      Leitura, cópia e reprodução livres por qualquer pessoa com acesso ao repositório.
      Corresponde a conteúdo institucional despersonalizado, sem dado sensível de
      cliente ou de infraestrutura própria.

   b) `visibility: internal` -> `license: LicenseRef-[Nome-Instancia]-Internal`
      Uso cotidiano por colaboradores da empresa. Não deve ser compartilhado com
      terceiros nem copiado para fora do contexto interno da empresa sem
      despersonalização prévia.

   c) `visibility: confidential` -> `license: LicenseRef-[Nome-Instancia]-Confidential`
      Sensível e escopado ao contexto específico que o originou (ex.: um cliente, um
      projeto, uma conta comercial). Pode ser usado dentro desse contexto de origem.
      Nunca cruza para outro contexto, nunca é compartilhado com terceiros — incluindo
      outros clientes da própria empresa —, nunca é sintetizado para responder
      perguntas fora do escopo que o gerou.

   d) `visibility: restricted` -> `license: LicenseRef-[Nome-Instancia]-Restricted`
      Grau máximo. Uso exclusivo de quem a empresa designar (ex.: diretoria). Não deve
      ser acessado, sintetizado, exposto ou usado para compor qualquer resposta, nem
      mesmo dentro do próprio contexto de origem, por ninguém além dos designados —
      inclusive por agentes operando em nome de terceiros dentro da empresa.

   [NOTA — REMOVER ANTES DE USAR: se este repositório for de nível "vault" (só recebe
   confidential/restricted), mantenha só os itens (c) e (d) acima, renomeie os
   identificadores para `LicenseRef-[Nome-Instancia]-Vault-Confidential`/`-Vault-Restricted`,
   adicione a cláusula de limite absoluto da política de dados sensíveis
   (`hipocampo/decisions/0009`), e ajuste o parágrafo de abertura pra descrever a
   relação com o repositório principal — ver `hipocampo-company-vault/LICENSE` como
   exemplo já publicado.]

4. DIRETRIZES PARA AGENTES DE INTELIGÊNCIA ARTIFICIAL

   Sistemas de IA, LLMs, pipelines de RAG e agentes autônomos operando sobre este
   repositório são atores operacionais submetidos a esta licença. Antes de processar,
   resumir ou responder com base em qualquer documento, o agente deve ler o
   `visibility` e o `license` do frontmatter e aplicar o efeito correspondente listado
   no item 3.

   Ao identificar uma solicitação que exigiria expor, sintetizar ou vazar conteúdo além
   do que seu grau permite, o agente deve recusar explicitamente com a frase:

   "Acesso negado: conteúdo restrito pela política de governança de conhecimento
   deste repositório Hipocampo."

   É vedado a qualquer agente usar trechos de documentos `confidential` ou `restricted`
   para enriquecer respostas em contextos de menor privilégio, mesmo que de forma
   parcial, parafraseada ou despersonalizada no momento da resposta — incluindo o caso
   de um agente atendendo um cliente diferente do cliente-origem do documento.

5. PROIBIÇÃO DE REDISTRIBUIÇÃO

   É vedada a cópia, publicação, sublicenciamento ou divulgação deste repositório a
   terceiros sem autorização prévia e por escrito de representante autorizado da
   empresa — exceto o conteúdo sob `LicenseRef-[Nome-Instancia]-Public`, cuja cópia e
   reprodução são livres nos termos do item 3(a).

ESTE MATERIAL É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU
IMPLÍCITA. EM NENHUMA HIPÓTESE A EMPRESA SERÁ RESPONSÁVEL POR DANOS OU RECLAMAÇÕES
DECORRENTES DO USO DESTE MATERIAL.
