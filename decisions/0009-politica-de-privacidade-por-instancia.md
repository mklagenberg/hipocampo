# 0009 — Política de privacidade e dados sensíveis por tipo de instância

**Status:** Aceito

## Contexto

Ao longo do Lote 4, sucessivos sub-lotes de migração esbarraram em decisões pontuais sobre nomes de colegas/clientes, avaliações de desempenho, dados de saúde e valores financeiros internos (salário, fornecedor, projeto) — tratadas ad hoc, sem regra explícita na metodologia. O sub-lote F, o mais volumoso (82 documentos de contexto de trabalho), tornou o padrão visível e insustentável: sem uma política declarada, cada instância corre risco de aplicar critério de sensibilidade de forma divergente, ou de reinventar a mesma decisão repetidamente. O SPEC.md define schema, temporalidade e camadas de memória (seção 5-A, DR0008), mas nunca tinha definido o que pode ou não ser escrito, por tipo de dado, dependendo de quem é o titular da instância.

## Decisão

O Hipocampo adota uma política de dados sensíveis diferenciada por tipo de instância (SPEC.md, nova seção 2-A):

Instância corporativa (`owner` é uma organização, não uma pessoa física) nunca armazena, independente do nível de `visibility`, mesmo no tier mais restrito:

- Conteúdo de contratos ou NDAs.
- Avaliação de desempenho de indivíduo identificável.
- Anotação sobre saúde de qualquer pessoa — titular da instância ou terceiro.
- Dado pessoal de qualquer pessoa: senha, endereço pessoal, telefone ou e-mail pessoal, nome de parente.
- Valor de salário, valor pago a fornecedor, ou valor de projeto/contrato — com uma exceção única: valor que representa resultado de negócio entregue a um cliente num `type: case` (receita gerada, custo evitado) pode ser mantido como valor absoluto, porque é o próprio produto do case, não exposição financeira interna.
- Aprendizado interno quantificado (ex.: economia de processo) é registrado como variação percentual, nunca como valor absoluto.

Dado financeiro sobre terceiro que não é fornecedor/parceiro comercial direto (ex.: faturamento de um concorrente ou potencial parceiro, extraído de fonte pública verificável, usado como inteligência de mercado) não conta como "valor de fornecedor ou projeto" e pode ser mantido — desde que a fonte pública seja citada explicitamente no documento.

Nome completo, cargo, e-mail profissional, telefone ou endereço profissional — de colega ou de contato de cliente — são permitidos em instância corporativa, desde que acompanhados de citação de ano/data: o registro é sempre uma fotografia datada, nunca um estado presumido atual.

Questões pessoais de qualquer indivíduo (saúde, situação financeira pessoal) nunca vão pra instância corporativa — sempre pra instância pessoal do titular relevante, se existir uma.

Detalhe técnico de vulnerabilidade ou exploração ativa (payload de ataque, query/dork que revela o comprometimento, credencial, endpoint explorável) nunca é registrado verbatim, em nenhuma instância — mesmo confidencial/restricted. Registra-se o fato (existência da falha, categoria, data do achado) e a resposta dada, nunca o material que reproduziria ou confirmaria o ataque pra quem ler o documento depois.

Quando um documento inteiro depende estruturalmente de um tipo de dado banido (não dá pra adaptar removendo só o trecho problemático), o agente não decide sozinho entre publicar mesmo assim ou descartar — sinaliza a violação ao humano responsável pela instância e aguarda decisão explícita.

## Racional

Fecha uma lacuna real, descoberta operacionalmente durante a migração de conteúdo de trabalho (sub-lote F): 82 documentos continham de tudo, de dado de RH sensível a taxa de fornecedor a nome de parente em nota solta, sem que a metodologia desse critério prévio pra decidir o que cabia. Sem essa política, o julgamento fica inteiramente ad hoc por sub-lote, o que não escala e gera inconsistência entre instâncias diferentes do mesmo método. A distinção "instância corporativa vs. pessoal" já existe implicitamente na arquitetura multi-repositório (`-company`/`-company-vault` vs. `-personal-vault`); este DR só torna explícito o que já era intenção de design.

## Alternativas descartadas

- **Deixar como critério implícito, decidido documento a documento.** Descartado: é exatamente o problema que motivou este DR.
- **Banir todo valor financeiro de instância corporativa, sem exceção pra impacto de case.** Descartado: um case comercial sem resultado quantificado perde a maior parte do valor como conhecimento reutilizável. A distinção entre "o que o cliente ganhou" (permitido) e "o que a organização cobrou/pagou internamente" (proibido) preserva o valor sem o risco.
- **Tratar avaliação de desempenho como só `restricted`/vault, em vez de banida.** Descartado: mesmo o nível mais alto de confidencialidade ainda é um repositório da organização — dado de desempenho de indivíduo identificável não pertence a nenhum tier corporativo, só à instância pessoal de quem faz a gestão, e mesmo lá exigiria descaracterização forte.
