# 0020 — Identidade de autor multi-conta e direção de convite entre instância pessoal e corporativa

**Status:** Aceito

## Contexto

Hipocampo é desenhado pra second brain tanto pessoal quanto de equipe/empresa (múltiplos repositórios, ver DR0002). Na prática, quem opera uma instância pessoal e também contribui pra uma instância corporativa frequentemente tem duas contas de git diferentes — uma pessoal, uma vinculada à organização empregadora — que precisam resolver para o mesmo `author` humano (seção 2, invariante 2: `author` é sempre uma pessoa). Sem um mecanismo formal, o esquema de autoria (e de convite de acesso entre repositórios pessoal e corporativo) fica ambíguo ou é resolvido de forma diferente por cada pessoa que adota a metodologia.

## Decisão

Duas regras novas:

1. **Registro de identidade multi-conta:** quando uma pessoa opera mais de uma conta de git que representam o mesmo `author` humano, essa relação (quais contas são a mesma pessoa) é registrada na instância — no `AGENTS.md` do repositório pessoal menos restrito (ver DR0015), nunca no `hipocampo`/`hipocampo-toolkit` públicos. O roteador de repositórios da skill (`hipocampo-toolkit/skill/SKILL.md`, seção de personalização) ganha um campo novo pra essa relação, preenchido só na cópia pessoal de cada usuário, nunca na cópia genérica.
2. **Direção de convite:** entre uma instância pessoal e uma instância corporativa da mesma pessoa, o convite de acesso (colaborador de repositório) sempre parte da conta pessoal convidando a conta profissional pro second brain **pessoal** — nunca o inverso (a conta profissional nunca convida a conta pessoal pra dentro de nada). Isso mantém a identidade pessoal como âncora de confiança: a pessoa decide trazer seu lado profissional pro conhecimento pessoal; o empregador nunca tem posição de conceder ou negar acesso ao conhecimento pessoal de alguém.

## Racional

A direção de convite espelha a relação real entre as duas esferas: conhecimento pessoal é sempre mais amplo em titularidade do que conhecimento corporativo (a pessoa é dona do seu second brain pessoal; a empresa é dona do corporativo, mas não da pessoa). Deixar a conta profissional convidar a pessoal inverteria essa relação de titularidade de forma sutil — daria à organização empregadora um papel de gatekeeper sobre conhecimento que não é dela. Registrar a relação de identidade multi-conta só no lado pessoal, nunca no público, segue o mesmo princípio já aplicado a todo dado de instância específica: metodologia (pública) nunca carrega identidade real de ninguém.

## Alternativas descartadas

- **Registrar a relação de identidade multi-conta no `hipocampo` público, como exemplo:** descartada — mesmo anonimizado, não haveria necessidade real de exemplo real no repositório público; o mecanismo genérico já é suficiente sem expor identidade de ninguém.
- **Deixar a direção de convite em aberto, a critério de cada pessoa:** descartada porque criaria inconsistência de titularidade entre instâncias diferentes, e o risco específico (organização controlando acesso a conhecimento pessoal) é sério o suficiente pra merecer uma regra explícita, não uma sugestão.
