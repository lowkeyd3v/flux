"""
VoiceService interface.

Abstraction over speech-to-text (e.g. Whisper) and text-to-speech.
This is a P2 feature — only implemented once the core MVP (P0/P1) works.
"""

from abc import ABC, abstractmethod


class VoiceService(ABC):
    @abstractmethod
    def speech_to_text(self, audio_bytes: bytes, language: str = "hi") -> str:
        raise NotImplementedError

    @abstractmethod
    def text_to_speech(self, text: str, language: str = "hi") -> bytes:
        raise NotImplementedError


class NotImplementedVoiceService(VoiceService):
    def speech_to_text(self, audio_bytes: bytes, language: str = "hi") -> str:
        raise NotImplementedError(
            "Voice service is not implemented yet (planned: Milestone 7, P2)."
        )

    def text_to_speech(self, text: str, language: str = "hi") -> bytes:
        raise NotImplementedError(
            "Voice service is not implemented yet (planned: Milestone 7, P2)."
        )
