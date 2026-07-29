# Hipocampo — Fundamentos de git e GitHub (pra quem nunca usou)

Este documento não pressupõe nenhum conhecimento prévio de git ou GitHub. Se você já usa os dois no dia a dia, pode pular direto pro [GETTING-STARTED.md](../GETTING-STARTED.md).

## Por que git + markdown, e não outra coisa

Hipocampo guarda conhecimento como arquivos de texto simples (`.md`, markdown) dentro de um repositório git. Duas razões práticas:

- **Markdown é texto puro.** Não depende de nenhum programa específico pra abrir — qualquer editor de texto lê. Isso significa que o conhecimento nunca fica preso a um formato proprietário.
- **Git versiona por natureza.** Toda mudança fica registrada com autor, data e o que mudou — sem precisar de um sistema separado de histórico.

**Paralelo com Obsidian:** se você já usa Obsidian (ou Notion, Logseq, etc.), a ideia de "notas em markdown ligadas por referência" já é familiar. Hipocampo é compatível com Obsidian, não concorrente — um vault do Obsidian é, estruturalmente, uma pasta de arquivos markdown, e um repositório Hipocampo também é. Você pode abrir um repositório Hipocampo como vault do Obsidian sem conflito algum; o que o Hipocampo adiciona por cima é o frontmatter estruturado (SPEC.md) e o versionamento/permissionamento do git/GitHub, que o Obsidian sozinho não oferece.

## Glossário básico

| Termo | O que é |
|---|---|
| **Git** | O sistema que registra o histórico de mudanças de um conjunto de arquivos. Roda localmente, não depende de internet pra funcionar. |
| **Repositório (repo)** | Uma pasta de arquivos com histórico de git. É a unidade que o GitHub permissiona — quem tem acesso a um repositório vê tudo dentro dele. |
| **Commit** | Um "salvamento" no histórico — um conjunto de mudanças, com autor, data e uma mensagem descrevendo o que mudou. |
| **Branch** | Uma linha paralela de desenvolvimento dentro do mesmo repositório — permite propor uma mudança sem afetar a versão "oficial" até que ela seja aceita. |
| **Pull Request (PR)** | Um pedido formal de "juntar as mudanças desta branch na branch principal", geralmente revisado antes de aceito. |
| **GitHub** | Um serviço que hospeda repositórios git na nuvem e adiciona permissionamento, interface web, e automação em cima do git puro. |
| **Template** | Um repositório marcado como "modelo" — usá-lo cria um repositório novo com os mesmos arquivos iniciais, sem herdar o histórico de commits do original. |
| **Organização (org)** | Uma conta de GitHub que representa um grupo/empresa, não uma pessoa. Repositórios corporativos geralmente vivem numa org, não na conta pessoal de ninguém. |

## Passo a passo: criar um repositório a partir de um template

Isso é o que você faz pra instanciar o Hipocampo a partir do `hipocampo-toolkit` (ver `GETTING-STARTED.md`, seção 2). Sem nenhuma suposição de conhecimento prévio:

1. Acesse a página do repositório `hipocampo-toolkit` no GitHub (`github.com/mklagenberg/hipocampo-toolkit`).
2. Perto do topo da página, à direita do nome do repositório, há um botão verde **"Use this template"**. Clique nele e escolha **"Create a new repository"** no menu que aparece.
3. Você chega numa tela de criação de repositório novo. Preencha:
   - **Owner** — sua conta pessoal, ou a organização da empresa, se você tiver permissão pra criar repositórios lá (ver "Organização" no glossário acima).
   - **Repository name** — o nome do seu repositório de conteúdo (ex.: `meu-second-brain` ou o nome que sua instância vai usar).
   - **Visibilidade** — escolha **Private**. Isso é obrigatório na metodologia (ver `SPEC.md`, seção 8) — nunca escolha Public aqui.
