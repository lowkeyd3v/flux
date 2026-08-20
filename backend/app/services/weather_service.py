"""
WeatherService interface.

Abstraction over whichever weather API FLUX integrates with (P1 feature).
Kept separate so it can be swapped or mocked for testing without touching
the demand prediction / recommendation logic that consumes it.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


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


class NotImplementedWeatherService(WeatherService):
    def get_forecast(self, location: str, target_date: date) -> WeatherContext:
        raise NotImplementedError(
            "Weather service is not implemented yet (planned: Milestone 4)."
        )
