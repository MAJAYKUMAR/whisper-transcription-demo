# whisper-transcription-demo

> **This is a small from-scratch demo built to show basic Whisper usage. It is not affiliated with and contains no code from any employer.**

A tiny command-line demo: give it one audio file, and it prints the transcript with segment timestamps and word-level timings, using [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (a fast reimplementation of OpenAI's Whisper). That's all it does — one small package, one audio file, one transcript.

## What it does

- Loads a Whisper model (`tiny` by default — small and fast, good enough for a demo)
- Transcribes a single audio file (wav, mp3, flac, ...)
- Prints each segment as `[start --> end]  text`, followed by per-word timings
- Auto-detects the spoken language unless you pass `--language`

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The first run downloads the `tiny` model (~75 MB) from Hugging Face and caches it in `~/.cache/huggingface`.

> **Note:** `requirements.txt` caps PyAV below 19 (`av>=11,<19`) because faster-whisper 1.2.1 calls `av.open(..., metadata_errors="ignore")`, which PyAV 19 removed. Without the cap, transcription fails with `TypeError: open() got an unexpected keyword argument 'metadata_errors'`.

## Get a sample

```bash
python scripts/get_sample.py
```

This downloads a short public speech sample (~34 s, ~0.5 MB, 8 kHz WAV) from the Open Speech Repository hosted at voiptroubleshooter.com:

https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav

It is saved to `samples/OSR_us_000_0010_8k.wav`. No audio files are committed to this repo — the script fetches the sample on demand.

## Run it

```bash
python -m transcribe samples/OSR_us_000_0010_8k.wav
python -m transcribe my-audio.mp3 --model base --language en
```

`python transcribe.py ...` still works too — it is a thin shim that hands off to the package.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The suite runs with no model download and no faster-whisper install: it covers argument defaults, timestamp formatting, printed output, and the missing-audio check — a missing file exits before the model is loaded.

## Example output

Example output from running the demo on the sample above with `--model tiny` (the tiny model mishears a word here and there — try `--model base` for a cleaner transcript):

```
Loading model 'tiny' on cpu ...
Transcribing samples/OSR_us_000_0010_8k.wav ...
Detected language: en (probability 1.00)
Audio duration: 33.6s

[00:00.000 --> 00:03.780]  The birch can use lid on the smooth planks.
    00:00.000 - 00:00.700   The
    00:00.700 - 00:01.120   birch
    00:01.120 - 00:01.380   can
    00:01.380 - 00:01.680   use
    00:01.680 - 00:01.960   lid
    00:01.960 - 00:02.240   on
    00:02.240 - 00:02.400   the
    00:02.400 - 00:02.700   smooth
    00:02.700 - 00:03.780   planks.

[00:04.600 --> 00:06.600]  Glue the sheet to the dark blue background.
    00:04.600 - 00:04.900   the
    00:04.900 - 00:05.060   sheet
    00:05.060 - 00:05.300   to
    00:05.300 - 00:05.440   the
    00:05.440 - 00:05.620   dark
    00:05.620 - 00:05.820   blue
    00:05.820 - 00:06.600   background.
```

## Files

| File | What it is |
| --- | --- |
| `transcribe/` | The demo, in three small modules: `cli.py` (arguments + output), `service.py` (the faster-whisper wrapper), `config.py` (defaults) |
| `transcribe.py` | Thin shim so `python transcribe.py ...` still works |
| `requirements.txt` | `faster-whisper` (+ a PyAV version cap, see note above) |
| `requirements-dev.txt` | Test-only dependencies (`pytest`) |
| `tests/` | pytest suite — runs with no model and no faster-whisper install |
| `scripts/get_sample.py` | Downloads the sample audio into `samples/` |
| `samples/` | Empty by default; the sample lands here when you fetch it |

## License

MIT — see [LICENSE](LICENSE).
