# Convert VOB to MP4 (H.264/AAC)

Simple Python script using `ffmpeg` to convert `.VOB` (DVD) files to `.mp4` (H.264/AAC), with options for quality and deinterlacing.

## Requirements

- macOS (or any OS with Python 3)
- Python 3.8+
- ffmpeg installed and available in `PATH`

On macOS, install ffmpeg via Homebrew:

```bash
brew install ffmpeg
```

## Quick Start

From the project folder, run:

```bash
python3 vobtomp4.py /path/to/vob_folder_or_file -o /path/to/output \
  --crf 20 --preset medium --deinterlace --overwrite
```

- `input`: a single `.VOB` file or a directory containing multiple `.VOB` files.
- `-o/--output-dir`: output directory (default: same directory as the input file).
- `--crf`: video quality (typical 18–23; lower = better; default 20).
- `--preset`: x264 speed (`ultrafast` … `veryslow`), default `medium`.
- `--deinterlace`: apply `yadif` filter (DVDs are often interlaced).
- `--overwrite`: overwrite existing outputs.
- `--dry-run`: only print the `ffmpeg` commands.
- `--threads`: set number of `ffmpeg` threads.

Examples:

```bash
# Convert a specific file, saving alongside it
python3 vobtomp4.py /Volumes/DVD/VIDEO_TS/VTS_01_1.VOB --deinterlace

# Convert all .VOB files in a directory to a chosen output folder
python3 vobtomp4.py /Volumes/DVD/VIDEO_TS -o ~/Movies/DVD01 --crf 20 --preset medium

# Only preview the commands, without executing
python3 vobtomp4.py /Volumes/DVD/VIDEO_TS -o ~/Movies/DVD01 --dry-run
```

## Notes

- The script re-encodes to H.264/AAC for broad compatibility. If you want remuxing (no re-encode), note that MPEG-2 in MP4 is not widely supported.
- For better quality with moderate size, try `--crf 18` or `--crf 20` with `--preset slow`.
- DVDs are often 480i/576i; using `--deinterlace` usually improves appearance.

## Common Issues

- "ffmpeg not found": install via `brew install ffmpeg` and try again.
- Permission errors on external volumes: check source and destination directory permissions.
