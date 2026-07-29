# 0011 — Migração de conteúdo pré-existente nunca copia arquivo direto

**Status:** Aceito

## Contexto

Ao longo do Lote 4 (migração real de centenas de documentos do Second Brain Pessoal legado para os repositórios Hipocampo), a prática seguida consistentemente foi nunca copiar um arquivo original verbatim para dentro de uma instância Hipocampo — sempre reescrever o frontmatter do zero conforme o schema vigente, e frequentemente também ajustar o corpo do documento (regra de atomicidade, remoção de dado banido pela política de privacidade, atualização de nomenclatura). Essa prática nunca foi formalizada como regra normativa — ficou só como convenção seguida ad hoc. Isso significa que uma migração futura, feita por outra pessoa, outra empresa adotando o Hipocampo, ou um agente de IA sem o histórico desta sessão, poderia legitimamente copiar arquivos direto, achando que está migrando corretamente.

## Decisão

Migração de conteúdo pré-existente — de um sistema legado, de uma versão anterior da mesma instância, ou de qualquer fonte externa — nunca copia o arquivo original diretamente para dentro do repositório de destino. O agente (ou humano) sempre:

1. Interpreta o conteúdo original.
2. Reescreve o frontmatter do zero, conforme a versão vigente do schema (SPEC.md, seção 2).
3. Aplica as regras de atomicidade, nomenclatura e política de privacidade vigentes ao corpo do documento (SPEC.md, seção 2-A), dividindo, expurgando ou reformatando conforme necessário.
4. Documenta a migração em `revision_note`, citando a origem e as mudanças aplicadas — o que foi preservado verbatim e o que foi alterado, e por quê.

Isso vale tanto para migração de conteúdo de fora do Hipocampo quanto para republicação de conteúdo de uma versão anterior da metodologia dentro da mesma instância.

## Racional

Copiar um arquivo direto propaga inconsistência de schema (frontmatter desatualizado, campos que não existem mais, convenções antigas) e propaga também violação de política de privacidade vigente que talvez não existisse quando o documento original foi escrito — por exemplo, dado pessoal que era aceitável registrar antes da `decisions/0009` existir. Reescrever força uma checagem de conformidade a cada migração, em vez de assumir que o conteúdo antigo já está correto. O custo adicional (mais trabalho por documento migrado) é aceitável porque migração é evento raro por documento — acontece uma vez —, enquanto o custo de propagar inconsistência se paga repetidamente, em toda leitura futura do documento mal migrado.

## Alternativas descartadas

- **Copiar arquivo direto e corrigir depois, sob demanda.** Descartada: sem checagem obrigatória no momento da migração, a correção "sob demanda" tende a nunca acontecer — ninguém revisita um documento já migrado e aparentemente funcional.
- **Migração automatizada sem revisão humana ou de agente.** Descartada: mesmo princípio do invariante 5 (SPEC.md, seção 8) e do processo já usado no Lote 4 — decisões de classificação (`type`, `category`, o que preservar vs. descartar) exigem julgamento, não podem ser mecanizadas cegamente.
- **Migrar só o frontmatter, preservando o corpo sempre verbatim.** Descartada: o corpo também pode violar regras vigentes (atomicidade, privacidade) que não existiam na origem; restringir a reescrita só ao frontmatter deixaria essas violações passarem.
