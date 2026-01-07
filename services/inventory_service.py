"""
Inventory Service - Handle inventory management
"""
from storage.inventory_storage import InventoryStorage
from typing import Optional


class InventoryService:
    """Inventory service for managing stock"""
    
    def __init__(self):
        """Initialize inventory service"""
        self.storage = InventoryStorage()
    
    def get_stock(self, product_id: str) -> int:
        """Get current stock for a product"""
        return self.storage.get_quantity(product_id)
    
    def check_stock(self, product_id: str, quantity: int) -> bool:
        """Check if there is enough stock"""
        return self.storage.has_stock(product_id, quantity)
    
    def reduce_stock(self, product_id: str, quantity: int) -> bool:
        """
        Reduce stock for a product
        Returns True if successful, False if insufficient stock
        """
        if not self.check_stock(product_id, quantity):
            return False
        return self.storage.reduce_quantity(product_id, quantity)
    
    def add_stock(self, product_id: str, quantity: int):
        """Add stock for a product (for returns)"""
        self.storage.add_quantity(product_id, quantity)
    
    def set_stock(self, product_id: str, quantity: int):
        """Set stock quantity for a product"""
        self.storage.set_quantity(product_id, quantity)

