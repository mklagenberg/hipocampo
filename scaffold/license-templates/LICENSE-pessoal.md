DIREITOS RESERVADOS E GOVERNANÇA DE CONHECIMENTO

Copyright (c) [ANO] [NOME COMPLETO] (@[usuario-github]). Todos os direitos reservados.

Este repositório (`[nome-do-repositorio]`) é um dos repositórios de conteúdo do Hipocampo,
metodologia versionada em `hipocampo`/`SPEC.md`. Contém uma base de conhecimento
pessoal identificável (trabalho e/ou vida pessoal) estruturada em arquivos Markdown (.md), de
titularidade individual de [NOME COMPLETO]. Não é um projeto colaborativo aberto —
contribuições de terceiros, quando existirem, são registradas via `contributors` no
frontmatter, nos termos do item 2.

1. TITULARIDADE E RETENÇÃO DE DIREITOS

   Todo o conteúdo deste repositório — documentos e respectivo frontmatter — é de
   autoria e propriedade exclusiva de [NOME COMPLETO], independentemente de ter
   sido redigido diretamente por ele(a) ou por um agente de inteligência artificial
   operando sob sua direção e curadoria. A autoria humana, nos termos da Lei nº
   9.610/98 (ou legislação equivalente aplicável), se sustenta pela direção criativa e
   curatorial exercida sobre o conteúdo gerado por agentes — o agente é instrumento,
   não autor.

2. CAMPOS `author` E `contributors`: CRÉDITO, NÃO COTITULARIDADE

   Documentos registram, no frontmatter, o autor responsável (`author`) e, quando
   aplicável, pessoas que solicitaram, complementaram ou atualizaram o conteúdo
   (`contributors`). Para conteúdo histórico migrado de acervo anterior ao Hipocampo,
   `author`/`contributors` podem referenciar uma seção de `CONTRIBUTORS.md` por
   `@nome-da-secao`, nos termos da `hipocampo/decisions/0006-creditos-de-contribuicao.md`
   — essa menção tem caráter exclusivamente de crédito e atribuição, individual ou
   coletivo, e não constitui cessão de coautoria, cotitularidade ou qualquer direito
   sobre o conteúdo, que permanece de titularidade integral do autor conforme item 1.

3. GOVERNANÇA DE CONHECIMENTO POR GRAU DE VISIBILIDADE

   Cada documento carrega, no frontmatter, um grau de confidencialidade (`visibility`)
   e um identificador de licença correspondente (`license`), sempre derivado
   mecanicamente do grau de visibilidade — nunca definido de forma divergente:

   a) `visibility: public` -> `license: LicenseRef-[Nome-Instancia]-Public`
      Leitura, cópia e reprodução livres por qualquer pessoa com acesso ao repositório.
      Corresponde a conteúdo pessoal já despersonalizado ou sem risco de exposição,
      sem vínculo sensível com terceiro identificável.

   b) `visibility: internal` -> `license: LicenseRef-[Nome-Instancia]-Internal`
      Uso cotidiano do autor ou de quem ele(a) autorizar. Não deve ser compartilhado
      com terceiros nem copiado para fora do contexto privado de uso sem
      despersonalização prévia.

   c) `visibility: confidential` -> `license: LicenseRef-[Nome-Instancia]-Confidential`
      Sensível e escopado ao contexto específico que o originou. Pode ser usado dentro
      desse contexto de origem. Nunca cruza para outro contexto, nunca é compartilhado
      com terceiros, nunca é sintetizado para responder perguntas fora do escopo que o
      gerou.

   d) `visibility: restricted` -> `license: LicenseRef-[Nome-Instancia]-Restricted`
      Grau máximo. Uso exclusivo do autor. Não deve ser acessado, sintetizado, exposto
      ou usado para compor qualquer resposta, nem mesmo dentro do próprio contexto de
      origem, por ninguém além do autor — inclusive por agentes operando em seu nome
      para outros fins.

   [NOTA — REMOVER ANTES DE USAR: se este repositório for de nível "vault" (só recebe
   confidential/restricted), mantenha só os itens (c) e (d) acima, renomeie os
   identificadores para `LicenseRef-[Nome-Instancia]-Vault-Confidential`/`-Vault-Restricted`,
   e ajuste o parágrafo de abertura pra descrever a relação com o repositório principal
   — ver `hipocampo-company-vault/LICENSE` como exemplo já publicado.]

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
   parcial, parafraseada ou despersonalizada no momento da resposta.

5. PROIBIÇÃO DE REDISTRIBUIÇÃO

   É vedada a cópia, publicação, sublicenciamento ou divulgação deste repositório a
   terceiros sem autorização prévia e por escrito do autor — exceto o conteúdo sob
   `LicenseRef-[Nome-Instancia]-Public`, cuja cópia e reprodução são livres nos
   termos do item 3(a).

ESTE MATERIAL É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU
IMPLÍCITA. EM NENHUMA HIPÓTESE O AUTOR SERÁ RESPONSÁVEL POR DANOS OU RECLAMAÇÕES
DECORRENTES DO USO DESTE MATERIAL.
