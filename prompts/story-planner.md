# Prompt Operacional: Planejador de Roteiro e Estrutura Temporal (`story-planner`)

Use este template quando receber uma nova história autoral do usuário para criar a camada narrativa do arquivo `stories/<slug>.json`.

---

## Instruções para a IA

1. Leia integralmente a história fornecida pelo autor.
2. Verifique se os seguintes elementos estão claros:
   - Cenário físico principal onde a câmera pode iniciar (`F_000`).
   - Sequência de acontecimentos essenciais.
   - Objeto ou detalhe revelador do clímax (`B5_40_50`).
   - Desfecho definido pelo autor e como ele permite retornar visualmente ao `F_000` (`B6_50_60`).
3. **Se faltar alguma informação essencial que altere a história, PARE e faça no máximo 3 perguntas diretas ao autor antes de gerar o roteiro.**
4. Caso a história esteja completa, estruture os 6 blocos temporais (`B1_00_10` a `B6_50_60`) obedecendo a `rules/storytelling.md`:
   - Duração total da locução: `58.0s` a `60.0s` (entre `125` e `150` palavras em PT-BR).
   - Gancho inicial (`00.0s – 03.0s`) que gere curiosidade genuína sem clichês.
   - Sincronia exata entre cada frase narrada e o que o zoom está revelando naquele bloco de 10 segundos.
   - Última frase do bloco `B6_50_60` desenhada para conectar semanticamente com a primeira frase do bloco `B1_00_10`.

## Formato de Saída Esperado (Mapeado para `stories/<slug>.json`)

Para cada um dos 6 blocos (`B1_00_10` a `B6_50_60`), entregue:
- `block_id`: Identificador padrão (`B1_00_10` ... `B6_50_60`).
- `time_start_sec` e `time_end_sec`: Janela exata em segundos.
- `narrative_goal`: O que este bloco cumpre na retenção e na história do autor.
- `narration_ptbr`: Texto exato em português brasileiro com marcações de pausa (`[pausa 0.4s]`).
- `word_count` e `estimated_speech_sec`: Contagem real de palavras e tempo estimado de leitura a `2.3 palavras/s`.
- `visual_discovery`: Qual elemento físico entra em evidência conforme o zoom avança neste trecho.