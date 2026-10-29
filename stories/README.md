# Diretório `stories/` — Manifestos de Padrão de Vídeo

Este diretório armazena os arquivos `.json` de cada história do projeto **Infinite Stories**.

## Como Funciona o Modelo de Leitura de Padrão de Vídeo

Para evitar o armazenamento de arquivos `.mp4` pesados no GitHub, cada arquivo `stories/<slug>.json` funciona como o **Contrato e Padrão de Vídeo (Video Pattern Manifest)** daquela produção. Ele contém:

1. **`story_metadata` & `author_lock`:** O resumo oficial da história do autor, fatos imutáveis e status atual de QA (`PASS`, `REVIEW`, `FAIL`).
2. **`video_pattern_expectation`:** O contrato técnico exato que o arquivo de vídeo final local (`output/<slug>_final.mp4`) e os clipes intermediários (`assets/generated/`) devem cumprir quando inspecionados pelo script `scripts/validate_project.py`.
3. **`visual_bible`:** Parâmetros fotográficos, iluminação, lentes, paleta HEX e âncoras visuais imutáveis da história.
4. **`loop_specification`:** Definição do quadro-âncora `F_000`, estratégia de retorno no último bloco e critérios de verificação da emenda `F_END -> F_000`.
5. **`macro_blocks` (`B1_00_10` a `B6_50_60`):** Os 6 blocos narrativos de 10 segundos com texto em PT-BR, contagem de palavras, objetivo dramático e descoberta visual.
6. **`segments` (`SEG_01` a `SEG_N`):** Os clipes operacionais reais que compõem o zoom profundo, cada um com sua técnica (`TECH_A_DIGITAL`, `TECH_B_GENERATIVE`, `TECH_C_HYBRID`), coordenadas espaciais (`spatial_lock`), caminhos locais de `frame_in`/`frame_out`, prompt individualizado completo para Google Flow/Veo, riscos de continuidade e critérios de aprovação.
7. **`audio_and_subtitles`:** Especificação da locução PT-BR e blocos de legenda sincronizados com posicionamento em zona segura.

## Convenção de Nomenclatura
- Use sempre `kebab-case` sem acentos: `stories/o-relogio-do-relojoeiro.json`.
- O exemplo oficial validável do sistema é `stories/example-story.json`.