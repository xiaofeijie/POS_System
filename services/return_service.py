"""
Return Service - Handle return process
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Tuple
from models.order import Order
from models.order_item import OrderItem
from storage.order_storage import OrderStorage
from services.inventory_service import InventoryService
from services.payment_service import PaymentService


class ReturnService:
    """Return service for processing returns"""
    
    def __init__(self):
        """Initialize return service"""
        self.order_storage = OrderStorage()
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
    
    def find_order(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        return self.order_storage.get_by_id(order_id)
    
    def get_returnable_items(self, order: Order) -> List[Dict]:
        """
        Get list of returnable items from order
        Returns list of items with return status
        """
        returnable = []
        for item in order.items:
            # Calculate how many can be returned
            # For simplicity, assume all items can be returned if order is not fully returned
            if order.status == 'returned':
                returnable_qty = 0
            elif order.status == 'partial_returned':
                # In a real system, we'd track which items were returned
                returnable_qty = item.quantity
            else:
                returnable_qty = item.quantity
            
            returnable.append({
                'item': item,
                'returnable_quantity': returnable_qty,
                'can_return': returnable_qty > 0
            })
        return returnable
    
    def process_return(self, order_id: str, return_items: Dict[str, int], reason: str = "") -> Tuple[bool, str, dict]:
        """
        Process return for an order
        return_items: {product_id: quantity_to_return}
        Returns: (success, message, return_info)
        """
        # Get order
        order = self.find_order(order_id)
        if order is None:
            return False, f"Order not found: {order_id}", {}
        
        if order.status == 'returned':
            return False, "Order has already been fully returned", {}
        
        # Validate return items
        return_amount = 0.0
        items_to_return = []
        
        for product_id, return_qty in return_items.items():
            if return_qty <= 0:
                continue
            
            # Find item in order
            order_item = None
            for item in order.items:
                if item.product.product_id == product_id:
                    order_item = item
                    break
            
            if order_item is None:
                return False, f"Product {product_id} not found in order", {}
            
            if return_qty > order_item.quantity:
                return False, f"Cannot return more than purchased for {order_item.product.name}", {}
            
            items_to_return.append({
                'item': order_item,
                'quantity': return_qty,
                'refund_amount': order_item.unit_price * return_qty
            })
            return_amount += order_item.unit_price * return_qty
        
        if len(items_to_return) == 0:
            return False, "No items to return", {}
        
        # Process return
        # Restore inventory
        for return_item in items_to_return:
            self.inventory_service.add_stock(
                return_item['item'].product.product_id,
                return_item['quantity']
            )
        
        # Update order status
        total_returned = sum(ri['quantity'] for ri in items_to_return)
        total_ordered = sum(item.quantity for item in order.items)
        
        if total_returned >= total_ordered:
            order.status = 'returned'
            order.payment_status = 'refunded'
        else:
            order.status = 'partial_returned'
        
        # Update order in storage
        self.order_storage.update(order)
        
        return_info = {
            'order_id': order_id,
            'return_amount': return_amount,
            'items': items_to_return,
            'reason': reason,
            'return_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return True, "Return processed successfully", return_info

