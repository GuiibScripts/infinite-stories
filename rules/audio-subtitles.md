# Regra Permanente: Narração em PT-BR, Design de Áudio e Legendagem

## 1. Isolamento Obrigatório da Camada de Voz
- **Regra Técnica:** Jamais utilizar fala gerada nativamente pelo modelo de vídeo (Veo/Flow) como narração final. Os clipes de vídeo devem ser tratados como **imagem pura** (ou apenas referência de som ambiente descartável).
- A narração oficial deve ser produzida em etapa dedicada via motor de síntese de voz (TTS neural de alta fidelidade em PT-BR) ou gravação controlada, salva em `assets/audio/<story_slug>_narration.wav` (`48kHz`, `24-bit` ou `16-bit PCM`).

## 2. Padrão de Qualidade da Narração PT-BR
1. **Pronúncia e Prosódia:** Sotaque brasileiro neutro e natural, com queda tonal correta no final de frases declarativas e suspensão sutil antes de revelações.
2. **Controle de Pausas:**
   - Pausas curtas entre orações: `0.25s` a `0.40s`.
   - Pausas dramáticas em viradas de bloco (especialmente antes do `B5_40_50`): `0.60s` a `1.00s`.
   - Margem de respiro no início (`0.00s` a `0.25s`) e no fim (`59.50s` a `60.00s`) para que a emenda do loop não corte sílabas ao meio.
3. **Verificação Fonética Obrigatória:** Nomes próprios, siglas, anos, números cardinais e palavras com heterofonia em português (ex.: *"colher"*, *"sede"*, *"acordo"*, *"começo"*) devem ser revisados auditivamente após a geração e, se necessário, grafados foneticamente no prompt de voz.

## 3. Mixagem e Loudness
- **Voz Principal (Narração):** Centralizada, clara, processada com filtro passa-altas suave em `80Hz`, compressão controlada e nível integrado em `-14 LUFS` (pico máximo `-1.0 dBTP`).
- **Camada de Ambiência e Sub-Bass de Movimento:** Deve acompanhar a física do espaço (ex.: tique-taque abafado que cresce conforme o zoom se aproxima do relógio, vento externo que diminui ao entrar em uma fresta), realizando ducking automático (`-6dB` a `-10dB`) sempre que a voz estiver ativa.

## 4. Regras de Legendagem (Pós-Produção Exclusiva)
- **Proibição Absoluta:** Nunca pedir ao gerador de imagens/vídeo para renderizar legendas dentro da cena.
- **Formato Base:** Gerar arquivo `.srt` (e opcionalmente `.ass` estilizado) em `assets/subtitles/<story_slug>.srt`.
- **Regras de Segmentação do Texto:**
  - Máximo de **28 caracteres por linha**.
  - Máximo de **2 linhas simultâneas** por bloco de legenda.
  - Duração mínima de exibição por legenda: `0.8s` | Duração máxima: `3.0s`.
  - Quebra sintática limpa (não separar artigo de substantivo em linhas diferentes).
- **Posicionamento e Safe Zones (`1080x1920`):**
  - Centralizado horizontalmente (margem mínima de `90px` na esquerda e direita).
  - Posicionado na faixa vertical inferior segura: entre `Y = 1380px` e `Y = 1580px` (`340px` a `540px` acima da borda inferior), evitando sobrepor os botões e a descrição da interface do Reels/TikTok/Shorts e **jamais cobrindo o centro óptico do zoom (`Y = 850px` a `1100px`)**.
  - Tipografia limpa sem serifa (ex.: `Montserrat Bold` ou `Inter ExtraBold`), cor branca (`#FFFFFF`) ou amarelo-claro (`#FFD700` para palavras-chave pontuais) com contorno escuro (`outline 3px #000000`) e sombra suave para legibilidade sobre qualquer fundo.