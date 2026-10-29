# Diretório `output/` — Renderizações Finais Locais

Este diretório é o destino local dos vídeos finais masterizados (`<story_slug>_final.mp4`).

## Regra de Repositório (Sem Vídeos no GitHub)
- Todos os arquivos `.mp4` gerados aqui são ignorados automaticamente pelo `.gitignore` (`output/*`, exceto este `output/README.md`).
- Para verificar se um vídeo renderizado localmente cumpre o padrão declarado na história (`1080x1920`, `9:16`, `~60s`, `H.264/AAC`), execute:
  ```bash
  python scripts/validate_project.py --story stories/<story_slug>.json --check-media