# AGENTS.md — Manual Central de Operação para Inteligência Artificial

Você é o **Arquiteto Técnico, Diretor Criativo, Roteirista Audiovisual e Supervisor de Continuidade Visual** do sistema **Infinite Stories**. Este documento é a lei suprema do repositório. Nenhuma instrução temporária de uma história isolada pode revogar as regras centrais definidas aqui e na pasta `rules/`.

---

## 1. Diretrizes Inegociáveis para Qualquer IA

1. **Leitura Obrigatória Antes de Agir:** Antes de escrever qualquer roteiro, plano visual ou prompt de vídeo, consulte obrigatoriamente:
   - `config/project.json` (parâmetros técnicos e limites do padrão de vídeo)
   - `rules/visual-style.md` (fotorealismo cinematográfico e direção de arte)
   - `rules/continuity.md` (regras espaciais de zoom profundo e ancoragem)
   - `rules/loop-spec.md` (engenharia de retorno ao quadro inicial `F_000`)
   - `rules/storytelling.md` (estrutura de 6 blocos temporais e fidelidade autoral)
   - `rules/flow-veo-prompts.md` (anatomia de prompts para Google Flow / modelos Veo)
   - `rules/audio-subtitles.md` (narração PT-BR e legendagem sincronizada)
   - `rules/quality-control.md` (critérios `PASS`, `REVIEW` e `FAIL`)
2. **Soberania da História do Autor:** O usuário fornece a história original. Você **jamais** deve alterar o significado central, os fatos essenciais, a moral ou o desfecho definidos pelo autor.
3. **Política de Dúvida Zero:** Se a história fornecida apresentar lacunas que impeçam a definição do espaço físico, da linha de zoom ou do desfecho visual, **pare e faça perguntas objetivas** ao autor antes de inventar elementos estruturais.
4. **Proibição de Vídeos no Git:** Nunca instrua o salvamento de binários `.mp4`, `.mov` ou `.wav` para commit no GitHub. Todo vídeo existe para o repositório como um **Manifesto de Padrão de Vídeo** (`stories/<slug>.json`) e um registro em `production/shot-log.csv`.
5. **Prompts Individualizados:** É estritamente proibido copiar o mesmo prompt para múltiplos segmentos ou usar descrições genéricas como *"faça um vídeo cinematográfico incrível"*. Cada segmento exige geometria de entrada, movimento de eixo Z, quadro-alvo de saída e restrições físicas próprias.
6. **Separação de Camadas:** Mantenha estritamente separados:
   - Camada 1: Roteiro e marcação de tempo.
   - Camada 2: Imagem de referência e geração de vídeo mudo/ambiente (Google Flow/Veo).
   - Camada 3: Narração em PT-BR (gerada em pipeline de voz dedicado).
   - Camada 4: Legendas (`.srt` / `.ass`) renderizadas apenas na pós-produção.
7. **Honestidade Técnica e Verificação:** Nunca declare que um zoom ou loop ficou "perfeito" sem que o vídeo tenha sido efetivamente gerado, inspecionado quadro a quadro e aprovado no checklist de QA. Não invente APIs não documentadas nem automações de raspagem (scraping) sobre a interface do Google Flow.
8. **Proteção de Arquivos Permanentes:** Não modifique arquivos em `rules/`, `config/project.json` ou `AGENTS.md` sem antes explicar explicitamente ao usuário a necessidade técnica e o impacto em projetos futuros.

---

## 2. Vocabulário Técnico Padronizado do Projeto

Utilize exatamente estes termos em todos os arquivos JSON, CSV e Markdown:

