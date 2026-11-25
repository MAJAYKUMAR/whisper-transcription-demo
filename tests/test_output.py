"""Tests for the transcript writers: JSON round-tripping and SRT output.

Runs with no faster-whisper install and no model download.
"""

import json

from transcribe.output import format_srt_time, write_json, write_srt
from tests.test_cli import make_info, make_segment, make_word


def sample_segments():
    return [
        make_segment(
            0.0,
            3.78,
            "The birch can use lid.",
            words=[make_word(0.0, 0.7, "The"), make_word(0.7, 1.12, "birch")],
        ),
        make_segment(4.6, 6.6, "Glue the sheet.", words=[]),
    ]


class TestFormatSrtTime:
    def test_zero(self):
        assert format_srt_time(0) == "00:00:00,000"

    def test_seconds_and_millis(self):
        assert format_srt_time(3.78) == "00:00:03,780"

    def test_minutes_and_hours(self):
        assert format_srt_time(3661.234) == "01:01:01,234"

    def test_rounds_to_nearest_millisecond(self):
        assert format_srt_time(1.2345) == "00:00:01,234"


class TestWriteJson:
    def test_round_trips_segments_and_metadata(self, tmp_path):
        out = tmp_path / "out.json"
        write_json(sample_segments(), make_info(), str(out))
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["language"] == "en"
        assert payload["language_probability"] == 1.0
        assert payload["duration"] == 33.6
        assert len(payload["segments"]) == 2
        first = payload["segments"][0]
        assert first["start"] == 0.0
        assert first["end"] == 3.78
        assert first["text"] == "The birch can use lid."
        assert first["words"] == [
            {"start": 0.0, "end": 0.7, "word": "The"},
            {"start": 0.7, "end": 1.12, "word": "birch"},
        ]
        assert payload["segments"][1]["words"] == []

    def test_empty_segments(self, tmp_path):
        out = tmp_path / "out.json"
        write_json([], make_info(), str(out))
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["segments"] == []


class TestWriteSrt:
    def test_blocks_numbered_with_timestamps(self, tmp_path):
        out = tmp_path / "out.srt"
        write_srt(sample_segments(), str(out))
        text = out.read_text(encoding="utf-8")
        assert text == (
            "1\n"
            "00:00:00,000 --> 00:00:03,780\n"
            "The birch can use lid.\n"
            "\n"
            "2\n"
            "00:00:04,600 --> 00:00:06,600\n"
            "Glue the sheet.\n"
            "\n"
        )

    def test_empty_segments_writes_empty_file(self, tmp_path):
        out = tmp_path / "out.srt"
        write_srt([], str(out))
        assert out.read_text(encoding="utf-8") == ""
