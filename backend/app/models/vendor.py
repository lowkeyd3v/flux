"""
Vendor ORM model.

Represents a street vendor / micro-entrepreneur's business profile.
Kept intentionally simple for the hackathon MVP — no auth, no multi-user
ownership model. A vendor is identified by its own UUID primary key.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    product: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)

    # Business context used later by recommendation/demand services.
    selling_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_inventory: Mapped[float] = mapped_column(Float, default=0.0)
    budget: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    sales_records: Mapped[list["SalesRecord"]] = relationship(
        "SalesRecord", back_populates="vendor", cascade="all, delete-orphan"
    )
