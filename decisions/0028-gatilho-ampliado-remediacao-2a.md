# 0028 — Gatilho ampliado pra remediação de violação da política de dados sensíveis (2-A)

**Status:** Proposto

## Contexto

`decisions/0010` cria uma exceção estreita ao invariante 3 (documento nunca apagado fisicamente), mas o gatilho, como está escrito, é específico: "acionado por uma solicitação legítima de eliminação de um titular de dado identificável". Isso cobre o caso de alguém exercer um direito de eliminação (LGPD Art. 16 / GDPR Art. 17). Não cobre um caso distinto e real: conteúdo que já viola a política de dados sensíveis (seção 2-A) — categoria banida incondicionalmente de instância corporativa, independente de qualquer pedido — é descoberto pela auditoria estrutural semanal (seção 5-C, função 3, que já existe especificamente pra achar isso) ou pelo próprio operador da instância, sem que o titular tenha formalmente solicitado nada ainda. Esperar por uma solicitação formal antes de corrigir uma violação já confirmada da própria política declarada da instância não parece ter sido a intenção original de `decisions/0010` — é um gap de escopo no texto, não uma escolha deliberada.

## Decisão

O mecanismo de `decisions/0010` (apagamento físico do conteúdo específico, substituído por tombstone, decisão humana sempre explícita, nunca automática, mesma ressalva sobre histórico do git não ser limpo automaticamente) passa a ter dois gatilhos, não um:

1. Solicitação legítima de eliminação de um titular de dado identificável (já existente, `decisions/0010`).
2. Violação confirmada da política de dados sensíveis por tipo de instância (seção 2-A), identificada pela auditoria estrutural semanal (seção 5-C) ou pelo operador da instância diretamente — mesmo sem solicitação formal de ninguém.

Em ambos os casos, a legitimidade da remediação é sempre avaliada pelo humano responsável pela instância, nunca decidida pelo agente sozinho (mesmo princípio já estabelecido em `decisions/0010` e no invariante 5).

Essa ação é referenciada operacionalmente como "Redbutton" — ver `SPEC.md`, seção 13, e `decisions/0027`.

## Racional

A política 2-A já proíbe certas categorias de dado incondicionalmente, "em nenhum nível de `visibility`" — a proibição não é condicionada a alguém pedir remoção. Faz sentido que a remediação também não dependa disso. Restringir a exceção só ao gatilho de solicitação do titular deixaria a instância sem caminho formal de correção rápida pra um vazamento óbvio que a própria auditoria da metodologia (5-C) foi desenhada pra achar — a auditoria ficaria com poder de detectar mas não de habilitar remediação, o que esvazia parte do propósito dela.

## Alternativas descartadas

- **Editar `decisions/0010` diretamente, em vez de criar uma decisão nova.** Descartada: `0010` já está `Aceito` e fez parte de uma release publicada (v1.4.0). Editar retroativamente um Decision Record aceito quebra o próprio princípio de auditabilidade que a metodologia defende — o padrão já usado (`decisions/0016` refina `0008`, `decisions/0022` fecha uma assimetria de `0019`) é sempre uma decisão nova que estende, nunca reescrever a antiga.
- **Deixar que só o operador humano identifique a violação, sem envolver a auditoria estrutural formalmente.** Descartada: a auditoria estrutural (5-C, função 3) já existe especificamente pra essa checagem — não faz sentido o mecanismo de remediação ignorar o mecanismo de detecção que a própria metodologia já construiu.
