"""
Warehouse operations service
"""
import logging
from typing import Optional, Dict, List
from datetime import datetime

from app.services.odoo_client import OdooClient
from app.models.warehouse import OrderDetails, OrderLine, ScanProductResponse

logger = logging.getLogger(__name__)


class WarehouseService:
    """Service for warehouse operations"""

    def __init__(self, odoo_client: OdooClient):
        self.odoo = odoo_client

    def get_picking_by_name(self, picking_name: str) -> Optional[Dict]:
        """
        Get picking/delivery order by name (e.g., OUT/00123)
        """
        try:
            pickings = self.odoo.search_read(
                "stock.picking",
                [("name", "=", picking_name)],
                fields=[
                    "id", "name", "partner_id", "scheduled_date",
                    "state", "origin", "picking_type_id", "move_ids_without_package"
                ],
                limit=1
            )
            return pickings[0] if pickings else None
        except Exception as e:
            logger.error(f"Error getting picking {picking_name}: {e}")
            return None

    def get_picking_details(self, picking_id: int) -> Optional[OrderDetails]:
        """
        Get detailed picking information with move lines
        """
        try:
            # Get picking
            pickings = self.odoo.read("stock.picking", [picking_id], [
                "name", "partner_id", "scheduled_date", "state", "origin", "move_ids_without_package"
            ])

            if not pickings:
                return None

            picking = pickings[0]

            # Get move lines (stock.move)
            move_ids = picking.get("move_ids_without_package", [])
            if not move_ids:
                return None

            moves = self.odoo.read("stock.move", move_ids, [
                "product_id", "product_uom_qty", "quantity_done", "product_uom", "move_line_ids"
            ])

            # Build order lines
            lines = []
            total_count = 0
            scanned_count = 0
            completed_lines = 0

            for move in moves:
                product_id = move["product_id"][0] if isinstance(move["product_id"], list) else move["product_id"]

                # Get product details including barcode
                products = self.odoo.read("product.product", [product_id], ["name", "default_code", "barcode"])
                product = products[0] if products else {}

                qty_ordered = move.get("product_uom_qty", 0)
                qty_done = move.get("quantity_done", 0)
                qty_remaining = qty_ordered - qty_done

                line = OrderLine(
                    id=move["id"],
                    product_id=product_id,
                    product_name=product.get("name", "Unknown Product"),
                    product_code=product.get("default_code"),
                    barcode=product.get("barcode"),
                    quantity_ordered=qty_ordered,
                    quantity_done=qty_done,
                    quantity_remaining=qty_remaining,
                    unit_of_measure=move["product_uom"][1] if isinstance(move["product_uom"], list) else "Units"
                )
                lines.append(line)

                total_count += int(qty_ordered)
                scanned_count += int(qty_done)
                if qty_remaining == 0:
                    completed_lines += 1

            partner_name = picking["partner_id"][1] if isinstance(picking["partner_id"], list) else None

            return OrderDetails(
                id=picking["id"],
                name=picking["name"],
                partner_name=partner_name,
                scheduled_date=picking.get("scheduled_date"),
                state=picking["state"],
                origin=picking.get("origin"),
                lines=lines,
                total_lines=len(lines),
                completed_lines=completed_lines,
                scanned_count=scanned_count,
                total_count=total_count,
                remaining_count=total_count - scanned_count
            )

        except Exception as e:
            logger.error(f"Error getting picking details {picking_id}: {e}")
            return None

    def scan_product(self, picking_id: int, barcode: str) -> ScanProductResponse:
        """
        Process product scan
        """
        try:
            # Get picking details
            order = self.get_picking_details(picking_id)
            if not order:
                return ScanProductResponse(
                    status="error",
                    message="Order not found",
                    scanned_count=0,
                    remaining_count=0,
                    total_count=0,
                    order_completed=False
                )

            # Find product by barcode
            matching_line = None
            for line in order.lines:
                if line.barcode == barcode or line.product_code == barcode:
                    if line.quantity_remaining > 0:
                        matching_line = line
                        break

            # Check if product not in order
            if not any(line.barcode == barcode or line.product_code == barcode for line in order.lines):
                return ScanProductResponse(
                    status="error_not_in_order",
                    message="Product not in this order",
                    scanned_count=order.scanned_count,
                    remaining_count=order.remaining_count,
                    total_count=order.total_count,
                    order_completed=False
                )

            # Check if product is extra (already completed)
            if not matching_line:
                return ScanProductResponse(
                    status="error_extra",
                    message="This product line is already completed",
                    scanned_count=order.scanned_count,
                    remaining_count=order.remaining_count,
                    total_count=order.total_count,
                    order_completed=False
                )

            # Update quantity_done in Odoo
            new_qty_done = matching_line.quantity_done + 1
            self.odoo.write("stock.move", [matching_line.id], {
                "quantity_done": new_qty_done
            })

            # Check if line completed
            line_completed = new_qty_done >= matching_line.quantity_ordered

            # Recalculate counts
            new_scanned = order.scanned_count + 1
            new_remaining = order.remaining_count - 1
            order_completed = new_remaining == 0

            status = "line_completed" if line_completed else "success"

            return ScanProductResponse(
                status=status,
                message="Product scanned successfully",
                scanned_count=new_scanned,
                remaining_count=new_remaining,
                total_count=order.total_count,
                order_completed=order_completed
            )

        except Exception as e:
            logger.error(f"Error scanning product: {e}")
            return ScanProductResponse(
                status="error",
                message=str(e),
                scanned_count=0,
                remaining_count=0,
                total_count=0,
                order_completed=False
            )

    def confirm_picking(self, picking_id: int) -> Dict:
        """
        Confirm/validate picking
        """
        try:
            # Validate the picking (button_validate in Odoo)
            result = self.odoo.execute("stock.picking", "button_validate", [picking_id])

            # Check if picking is now done
            pickings = self.odoo.read("stock.picking", [picking_id], ["state", "name"])
            picking = pickings[0] if pickings else {}

            return {
                "success": True,
                "message": "Order confirmed successfully",
                "tracking_number": picking.get("name"),
                "state": picking.get("state")
            }

        except Exception as e:
            logger.error(f"Error confirming picking {picking_id}: {e}")
            return {
                "success": False,
                "message": str(e),
                "tracking_number": None
            }

    def cancel_picking(self, picking_id: int, reason: Optional[str] = None) -> Dict:
        """
        Cancel picking
        """
        try:
            # Reset quantities to 0
            picking = self.odoo.read("stock.picking", [picking_id], ["move_ids_without_package"])[0]
            move_ids = picking.get("move_ids_without_package", [])

            for move_id in move_ids:
                self.odoo.write("stock.move", [move_id], {"quantity_done": 0})

            # Cancel the picking
            self.odoo.execute("stock.picking", "action_cancel", [picking_id])

            return {
                "success": True,
                "message": "Order cancelled successfully"
            }

        except Exception as e:
            logger.error(f"Error cancelling picking {picking_id}: {e}")
            return {
                "success": False,
                "message": str(e)
            }
