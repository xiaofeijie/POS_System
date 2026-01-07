"""
Inventory Storage - JSON file storage for inventory
"""
import json
import os
from typing import Dict
from storage.product_storage import ProductStorage


class InventoryStorage:
    """Inventory storage using JSON file"""
    
    def __init__(self, file_path: str = "data/inventory.json"):
        """Initialize inventory storage"""
        self.file_path = file_path
        self.product_storage = ProductStorage()
        self._ensure_data_dir()
        self._ensure_file()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def _ensure_file(self):
        """Ensure JSON file exists"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def load_all(self) -> Dict[str, int]:
        """Load all inventory from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_all(self, inventory: Dict[str, int]):
        """Save all inventory to file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, ensure_ascii=False, indent=2)
    
    def get_quantity(self, product_id: str) -> int:
        """Get inventory quantity for a product"""
        inventory = self.load_all()
        return inventory.get(product_id, 0)
    
    def set_quantity(self, product_id: str, quantity: int):
        """Set inventory quantity for a product"""
        inventory = self.load_all()
        inventory[product_id] = max(0, quantity)  # Ensure non-negative
        self.save_all(inventory)
    
    def add_quantity(self, product_id: str, quantity: int):
        """Add quantity to inventory"""
        current = self.get_quantity(product_id)
        self.set_quantity(product_id, current + quantity)
    
    def reduce_quantity(self, product_id: str, quantity: int) -> bool:
        """Reduce quantity from inventory, returns True if successful"""
        current = self.get_quantity(product_id)
        if current >= quantity:
            self.set_quantity(product_id, current - quantity)
            return True
        return False
    
    def has_stock(self, product_id: str, quantity: int) -> bool:
        """Check if there is enough stock"""
        return self.get_quantity(product_id) >= quantity

