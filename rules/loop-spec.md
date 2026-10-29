# Regra Permanente: Engenharia de Loop Visual e Auditivo Imperceptível

## 1. Regra de Ouro do Loop
O loop no **Infinite Stories** nunca é improvisado na edição final. O vídeo começa no **Quadro-Âncora Mestre (`F_000`)** no instante `00:00.000` e toda a jornada espacial dos 60 segundos é desenhada para que o último segmento (`B6_50_60`) desemboque geometricamente no próprio `F_000` no instante final (`F_END`).

## 2. Estratégias Aprovadas de Loop (`loop_strategy`)

Cada história deve selecionar **uma** das quatro estratégias abaixo desde a concepção do roteiro:

1. **`PORTAL_FRAME_MATCH` (Portal / Enquadramento Recursivo):**
   - O zoom final atravessa uma abertura física coerente com a narrativa (uma fotografia antiga sobre uma mesa, a tela de um monitor de segurança, o visor de uma câmera, uma janela ou espelho) cuja imagem interna revela ser exatamente a cena aberta inicial `F_000`.
   - Exige composição de máscara na pós-produção para embutir o próprio `F_000` dentro da superfície do portal nos últimos 3 a 4 segundos do vídeo.
2. **`OPTICAL_SURFACE_MATCH` (Reflexo Óptico):**
   - A câmera aproxima-se de uma superfície reflexiva (pupila de um olho, lente de óculos, vidro de um relógio, gota de água, lâmina metálica) onde o reflexo nítido contém o plano aberto `F_000`. Ao preencher 100% do quadro `1080x1920`, o reflexo assume o lugar do `F_000`.
3. **`MICRO_TO_MACRO_TEXTURE_MATCH` (Oclusão/Textura Natural):**
   - O zoom mergulha em uma zona de sombra real ou textura homogênea fisicamente justificada (ex.: a escuridão interna do cano de uma fechadura, a madeira escura de um caixote que também compõe a borda inicial de `F_000`) e emerge imediatamente no plano inicial mantendo o mesmo vetor de velocidade no eixo Z.
4. **`CAMERA_PULLBACK_RESET` (Retorno Físico Acelerado Motivado):**
   - Nos últimos 4 a 6 segundos, após a revelação principal, a câmera executa um recuo contínuo (reverse dolly / hyper-pullback motivado pelo choque da revelação) refazendo exatamente o túnel espacial até cravar no `F_000`.

## 3. Proibições Estritas na Costura do Loop
- **PROIBIDO usar `crossfade` / `dissolve` genérico entre o último clipe e o primeiro:** Isso gera efeito fantasma (dupla exposição) denunciando imediatamente o corte.
- **PROIBIDO usar flashes brancos, glitch artificial ou fade-to-black:** Quebra a hipnose do zoom contínuo.
- **PROIBIDO salto de velocidade no frame zero:** Se o vídeo termina avançando a uma taxa de escala de `15% por segundo`, o primeiro segundo do vídeo (`00:00` a `00:01`) deve iniciar na mesma velocidade aparente de avanço.

## 4. Verificação Técnica da Emenda (`F_END` -> `F_000`)
Na etapa de pós-produção e QA:
1. O frame `F_000` deve ser usado literalmente como alvo de alinhamento (`frame_out`) do último segmento.
2. Em estratégias `PORTAL_FRAME_MATCH` e `OPTICAL_SURFACE_MATCH`, os primeiros 15 frames do vídeo (`SEG_01`) devem ser pré-compostos dentro do objeto-portal do último clipe para que até o movimento interno já esteja acontecendo quando o loop virar.
3. **Continuidade de Áudio no Loop:**
   - A ambiência sonora (room tone / drone grave) deve ser exportada com técnica de *seamless audio loop* (cortando o áudio nos últimos 2 segundos e aplicando crossfade de potência constante na trilha de fundo com o início, nunca na voz).
   - A última frase da narração (entre `56.0s` e `59.5s`) deve construir uma ponte semântica que se conecte naturalmente com a primeira frase do gancho (`00.2s`), incentivando o replay imediato.