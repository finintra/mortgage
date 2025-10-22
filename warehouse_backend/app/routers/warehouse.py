"""
Warehouse operations endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends, Path
import logging

from app.models.warehouse import (
    OrderDetails, ScanProductRequest, ScanProductResponse,
    ConfirmOrderRequest, ConfirmOrderResponse,
    CancelOrderRequest, CancelOrderResponse
)
from app.services.odoo_client import get_odoo_client, OdooClient
from app.services.warehouse_service import WarehouseService
from app.dependencies.auth import get_current_active_user
from app.models.auth import TokenData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/warehouse", tags=["Warehouse"])


def get_warehouse_service(
    odoo: OdooClient = Depends(get_odoo_client)
) -> WarehouseService:
    """Dependency to get warehouse service"""
    return WarehouseService(odoo)


@router.get("/orders/{order_name}", response_model=OrderDetails)
async def get_order_by_name(
    order_name: str = Path(..., description="Order name like OUT/00123"),
    current_user: TokenData = Depends(get_current_active_user),
    warehouse: WarehouseService = Depends(get_warehouse_service)
):
    """
    Get order/picking details by name (invoice number)
    Example: OUT/00123
    """
    try:
        # Get picking by name
        picking = warehouse.get_picking_by_name(order_name)

        if not picking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_name} not found"
            )

        # Get full details
        order_details = warehouse.get_picking_details(picking["id"])

        if not order_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not load order details"
            )

        logger.info(f"User {current_user.username} loaded order {order_name}")

        return order_details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order {order_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading order"
        )


@router.get("/orders/id/{order_id}", response_model=OrderDetails)
async def get_order_by_id(
    order_id: int = Path(..., description="Order ID"),
    current_user: TokenData = Depends(get_current_active_user),
    warehouse: WarehouseService = Depends(get_warehouse_service)
):
    """
    Get order/picking details by ID
    """
    try:
        order_details = warehouse.get_picking_details(order_id)

        if not order_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order ID {order_id} not found"
            )

        logger.info(f"User {current_user.username} loaded order ID {order_id}")

        return order_details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading order"
        )


@router.post("/orders/{order_id}/scan", response_model=ScanProductResponse)
async def scan_product(
    order_id: int = Path(..., description="Order ID"),
    request: ScanProductRequest = None,
    current_user: TokenData = Depends(get_current_active_user),
    warehouse: WarehouseService = Depends(get_warehouse_service)
):
    """
    Scan product barcode for specific order
    Returns status: success, error_extra, error_not_in_order, line_completed
    """
    try:
        result = warehouse.scan_product(order_id, request.barcode)

        logger.info(
            f"User {current_user.username} scanned {request.barcode} "
            f"for order {order_id}: {result.status}"
        )

        return result

    except Exception as e:
        logger.error(f"Error scanning product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing scan"
        )


@router.post("/orders/{order_id}/confirm", response_model=ConfirmOrderResponse)
async def confirm_order(
    order_id: int = Path(..., description="Order ID"),
    current_user: TokenData = Depends(get_current_active_user),
    warehouse: WarehouseService = Depends(get_warehouse_service)
):
    """
    Confirm/validate order (picking)
    This marks the picking as done in Odoo
    """
    try:
        result = warehouse.confirm_picking(order_id)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        logger.info(f"User {current_user.username} confirmed order {order_id}")

        return ConfirmOrderResponse(
            success=result["success"],
            message=result["message"],
            tracking_number=result.get("tracking_number")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error confirming order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error confirming order"
        )


@router.post("/orders/{order_id}/cancel", response_model=CancelOrderResponse)
async def cancel_order(
    order_id: int = Path(..., description="Order ID"),
    request: CancelOrderRequest = None,
    current_user: TokenData = Depends(get_current_active_user),
    warehouse: WarehouseService = Depends(get_warehouse_service)
):
    """
    Cancel order picking
    Resets all quantities to 0 and cancels the picking
    """
    try:
        result = warehouse.cancel_picking(order_id, request.reason if request else None)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        logger.info(
            f"User {current_user.username} cancelled order {order_id}"
            f"{' - Reason: ' + request.reason if request and request.reason else ''}"
        )

        return CancelOrderResponse(
            success=result["success"],
            message=result["message"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error cancelling order"
        )
