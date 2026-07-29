# FAQ e erros comuns

Este documento junta duas coisas: perguntas que voltam com frequência, e erros de instanciação/operação já encontrados de verdade em repositórios reais rodando a metodologia (não hipotéticos). Se você tem uma dúvida ou esbarrou em algo estranho, provavelmente já está aqui.

## Erros comuns de instanciação

### "Cliquei em 'Use this template', mas a skill não parece funcionar"

Esperado. **"Use this template" copia o esqueleto do repositório, não instala a skill.** `skill/SKILL.md` chega no seu repositório novo como um arquivo — mas pra um agente de IA realmente usá-la, ela precisa ser personalizada (preenchido o roteador de repositórios da sua instância) e instalada de fato (no Cowork, isso é `save_skill`; outras ferramentas têm mecanismo próprio, ver `docs/USO-MULTI-FERRAMENTA.md`). Esse passo está no `POS-INSTANCIACAO.md` do `hipocampo-toolkit` — se você pulou ele, volte lá.

### "Meu repositório novo tem uma licença Apache-2.0, isso está certo?"

Não, é um bug conhecido do mecanismo de template do GitHub: ele copia o `LICENSE` do `hipocampo-toolkit` (Apache-2.0, correto pra metodologia/ferramental) pro seu repositório novo — mas seu repositório novo guarda **conteúdo**, não metodologia, e conteúdo nunca deveria ser Apache-2.0 (ver `decisions/0007-licenciamento-repos-de-conteudo.md`). Troque o `LICENSE` manualmente pelo template certo em `hipocampo-toolkit/license-templates/` (pessoal ou corporativo) assim que instanciar. Isso também está no `POS-INSTANCIACAO.md`.

### "Meu `CLAUDE.md` ainda diz uma versão antiga da metodologia"

Isso significa que a instância não passou pela rotina de release (ver `decisions/0014-rotina-obrigatoria-de-release.md`) nas últimas vezes que a metodologia evoluiu — ou que ninguém atualizou manualmente depois de instanciar. Não há sincronização automática entre repositórios (ver `decisions/0002`, arquitetura multi-repo sem replicação) — é responsabilidade de quem mantém cada instância acompanhar o `CHANGELOG.md` do `hipocampo` e atualizar o `CLAUDE.md` local. A skill, quando instalada corretamente, ajuda avisando quando há release nova — mas não aplica a atualização sozinha.

### "Não consigo criar o repositório a partir do template dentro da minha organização do GitHub"

Provavelmente falta permissão. Criar repositório a partir de template dentro de uma organização (em vez da sua conta pessoal) normalmente exige que um administrador da organização libere isso, ou que você peça pra alguém com permissão criar em seu nome. Não é uma limitação da metodologia — é uma configuração do GitHub. Ver a nota correspondente em `docs/FUNDAMENTOS.md`.

### "Migrei um documento antigo e só copiei o arquivo, é isso mesmo?"

Não. Migração nunca é cópia direta de arquivo (ver `decisions/0011-migracao-nunca-copia-arquivo-direto.md` e `SPEC.md`, seção 10). O conteúdo precisa ser reinterpretado e reescrito conforme o schema de frontmatter vigente na versão atual da metodologia, com atomicidade, nomenclatura e classificação de privacidade corretas — mesmo que isso signifique dividir um arquivo antigo em vários novos, ou reclassificar o `visibility`.

## Perguntas frequentes

### Por que documento nunca é apagado fisicamente?

Porque apagar destrói o histórico de por que uma decisão foi tomada ou um fato mudou — o Hipocampo prefere `status: archived` ou `status: superseded` (ver invariante 3, `SPEC.md` seção 8). A única exceção formal é uma solicitação legítima de eliminação de dado pessoal (LGPD Art. 16 / GDPR Art. 17), sempre com decisão humana explícita e substituição por um "tombstone" mínimo — ver `decisions/0010-excecao-apagamento-obrigacao-legal.md`.

### O que acontece com meus dados se o produto de IA que eu uso sair do ar?

Nada — seus dados continuam existindo, legíveis, em markdown puro dentro de um repositório git, independente de qualquer produto de IA estar no ar ou não. Isso é um princípio formal da metodologia desde a v1.5.0 (ver `decisions/0013-dados-sempre-human-readable.md`). Uma instabilidade específica de um produto (mesmo que real e documentada) nunca é motivo pra perder acesso ao seu próprio conhecimento.

### Preciso da skill pra usar a metodologia, ou dá pra usar só escrevendo prompts manuais?

A skill não é estritamente obrigatória — o `SPEC.md` e o `CLAUDE.md` da sua instância já são suficientes pra qualquer agente de IA capaz de ler arquivos e usar o MCP do GitHub operar corretamente, mesmo sem skill instalada. A skill existe pra automatizar rituais recorrentes (checagem de release nova, ritual REM, ritual de staleness, resolução de `related` cross-repositório) sem você precisar lembrar de pedir cada um manualmente.

### Qual a diferença entre a licença da metodologia e a licença do meu conteúdo?

São duas entidades diferentes. A metodologia (`hipocampo`, `hipocampo-toolkit`) é sua, aberta, sempre Apache-2.0. Seu conteúdo, depois de instanciado, é seu (ou da sua empresa) e nunca deveria carregar a licença aberta da metodologia — sempre proprietário/confidencial (`LicenseRef-<idstring>`, ver `decisions/0007`). Instanciar o template não muda quem é dono do conhecimento que você coloca lá dentro.

### Como eu sei se saiu uma versão nova da metodologia?

Se a skill estiver instalada e personalizada, ela checa o `hipocampo` por releases novas e avisa você. Manualmente, o `CHANGELOG.md` do `hipocampo` é a fonte de verdade — cada entrada nova é uma release.

### Posso usar isso em outro git host além do GitHub?

O `hipocampo-toolkit` é desenhado como template genérico (git + markdown), então tecnicamente não há dependência de GitHub especificamente. Na prática, hoje, toda a automação (skill, MCP, rotina de release) foi construída e testada em cima do MCP do GitHub — usar outro host funciona pro conteúdo em si, mas exigiria adaptar a parte de automação.

### Esqueci de marcar meu repositório como privado na criação, e agora?

Corrija imediatamente — vá nas configurações do repositório no GitHub e mude a visibilidade pra Private. É o invariante 1 da metodologia (`SPEC.md`, seção 8) e não tem exceção. Depois de corrigir, vale revisar o histórico de commits: se algum conteúdo sensível chegou a ficar público, mesmo que brevemente, considere se algo precisa de rotação (por exemplo, se algum segredo foi exposto).
