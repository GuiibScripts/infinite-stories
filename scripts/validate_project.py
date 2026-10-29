#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infinite Stories — Validador Arquitetural e Leitor de Padrão de Vídeo
Verifica a estrutura do repositório, as regras permanentes e valida os manifestos
de histórias (stories/*.json) no modo Blueprint (Git) e no modo Mídia Local (ffprobe).
"""

import argparse
import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "config/project.json",
    "config/providers.example.json",
    "rules/visual-style.md",
    "rules/continuity.md",
    "rules/loop-spec.md",
    "rules/storytelling.md",
    "rules/audio-subtitles.md",
    "rules/flow-veo-prompts.md",
    "rules/quality-control.md",
    "prompts/story-planner.md",
    "prompts/visual-planner.md",
    "prompts/flow-clip.md",
    "prompts/narration.md",
    "prompts/quality-review.md",
    "stories/README.md",
    "stories/example-story.json",
    "production/shot-log.csv",
    "production/qa-checklist.md",
    "scripts/README.md",
    "scripts/validate_project.py",
    "output/README.md",
]

REQUIRED_DIRS = [
    "config",
    "rules",
    "prompts",
    "stories",
    "production",
    "production/reports",
    "scripts",
    "assets/references",
    "assets/generated",
    "assets/audio",
    "assets/subtitles",
    "output",
]

BANNED_VAGUE_PHRASES = [
    "faça um vídeo cinematográfico incrível",
    "make an amazing cinematic video",
    "ultra 8k masterpiece magic",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_repository_structure(root: Path) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for rel_dir in REQUIRED_DIRS:
        p = root / rel_dir
        if not p.is_dir():
            errors.append(f"[ESTRUTURA] Diretório obrigatório ausente: {rel_dir}")

    for rel_file in REQUIRED_FILES:
        p = root / rel_file
        if not p.is_file():
            errors.append(f"[ESTRUTURA] Arquivo permanente ausente: {rel_file}")
        elif p.stat().st_size < 50:
            errors.append(f"[ESTRUTURA] Arquivo parece vazio ou incompleto: {rel_file}")

    gitignore_path = root / ".gitignore"
    if gitignore_path.is_file():
        content = gitignore_path.read_text(encoding="utf-8")
        for pattern in ["*.mp4", "*.mov", "*.wav", "output/*", "config/providers.json"]:
            if pattern not in content:
                errors.append(
                    f"[GITIGNORE] Regra obrigatória '{pattern}' ausente no .gitignore (proteção contra vídeos/segredos no Git)."
                )

    return errors, warnings


def probe_local_video(video_path: Path, expected_pattern: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    if not video_path.is_file():
        errors.append(f"[MIDIA LOCAL] Arquivo de vídeo esperado não encontrado no disco: {video_path}")
        return errors, warnings

    ffprobe_bin = shutil.which("ffprobe")
    if not ffprobe_bin:
        warnings.append(
            f"[MIDIA LOCAL] 'ffprobe' não encontrado no PATH. Não foi possível inspecionar metadados internos de {video_path.name}."
        )
        return errors, warnings

    cmd = [
        ffprobe_bin,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_name,codec_type,width,height,pix_fmt",
        "-of",
        "json",
        str(video_path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(proc.stdout)
    except Exception as exc:
        errors.append(f"[MIDIA LOCAL] Falha ao executar ffprobe em {video_path}: {exc}")
        return errors, warnings

    streams = info.get("streams", [])
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    if not video_streams:
        errors.append(f"[MIDIA LOCAL] Nenhuma trilha de vídeo encontrada em {video_path}")
    else:
        vs = video_streams[0]
        w = int(vs.get("width", 0))
        h = int(vs.get("height", 0))
        codec = vs.get("codec_name", "")
        exp_w = int(expected_pattern.get("width_px", 1080))
        exp_h = int(expected_pattern.get("height_px", 1920))
        if (w, h) != (exp_w, exp_h):
            errors.append(
                f"[MIDIA LOCAL] Resolução inválida em {video_path.name}: encontrado {w}x{h}, esperado {exp_w}x{exp_h} (9:16)."
            )
        if codec != expected_pattern.get("video_codec", "h264"):
            warnings.append(
                f"[MIDIA LOCAL] Codec de vídeo em {video_path.name} é '{codec}', padrão recomendado é '{expected_pattern.get('video_codec', 'h264')}'."
            )

    if not audio_streams:
        warnings.append(f"[MIDIA LOCAL] Nenhuma trilha de áudio encontrada em {video_path.name}.")

    fmt_duration = float(info.get("format", {}).get("duration", 0.0))
    target_dur = float(expected_pattern.get("target_duration_sec", 60.0))
    tol_dur = float(expected_pattern.get("duration_tolerance_sec", 2.0))
    if abs(fmt_duration - target_dur) > tol_dur:
        errors.append(
            f"[MIDIA LOCAL] Duração fora da tolerância em {video_path.name}: {fmt_duration:.2f}s (esperado {target_dur:.1f}s +/- {tol_dur:.1f}s)."
        )

    return errors, warnings


def validate_story_manifest(
    root: Path,
    story_path: Path,
    project_cfg: Dict[str, Any],
    check_media: bool = False,
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    prefix = f"[{story_path.name}]"

    try:
        story = load_json(story_path)
    except Exception as exc:
        return [f"{prefix} JSON inválido: {exc}"], []

    # 1. Campos raiz obrigatórios
    required_root_keys = [
        "schema_version",
        "story_id",
        "slug",
        "title",
        "qa_status",
        "author_lock",
        "video_pattern_expectation",
        "visual_bible",
        "loop_specification",
        "macro_blocks",
        "segments",
        "audio_and_subtitles",
    ]
    for k in required_root_keys:
        if k not in story:
            errors.append(f"{prefix} Campo raiz obrigatório ausente: '{k}'")

    if errors:
        return errors, warnings

    # 2. Validação do QA Status
    allowed_statuses = project_cfg["qa_policy"]["allowed_statuses"]
    qa_status = story.get("qa_status")
    if qa_status not in allowed_statuses:
        errors.append(f"{prefix} qa_status '{qa_status}' inválido. Permitidos: {allowed_statuses}")

    # 3. Validação do Author Lock
    author_lock = story["author_lock"]
    if not author_lock.get("original_author_premise") or len(author_lock.get("immutable_facts", [])) < 2:
        errors.append(f"{prefix} 'author_lock' deve conter 'original_author_premise' e pelo menos 2 'immutable_facts'.")

    # 4. Validação do Padrão de Vídeo Declarado (Video Pattern Expectation)
    vpe = story["video_pattern_expectation"]
    std = project_cfg["video_pattern_standard"]
    if vpe.get("aspect_ratio") != std["aspect_ratio"]:
        errors.append(f"{prefix} aspect_ratio inválido: {vpe.get('aspect_ratio')} (esperado {std['aspect_ratio']})")
    if vpe.get("width_px") != std["width_px"] or vpe.get("height_px") != std["height_px"]:
        errors.append(
            f"{prefix} Resolução declarada inválida: {vpe.get('width_px')}x{vpe.get('height_px')} (esperado 1080x1920)"
        )

    # 5. Validação da Bíblia Visual e Especificação de Loop
    vb = story["visual_bible"]
    for vk in ["era_and_setting", "color_palette_hex", "lighting_setup", "lens_profile", "immutable_anchors"]:
        if not vb.get(vk):
            errors.append(f"{prefix} Campo '{vk}' ausente ou vazio em 'visual_bible'.")

    loop_spec = story["loop_specification"]
    allowed_loops = project_cfg["zoom_and_continuity"]["allowed_loop_strategies"]
    if loop_spec.get("loop_strategy") not in allowed_loops:
        errors.append(
            f"{prefix} loop_strategy '{loop_spec.get('loop_strategy')}' inválida. Permitidas: {allowed_loops}"
        )
    f000_path = loop_spec.get("anchor_frame_f000_path", "")
    if not f000_path:
        errors.append(f"{prefix} 'anchor_frame_f000_path' (F_000) não definido em 'loop_specification'.")

    # 6. Validação dos 6 Blocos Temporais (00-60s)
    blocks = story["macro_blocks"]
    expected_block_ids = project_cfg["narrative_structure"]["macro_block_ids"]
    if len(blocks) != 6:
        errors.append(f"{prefix} Devem existir exatamente 6 macro_blocks (encontrados: {len(blocks)}).")
    else:
        total_words = 0
        for idx, blk in enumerate(blocks):
            exp_id = expected_block_ids[idx]
            if blk.get("block_id") != exp_id:
                errors.append(f"{prefix} Bloco {idx+1} tem ID '{blk.get('block_id')}', esperado '{exp_id}'.")
            expected_start = float(idx * 10)
            expected_end = float((idx + 1) * 10)
            if float(blk.get("time_start_sec", -1)) != expected_start or float(blk.get("time_end_sec", -1)) != expected_end:
                errors.append(
                    f"{prefix} Bloco {exp_id} deve cobrir {expected_start:.1f}s a {expected_end:.1f}s."
                )
            narration = blk.get("narration_ptbr", "").strip()
            if not narration:
                errors.append(f"{prefix} Bloco {exp_id} está sem 'narration_ptbr'.")
            total_words += int(blk.get("word_count", 0))

        min_w = project_cfg["narrative_structure"]["min_words_total"]
        max_w = project_cfg["narrative_structure"]["max_words_total"]
        if not (min_w <= total_words <= max_w):
            warnings.append(
                f"{prefix} Total de palavras da narração ({total_words}) fora da faixa ideal ({min_w}–{max_w} palavras para 60s)."
            )

    # 7. Validação dos Segmentos, Continuidade Espacial, Prompts e Fechamento do Loop
    segments = story["segments"]
    allowed_techs = project_cfg["zoom_and_continuity"]["allowed_techniques"]
    if not segments:
        errors.append(f"{prefix} Lista de 'segments' está vazia.")
    else:
        total_seg_dur = 0.0
        seen_prompts = set()
        prev_frame_out = None
        prev_seg_id = None

        for i, seg in enumerate(segments):
            seg_id = seg.get("segment_id", f"INDEX_{i}")
            dur = float(seg.get("duration_sec", 0.0))
            total_seg_dur += dur

            tech = seg.get("zoom_technique")
            if tech not in allowed_techs:
                errors.append(f"{prefix} [{seg_id}] zoom_technique '{tech}' inválida.")

            # Validação de encadeamento espacial de quadros (frame_in / frame_out)
            f_in = seg.get("frame_in_ref", "")
            f_out = seg.get("frame_out_ref", "")
            if not f_in or not f_out:
                errors.append(f"{prefix} [{seg_id}] 'frame_in_ref' e 'frame_out_ref' são obrigatórios.")
            if i == 0 and f_in != f000_path:
                errors.append(
                    f"{prefix} [{seg_id}] O primeiro segmento deve iniciar exatamente no 'anchor_frame_f000_path' ({f000_path})."
                )
            if i > 0 and f_in != prev_frame_out:
                errors.append(
                    f"{prefix} [{seg_id}] Quebra de continuidade de quadro-chave: frame_in_ref ({f_in}) difere do frame_out_ref anterior ({prev_frame_out})."
                )

            # Validação do Spatial Lock
            slock = seg.get("spatial_lock", {})
            if i > 0 and slock.get("parent_segment_id") != prev_seg_id:
                errors.append(
                    f"{prefix} [{seg_id}] spatial_lock.parent_segment_id ('{slock.get('parent_segment_id')}') deve apontar para '{prev_seg_id}'."
                )
            roi = slock.get("target_roi_norm", [])
            if len(roi) != 4 or any(not (0.0 < float(v) <= 1.0) for v in roi):
                errors.append(
                    f"{prefix} [{seg_id}] spatial_lock.target_roi_norm deve ter 4 valores normalizados entre 0.0 e 1.0."
                )

            # Validação de Prompt Individualizado
            prompt_text = seg.get("generation_prompt", "").strip()
            if len(prompt_text) < 250:
                errors.append(
                    f"{prefix} [{seg_id}] 'generation_prompt' curto demais ({len(prompt_text)} chars). Deve especificar ambiente, lente, eixo Z, iluminação e restrições."
                )
            if prompt_text in seen_prompts:
                errors.append(f"{prefix} [{seg_id}] Prompt duplicado detectado! Cada segmento exige prompt próprio.")
            seen_prompts.add(prompt_text)

            for banned in BANNED_VAGUE_PHRASES:
                if banned in prompt_text.lower():
                    errors.append(f"{prefix} [{seg_id}] Prompt contém frase vaga proibida: '{banned}'.")

            if not seg.get("continuity_risks") or not seg.get("approval_criteria"):
                errors.append(f"{prefix} [{seg_id}] Deve listar 'continuity_risks' e 'approval_criteria'.")

            prev_frame_out = f_out
            prev_seg_id = seg_id

        # Verifica fechamento matemático do loop no último segmento
        if prev_frame_out != f000_path:
            errors.append(
                f"{prefix} [LOOP QUEBRADO] O 'frame_out_ref' do último segmento ({prev_frame_out}) deve retornar exatamente ao quadro inicial F_000 ({f000_path})."
            )

        if abs(total_seg_dur - 60.0) > 0.01:
            errors.append(
                f"{prefix} Soma da duração dos segmentos é {total_seg_dur:.2f}s (esperado exatamente 60.00s no planejamento)."
            )

    # 8. Validação de Legendas (limites de tela de celular)
    subs = story["audio_and_subtitles"].get("subtitle_blocks", [])
    max_chars = project_cfg["subtitles_standard"]["max_chars_per_line"]
    max_lines = project_cfg["subtitles_standard"]["max_lines_per_block"]
    if not subs:
        errors.append(f"{prefix} 'subtitle_blocks' está vazio em 'audio_and_subtitles'.")
    else:
        for sb in subs:
            lines = sb.get("text", "").split("\n")
            if len(lines) > max_lines:
                errors.append(
                    f"{prefix} [Legenda #{sb.get('index')}] Possui {len(lines)} linhas (máximo permitido: {max_lines})."
                )
            for ln in lines:
                if len(ln) > max_chars:
                    warnings.append(
                        f"{prefix} [Legenda #{sb.get('index')}] Linha '{ln}' tem {len(ln)} chars (recomendado <= {max_chars})."
                    )

    # 9. Verificação de Mídia Local e Trava de Segurança para status PASS
    final_video_rel = vpe.get("final_output_local_path", "")
    final_video_abs = root / final_video_rel

    if qa_status == "PASS" and not final_video_abs.is_file():
        errors.append(
            f"{prefix} [TRAVA DE QA] Status não pode ser 'PASS' sem que o vídeo final exista localmente em '{final_video_rel}' e seja inspecionado."
        )

    if check_media:
        m_err, m_warn = probe_local_video(final_video_abs, vpe)
        errors.extend(m_err)
        warnings.extend(m_warn)

    return errors, warnings


def validate_shot_log(root: Path) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    csv_path = root / "production/shot-log.csv"
    if not csv_path.is_file():
        return ["[SHOT-LOG] Arquivo production/shot-log.csv não encontrado."], []

    required_cols = {
        "story_id",
        "segment_id",
        "macro_block_id",
        "technique",
        "model_or_tool",
        "duration_sec",
        "frame_in_path",
        "frame_out_path",
        "output_clip_path",
        "qa_decision",
    }
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        missing = required_cols - fieldnames
        if missing:
            errors.append(f"[SHOT-LOG] Colunas obrigatórias ausentes em shot-log.csv: {sorted(missing)}")
        rows = list(reader)
        if not rows:
            warnings.append("[SHOT-LOG] shot-log.csv não possui linhas de registro.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validador do sistema Infinite Stories (Blueprint Git & Leitura de Padrão de Vídeo Local)."
    )
    parser.add_argument(
        "--story",
        type=str,
        default=None,
        help="Caminho para um arquivo JSON de história específico (ex: stories/example-story.json).",
    )
    parser.add_argument(
        "--check-media",
        action="store_true",
        help="Inspeciona também os arquivos de vídeo/áudio locais declarados no manifesto via ffprobe.",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Salva um relatório JSON detalhado da validação em production/reports/.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    all_errors: List[str] = []
    all_warnings: List[str] = []

    print("=" * 72)
    print("INFINITE STORIES — VALIDADOR DE PROJETO E PADRÃO DE VÍDEO")
    print("=" * 72)

    # 1. Estrutura de pastas e arquivos permanentes
    struct_err, struct_warn = validate_repository_structure(root)
    all_errors.extend(struct_err)
    all_warnings.extend(struct_warn)

    # 2. Configuração central
    cfg_path = root / "config/project.json"
    if not cfg_path.is_file():
        print("[FALHA CRÍTICA] config/project.json não encontrado.")
        return 1
    project_cfg = load_json(cfg_path)

    # 3. Shot log
    log_err, log_warn = validate_shot_log(root)
    all_errors.extend(log_err)
    all_warnings.extend(log_warn)

    # 4. Histórias (Manifestos de Padrão de Vídeo)
    if args.story:
        story_files = [root / args.story]
    else:
        story_files = sorted((root / "stories").glob("*.json"))

    if not story_files:
        all_errors.append("[STORIES] Nenhum arquivo .json encontrado em stories/.")

    for sf in story_files:
        s_err, s_warn = validate_story_manifest(root, sf, project_cfg, check_media=args.check_media)
        all_errors.extend(s_err)
        all_warnings.extend(s_warn)

    # Exibição do resultado
    print(f"Arquivos permanentes verificados : {len(REQUIRED_FILES)}")
    print(f"Histórias (Padrões JSON) lidas   : {len(story_files)}")
    print(f"Modo de verificação de mídia     : {'ATIVO (--check-media)' if args.check_media else 'BLUEPRINT (Git-safe)'}")
    print("-" * 72)

    if all_warnings:
        print(f"AVISOS ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"  [!] {w}")
        print("-" * 72)

    if all_errors:
        print(f"ERROS ENCONTRADOS ({len(all_errors)}):")
        for e in all_errors:
            print(f"  [X] {e}")
        print("-" * 72)
        final_state = "FAIL"
    else:
        print("NENHUM ERRO ESTRUTURAL OU DE PADRÃO ENCONTRADO.")
        final_state = "PASS (BLUEPRINT)" if not args.check_media else "PASS (BLUEPRINT + MIDIA LOCAL)"

    print(f"RESULTADO DA VALIDAÇÃO: {final_state}")
    print("=" * 72)

    if args.save_report:
        report_dir = root / "production/reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "latest_validation_report.json"
        report_payload = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "MEDIA_AND_BLUEPRINT" if args.check_media else "BLUEPRINT_ONLY",
            "stories_checked": [str(p.relative_to(root)) for p in story_files],
            "errors_count": len(all_errors),
            "warnings_count": len(all_warnings),
            "errors": all_errors,
            "warnings": all_warnings,
            "validation_result": final_state,
        }
        report_path.write_text(json.dumps(report_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Relatório salvo em: {report_path.relative_to(root)}")

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())