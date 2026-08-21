"""
Sales record API routes.

Sales records are always scoped to a vendor (nested resource), since a
sales history only makes sense in the context of one vendor's business.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vendor import Vendor
from app.models.sales_record import SalesRecord
from app.schemas.sales_record import (
    SalesRecordCreate,
    SalesRecordBulkCreate,
    SalesRecordResponse,
)

router = APIRouter(prefix="/vendors/{vendor_id}/sales", tags=["sales"])


def _get_vendor_or_404(vendor_id: uuid.UUID, db: Session) -> Vendor:
    vendor = db.get(Vendor, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.post("", response_model=SalesRecordResponse, status_code=status.HTTP_201_CREATED)
def create_sales_record(
    vendor_id: uuid.UUID, payload: SalesRecordCreate, db: Session = Depends(get_db)
):
    _get_vendor_or_404(vendor_id, db)
    record = SalesRecord(vendor_id=vendor_id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post(
    "/bulk", response_model=list[SalesRecordResponse], status_code=status.HTTP_201_CREATED
)
def bulk_create_sales_records(
    vendor_id: uuid.UUID, payload: SalesRecordBulkCreate, db: Session = Depends(get_db)
):
    """
    Insert multiple historical sales records at once — e.g. from a CSV
    upload of past sales data. Useful for seeding a vendor's history
    before demand forecasting (Milestone 3) needs it.
    """
    _get_vendor_or_404(vendor_id, db)
    records = [
        SalesRecord(vendor_id=vendor_id, **r.model_dump()) for r in payload.records
    ]
    db.add_all(records)
    db.commit()
    for r in records:
        db.refresh(r)
    return records


@router.get("", response_model=list[SalesRecordResponse])
def list_sales_records(vendor_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_vendor_or_404(vendor_id, db)
    return (
        db.query(SalesRecord)
        .filter(SalesRecord.vendor_id == vendor_id)
        .order_by(SalesRecord.sale_date.desc())
        .all()
    )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sales_record(
    vendor_id: uuid.UUID, record_id: uuid.UUID, db: Session = Depends(get_db)
):
    _get_vendor_or_404(vendor_id, db)
    record = db.get(SalesRecord, record_id)
    if record is None or record.vendor_id != vendor_id:
        raise HTTPException(status_code=404, detail="Sales record not found")
    db.delete(record)
    db.commit()
    return None
