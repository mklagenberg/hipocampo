# 0019 — Auditoria estrutural semanal: atomicidade, posicionamento e vazamento de dado sensível

**Status:** Aceito

## Contexto

Nem o ritual REM (consolidação) nem o frontmatter audit (checagem mecânica de campo) avaliam a saúde estrutural de um repositório como um todo — se a atomicidade dos documentos já consolidados ainda está boa, se algum arquivo deveria mudar de `category`/pasta, e principalmente, se algum dado sensível vazou pra um repositório de classificação errada (por exemplo, dado que a política de privacidade por instância, seção 2-A e DR0009, proíbe numa instância corporativa). Essa política existe como regra desde a v1.3.0, mas nunca teve nenhum mecanismo periódico que de fato verifica se ela está sendo cumprida.

## Decisão

Auditoria estrutural é um ritual novo, com cadência recomendada semanal, com três funções:

1. **Atomicidade:** revisar se documentos consolidados recentemente (ou apontados pela fila de manutenção, DR0017) ainda representam um conceito só, ou se deveriam ser divididos.
2. **Posicionamento:** avaliar se a estrutura de `category`/pastas do repositório ainda faz sentido — se massa crítica nova justifica uma subpasta que não existia (seção 4), ou se um documento está no lugar errado dado o escopo do repositório (ver escopo declarado no `AGENTS.md`, DR0015).
3. **Vazamento de dado sensível:** verificar, contra a política de dados sensíveis por tipo de instância (seção 2-A, DR0009), se algum documento no repositório contém algo que não deveria estar ali — essa é a primeira vez que essa política ganha um mecanismo de verificação periódica, em vez de só a regra.

Qualquer achado da auditoria estrutural é sempre apresentado ao humano responsável pela instância antes de qualquer ação — mover, dividir ou remover documento nunca acontece automaticamente (invariante 5).

## Racional

Cadência semanal (mais espaçada que a diária do frontmatter audit/REM) reflete a natureza da checagem: problema estrutural e vazamento de dado sensível se acumulam mais devagar que item de captura nova, e revisão de estrutura é mais cara (exige mais julgamento, potencialmente mais leitura de corpo de documento) que a checagem mecânica de frontmatter. Colocar a checagem de vazamento de dado sensível aqui, e não como ritual isolado, evita multiplicar gatilho pra fluxos que já fazem sentido acontecer juntos (mesmo princípio já usado na decisão de dobrar a skill `design-system` dentro da `qualidade-visual`, precedente do Second Brain Pessoal).

## Alternativas descartadas

- **Verificação de vazamento de dado sensível como ritual isolado, separado da auditoria estrutural:** descartada pelo mesmo motivo de não multiplicar gatilhos desnecessariamente — ambas exigem "olhar o repositório inteiro com julgamento", não só um documento por vez.
- **Cadência diária, igual ao frontmatter audit:** descartada por custo desproporcional ao ritmo real de acúmulo do problema que resolve — reavaliação de estrutura inteira todo dia é caro e na prática não vai ter mudança suficiente pra justificar.
