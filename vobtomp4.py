#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional


def ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit(
            "ffmpeg não encontrado. Instale-o (ex.: brew install ffmpeg) e tente novamente."
        )


def discover_vob_files(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".vob" else []
    files: List[Path] = []
    for p in input_path.rglob("*"):
        if p.is_file() and p.suffix.lower() == ".vob":
            files.append(p)
    return sorted(files)


def build_ffmpeg_cmd(
    src: Path,
    dst: Path,
    *,
    preset: str = "medium",
    crf: int = 20,
    deinterlace: bool = False,
    audio_bitrate: str = "192k",
    overwrite: bool = False,
    threads: Optional[int] = None,
) -> List[str]:
    cmd: List[str] = [
        "ffmpeg",
        "-hide_banner",
        "-nostdin",
        "-y" if overwrite else "-n",
        "-i",
        str(src),
        "-map",
        "0:v:0?",
        "-map",
        "0:a:0?",
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        str(crf),
        "-c:a",
        "aac",
        "-b:a",
        audio_bitrate,
        "-movflags",
        "+faststart",
    ]

    if deinterlace:
        cmd += ["-vf", "yadif"]

    if threads is not None and threads > 0:
        cmd += ["-threads", str(threads)]

    cmd.append(str(dst))
    return cmd


def convert_one(
    src: Path,
    out_dir: Path,
    *,
    preset: str,
    crf: int,
    deinterlace: bool,
    audio_bitrate: str,
    overwrite: bool,
    dry_run: bool,
    threads: Optional[int],
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / (src.stem + ".mp4")

    if dst.exists() and not overwrite:
        print(f"[skip] já existe: {dst}")
        return 0

    cmd = build_ffmpeg_cmd(
        src,
        dst,
        preset=preset,
        crf=crf,
        deinterlace=deinterlace,
        audio_bitrate=audio_bitrate,
        overwrite=overwrite,
        threads=threads,
    )

    print("[ffmpeg]", " ".join(cmd))
    if dry_run:
        return 0

    proc = subprocess.run(cmd)
    return proc.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converter arquivos VOB em MP4 usando ffmpeg (H.264/AAC)",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Caminho de arquivo .VOB ou diretório contendo VOBs",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="Diretório de saída (default: mesmo diretório de cada arquivo)",
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=20,
        help="Qualidade CRF para H.264 (menor = melhor; típico 18-23; default: 20)",
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="medium",
        choices=[
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
        ],
        help="Preset de codificação x264 (velocidade vs compressão)",
    )
    parser.add_argument(
        "--audio-bitrate",
        type=str,
        default="192k",
        help="Bitrate de áudio AAC (ex.: 160k, 192k, 256k)",
    )
    parser.add_argument(
        "--deinterlace",
        action="store_true",
        help="Aplicar deinterlace (yadif), útil para DVDs entrelaçados",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Substituir arquivos MP4 existentes",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostrar os comandos, sem executar",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=None,
        help="Número de threads para ffmpeg (opcional)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_ffmpeg_available()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Caminho não existe: {input_path}")

    files = discover_vob_files(input_path)
    if not files:
        raise SystemExit("Nenhum arquivo .vob encontrado.")

    if args.output_dir:
        out_base = Path(args.output_dir).expanduser().resolve()
        out_base.mkdir(parents=True, exist_ok=True)
    else:
        out_base = None

    failures = 0
    for src in files:
        out_dir = out_base if out_base is not None else src.parent
        rc = convert_one(
            src,
            out_dir,
            preset=args.preset,
            crf=args.crf,
            deinterlace=args.deinterlace,
            audio_bitrate=args.audio_bitrate,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            threads=args.threads,
        )
        if rc != 0:
            print(f"[erro] falhou: {src}")
            failures += 1

    if failures:
        raise SystemExit(f"Conversão concluída com falhas: {failures} arquivo(s)")
    else:
        print("Conversão concluída com sucesso.")


if __name__ == "__main__":
    main()
