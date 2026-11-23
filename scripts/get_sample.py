#!/usr/bin/env python3
"""Download a small public speech sample so the demo can be run immediately.

Source: the Open Speech Repository sample hosted at voiptroubleshooter.com,
a short (~34 s, ~0.5 MB) 8 kHz WAV of a single speaker reading ten
Harvard sentences.
Saved to samples/OSR_us_000_0010_8k.wav (skipped if already present).

Usage:
    python scripts/get_sample.py
"""

import os
import urllib.request

SAMPLE_URL = (
    "https://www.voiptroubleshooter.com/open_speech/american/"
    "OSR_us_000_0010_8k.wav"
)
SAMPLE_NAME = "OSR_us_000_0010_8k.wav"


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    samples_dir = os.path.join(here, "samples")
    os.makedirs(samples_dir, exist_ok=True)
    dest = os.path.join(samples_dir, SAMPLE_NAME)

    if os.path.exists(dest):
        print(f"Already present: {dest}")
        return 0

    print(f"Downloading {SAMPLE_URL} ...")
    # The host returns HTTP 406 for short/generic user-agents, so send a
    # full browser-style user-agent plus an Accept header.
    request = urllib.request.Request(
        SAMPLE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            ),
            "Accept": "audio/wav,audio/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request) as response, open(dest, "wb") as out:
        out.write(response.read())
    size_kb = os.path.getsize(dest) / 1024
    print(f"Saved {dest} ({size_kb:.0f} KB)")
    print("Run it with: python transcribe.py samples/" + SAMPLE_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
