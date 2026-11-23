"""Configuration defaults for the demo.

One place for the knobs the CLI exposes: which model to load, which
device to run on, and how transcription output is produced.
"""

# Whisper model size, e.g. "tiny", "base", "small". Tiny is small and fast,
# good enough for a demo.
DEFAULT_MODEL = "tiny"

# Device to run on: "cpu" or "cuda".
DEFAULT_DEVICE = "cpu"

# Compute type passed to faster-whisper. int8 keeps the tiny model light
# on CPU.
DEFAULT_COMPUTE_TYPE = "int8"

# Ask faster-whisper for per-word start/end times alongside each segment.
WORD_TIMESTAMPS = True
