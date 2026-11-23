"""Transcription service: a thin wrapper around faster-whisper.

Kept deliberately small: load a model once, transcribe one audio file,
return the segments and the language/duration info faster-whisper reports.
No batching, no pipeline, no server — just the model call.
"""


class Transcriber:
    """Loads a Whisper model once and transcribes audio files with it."""

    def __init__(self, model_name, device, compute_type):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model = None

    def load(self):
        # Imported lazily so importing this module (and `python -m py_compile`)
        # works without faster-whisper installed.
        from faster_whisper import WhisperModel

        self._model = WhisperModel(
            self.model_name, device=self.device, compute_type=self.compute_type
        )

    def transcribe(self, audio_path, language=None, word_timestamps=True):
        """Transcribe one audio file; returns (segments, info)."""
        if self._model is None:
            self.load()
        segments, info = self._model.transcribe(
            audio_path, language=language, word_timestamps=word_timestamps
        )
        return segments, info