4. Clique no botão verde **"Create repository from template"**. Em poucos segundos, você tem um repositório novo, com os mesmos arquivos do `hipocampo-toolkit`, mas sem o histórico de commits dele — é uma cópia limpa, começando do zero.
5. A partir daqui, siga `hipocampo-toolkit/POS-INSTANCIACAO.md` — o template não deixa nada pronto pra uso sozinho, tem um checklist obrigatório de primeira configuração (trocar a licença herdada, instalar sua própria cópia da skill, entre outros passos).

**Se o repositório precisa ficar dentro de uma organização (ex.: uma empresa) e você não vê a organização na lista de "Owner":** você provavelmente não tem permissão de criar repositórios lá — peça pra quem administra a organização criar o repositório, ou te conceder essa permissão.

## Por que GitHub especificamente

O modelo de privacidade do Hipocampo depende estruturalmente do permissionamento real do GitHub por repositório — não é uma escolha de conveniência. `visibility` no frontmatter (SPEC.md, seção 2) é convenção de leitura; quem de fato impede acesso não autorizado é a configuração de "privado" do repositório no GitHub. Isso é o que torna o invariante "nenhum repositório de conhecimento é público" (SPEC.md, seção 8) uma garantia técnica real, e não só uma promessa de boa conduta.

## Privacidade de repositório privado no GitHub

Um repositório marcado como **privado** só é visível para quem o dono explicitamente convidou (ou, no caso de organização, para quem tem permissão dentro daquele org). Isso é diferente de "não indexado" ou "difícil de achar" — é controle de acesso de fato, imposto pelo próprio GitHub, não por obscuridade.

**O que muda quando ferramentas de IA entram na equação:** ao usar Copilot (ou qualquer assistente de IA integrado ao GitHub) dentro de um repositório privado, vale checar a política de uso de dado daquela ferramenta especificamente — ela pode ser diferente da política de visibilidade do repositório em si. Achado verificado em `docs.github.com` nesta redação (27/07/2026): desde 24 de abril de 2026, para planos **Copilot Free, Pro, Pro+ e Max**, a GitHub pode usar as interações do usuário com os recursos do Copilot (entradas, saídas, trechos de código e contexto associado) para treinar e melhorar modelos de IA, com opção de **opt-out** disponível nas configurações pessoais de Copilot. Para **Copilot Business e Copilot Enterprise**, o dado do cliente não é usado para treinar modelos — fica protegido pelo Data Protection Agreement da GitHub. Esse é o tipo de política que muda com o tempo — antes de assumir que um plano específico não treina modelo com seu dado, confira a página atual em `docs.github.com` (seção Copilot → Privacy), não confie só neste parágrafo.

**Princípio geral, independente da política do dia:** se essa política mudar de forma material (por exemplo, planos pagos passarem a treinar por padrão sem opt-out, ou o escopo de dado coletado se ampliar), a garantia de privacidade que o método Hipocampo pressupõe precisa ser reavaliada — não é algo que se decide uma vez e nunca mais se confere.

## Privacidade de motores de IA em geral

O mesmo cuidado vale para o agente de IA usado para operar a instância Hipocampo (Claude, ChatGPT, Copilot, ou outro) — a política de treinamento de modelo varia por provedor e por plano, e muda com o tempo. Em vez de uma tabela fixa (que fica desatualizada), use este checklist de perguntas antes de conectar um agente de IA a um repositório Hipocampo com conteúdo sensível:

1. O plano que estou usando (gratuito/individual vs. time/empresa/API) treina modelo com meu conteúdo por padrão?
2. Existe opção de opt-out, e ela está ativada?
3. Se for plano de time/empresa/API, existe garantia contratual explícita de não-treinamento (não só uma alegação em página de marketing)?
4. Onde está a página oficial e atual dessa política — e quando foi a última vez que eu conferi?

O padrão observado nos principais provedores (Claude, ChatGPT, Copilot), nesta redação: plano consumer/gratuito tende a treinar por padrão com opção de opt-out; plano Team/Enterprise/API tende a não treinar por padrão, com garantia contratual. Trate esse padrão como ponto de partida para pesquisar, não como fato fixo — confirme na documentação oficial de cada provedor antes de decidir o que conectar a conteúdo sensível.