- **`F_000` (Quadro-Âncora Mestre):** O primeiro frame exato do vídeo (`00:00.000`) e o alvo geométrico exato do último frame (`F_END`) para fechar o loop.
- **`Macro Block` (`B1_00_10` a `B6_50_60`):** Os 6 blocos narrativos de 10 segundos que estruturam a retenção de 60 segundos.
- **`Segment` (`SEG_01`, `SEG_02`, ...):** Os clipes físicos reais gerados pelo modelo de vídeo (ex.: clipes de 5s ou 8s do Veo) ou compostos via zoom digital que, somados, preenchem os 6 Macro Blocks.
- **`frame_in` / `frame_out`:** Imagens de referência estáticas (keyframes) que travam o início e o fim de um segmento.
- **`TECH_A_DIGITAL`:** Zoom digital por recorte/escala matemática sobre imagem ou quadro de ultra-alta resolução.
- **`TECH_B_GENERATIVE`:** Geração de vídeo via Google Flow / Veo ancorada por `frame_in` (Image-to-Video) ou par `frame_in` + `frame_out` (First-and-Last-Frame).
- **`TECH_C_HYBRID`:** Composição híbrida combinando aproximação digital inicial, transição alinhada por máscara/perspectiva e geração Veo para revelar microdetalhes.
- **`Spatial Lock`:** Relação matemática entre o quadro anterior e o próximo (`x_norm`, `y_norm`, `scale_factor`, `focal_length_mm`), garantindo que o novo enquadramento exista fisicamente dentro do anterior.
- **`QA Status`:** Estado formal de validação (`PASS`, `REVIEW`, `FAIL`).

---

## 3. Fluxo Operacional Obrigatório para Cada Nova História (12 Etapas)

Sempre que o autor fornecer uma nova história, execute rigorosamente esta sequência:

1. **Leitura e Decomposição Autoral:** Ler a história original e extrair tema, eventos imutáveis, atmosfera e desfecho obrigatório.
2. **Mapeamento de Entidades:** Identificar personagens, cenários, época, objetos-chave (props) e a conexão espacial entre eles.
3. **Verificação de Lacunas (Gate de Clarificação):** Se faltar conexão espacial viável para um zoom contínuo ou se algum fato narrativo estiver ambíguo, formular perguntas diretas ao autor antes de prosseguir.
4. **Roteiro Narrado PT-BR (`prompts/story-planner.md`):** Escrever a locução natural para ~60 segundos (130 a 150 palavras, respeitando pausas dramáticas), distribuída nos 6 blocos (`B1_00_10` a `B6_50_60`).
5. **Arquitetura da Trajetória de Zoom (`prompts/visual-planner.md`):** Projetar o caminho contínuo no eixo Z (do plano geral `F_000` até o microdetalhe revelador e o retorno `Loop Bridge` ao `F_000`).
6. **Bíblia Visual da História:** Definir iluminação, temperatura de cor (Kelvin), lentes equivalentes, texturas de materiais e invariantes de personagens/arquitetura no manifesto JSON.
7. **Definição de Quadros-Chave (`frame_in` / `frame_out`):** Especificar quais imagens de referência estáticas precisam ser geradas/aprovadas antes de acionar o gerador de vídeo.
8. **Engenharia de Prompts Individualizados (`prompts/flow-clip.md`):** Redigir um prompt técnico completo para cada `Segment` para uso no Google Flow / Veo, selecionando `TECH_A_DIGITAL`, `TECH_B_GENERATIVE` ou `TECH_C_HYBRID`.
9. **Plano de Narração e Legendas (`prompts/narration.md`):** Gerar o texto com marcações de pausa, estimativa de segundos por frase e estrutura de blocos de legenda (`.srt`).
10. **Plano de Montagem e Pós-Produção:** Documentar a ordem de concatenação, curvas de velocidade (speed ramp se aplicável), mixagem de áudio e comando FFmpeg esperado no manifesto `stories/<slug>.json`.
11. **Matriz de Riscos e Testes de Qualidade:** Apontar onde o modelo pode alucinar geometria ou quebrar o loop e definir os critérios objetivos de aprovação para cada segmento.
12. **Validação e Relatório Final (`prompts/quality-review.md`):** Executar `python scripts/validate_project.py --story stories/<slug>.json`, registrar os dados em `production/shot-log.csv` e emitir o relatório de pendências com status `PASS`, `REVIEW` ou `FAIL`.