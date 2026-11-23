#!/usr/bin/env python3
"""Command-line entry point for the whisper-transcription-demo.

Parses arguments, drives the transcription service, and prints each
segment with start/end timestamps plus word-level timings.

Usage:
    python -m transcribe samples/OSR_us_000_0010_8k.wav
    python -m transcribe my-audio.mp3 --model base --language en
"""

import argparse
import sys

from . import config
from .service import Transcriber


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Transcribe one audio file with faster-whisper."
    )
    parser.add_argument("audio", help="Path to an audio file (wav, mp3, flac, ...)")
    parser.add_argument(
        "--model",
        default=config.DEFAULT_MODEL,
        help='Whisper model size, e.g. "tiny", "base", "small" (default: tiny)',
    )
    parser.add_argument(
        "--language",
        default=None,
        help='Spoken language code, e.g. "en" (default: auto-detect)',
    )
    parser.add_argument(
        "--device",
        default=config.DEFAULT_DEVICE,
        help='Device to run on: "cpu" or "cuda" (default: cpu)',
    )
    return parser.parse_args(argv)


def format_time(seconds):
    """Format seconds as mm:ss.mmm."""
    minutes, secs = divmod(seconds, 60)
    return f"{int(minutes):02d}:{secs:06.3f}"


def print_result(segments, info):
    """Print detected language, duration, segments and word timings."""
    print(f"Detected language: {info.language} "
          f"(probability {info.language_probability:.2f})")
    print(f"Audio duration: {info.duration:.1f}s\n")

    for segment in segments:
        start = format_time(segment.start)
        end = format_time(segment.end)
        print(f"[{start} --> {end}]  {segment.text.strip()}")
        for word in segment.words:
            w_start = format_time(word.start)
            w_end = format_time(word.end)
            print(f"    {w_start} - {w_end}  {word.word}")
        print()


def main(argv=None):
    args = parse_args(argv)

    transcriber = Transcriber(
        args.model, args.device, config.DEFAULT_COMPUTE_TYPE
    )

    print(f"Loading model {args.model!r} on {args.device} ...")
    try:
        transcriber.load()
    except ImportError:
        print(
            "faster-whisper is not installed. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    print(f"Transcribing {args.audio} ...")
    segments, info = transcriber.transcribe(
        args.audio,
        language=args.language,
        word_timestamps=config.WORD_TIMESTAMPS,
    )
    print_result(segments, info)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
