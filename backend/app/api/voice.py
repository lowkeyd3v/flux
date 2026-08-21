"""
Voice & Multilingual API routes (Milestone 7).

Endpoints for parsing spoken vendor voice commands into structured actions
and querying supported voice/language capabilities.
"""

from fastapi import APIRouter, Depends

from app.schemas.voice import (
    SupportedLanguagesResponse,
    VoiceIntentRequest,
    VoiceIntentResponse,
)
from app.services.voice_service import VoiceService, get_voice_service

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/parse-intent", response_model=VoiceIntentResponse)
def parse_voice_intent(
    payload: VoiceIntentRequest,
    voice_service: VoiceService = Depends(get_voice_service),
):
    """
    Parse a voice transcript into an actionable intent (Scheme search, demand forecast,
    smart recommendation, sales logging) across English, Hindi, and Hinglish.
    """
    return voice_service.parse_intent(
        transcript=payload.transcript,
        language=payload.language,
        vendor_id=payload.vendor_id,
    )


@router.get("/supported-languages", response_model=SupportedLanguagesResponse)
def get_supported_languages():
    """
    Get the list of supported languages, scripts, and voice synthesizer models.
    """
    return SupportedLanguagesResponse(
        supported_languages=[
            {"code": "en", "name": "English", "script": "Latin", "speech_tag": "en-IN"},
            {"code": "hi", "name": "हिंदी (Hindi)", "script": "Devanagari", "speech_tag": "hi-IN"},
            {"code": "hinglish", "name": "Hinglish", "script": "Latin (Colloquial Hindi)", "speech_tag": "hi-IN"},
        ],
        voice_models=[
            {"id": "web-speech-native", "type": "client_side", "description": "High-speed zero-latency browser Web Speech API"},
            {"id": "whisper-compatible", "type": "server_side", "description": "OpenAI Whisper multilingual transcription interface"},
        ],
    )
