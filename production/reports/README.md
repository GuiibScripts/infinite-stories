# Diretório `production/reports/` — Relatórios de Qualidade e Validação

Esta pasta armazena os relatórios gerados para cada história após a execução do script `scripts/validate_project.py` e da auditoria humana baseada em `production/qa-checklist.md`.

## Padrão de Nomenclatura
- Relatório automatizado JSON: `production/reports/<story_slug>_validation_report.json`
- Parecer humano Markdown: `production/reports/<story_slug>_qa_review.md`

## Regra de Versionamento
Estes arquivos são leves (texto/JSON) e **devem ser versionados no GitHub** como prova auditável do histórico de aprovação (`PASS`, `REVIEW`, `FAIL`) de cada história, sem nunca anexar os vídeos `.mp4` no repositório.