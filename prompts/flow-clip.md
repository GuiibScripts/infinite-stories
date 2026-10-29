# Prompt Operacional: Gerador de Prompts Individualizados para Google Flow / Veo (`flow-clip`)

Use este template para construir o campo `generation_prompt` de cada segmento individual dentro de `stories/<slug>.json`.

---

## Regras de Construção

- **Nunca reutilize o mesmo prompt entre dois segmentos.**
- Todo prompt deve respeitar a sintaxe física e óptica detalhada em `rules/flow-veo-prompts.md`.
- Se o segmento for `TECH_A_DIGITAL`, forneça o prompt de geração da imagem estática 4K (`frame_in` / `frame_out`) + os parâmetros matemáticos exatos de zoom (`scale_start`, `scale_end`, `x_center`, `y_center`).
- Se o segmento for `TECH_B_GENERATIVE` ou `TECH_C_HYBRID`, preencha obrigatoriamente o template abaixo para o gerador de vídeo:

## Template Estruturado por Segmento

```text
[ASPECT & FORMAT]: Vertical 9:16 (1080x1920), photorealistic live-action cinema footage, shot on ARRI Alexa Mini LF, [LENS_MM] prime lens, [DURATION_SEC] seconds, 30fps.
[CONTINUITY ANCHOR]: Seamless spatial continuation starting strictly from the provided input reference frame ([FRAME_IN_FILE]). Maintain exact perspective lines, architectural geometry, and object proportions.
[SCENE & ENVIRONMENT]: [Descrição física detalhada do ambiente visível neste recorte espacial].
[IMMUTABLE SUBJECTS]: [Descrição invariável de personagens, roupas, objetos e materiais presentes no quadro].
[SUBTLE PHYSICAL ACTION]: [Ação mínima fisicamente plausível que não distorça a geometria durante o zoom].
[CAMERA Z-AXIS TRAJECTORY]: Continuous, ultra-stable motion-control dolly-in along the Z-axis at constant linear velocity, advancing from [START_SCALE_DESC] directly toward [TARGET_POI_DESC] located at [ROI_COORDINATES_DESC].
[OPTICAL FOCUS & LIGHTING]: Smooth rack focus keeping [TARGET_POI_DESC] tack-sharp; [LIGHTING_DIRECTION_AND_KELVIN]; consistent shadows and natural surface specular reflections.
[TARGET EXIT FRAME]: By the final second, the camera framing must match the target exit reference ([FRAME_OUT_FILE]), filling the frame with [EXIT_FRAME_CONTENT_DESC].
[NEGATIVE CONSTRAINTS]: No camera cuts, no transitions, no sudden speed ramps, no morphing objects, no geometry warping, no vanishing items, no on-screen text, no 3D CGI rendering look.