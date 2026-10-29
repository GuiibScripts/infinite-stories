# Prompt Operacional: Arquiteto de Bíblia Visual e Trajetória de Zoom (`visual-planner`)

Use este template após aprovar o roteiro narrativo para projetar a geometria espacial, a bíblia visual e a estratégia de loop da história.

---

## Instruções para a IA

Consulte `rules/visual-style.md`, `rules/continuity.md` e `rules/loop-spec.md`. Projete a travessia contínua no eixo Z garantindo que nenhum segmento pareça uma cena desconectada:

1. **Defina a Bíblia Visual (`visual_bible`):**
   - Época, local exato, paleta de cores (HEX), configuração de iluminação (direção, temperatura em Kelvin, contraste), perfil óptico de lente e lista de elementos imutáveis (`immutable_anchors`).
2. **Defina o Quadro-Âncora Mestre (`F_000`):**
   - Descreva com precisão fotográfica o primeiro frame (`00:00.000`). Indique exatamente onde, dentro de `F_000`, está localizado o ponto de interesse para onde a câmera avançará.
3. **Mapeie a Cadeia de Escalas (`Segments`):**
   - Divida os 60 segundos em segmentos compatíveis com os limites reais de geração e composição (ex.: segmentos de `5s` a `8s`).
   - Para cada segmento, defina:
     - `zoom_technique`: `TECH_A_DIGITAL`, `TECH_B_GENERATIVE` ou `TECH_C_HYBRID`.
     - `camera_position` e `focal_point`: Posição da câmera e ponto de foco.
     - `framing_scale`: Escala cinematográfica (Extreme Wide -> Wide -> Medium -> Close-Up -> Extreme Close-Up / Macro).
     - `spatial_lock`: Coordenadas normalizadas `[x_center, y_center, width_ratio, height_ratio]` que provam onde este quadro reside dentro do quadro anterior, além do `scale_factor`.
     - `frame_in_ref` e `frame_out_ref`: Caminhos locais esperados em `assets/references/`.
4. **Projete o Fechamento do Loop (`loop_bridge`):**
   - Escolha entre `PORTAL_FRAME_MATCH`, `OPTICAL_SURFACE_MATCH`, `MICRO_TO_MACRO_TEXTURE_MATCH` ou `CAMERA_PULLBACK_RESET`.
   - Explique mecanicamente como o último segmento retorna ao `F_000` sem salto de escala, iluminação, textura ou velocidade.