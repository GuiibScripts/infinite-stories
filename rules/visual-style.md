# Regra Permanente: Direção de Arte e Hiper-Realismo Cinematográfico

## 1. Identidade Visual Central
A assinatura do projeto **Infinite Stories** é a aparência de **filmagem óptica real capturada por câmera de cinema digital (ex.: ARRI Alexa Mini LF / RED V-Raptor)** com lentes prime esféricas de alta nitidez. O espectador deve sentir que está observando um espaço físico tangível, jamais uma animação 3D, pintura digital ou colagem de IA.

## 2. Pilares Obrigatórios de Fotorealismo
1. **Física dos Materiais (PBR Realista):**
   - Metais devem apresentar micro-arranhões anisotrópicos, oxidação natural nas bordas e reflexos coerentes com o entorno.
   - Madeira deve exibir veios contínuos, porosidade e variação de verniz conforme o ângulo da luz.
   - Pele humana deve conter poros visíveis, penugem fina (vellus hair), variação sutil de sub-surface scattering (SSS) e assimetrias naturais.
   - Tecidos devem mostrar trama de fios real, dobras gravitacionais coerentes e desgaste orgânico.
2. **Iluminação Motivada:**
   - Toda fonte de luz dentro do quadro precisa ter uma origem física justificável (janela lateral, lâmpada de tungstênio de 2700K, luz do entardecer a 4500K, farol distante).
   - A queda de luz (light falloff) deve obedecer à lei do inverso do quadrado.
   - Sombras projetadas não podem mudar de ângulo durante o avanço da câmera no eixo Z.
3. **Óptica e Profundidade de Campo (DoF):**
   - Evitar fundo infinitamente nítido artificial (aspecto de renderização 3D barata) e evitar bokeh exagerado que destrua a leitura do cenário ao redor.
   - Utilizar profundidade de campo equivalente a f/4.0 – f/5.6 em planos médios/abertos e ajustar gradualmente o plano focal conforme a câmera avança para macro (f/8.0 – f/11 com foco cravado no ponto de interesse).
   - Textura orgânica de sensor (grão cinematográfico 35mm fino, quase imperceptível, adicionado de forma uniforme na pós-produção para unificar diferentes gerações).

## 3. O Que É Estritamente Proibido (Negative Visual Rules)
- Estética de plástico liso, pele de boneca de cera ou brilho especular artificial ("AI gloss").
- Textos, placas, relógios com números deformados ou pseudo-alfabetos gerados pelo modelo de vídeo (qualquer texto diegético essencial deve ser ancorado por imagem de referência limpa ou evitado).
- Aberração cromática exagerada, lens flares falsos não motivados ou vinhetas pesadas.
- Deformação anatômica (mãos com dedos extras/fundidos, olhos assimétricos sem foco, articulações dobrando no sentido oposto).
- Arquitetura impossível (linhas de parede tortas, janelas que mudam de grade, pisos cujo padrão de ladrilho se dissolve).

## 4. Bíblia Visual Individual por História
A identidade do projeto é o **realismo e a continuidade espacial**, não a repetição do mesmo cenário. Cada arquivo em `stories/<slug>.json` deve declarar seu objeto `visual_bible` próprio contendo:
- `era_and_setting`: Período histórico e localização física exata.
- `color_palette_hex`: 4 a 5 cores dominantes e de destaque.
- `lighting_setup`: Direção principal (key light), temperatura em Kelvin, contraste (ratio) e atmosfera volumétrica.
- `lens_profile`: Distância focal inicial e comportamento óptico durante o avanço.
- `immutable_anchors`: Lista de objetos, feições de personagens, roupas e estruturas arquitetônicas que não podem sofrer mutação entre segmentos.