# Prompt Operacional: Auditoria de Continuidade e Controle de Qualidade (`quality-review`)

Use este template para auditar um manifesto de história (`stories/<slug>.json`) e os resultados de produção antes de definir o status final (`PASS`, `REVIEW` ou `FAIL`).

---

## Instruções de Auditoria para a IA

Analise rigorosamente o projeto em duas frentes e nunca aprove (`PASS`) um vídeo sem evidência concreta de verificação:

### Frente 1: Auditoria de Blueprint (Manifesto JSON)
1. **Fidelidade Autoral:** Compare a história original do autor com os 6 blocos do JSON. Algum fato, personagem ou o desfecho foi alterado sem autorização? (Se sim -> `FAIL`).
2. **Cobertura Temporal:** Os 6 blocos cobrem continuamente de `0.0s` a `60.0s` sem buracos nem sobreposições? A soma das durações dos `segments` é igual a `60.0s`?
3. **Continuidade Matemática do Zoom (`Spatial Lock`):** Cada segmento a partir do `SEG_02` referencia corretamente o `frame_out` do segmento anterior como seu `frame_in`? As coordenadas `target_roi_norm` estão dentro de `[0.0, 1.0]`?
4. **Especificidade dos Prompts:** Todos os segmentos possuem prompts completos, sem repetição preguiçosa e sem frases genéricas?
5. **Viabilidade do Loop:** A estratégia `loop_bridge` explica tecnicamente como o último segmento reconstrói o `F_000` sem usar crossfade genérico?

### Frente 2: Auditoria de Mídia Renderizada (Quando os arquivos locais existirem)
1. Execute `python scripts/validate_project.py --story stories/<slug>.json --check-media`.
2. Verifique os resultados do `production/qa-checklist.md` preenchidos após inspeção visual humana:
   - Existe qualquer salto de escala, iluminação ou textura nas emendas dos segmentos?
   - Há deformação de objetos, mãos, rostos ou linhas arquitetônicas?
   - A passagem de `59.9s` para `00.0s` em reprodução em loop chama a atenção do olho ou do ouvido?
3. Emita o parecer técnico estruturado classificando o projeto como **`PASS`**, **`REVIEW`** ou **`FAIL`** e listando as correções exatas necessárias para cada item reprovado.