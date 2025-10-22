"""
Warehouse operation models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ScanProductRequest(BaseModel):
    """Scan product request"""
    barcode: str = Field(..., min_length=1, max_length=100)


class ScanProductResponse(BaseModel):
    """Scan product response"""
    status: str  # success, error_extra, error_not_in_order, line_completed
    message: Optional[str] = None
    scanned_count: int
    remaining_count: int
    total_count: int
    order_completed: bool = False


class OrderLine(BaseModel):
    """Order line details"""
    id: int
    product_id: int
    product_name: str
    product_code: Optional[str] = None
    barcode: Optional[str] = None
    quantity_ordered: float
    quantity_done: float
    quantity_remaining: float
    unit_of_measure: str


class OrderDetails(BaseModel):
    """Order/Picking details"""
    id: int
    name: str  # OUT/00123
    partner_name: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    state: str  # draft, waiting, confirmed, assigned, done, cancel
    origin: Optional[str] = None  # sale order reference
    lines: List[OrderLine]
    total_lines: int
    completed_lines: int
    scanned_count: int
    total_count: int
    remaining_count: int


class ConfirmOrderRequest(BaseModel):
    """Confirm order request"""
    order_id: int


class ConfirmOrderResponse(BaseModel):
    """Confirm order response"""
    success: bool
    message: str
    tracking_number: Optional[str] = None


class CancelOrderRequest(BaseModel):
    """Cancel order request"""
    order_id: int
    reason: Optional[str] = None


class CancelOrderResponse(BaseModel):
    """Cancel order response"""
    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Generic error response"""
    detail: str
    code: Optional[str] = None
