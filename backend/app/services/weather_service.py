"""
WeatherService interface + implementation.

Abstraction over whichever weather API FLUX integrates with (P1 feature,
Milestone 4). Kept separate so it can be swapped or mocked for testing
without touching the demand prediction / recommendation logic that
consumes it.

Concrete implementation uses OpenWeatherMap:
  - Current conditions: /data/2.5/weather
  - Future dates (tomorrow up to ~5 days out): /data/2.5/forecast
    (3-hour steps; we pick the slot closest to local noon on the target
    date and sum rainfall across that day's slots).

OpenWeatherMap's free tier only covers ~5 days out. For dates further in
the future we don't invent a forecast -- we raise a clear error so the
caller can fall back to asking the vendor for manual weather input
(the /predict and /recommend endpoints already support that).
"""

import logging
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone

import requests

from app.core.config import get_settings

logger = logging.getLogger(__name__)

OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5"
MAX_FORECAST_DAYS = 5  # OpenWeatherMap free-tier forecast horizon


@dataclass
class WeatherContext:
    location: str
    target_date: date
    temperature_celsius: float
    rainfall_mm: float
    condition: str  # e.g. "clear", "rain", "extreme_heat"


class WeatherService(ABC):
    @abstractmethod
    def get_forecast(self, location: str, target_date: date) -> WeatherContext:
        raise NotImplementedError


class WeatherServiceUnavailableError(RuntimeError):
    """Raised when a forecast genuinely can't be produced (API error, date
    too far out, location not found) so callers can degrade gracefully
    instead of getting a confusing stack trace."""


def _map_condition(owm_main: str, temperature_celsius: float) -> str:
    """
    Collapse OpenWeatherMap's ~50 condition codes down to the small set
    the demand model was trained on (see ml/preprocessing/features.py):
    clear, cloudy, rain, extreme_heat.
    """
    owm_main = (owm_main or "").lower()

    if temperature_celsius >= 40:
        return "extreme_heat"
    if owm_main in {"rain", "drizzle", "thunderstorm"}:
        return "rain"
    if owm_main in {"clouds", "mist", "fog", "haze", "smoke"}:
        return "cloudy"
    if owm_main == "clear":
        return "clear"
    return "cloudy"  # safe default for snow/dust/etc. in this domain


class OpenWeatherMapWeatherService(WeatherService):
    """Real implementation backed by the OpenWeatherMap API."""

    def __init__(self, api_key: str, session: requests.Session | None = None):
        self.api_key = api_key
        self.session = session or requests.Session()

    def get_forecast(self, location: str, target_date: date) -> WeatherContext:
        today = datetime.now(timezone.utc).date()
        days_out = (target_date - today).days

        if days_out < 0:
            raise WeatherServiceUnavailableError(
                f"Cannot forecast for a past date ({target_date})."
            )
        if days_out == 0:
            return self._current_weather(location, target_date)
        if days_out <= MAX_FORECAST_DAYS:
            return self._forecast_weather(location, target_date)

        raise WeatherServiceUnavailableError(
            f"{target_date} is {days_out} days out; OpenWeatherMap's free "
            f"forecast only covers {MAX_FORECAST_DAYS} days. Pass "
            "temperature_celsius/weather_condition manually for dates "
            "further out."
        )

    def _current_weather(self, location: str, target_date: date) -> WeatherContext:
        data = self._request("weather", location)
        temp = data["main"]["temp"]
        rain_mm = data.get("rain", {}).get("1h", 0.0)
        condition = _map_condition(data["weather"][0]["main"], temp)
        return WeatherContext(
            location=location,
            target_date=target_date,
            temperature_celsius=round(temp, 1),
            rainfall_mm=round(rain_mm, 1),
            condition=condition,
        )

    def _forecast_weather(self, location: str, target_date: date) -> WeatherContext:
        data = self._request("forecast", location)
        slots = [
            entry
            for entry in data.get("list", [])
            if datetime.fromtimestamp(entry["dt"], tz=timezone.utc).date() == target_date
        ]
        if not slots:
            raise WeatherServiceUnavailableError(
                f"No forecast slots returned for {location} on {target_date}."
            )

        # Prefer the slot nearest local noon (roughly peak footfall hours)
        # for temperature/condition; sum rainfall across the whole day.
        midday_slot = min(
            slots,
            key=lambda e: abs(
                datetime.fromtimestamp(e["dt"], tz=timezone.utc).hour - 12
            ),
        )
        temp = midday_slot["main"]["temp"]
        rain_mm = sum(s.get("rain", {}).get("3h", 0.0) for s in slots)
        conditions = Counter(s["weather"][0]["main"] for s in slots)
        dominant_condition = conditions.most_common(1)[0][0]
        condition = _map_condition(dominant_condition, temp)

        return WeatherContext(
            location=location,
            target_date=target_date,
            temperature_celsius=round(temp, 1),
            rainfall_mm=round(rain_mm, 1),
            condition=condition,
        )

    def _request(self, endpoint: str, location: str) -> dict:
        try:
            response = self.session.get(
                f"{OPENWEATHERMAP_BASE_URL}/{endpoint}",
                params={
                    "q": f"{location},IN",
                    "appid": self.api_key,
                    "units": "metric",
                },
                timeout=5,
            )
        except requests.RequestException as e:
            raise WeatherServiceUnavailableError(
                f"Could not reach the weather API: {e}"
            ) from e

        if response.status_code == 404:
            raise WeatherServiceUnavailableError(
                f"Weather API doesn't recognize location '{location}'."
            )
        if not response.ok:
            logger.warning(
                "OpenWeatherMap %s returned %s: %s",
                endpoint,
                response.status_code,
                response.text[:200],
            )
            raise WeatherServiceUnavailableError(
                f"Weather API error (status {response.status_code})."
            )

        return response.json()


class NotImplementedWeatherService(WeatherService):
    """
    Used when WEATHER_API_KEY isn't configured. Raises a clear error
    rather than crashing, mirroring NotImplementedDemandPredictionService.
    Callers (the /recommend endpoint) treat this as "no auto weather" and
    fall back to requiring the vendor to supply weather manually.
    """

    def get_forecast(self, location: str, target_date: date) -> WeatherContext:
        raise NotImplementedError(
            "Weather service is not configured (WEATHER_API_KEY is empty). "
            "Pass temperature_celsius/weather_condition manually instead."
        )


def get_weather_service() -> WeatherService:
    """Factory used as a FastAPI dependency."""
    settings = get_settings()
    if settings.WEATHER_API_KEY:
        return OpenWeatherMapWeatherService(api_key=settings.WEATHER_API_KEY)
    return NotImplementedWeatherService()
