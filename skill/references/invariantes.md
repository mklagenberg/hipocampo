# Invariantes — o que e por quê

Cinco regras que nenhuma instância Hipocampo sobrescreve, em nenhuma circunstância (`hipocampo/SPEC.md`, seção 8). Cada uma existe por um motivo estrutural específico, não por convenção arbitrária — importante saber o porquê pra reconhecer quando uma situação nova ainda cai sob a regra, mesmo que não pareça óbvio à primeira vista.

## 1. Nenhum repositório de conhecimento é público à internet

`visibility` no frontmatter (`public | internal | confidential | restricted`) é só uma etiqueta de intenção — o GitHub aplica permissão real por **repositório**, não por arquivo dentro dele. Uma etiqueta `confidential` num repositório público não impede ninguém de ler o arquivo; é decorativa. A única camada de enforcement que o host de fato aplica é a visibilidade do repositório. Por isso essa regra é invariante estrutural, não sugestão.

## 2. `author` é sempre uma pessoa, nunca a IA

Um agente pode escrever o texto, mas quem decidiu que aquilo virou conhecimento válido — quem responde pela afirmação registrada — é sempre humano. Sem isso, o second brain vira uma caixa preta de alegações sem dono rastreável. Exceção escopada só a conteúdo histórico/migrado sem autoria individual recuperável na origem (`CONTRIBUTORS.md`, `@nome-da-secao`) — documento novo nunca usa essa exceção.

## 3. Documento nunca é apagado fisicamente — só arquivado ou superseded

Preserva histórico de decisão (inclusive "por que eu achava isso antes"), evita perda silenciosa de contexto, e cria fricção deliberada contra apagar por conveniência. Exceção formal e estreita: obrigação legal real de eliminação de dado pessoal (LGPD Art. 16 / GDPR Art. 17) — sempre com decisão humana explícita, nunca decidida pelo agente sozinho, e sempre substituída por um registro mínimo do fato ("tombstone"), nunca rastro zero.

## 4. Separação de acesso é sempre por repositório, nunca por etiqueta dentro de um repositório compartilhado

Mesma lógica da invariante 1, aplicada dentro de um repositório com múltiplas pessoas: a granularidade real de permissão do GitHub é o repositório. `visibility: restricted` num repositório que o time inteiro acessa não impede ninguém do time de ler aquele arquivo especificamente. Conteúdo que precisa de enforcement técnico de fato vai para um repositório separado com permissão restrita — nunca só uma etiqueta de frontmatter num repositório mais aberto.

## 5. O agente nunca escreve, edita ou apaga conteúdo sem pedido explícito do usuário na conversa atual

Ponto de controle humano contra deriva autônoma. Mesmo os rituais recorrentes (frontmatter audit, REM, auditoria estrutural) só chegam sozinhos a **plano proposto** — a execução real de qualquer mudança de conteúdo sempre espera confirmação explícita nessa conversa. "Rodar o REM" não é a mesma coisa que "aplicar as decisões do REM sem revisão".
