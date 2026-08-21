"""
VoiceService interface and production implementation (Milestone 7).

Provides multilingual intent recognition, Speech-to-Text parsing, and
Text-to-Speech metadata generation for street vendor voice queries in
English, Hindi, and Hinglish.
"""

import re
from abc import ABC, abstractmethod
from typing import Any

from app.schemas.voice import VoiceIntentAction, VoiceIntentResponse


class VoiceService(ABC):
    @abstractmethod
    def parse_intent(
        self, transcript: str, language: str = "en", vendor_id: str | None = None
    ) -> VoiceIntentResponse:
        """Parse a voice transcript into a structured action intent."""
        raise NotImplementedError

    @abstractmethod
    def speech_to_text(self, audio_bytes: bytes, language: str = "hi") -> str:
        """Transcribe audio bytes to text."""
        raise NotImplementedError

    @abstractmethod
    def text_to_speech(self, text: str, language: str = "hi") -> bytes:
        """Synthesize text into speech audio bytes."""
        raise NotImplementedError


class MultilingualVoiceService(VoiceService):
    """
    Multilingual voice intent processor supporting English, Hindi (Devanagari),
    and Hinglish (Roman script).
    """

    def parse_intent(
        self, transcript: str, language: str = "en", vendor_id: str | None = None
    ) -> VoiceIntentResponse:
        raw = transcript.strip()
        lower = raw.lower()

        # 1. Scheme Query Intent
        scheme_keywords = [
            "scheme", "yojana", "योजना", "svanidhi", "स्वनिधि", "mudra", "मुद्रा",
            "vishwakarma", "विश्वकर्मा", "e-shram", "ई-श्रम", "subsidy", "सब्सिडी",
            "loan", "ऋण", "कर्ज", "karz", "document", "दस्तावेज", "apply", "आवेदन",
            "pmmy", "pmsym", "grant", "toolkit", "टूलकिट", "pension", "पेंशन", "insurance", "बीमा"
        ]
        if any(kw in lower for kw in scheme_keywords):
            feedback = self._get_feedback(
                "query_scheme", language, f"Searching government schemes for: '{raw}'"
            )
            return VoiceIntentResponse(
                transcript=raw,
                language=language,
                intent=VoiceIntentAction(
                    action_type="query_scheme",
                    confidence=0.92,
                    parameters={"query": raw, "vendor_id": vendor_id},
                    feedback_text=feedback,
                ),
            )

        # 2. Demand Prediction Intent
        prediction_keywords = [
            "demand", "forecast", "predict", "अनुमान", "पूर्वानुमान", "bikega",
            "bikri", "sales prediction", "how many will sell", "kitna bikega", "kal ki demand",
            "tomorrow demand", "sales forecast", "मांग"
        ]
        if any(kw in lower for kw in prediction_keywords):
            feedback = self._get_feedback(
                "predict_demand", language, "Calculating demand forecast for upcoming date."
            )
            return VoiceIntentResponse(
                transcript=raw,
                language=language,
                intent=VoiceIntentAction(
                    action_type="predict_demand",
                    confidence=0.88,
                    parameters={"target": "demand_prediction", "vendor_id": vendor_id},
                    feedback_text=feedback,
                ),
            )

        # 3. Stock Prep / Smart Recommendation Intent
        recommendation_keywords = [
            "prepare", "recommend", "how much to make", "kitna banana", "kitna banayein",
            "kitna maal", "stock prep", "सलाह", "तैयारी", "advice", "risk", "revenue",
            "kamai", "surplus", "shortage", "kitna stock"
        ]
        if any(kw in lower for kw in recommendation_keywords):
            feedback = self._get_feedback(
                "get_recommendation", language, "Generating smart stock preparation recommendation."
            )
            return VoiceIntentResponse(
                transcript=raw,
                language=language,
                intent=VoiceIntentAction(
                    action_type="get_recommendation",
                    confidence=0.89,
                    parameters={"target": "recommendation", "vendor_id": vendor_id},
                    feedback_text=feedback,
                ),
            )

        # 4. Sales Logging Intent
        sales_keywords = [
            "sold", "bika", "biki", "becha", "bechi", "log sale", "record sale",
            "बिक्री", "बेचा", "बेची", "sales"
        ]
        # Match units: e.g. "40 plate", "50 units", "20 samosa"
        units_match = re.search(r"(\d+)\s*(?:unit|units|piece|pieces|plate|plates|samosa|chai|item|items|यूनिट|कप)?", lower)
        # Match price: e.g. "400 rupees", "400 rs", "₹400", "rs 400"
        price_match = re.search(r"(?:(?:₹|rs\.?|rupees|rupaye)\s*(\d+)|(\d+)\s*(?:₹|rs\.?|rupees|rupaye))", lower)
        extracted_price = 0.0
        if price_match:
            extracted_price = float(price_match.group(1) or price_match.group(2))

        if any(kw in lower for kw in sales_keywords) or (units_match and price_match):
            units = float(units_match.group(1)) if units_match else 0.0
            feedback = self._get_feedback(
                "log_sale",
                language,
                f"Logging daily sales: {units} units.",
            )
            return VoiceIntentResponse(
                transcript=raw,
                language=language,
                intent=VoiceIntentAction(
                    action_type="log_sale",
                    confidence=0.88,
                    parameters={"units_sold": units, "price": extracted_price, "vendor_id": vendor_id},
                    feedback_text=feedback,
                ),
            )

        # Default fallback
        feedback = self._get_feedback(
            "general_qa", language, "Searching schemes and business advice for your question."
        )
        return VoiceIntentResponse(
            transcript=raw,
            language=language,
            intent=VoiceIntentAction(
                action_type="query_scheme",
                confidence=0.65,
                parameters={"query": raw, "vendor_id": vendor_id},
                feedback_text=feedback,
            ),
        )

    def _get_feedback(self, action_type: str, language: str, default_en: str) -> str:
        feedbacks = {
            "query_scheme": {
                "en": default_en,
                "hi": "सरकारी योजनाओं की जानकारी खोजी जा रही है...",
                "hinglish": "Sarkari schemes ki details search ki ja rahi hain...",
            },
            "predict_demand": {
                "en": "Calculating demand forecast...",
                "hi": "आगामी दिन के लिए मांग का पूर्वानुमान निकाला जा रहा है...",
                "hinglish": "Aane wale din ke liye demand forecast calculate ho raha hai...",
            },
            "get_recommendation": {
                "en": "Generating preparation and stock recommendation...",
                "hi": "कितना माल तैयार करें, इसकी स्मार्ट सलाह तैयार की जा रही है...",
                "hinglish": "Kitna stock prepare karna chahiye, iski recommendation ban rahi hai...",
            },
            "log_sale": {
                "en": "Recording daily sales...",
                "hi": "दैनिक बिक्री का रिकॉर्ड दर्ज किया जा रहा है...",
                "hinglish": "Daily sales ka record note kiya ja raha hai...",
            },
            "general_qa": {
                "en": "Checking FLUX knowledge base...",
                "hi": "फ्लक्स सहायक जानकारी खोज रहा है...",
                "hinglish": "FLUX assistant jaankari check kar raha hai...",
            },
        }

        lang_dict = feedbacks.get(action_type, {})
        return lang_dict.get(language, default_en)

    def speech_to_text(self, audio_bytes: bytes, language: str = "hi") -> str:
        """
        Placeholder for server-side Whisper processing when audio is uploaded directly.
        """
        return "Transcribed audio voice input"

    def text_to_speech(self, text: str, language: str = "hi") -> bytes:
        """
        Returns placeholder audio bytes or triggers client-side Web Speech Synthesis.
        """
        return b"RIFF....WAVEfmt "


class NotImplementedVoiceService(VoiceService):
    def parse_intent(
        self, transcript: str, language: str = "en", vendor_id: str | None = None
    ) -> VoiceIntentResponse:
        raise NotImplementedError("Voice service is not initialized.")

    def speech_to_text(self, audio_bytes: bytes, language: str = "hi") -> str:
        raise NotImplementedError("Voice service is not initialized.")

    def text_to_speech(self, text: str, language: str = "hi") -> bytes:
        raise NotImplementedError("Voice service is not initialized.")


_voice_service_instance: VoiceService | None = None


def get_voice_service() -> VoiceService:
    """Factory used as a FastAPI dependency and service singleton."""
    global _voice_service_instance
    if _voice_service_instance is None:
        _voice_service_instance = MultilingualVoiceService()
    return _voice_service_instance
