# Regra Permanente: Engenharia de Prompts para Google Flow e Modelos Veo

## 1. Filosofia de Comando para Geradores de Vídeo
Modelos de geração de vídeo como **Google Veo** (operados via **Google Flow** ou Vertex AI) não interpretam intenções abstratas; eles respondem à descrição física da cena, à geometria óptica da câmera e às âncoras visuais (`frame_in` e `frame_out`).
- **Proibido:** Termos vazios como *"ultra 8k masterpiece"*, *"incrível"*, *"mágico"*, *"hipnotizante"*, *"sem cortes"*.
- **Obrigatório:** Descrever **o que existe fisicamente no quadro**, **como a luz incide sobre as superfícies**, **qual é o movimento exato da câmera no eixo Z** e **qual é o enquadramento final esperado**.

## 2. Adaptação às Limitações Reais do Modelo
- Não presuma que o modelo gerará 60 segundos contínuos em um único clipe. Os modelos Veo operam tipicamente em segmentos curtos (ex.: `5s` a `8s`, ou extensões controladas no Google Flow).
- Portanto, os 6 blocos narrativos de 10 segundos (`B1` a `B6`) devem ser decompostos em **Segmentos de Produção (`SEG_01`, `SEG_02`, ...)** cuja duração individual respeite o limite real do gerador (ex.: 8 segmentos de `7.5s` ou 10 segmentos de `6.0s`, ou combinação de clipes Veo de `8s` com trechos `TECH_A_DIGITAL` de `2s`).

## 3. Estrutura Obrigatória de Cada Prompt Individualizado (12 Campos)

Todo prompt gerado para um segmento em `stories/<slug>.json` deve conter na sua string estruturada (em inglês técnico para máxima precisão no Veo, acompanhado da documentação em português no manifesto):

1. **[FORMAT & DURATION]:** Vertical `9:16` aspect ratio, photorealistic live-action cinema footage, duration compatible with segment (`5s` / `8s`).
2. **[SPATIAL CONTINUITY FROM PREVIOUS]:** Exact continuation from input reference frame (`frame_in`), preserving spatial geometry and perspective lines.
3. **[ENVIRONMENT & ARCHITECTURE]:** Descrição objetiva do cenário e das estruturas fixas visíveis ao redor.
4. **[IMMUTABLE ELEMENTS & CHARACTERS]:** Aparência exata dos personagens/objetos presentes que não podem sofrer alteração de cor, formato ou posição.
5. **[SUBTLE SCENE ACTION]:** Micro-movimentos físicos plausíveis no ambiente (ex.: poeira flutuando no feixe de luz, leve respiração do personagem, ponteiro de relógio vibrando) — manter a cena quase estática durante zooms rápidos para evitar deformação de malha.
6. **[CAMERA & LENS SPEC]:** Lente equivalente (ex.: `35mm` avançando para `85mm` / macro `100mm`), câmera estabilizada em trilho óptico (motion-control rig).
7. **[Z-AXIS MOVEMENT VECTOR]:** Direção, velocidade constante e ponto exato do quadro para onde o eixo óptico converge (ex.: `Continuous smooth forward dolly-in along the Z-axis directly toward the brass keyhole at the center-left of the frame`).
8. **[FOCUS & DEPTH OF FIELD]:** Transição de foco (rack focus progressivo mantendo o alvo central perfeitamente nítido).
9. **[LIGHTING & ATMOSPHERE]:** Direção da fonte de luz principal, temperatura em Kelvin, comportamento das sombras e reflexos.
10. **[MATERIALS & TEXTURES]:** Especificação tátil das superfícies que estão sendo ampliadas (poros, fibras, ferrugem, vidro riscado).
11. **[TARGET EXIT FRAME (`frame_out`)]:** Descrição exata de como o quadro deve terminar no último segundo do clipe para conectar com o próximo segmento.
12. **[STRICT NEGATIVE CONSTRAINTS]:** `No camera cuts, no dissolve transitions, no sudden rotation, no morphing geometry, no floating artifacts, no text overlays, no 3D CGI look.`

## 4. Registro Obrigatório em `production/shot-log.csv`
Cada tentativa ou aprovação de geração no Google Flow/Veo deve ser registrada em `production/shot-log.csv` com:
- `story_id`, `segment_id`, `macro_block_id`, `technique`, `model_version`, `duration_sec`, `frame_in_path`, `frame_out_path`, `output_clip_path`, `continuity_score`, `defects_found`, `qa_decision`.