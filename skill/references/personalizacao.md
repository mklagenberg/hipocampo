# Personalização obrigatória — roteador de repositórios e identidade

Esta skill genérica (`hipocampo/skill/SKILL.md`) só conhece um repositório universal, o mesmo pra qualquer usuário: `mklagenberg/hipocampo` (a metodologia em si — spec, decisions, scaffold). Ela **não** conhece nenhum repositório pessoal ou corporativo — hardcodar quebraria a possibilidade de qualquer pessoa ou empresa adotar a mesma skill.

Antes de usar de verdade, quem adota a metodologia salva sua própria cópia personalizada (ex.: via `save_skill`), preenchendo as duas tabelas abaixo.

## Roteador de repositórios

```
| Papel                          | Repositório               |
|---------------------------------|----------------------------|
| Conceitos pessoais (público*)   | [preencher: owner/repo]    |
| Vault pessoal                   | [preencher: owner/repo]    |
| Conteúdo corporativo             | [preencher: owner/repo]    |
| Vault corporativo                | [preencher: owner/repo]    |
```

\* "público" aqui é só "menos restrito dentro do escopo pessoal" — nenhum repositório de conteúdo é público à internet (invariante 1, ver `invariantes.md`).

Nem toda instância tem os quatro papéis — preencher só o que existir. Sem essa tabela preenchida, a skill não sabe onde ler/escrever conhecimento além da própria metodologia.

## Identidade de autor multi-conta (preencher se aplicável)

Se a mesma pessoa opera mais de uma conta de git que resolvem pro mesmo `author` humano (ex.: conta pessoal e conta vinculada a um empregador):

```
| Conta de git         | Papel                     |
|-----------------------|----------------------------|
| [preencher: @handle]  | Pessoal                    |
| [preencher: @handle]  | Profissional/corporativo   |
```

Nunca preencher isso na cópia genérica do template — só na cópia pessoal. Direção de convite entre instância pessoal e corporativa: a conta pessoal sempre convida a profissional pro second brain **pessoal**, nunca o inverso (`hipocampo/SPEC.md`, seção 12; `decisions/0020`).

## Exemplo de uso do roteador

> Usuário: "salva essa decisão sobre o projeto X no meu second brain"
>
> Se "projeto X" é claramente de contexto de trabalho, a skill personalizada sabe (pela tabela acima) que "conteúdo corporativo" é `owner-empresa/repo-corporativo`, não o vault pessoal. Se a instância ainda não tem a tabela preenchida, a skill não adivinha — pergunta em qual repositório o usuário quer salvar.
