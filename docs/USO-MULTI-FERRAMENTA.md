# Uso do Hipocampo em diferentes ferramentas de IA

Referência central — ver `hipocampo/decisions/0002` sobre por que este conteúdo mora aqui e instâncias novas recebem só o link, não uma cópia.

## O princípio comum

Hipocampo não é acoplado a nenhuma ferramenta de IA específica. O que qualquer ferramenta precisa, pra operar uma instância, é acesso de leitura/escrita ao repositório via **MCP do GitHub** (ou mecanismo equivalente de integração com git). Uma vez que essa conexão existe, os mesmos princípios se aplicam em qualquer ferramenta: ler o frontmatter primeiro (seção 2-B do SPEC.md), respeitar os invariantes (seção 8), nunca escrever sem pedido explícito, e seguir a skill Hipocampo personalizada (`hipocampo-toolkit/skill/SKILL.md`) como fonte de instrução operacional.

O que muda entre ferramentas é só **como** cada uma se conecta ao GitHub — não o que fazer depois de conectada.

## Especificidades por ferramenta

**Claude (Cowork, Claude Code, Claude via API/Desktop)** — conecta ao GitHub via um conector MCP dedicado. Uma vez conectado, a skill Hipocampo pode ser carregada como skill do usuário (ex.: via `save_skill` em Cowork) e persiste entre sessões.

**ChatGPT** — conecta ao GitHub via conectores/GPTs com acesso a ferramentas externas, ou via um MCP equivalente quando disponível na conta. A instrução da skill Hipocampo pode ser colada como instrução customizada ou mantida como um "GPT" dedicado, dependendo do plano.

**Gemini** — conecta via extensões/ferramentas do Gemini com acesso ao GitHub, ou via Gemini CLI/API quando o MCP do GitHub está disponível no ambiente.

**GitHub Copilot** — já roda dentro do próprio GitHub/IDE, com acesso nativo ao repositório em que está operando — não precisa de um MCP externo pra alcançar o próprio host onde já vive. A instrução da skill pode ser mantida como um arquivo de instrução customizada do Copilot (ex.: `.github/copilot-instructions.md`) além do `CLAUDE.md` já usado por outras ferramentas.

**Antigravity** (e outros IDEs/agentes com MCP configurável) — mesmo princípio das ferramentas acima: conectar o MCP do GitHub, carregar a instrução da skill Hipocampo personalizada, operar normalmente.

**Verificação recomendada, em qualquer ferramenta nova:** antes de conectar a um repositório de conteúdo sensível, revisitar o checklist de privacidade de `docs/FUNDAMENTOS.md` ("Privacidade de motores de IA em geral") — a política de treinamento de modelo varia por ferramenta e por plano, e muda com o tempo.

## O que nunca muda, em nenhuma ferramenta

Os cinco invariantes (SPEC.md, seção 8), a mecânica CRUD/frontmatter-first (seção 2-B), e o princípio de dados sempre human-readable (`DISCLAIMER.md`) — nenhum deles é específico de ferramenta. Uma instância Hipocampo bem configurada se comporta de forma consistente seja qual for a ferramenta de IA usada para operá-la num dado momento.
