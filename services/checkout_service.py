"""
Checkout Service - Handle checkout process
"""
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from storage.product_storage import ProductStorage
from storage.order_storage import OrderStorage
from services.inventory_service import InventoryService
from services.payment_service import PaymentService


class CheckoutService:
    """Checkout service for processing sales"""
    
    def __init__(self):
        """Initialize checkout service"""
        self.product_storage = ProductStorage()
        self.order_storage = OrderStorage()
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
        self.current_order: Optional[Order] = None
    
    def start_new_order(self) -> Order:
        """Start a new order"""
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"
        self.current_order = Order(order_id=order_id)
        return self.current_order
    
    def add_item(self, product_id: str, quantity: int = 1) -> Tuple[bool, str]:
        """
        Add item to current order
        Returns: (success, message)
        """
        if self.current_order is None:
            self.start_new_order()
        
        # Get product
        product = self.product_storage.get_by_id(product_id)
        if product is None:
            return False, f"Product not found: {product_id}"
        
        # Check stock
        if not self.inventory_service.check_stock(product_id, quantity):
            available = self.inventory_service.get_stock(product_id)
            return False, f"Insufficient stock. Available: {available}, Requested: {quantity}"
        
        # Check if item already exists in order
        for item in self.current_order.items:
            if item.product.product_id == product_id:
                # Update quantity
                new_quantity = item.quantity + quantity
                if not self.inventory_service.check_stock(product_id, new_quantity):
                    available = self.inventory_service.get_stock(product_id)
                    return False, f"Insufficient stock. Available: {available}, Requested: {new_quantity}"
                item.quantity = new_quantity
                self.current_order.calculate_total()
                return True, f"Updated quantity for {product.name}"
        
        # Add new item
        order_item = OrderItem(
            product=product,
            quantity=quantity,
            unit_price=product.price
        )
        self.current_order.items.append(order_item)
        self.current_order.calculate_total()
        return True, f"Added {product.name} x{quantity}"
    
    def remove_item(self, product_id: str) -> bool:
        """Remove item from current order"""
        if self.current_order is None:
            return False
        
        self.current_order.items = [
            item for item in self.current_order.items
            if item.product.product_id != product_id
        ]
        self.current_order.calculate_total()
        return True
    
    def update_item_quantity(self, product_id: str, quantity: int) -> Tuple[bool, str]:
        """
        Update item quantity in current order
        Returns: (success, message)
        """
        if self.current_order is None:
            return False, "No active order"
        
        if quantity <= 0:
            return self.remove_item(product_id), "Item removed"
        
        # Check stock
        if not self.inventory_service.check_stock(product_id, quantity):
            available = self.inventory_service.get_stock(product_id)
            return False, f"Insufficient stock. Available: {available}, Requested: {quantity}"
        
        # Update quantity
        for item in self.current_order.items:
            if item.product.product_id == product_id:
                item.quantity = quantity
                self.current_order.calculate_total()
                return True, "Quantity updated"
        
        return False, "Item not found in order"
    
    def get_current_total(self) -> float:
        """Get current order total"""
        if self.current_order is None:
            return 0.0
        return self.current_order.total_amount
    
    def process_payment(self, payment_method: str, paid_amount: float = None) -> Tuple[bool, str, dict]:
        """
        Process payment for current order
        Returns: (success, message, payment_info)
        """
        if self.current_order is None or len(self.current_order.items) == 0:
            return False, "No items in order", {}
        
        total = self.current_order.total_amount
        
        # Validate and process payment
        try:
            payment_info = self.payment_service.process_payment(
                payment_method, total, paid_amount
            )
        except ValueError as e:
            return False, str(e), {}
        
        # Update order
        self.current_order.payment_method = payment_info['method']
        self.current_order.payment_status = 'paid'
        
        # Reduce inventory
        for item in self.current_order.items:
            if not self.inventory_service.reduce_stock(item.product.product_id, item.quantity):
                # Rollback - this shouldn't happen if we checked earlier
                return False, f"Failed to reduce stock for {item.product.name}", {}
        
        # Save order
        if not self.order_storage.add(self.current_order):
            return False, "Failed to save order", {}
        
        order = self.current_order
        self.current_order = None
        
        return True, "Payment processed successfully", {
            'order': order,
            'payment': payment_info
        }
    
    def cancel_order(self):
        """Cancel current order"""
        self.current_order = None

