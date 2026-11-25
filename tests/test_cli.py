"""Tests for the CLI: argument defaults, timestamp formatting, printed
output, and the missing-audio fail-fast check.

Runs with no faster-whisper install and no model download.
"""

from types import SimpleNamespace

import pytest

from transcribe import cli
from transcribe.cli import format_time, main, parse_args, print_result


def make_word(start, end, word):
    return SimpleNamespace(start=start, end=end, word=word)


def make_segment(start, end, text, words=()):
    return SimpleNamespace(start=start, end=end, text=text, words=list(words))


def make_info(language="en", language_probability=1.0, duration=33.6):
    return SimpleNamespace(
        language=language,
        language_probability=language_probability,
        duration=duration,
    )


class TestFormatTime:
    def test_zero(self):
        assert format_time(0) == "00:00.000"

    def test_seconds_with_millis(self):
        assert format_time(3.78) == "00:03.780"

    def test_minutes(self):
        assert format_time(65.5) == "01:05.500"

    def test_over_an_hour(self):
        assert format_time(3661.234) == "61:01.234"


class TestParseArgs:
    def test_defaults(self):
        args = parse_args(["some-audio.wav"])
        assert args.audio == "some-audio.wav"
        assert args.model == "tiny"
        assert args.language is None
        assert args.device == "cpu"

    def test_overrides(self):
        args = parse_args(
            ["clip.mp3", "--model", "base", "--language", "en", "--device", "cuda"]
        )
        assert args.model == "base"
        assert args.language == "en"
        assert args.device == "cuda"


class TestPrintResult:
    def test_segments_and_words(self, capsys):
        segments = [
            make_segment(
                0.0,
                3.78,
                "The birch can use lid.",
                words=[make_word(0.0, 0.7, "The"), make_word(0.7, 1.12, "birch")],
            ),
            make_segment(4.6, 6.6, "Glue the sheet.", words=[]),
        ]
        print_result(segments, make_info())
        out = capsys.readouterr().out
        assert "Detected language: en (probability 1.00)" in out
        assert "Audio duration: 33.6s" in out
        assert "[00:00.000 --> 00:03.780]  The birch can use lid." in out
        assert "00:00.000 - 00:00.700  The" in out
        assert "[00:04.600 --> 00:06.600]  Glue the sheet." in out

    def test_empty_segments(self, capsys):
        print_result([], make_info())
        out = capsys.readouterr().out
        assert "Detected language: en" in out
        assert "[00:" not in out


class TestMissingAudio:
    def test_missing_file_exits_before_model_load(self, monkeypatch, capsys):
        loaded = []

        class StubTranscriber:
            def __init__(self, *args, **kwargs):
                pass

            def load(self):
                loaded.append(True)

        monkeypatch.setattr(cli, "Transcriber", StubTranscriber)
        code = main(["does-not-exist.wav"])
        assert code == 2
        assert loaded == []
        err = capsys.readouterr().err
        assert "does-not-exist.wav" in err
