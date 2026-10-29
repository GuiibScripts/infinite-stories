# Checklist Obrigatório de Controle de Qualidade (QA) — Infinite Stories

**Regra de Governança:** Nenhum vídeo pode receber o status `PASS` sem que todas as verificações abaixo tenham sido comprovadamente executadas sobre o arquivo renderizado local (`output/<slug>_final.mp4`).

---

## Identificação da Produção
- **Story ID / Slug:** `____________________`
- **Arquivo Inspecionado:** `output/____________________.mp4`
- **Data da Auditoria:** `____/____/2026`
- **Status Final Atribuído:** `[ ] PASS` | `[ ] REVIEW` | `[ ] FAIL`

---

## 1. Conformidade Técnica do Padrão de Vídeo (`validate_project.py --check-media`)
- [ ] **Proporção e Resolução:** Arquivo final possui exatamente `1080x1920` pixels (`9:16`, `SAR 1:1`).
- [ ] **Duração Total:** Entre `58.0s` e `62.0s` (alvo `60.0s`).
- [ ] **Taxa de Quadros (FPS):** Constante (`30 fps` ou `60 fps`), sem quedas ou frames duplicados irregulares.
- [ ] **Codecs e Container:** Vídeo `H.264 (yuv420p)` e áudio `AAC (48kHz)` em container `.mp4`.

## 2. Integridade Autoral e Roteiro
- [ ] **Fidelidade à História:** O roteiro final preserva 100% dos fatos essenciais, significado e desfecho definidos pelo autor.
- [ ] **Cadência dos 6 Blocos:** Gancho inicial nos primeiros 3s, progressão de descobertas (`B1` a `B4`), revelação principal no `B5_40_50` e ponte de retorno no `B6_50_60`.

## 3. Continuidade Visual Absoluta e Zoom Profundo
- [ ] **Ausência de Cortes Secos:** Não há cortes convencionais nem cenas sem relação espacial direta com o quadro anterior.
- [ ] **Continuidade de Perspectiva e Geometria:** Linhas arquitetônicas e objetos mecânicos não entortam nem "respiram" durante o avanço no eixo Z.
- [ ] **Continuidade de Iluminação e Cor:** A direção das sombras e a temperatura de cor permanecem consistentes nas emendas entre segmentos.
- [ ] **Consistência de Personagens e Objetos:** Nenhuma mão, rosto, roupa ou objeto sofre deformação anatômica ou mutação de modelo.
- [ ] **Nitidez no Zoom:** Nenhum trecho `TECH_A_DIGITAL` apresenta pixelização ou borramento por excesso de escala.

## 4. Qualidade do Loop (`F_END` -> `F_000`)
- [ ] **Correspondência Espacial:** O último quadro (`F_END`) coincide geometricamente e cromaticamente com o primeiro quadro (`F_000`).
- [ ] **Ausência de Crossfade Fantasma:** Não há dupla exposição ou efeito fantasma na virada do loop.
- [ ] **Continuidade de Velocidade:** O vídeo foi reproduzido 3 vezes seguidas em player com *repeat* ativado e não apresenta parada brusca nem solavanco de escala na passagem do último segundo para o segundo zero.

## 5. Áudio, Narração PT-BR e Legendas
- [ ] **Pronúncia e Naturalidade:** Voz em português brasileiro clara, com entonação adequada e zero erros de pronúncia em nomes, números ou palavras heterofônicas.
- [ ] **Mixagem e Loudness:** Voz inteligível em `-14 LUFS`, ambiência com ducking correto e emenda de áudio suave na virada do loop.
- [ ] **Legendas Sincronizadas em Safe Zone:** Legendas revisadas ortograficamente, máximo de 28 caracteres por linha (até 2 linhas), posicionadas na zona segura inferior (`Y = 1380px–1580px`) sem cobrir o ponto focal do zoom.