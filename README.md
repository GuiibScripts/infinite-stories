# Infinite Stories — Sistema de Produção de Vídeos Hiper-Realistas em Zoom Infinito

Sistema documental, arquitetural e operacional para planejamento, direção de arte, geração assistida, pós-produção e controle de qualidade de vídeos verticais hiper-realistas (`9:16`, `1080x1920`, `~60s`) com zoom profundo contínuo e loop visual imperceptível.

## Arquitetura "Pattern-First" (Sem Vídeos no GitHub)

Este repositório **não armazena arquivos de vídeo, áudio ou imagens pesadas no Git**. Em vez disso, opera sob o modelo de **Leitura de Padrão de Vídeo (Video Pattern Manifest)**:

1. Cada história em `stories/<slug>.json` define o **padrão completo esperado do vídeo** (resolução, FPS, codec, duração por bloco, coordenadas espaciais de zoom, caminhos locais de entrada/saída, hashes opcionais e critérios de aprovação).
2. As mídias geradas ficam exclusivamente na máquina local dentro de `assets/` e `output/` (bloqueadas pelo `.gitignore`).
3. O script `scripts/validate_project.py` lê o manifesto da história e valida:
   - **Modo Blueprint (Padrão/Git):** Valida toda a coerência estrutural, continuidade matemática do zoom, presença de prompts individualizados, regras de loop e integridade da história sem exigir os arquivos `.mp4` no repositório.
   - **Modo Mídia Local (`--check-media`):** Lê o padrão declarado no JSON e inspeciona os arquivos locais em `assets/` e `output/` via `ffprobe` para confirmar se os vídeos renderizados obedecem exatamente ao padrão técnico do projeto.

---

## Especificações Técnicas Globais (Padrão Imutável)

| Parâmetro | Valor Obrigatório |
| :--- | :--- |
| **Proporção (Aspect Ratio)** | `9:16` (Vertical nativo) |
| **Resolução Final** | `1080x1920` pixels |
| **Duração Alvo** | `60.0s` (Tolerância operacional: `58.0s` a `62.0s`) |
| **Frame Rate (FPS) de Entrega** | `30 fps` ou `60 fps` (constante, CFR) |
| **Codec de Vídeo / Áudio** | `H.264 (libx264, High Profile, crf 18)` / `AAC-LC (48kHz, 192kbps+)` |
| **Estética Visual** | Fotorealismo cinematográfico (aparência de filmagem óptica real) |
| **Linguagem de Câmera** | Zoom profundo contínuo (eixo Z progressivo) sem cortes secos aparentes |
| **Fechamento Visual** | Loop contínuo retornando ao `F_000` (Quadro-Âncora Inicial) |
| **Narração e Legendas** | Voz sintética natural em PT-BR + Legendas `.srt`/`.ass` queimadas na pós |

---

## Como Começar Localmente

### 1. Pré-requisitos
- **Python 3.10+** (biblioteca padrão — sem dependências externas obrigatórias para validação do blueprint).
- **FFmpeg / FFprobe** instalado no `PATH` do sistema (necessário para montagem final e validação de mídia local com `--check-media`).
- **Git** para controle de versão dos manifestos, regras e prompts.

### 2. Executar o Validador do Projeto
Na raiz do repositório (`infinite-stories/`), execute:

```bash
# Valida a estrutura de pastas, configurações e o padrão de vídeo (JSON) de todas as histórias
python scripts/validate_project.py

# Valida uma história específica e verifica os arquivos de mídia locais via ffprobe
python scripts/validate_project.py --story stories/example-story.json --check-media
```

---

## Como Inicializar o Repositório Git e Enviar ao GitHub

```bash
cd infinite-stories
git init
git branch -M main

# Cria os arquivos .gitkeep nas pastas de mídia vazias para manter a estrutura no Git
touch assets/references/.gitkeep assets/generated/.gitkeep assets/audio/.gitkeep assets/subtitles/.gitkeep

# Verifica se nenhum arquivo de mídia pesado está sendo rastreado
git status

git add .
git commit -m "chore: bootstrap Infinite Stories architecture and video pattern system"
git remote add origin [https://github.com/SEU_USUARIO/infinite-stories.git](https://github.com/SEU_USUARIO/infinite-stories.git)
git push -u origin main
```

---

## Como Usar Esta Pasta como Fonte Permanente no Gemini ou Outra IA

1. **No Gemini (via upload de pasta/arquivos ou integração com repositório GitHub):**
   - Carregue o arquivo `AGENTS.md`, a pasta `rules/`, a pasta `prompts/` e o arquivo `config/project.json` no contexto da sessão.
   - Inicie o comando sempre com: *"Atue conforme o manual `AGENTS.md` do projeto Infinite Stories. Aqui está a nova história autoral: [...]"*.
2. **Em Editores com IA (VS Code, Cursor, Windsurf, Claude Code, Gemini Code Assist):**
   - Abra a pasta raiz `infinite-stories/`.
   - O arquivo `AGENTS.md` na raiz orienta automaticamente o agente a ler `rules/` e `config/project.json` antes de gerar qualquer plano em `stories/<slug>.json`.

---

## O Que é Automatizado vs. O Que Exige Execução Manual

| Etapa do Pipeline | Status no Repositório | Modo de Operação |
| :--- | :--- | :--- |
| **Estrutura, Regras e Padrão de Dados** | Pronto e ativo | Automatizado via JSON Schema interno |
| **Validação de Blueprint e Continuidade Lógica** | Pronto (`validate_project.py`) | Automatizado via CLI Python |
| **Inspeção Técnica de Vídeos Locais** | Pronto (`--check-media`) | Automatizado via `ffprobe` local |
| **Roteirização, Bíblia Visual e Prompts Veo** | Pronto (`prompts/*.md`) | Assistido por IA seguindo `AGENTS.md` |
| **Geração de Clipes no Google Flow / Veo** | Procedimento documentado | Manual na UI oficial do Google Flow ou via Vertex AI Veo API (com credenciais próprias) |
| **Síntese de Voz PT-BR e Legendas** | Configurável (`providers.example.json`) | Via API configurada pelo usuário ou exportação manual para `assets/audio/` |
| **Composição de Loop e Render FFmpeg** | Comandos documentados | Execução local via FFmpeg + revisão visual humana obrigatória |