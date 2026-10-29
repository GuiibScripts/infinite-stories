# Regra Permanente: Continuidade Visual Absoluta e Engenharia de Zoom Profundo

## 1. O Princípio da Realidade Única
O vídeo de 60 segundos do **Infinite Stories** não é uma montagem de cenas separadas; é uma **travessia contínua pelo eixo Z dentro de um mesmo universo tridimensional coerente**. Cada novo enquadramento (`Segment N+1`) deve existir fisicamente dentro de uma sub-região identificável do enquadramento anterior (`Segment N`).

## 2. Os 10 Mandamentos da Continuidade Espacial
1. **Continuidade de Perspectiva:** O ponto de fuga central ou secundário do quadro de saída de um clipe deve coincidir com o ponto de fuga do quadro de entrada do clipe seguinte.
2. **Continuidade de Iluminação:** Se a luz incide da esquerda a 35 graus no plano aberto, o objeto microscópico revelado 15 segundos depois deve receber luz da esquerda sob a mesma inclinação (salvo se estiver dentro de uma cavidade com fonte luminosa própria visível antes).
3. **Continuidade de Cores e Texturas:** A temperatura de cor e o balanço de branco não podem saltar na transição entre dois clipes gerados.
4. **Preservação da Geometria:** Linhas retas de mesas, molduras, portas e objetos mecânicos não podem curvar ou "respirar" (warping) durante o movimento.
5. **Consistência de Personagens e Materiais:** A roupa, textura da pele, idade e posição estática/dinâmica de um personagem não podem sofrer reinterpretação entre o plano aberto e o close-up.
6. **Vetor de Câmera Constante:** O movimento de dolly-in / zoom deve manter velocidade linear ou curva suave controlada (ease-in/ease-out apenas quando motivado pela narração), sem trancos de desaceleração a cada 5 ou 8 segundos.
7. **Tolerância Zero a Morphing:** Objetos não podem derreter ou se transformar em outros objetos para forçar uma transição.
8. **Permanência de Objetos:** Nenhum elemento presente na região central de foco pode desaparecer subitamente nem surgir do nada sem estar previamente sugerido na escala anterior.
9. **Estabilidade Arquitetônica:** Paredes, janelas, móveis e fundos periféricos devem sair pelas bordas do quadro seguindo rigorosamente a paralaxe óptica natural.
10. **Costura Invisível entre Gerações:** A passagem entre o último frame do `SEG_N` e o primeiro frame do `SEG_N+1` deve ser ancorada pelo mesmo keyframe (`frame_out` de N = `frame_in` de N+1).

## 3. Seleção das Três Técnicas de Zoom

O planejador visual deve escolher explicitamente entre três técnicas para cada segmento em `stories/<slug>.json`:

### Técnica A — `TECH_A_DIGITAL` (Zoom Digital Matemático)
- **Como funciona:** Ampliação progressiva via matriz de escala e translação (FFmpeg `zoompan` ou composição em 4K/8K reduzida para `1080x1920`) sobre um quadro estático de altíssima resolução.
- **Quando usar:** Atravessar até `2.0x` de aproximação onde o objeto já está nítido na imagem 4K base, ou para estabilizar o início/fim de um loop.
- **Limite:** Proibido ultrapassar `2.2x` de ampliação pura sem reancoragem generativa, pois causa perda de nitidez perceptível (pixelização/blur).

### Técnica B — `TECH_B_GENERATIVE` (Geração de Quadros via Google Flow / Veo)
- **Como funciona:** Uso do modelo Veo condicionado por `frame_in` (Image-to-Video) e, sempre que suportado pela versão em uso, `frame_out` (First-and-Last-Frame interpolation), instruindo avanço físico de câmera (`slow steady dolly-in along Z-axis`).
- **Quando usar:** Quando há movimento sutil na cena (fumaça, poeira em suspensão, respiração de personagem, oscilação de pêndulo, paralaxe 3D real entre primeiro plano e fundo).
- **Mitigação de Risco:** Como modelos de vídeo podem alterar o contraste ou suavizar texturas no final do clipe, o último frame real aprovado do `SEG_N` deve ser extraído via FFmpeg (`-vf "select=eq(n\,LAST_FRAME)"`) e usado como `frame_in` exato do `SEG_N+1`, ou corrigido com color-match na pós.

### Técnica C — `TECH_C_HYBRID` (Composição Híbrida de Alta Precisão)
- **Como funciona:** Combina um zoom digital inicial sobre o quadro de alta resolução (`1.0x` a `1.5x`) enquanto o centro do quadro faz blend com máscara de borda suave (feathering radial) para um quadro-alvo detalhado que inicia o clipe Veo seguinte.
- **Quando usar:** Na transição crítica entre escalas extremas (ex.: do rosto de uma pessoa para o reflexo na pupila; da fechadura de uma porta para o interior escuro do mecanismo).

## 4. Protocolo de Ancoragem Espacial (`Spatial Lock`)
Todo segmento no manifesto JSON deve declarar seu objeto `spatial_lock`:
- `parent_segment_id`: ID do segmento imediatamente anterior (`null` para `SEG_01`).
- `target_roi_norm`: Coordenadas normalizadas `[x_center, y_center, width_ratio, height_ratio]` (valores de `0.0` a `1.0`) indicando exatamente em qual retângulo do `frame_in` o `frame_out` está contido.
- `scale_factor`: Multiplicador de aproximação do segmento (ex.: `2.5` significa que o quadro final mostra uma área 2.5x menor que o quadro inicial).