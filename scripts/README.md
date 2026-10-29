# Diretório `scripts/` — Validação de Estrutura e Leitura de Padrão de Vídeo

Contém os utilitários em Python para garantir que todas as histórias em `stories/*.json` respeitem rigorosamente o padrão arquitetural do **Infinite Stories**, tanto no nível de **Blueprint (repositório Git)** quanto no nível de **Mídia Local (pós-produção)**.

## `validate_project.py`

Script escrito utilizando exclusivamente a biblioteca padrão do Python 3 (`json`, `csv`, `os`, `sys`, `pathlib`, `argparse`, `subprocess`), garantindo execução imediata em qualquer máquina sem necessidade de `pip install`.

### O Que o Script Verifica

1. **Integridade da Árvore de Diretórios e Arquivos Permanentes:** Confirma a existência de `AGENTS.md`, `.gitignore`, `config/project.json`, todos os 7 arquivos em `rules/`, todos os 5 templates em `prompts/` e os registros em `production/`.
2. **Validação da Regra Anti-Vídeo no Git:** Verifica se `.gitignore` bloqueia extensões `.mp4`, `.mov`, `.wav`, `.png` e a pasta `output/*`.
3. **Validação Completa do Manifesto da História (`stories/<slug>.json`):**
   - Presença de `story_id`, `slug`, `title`, `qa_status` válido (`PASS`, `REVIEW`, `FAIL`) e `author_lock` (premissa e fatos imutáveis).
   - Conformidade de `video_pattern_expectation` com `config/project.json` (`9:16`, `1080x1920`, duração ~60s, H.264/AAC).
   - Completude de `visual_bible` e `loop_specification` (estratégia permitida e caminho do `F_000`).
   - Presença exata dos 6 blocos temporais (`B1_00_10` a `B6_50_60`) cobrindo de `0.0s` a `60.0s` sem lacunas, com contagem de palavras compatível com locução natural em PT-BR.
   - Validação de todos os `segments`: soma exata de `60.0s`, técnicas válidas (`TECH_A_DIGITAL`, `TECH_B_GENERATIVE`, `TECH_C_HYBRID`), encadeamento contínuo de keyframes (`frame_out` de `N` igual a `frame_in` de `N+1`, e último `frame_out` igual ao `F_000` para fechar o loop), coordenadas `spatial_lock` normalizadas e prompts individualizados (rejeitando prompts duplicados ou curtos/genéricos).
   - Validação dos blocos de legenda (`.srt`), verificando o limite de 28 caracteres por linha e máximo de 2 linhas por legenda.
4. **Leitura de Padrão de Vídeo Local (`--check-media`):**
   - Quando acionado localmente após a produção, verifica se os arquivos de vídeo referenciados no manifesto existem no disco e executa `ffprobe` para comprovar se a resolução (`1080x1920`), proporção (`9:16`), codec (`h264`) e duração obedecem ao padrão declarado.
   - Impede que uma história tenha `qa_status: "PASS"` se o vídeo final local não existir ou falhar na inspeção técnica.

### Exemplos de Uso

```bash
# 1. Validar todo o projeto e todas as histórias no modo Blueprint (ideal para Git/GitHub)
python scripts/validate_project.py

# 2. Validar uma história específica e salvar relatório JSON em production/reports/
python scripts/validate_project.py --story stories/example-story.json --save-report

# 3. Validar o padrão de vídeo inspecionando os arquivos .mp4/.wav locais via ffprobe
python scripts/validate_project.py --story stories/example-story.json --check-media
```