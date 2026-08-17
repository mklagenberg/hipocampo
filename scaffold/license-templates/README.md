# Templates de LICENSE — como o agente usa isto

Quando o agente instancia um repositório de conteúdo novo (ver `hipocampo/skill/references/instanciacao.md`), ele gera o `LICENSE` da raiz a partir de um destes templates — nunca copia o Apache-2.0 da metodologia (`hipocampo/LICENSE`), que é correto para `hipocampo` mas errado para um repositório de conteúdo, mesmo privado, porque o texto da licença em si já afirmaria uma permissão de uso que não é sua intenção (ver `hipocampo/decisions/0007-licenciamento-repos-de-conteudo.md`).

## Como o agente escolhe

1. Pelo titular do conteúdo, declarado como input no profile de scaffold:
   - **`LICENSE-pessoal.md`** — se o titular é uma pessoa física.
   - **`LICENSE-corporativo.md`** — se o titular é uma empresa.
2. Preenche os placeholders (`[NOME COMPLETO]`/`[@usuario-github]` ou `[NOME DA EMPRESA]`) a partir dos inputs coletados do usuário.
3. Se o repositório for de nível "vault" (só recebe `visibility: confidential`/`restricted`, nunca `public`/`internal` — ver `hipocampo/SPEC.md`, seção 2), mantém só as seções (c) e (d) do template, seguindo a nota de ajuste dentro do próprio template.
4. Salva o resultado como `LICENSE` na raiz do repositório novo.

Confirme o resultado no passo 2 de `POS-INSTANCIACAO.md` — não é opcional nem cosmético: sem ele, um repositório de conteúdo privado carregaria, tecnicamente, uma licença de código aberto.
