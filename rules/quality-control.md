# Regra Permanente: Controle de Qualidade (QA), Pipeline FFmpeg e Estados de Aprovação

## 1. Pipeline Padrão de Pós-Produção (12 Etapas Operacionais)

Antes de submeter qualquer vídeo à validação final, o pipeline local deve cumprir as 12 etapas abaixo:

1. **Organização de Arquivos:** Conferir se todos os keyframes estão em `assets/references/`, clipes brutos em `assets/generated/`, locução em `assets/audio/` e legendas em `assets/subtitles/`.
2. **Inspeção de Metadados Brutos (`ffprobe`):** Verificar resolução, FPS e duração real de cada segmento gerado.
3. **Padronização de Resolução e Proporção:** Converter/escalar todos os segmentos para `1080x1920`, `SAR 1:1`, `DAR 9:16`, `yuv420p`.
4. **Correção de Taxa de Quadros (CFR):** Normalizar todos os clipes para exatamente `30 fps` (ou `60 fps` conforme definido na história) sem duplicação irregular de frames.
5. **Alinhamento Espacial e Montagem:** Concatenar os segmentos aplicando o alinhamento de máscara/escala nas transições `TECH_C_HYBRID`.
6. **Unificação Visual (Color Match & Grain):** Aplicar ajuste fino de luminância/cor entre emendas de clipes e adicionar camada sutil de grão cinematográfico uniforme para mascarar diferenças de textura entre `TECH_A_DIGITAL` e `TECH_B_GENERATIVE`.
7. **Sincronização da Narração PT-BR:** Alinhar o arquivo `.wav` de locução aos marcos temporais dos 6 blocos narrativos.
8. **Mixagem de Ambiência e Efeitos:** Integrar sound design espacial com loop de áudio perfeito nas extremidades e normalizar em `-14 LUFS`.
9. **Incorporação de Legendas:** Queimar as legendas revisadas dentro da margem segura inferior (`Y = 1380px–1580px`).
10. **Fechamento e Teste do Loop (`F_END` -> `F_000`):** Verificar a emenda exata entre o último frame e o primeiro frame em reprodução contínua.
11. **Exportação Master (`output/<story_slug>_final.mp4`):**
    ```bash
    ffmpeg -y -i composed_video.mp4 -i mixed_audio.wav \
      -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30,subtitles=assets/subtitles/story.ass" \
      -c:v libx264 -profile:v high -level:v 4.2 -pix_fmt yuv420p -crf 18 -preset slow \
      -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
      output/story_final.mp4
    ```
12. **Emissão do Relatório de Qualidade:** Executar `python scripts/validate_project.py --story stories/<slug>.json --check-media` e preencher o checklist humano em `production/reports/`.

---

## 2. Limitações Técnicas Reais e Honestidade de Diagnóstico

É proibido fingir que geradores de vídeo atuais não possuem limitações físicas. O supervisor de QA deve monitorar ativamente os 4 defeitos estruturais mais comuns:
1. **Deriva de Textura e Contraste (boiling/shifting):** Em clipes gerados por IA (`TECH_B_GENERATIVE`), texturas finas no fundo costumam mudar sutilmente entre o segundo 0 e o segundo 8, criando um salto perceptível ao colar no próximo clipe. *Solução obrigatória:* Usar o frame final real extraído do clipe anterior como `frame_in` ou aplicar blend espacial de 6 a 10 frames apenas nas bordas periféricas enquanto o centro avança.
2. **Perda de Nitidez no Zoom Digital (`TECH_A_DIGITAL`):** Ampliar mais de `2.2x` uma imagem 1080p ou 4K causa suavização artificial. *Solução obrigatória:* Intercalar reancoragem por imagem de alta resolução (upscale controlado / inpainting local) antes de prosseguir o zoom.
3. **Inversão de Vetor na Emenda do Loop:** Mesmo quando `F_END` e `F_000` são visualmente idênticos (SSIM alto / MSE baixo), se o clipe final desacelera (ease-out) e o primeiro clipe acelera (ease-in), o olho humano percebe uma "parada" na virada do loop. *Solução obrigatória:* Manter velocidade constante de escala nos últimos 30 frames e nos primeiros 30 frames.
4. **Insuficiência de Métricas Matemáticas:** Um cálculo automatizado de MSE/PSNR entre o último e o primeiro quadro avalia apenas dois frames estáticos; **não detecta** deformações no meio do vídeo nem solavancos de movimento. A inspeção visual e auditiva humana em player com *repeat* ativado é insubstituível.

---

## 3. Os Três Estados Oficiais de Aprovação (`qa_status`)

- **`PASS` (Aprovado para Publicação):**
  - Todos os campos do manifesto JSON passaram na validação estrutural.
  - O arquivo de vídeo local existe, foi inspecionado via `ffprobe` (`1080x1920`, `9:16`, `58s–62s`, `H.264/AAC`) e todos os itens obrigatórios do checklist humano (continuidade espacial, loop imperceptível, pronúncia PT-BR, legendas em safe zone e fidelidade autoral) foram comprovadamente verificados sem falhas.
- **`REVIEW` (Pendente de Análise Humana / Pós-Produção):**
  - Estado padrão de todo plano recém-criado ou quando há desvios menores que exigem decisão criativa/humana (ex.: blueprint 100% válido aguardando geração dos vídeos locais, ou leve variação de cor no bloco 4 que requer ajuste manual).
- **`FAIL` (Reprovado — Bloqueado para Publicação):**
  - Qualquer violação da história do autor, corte seco aparente entre segmentos, deformação anatômica/arquitetônica visível, quebra perceptível no loop `F_END -> F_000`, erro de pronúncia na narração, legenda cortada/cobrindo o ponto focal ou resolução fora de `1080x1920`.