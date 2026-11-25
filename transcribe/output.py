"""Transcript writers: save segments as JSON or SRT subtitles.

The CLI prints text to the terminal by default; these writers let the
transcript feed something else instead — a JSON file for tooling, or an
SRT file for video players and subtitle workflows.
"""

import json


def format_srt_time(seconds):
    """Format seconds as HH:MM:SS,mmm (SRT timestamp)."""
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3600000)
    minutes, rem = divmod(rem, 60000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def segment_dict(segment):
    """One segment (with word timings) as a plain dict."""
    return {
        "start": segment.start,
        "end": segment.end,
        "text": segment.text.strip(),
        "words": [
            {"start": word.start, "end": word.end, "word": word.word}
            for word in segment.words
        ],
    }


def write_json(segments, info, path):
    """Write the full transcript (segments + language metadata) as JSON."""
    payload = {
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "segments": [segment_dict(segment) for segment in segments],
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_srt(segments, path):
    """Write segments as SRT subtitle blocks (1-based, blank-line separated)."""
    with open(path, "w", encoding="utf-8") as handle:
        for index, segment in enumerate(segments, start=1):
            handle.write(f"{index}\n")
            handle.write(
                f"{format_srt_time(segment.start)} --> "
                f"{format_srt_time(segment.end)}\n"
            )
            handle.write(f"{segment.text.strip()}\n\n")
