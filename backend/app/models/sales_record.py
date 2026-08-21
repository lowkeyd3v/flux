"""
SalesRecord ORM model.

Represents a single day's historical sales entry for a vendor. This is
the data the demand-forecasting model (Milestone 3) will train and infer
on, so the schema favors fields that are realistic forecasting features.
"""

import uuid
from datetime import datetime, date, timezone

from sqlalchemy import String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class SalesRecord(Base):
    __tablename__ = "sales_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    vendor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False
    )

    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    units_sold: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional context fields — useful demand-forecasting features later.
    is_holiday_or_event: Mapped[bool] = mapped_column(Boolean, default=False)
    weather_condition: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="sales_records")
