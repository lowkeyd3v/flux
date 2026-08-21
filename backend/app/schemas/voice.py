"""
Pydantic schemas for Voice Assistant and Multilingual Services (Milestone 7).
"""

from typing import Any
from pydantic import BaseModel, Field


class VoiceIntentRequest(BaseModel):
    transcript: str = Field(..., min_length=1, description="Voice utterance or transcribed command text")
    language: str = Field(default="en", description="Language of the transcript: 'en', 'hi', or 'hinglish'")
    vendor_id: str | None = Field(default=None, description="Optional active vendor ID for contextual execution")


class VoiceIntentAction(BaseModel):
    action_type: str  # "query_scheme" | "predict_demand" | "get_recommendation" | "log_sale" | "general_qa" | "unknown"
    confidence: float
    parameters: dict[str, Any] = Field(default_factory=dict)
    feedback_text: str  # Plain-language confirmation message in the user's language


class VoiceIntentResponse(BaseModel):
    transcript: str
    language: str
    intent: VoiceIntentAction


class SupportedLanguagesResponse(BaseModel):
    supported_languages: list[dict[str, str]]
    voice_models: list[dict[str, str]]
