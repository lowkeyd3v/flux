"""
SalesRecord request/response schemas.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class SalesRecordBase(BaseModel):
    sale_date: date = Field(..., examples=["2026-08-15"])
    units_sold: float = Field(..., ge=0, examples=[45.0])
    price: float = Field(..., gt=0, examples=[10.0])
    is_holiday_or_event: bool = Field(default=False)
    weather_condition: str | None = Field(default=None, max_length=50, examples=["clear"])


class SalesRecordCreate(SalesRecordBase):
    """Payload for logging a single day's sales for a vendor."""
    pass


class SalesRecordBulkCreate(BaseModel):
    """Payload for uploading multiple historical sales records at once."""
    records: list[SalesRecordCreate] = Field(..., min_length=1)


class SalesRecordResponse(SalesRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vendor_id: uuid.UUID
    created_at: datetime
