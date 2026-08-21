"""
Vendor request/response schemas.

Kept separate from the ORM model (app/models/vendor.py) so API contracts
can evolve independently of the database schema.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["Ramesh Kumar"])
    product: str = Field(..., min_length=1, max_length=120, examples=["Samosa"])
    location: str = Field(..., min_length=1, max_length=120, examples=["Prayagraj"])
    selling_price: float = Field(..., gt=0, examples=[10.0])
    current_inventory: float = Field(default=0.0, ge=0, examples=[50.0])
    budget: float = Field(default=0.0, ge=0, examples=[2000.0])


class VendorCreate(VendorBase):
    """Payload for creating a new vendor profile."""
    pass


class VendorUpdate(BaseModel):
    """Payload for partially updating a vendor profile. All fields optional."""
    name: str | None = Field(default=None, min_length=1, max_length=120)
    product: str | None = Field(default=None, min_length=1, max_length=120)
    location: str | None = Field(default=None, min_length=1, max_length=120)
    selling_price: float | None = Field(default=None, gt=0)
    current_inventory: float | None = Field(default=None, ge=0)
    budget: float | None = Field(default=None, ge=0)


class VendorResponse(VendorBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
