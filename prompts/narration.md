# Prompt Operacional: Direção de Voz PT-BR e Sincronização de Legendas (`narration`)

Use este template para transformar o texto narrado dos 6 blocos em um plano de produção de voz sintética e um arquivo de legendas `.srt` perfeitamente cronometrado.

---

## Instruções para a IA

1. **Validação de Tempo de Fala:**
   - Some todas as palavras dos 6 blocos. A média deve ficar entre `125` e `150` palavras totais para caber em `60.0s` sem aceleração artificial da voz.
   - Verifique cada bloco de 10 segundos: nenhum bloco pode ter mais de `28 palavras` (máximo absoluto para 10 segundos com dicção clara em PT-BR).
2. **Guia Fonético e de Entonação:**
   - Destaque palavras que exigem atenção na pronúncia em português brasileiro (números por extenso, nomes estrangeiros aportuguesados ou termos ambíguos).
   - Especifique a curva emocional de cada bloco (ex.: `B1_00_10`: tom de curiosidade contida e grave; `B5_40_50`: tom firme de revelação precedido por pausa de `0.7s`).
3. **Geração da Grade de Legendas (`.srt`):**
   - Quebre a locução em blocos curtos (máximo de `28 caracteres por linha`, máximo de `2 linhas por legenda`, duração entre `1.0s` e `2.8s`).
   - Posicione todas as legendas na zona segura inferior (`Y = 1380px–1580px`) para nunca obstruir o eixo central do zoom.
   - Entregue o conteúdo completo pronto para salvar em `assets/subtitles/<story_slug>.srt`.