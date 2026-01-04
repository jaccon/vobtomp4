# Converter VOB para MP4 (H.264/AAC)

Script simples em Python usando `ffmpeg` para converter arquivos `.VOB` (DVD) para `.mp4` (H.264/AAC), com opções de qualidade e deinterlace.

## Requisitos

- macOS (ou outro SO com Python 3)
- Python 3.8+
- ffmpeg instalado e no `PATH`

No macOS, instale o ffmpeg via Homebrew:

```bash
brew install ffmpeg
```

## Uso rápido

Entre na pasta do projeto e execute:

```bash
python3 convert_vob_to_mp4.py /caminho/para/pasta_ou_arquivo_vob -o /caminho/saida \
  --crf 20 --preset medium --deinterlace --overwrite
```

- `input`: arquivo `.VOB` único ou diretório com múltiplos `.VOB`.
- `-o/--output-dir`: diretório de saída (default: mesmo diretório do arquivo).
- `--crf`: qualidade do vídeo (18-23 é típico; menor = melhor; default 20).
- `--preset`: velocidade x264 (`ultrafast` … `veryslow`), default `medium`.
- `--deinterlace`: aplica filtro `yadif` (DVDs costumam ser entrelaçados).
- `--overwrite`: sobrescreve saídas existentes.
- `--dry-run`: apenas mostra os comandos `ffmpeg`.
- `--threads`: define número de threads do `ffmpeg`.

Exemplos:

```bash
# Converter um arquivo específico, salvando ao lado
python3 convert_vob_to_mp4.py /Volumes/DVD/VIDEO_TS/VTS_01_1.VOB --deinterlace

# Converter todos os .VOB de um diretório para uma pasta de saída
python3 convert_vob_to_mp4.py /Volumes/DVD/VIDEO_TS -o ~/Filmes/DVD01 --crf 20 --preset medium

# Apenas visualizar os comandos, sem executar
python3 convert_vob_to_mp4.py /Volumes/DVD/VIDEO_TS -o ~/Filmes/DVD01 --dry-run
```

## Observações

- O script recodifica para H.264/AAC por compatibilidade ampla. Se quiser apenas remux (sem recodificar), MPEG-2 em MP4 não é amplamente suportado.
- Para melhor qualidade com tamanho moderado, teste `--crf 18` ou `--crf 20` e `--preset slow`.
- DVDs costumam ser 480i/576i; usar `--deinterlace` geralmente melhora a aparência.

## Problemas comuns

- "ffmpeg não encontrado": instale com `brew install ffmpeg` e tente novamente.
- Erro de permissão em volumes externos: confirme permissões do diretório de origem e destino.
