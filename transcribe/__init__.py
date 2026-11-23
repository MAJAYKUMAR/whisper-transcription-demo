"""A tiny command-line demo: transcribe one audio file with faster-whisper.

Layout:
- ``transcribe.config``  — defaults (model, device, output options)
- ``transcribe.service`` — thin wrapper around faster-whisper
- ``transcribe.cli``     — argument parsing, output formatting, entry point

Run it as ``python -m transcribe <audio>`` (or ``python transcribe.py <audio>``).
"""
