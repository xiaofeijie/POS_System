"""
Inventory Storage - SQLite database storage for inventory
"""
from typing import Dict
from database.db_connection import DatabaseConnection
from storage.product_storage import ProductStorage


class InventoryStorage:
    """Inventory storage using SQLite database"""
    
    def __init__(self, db: DatabaseConnection = None):
        """Initialize inventory storage"""
        self.db = db or DatabaseConnection()
        self.product_storage = ProductStorage(self.db)
    
    def load_all(self) -> Dict[str, int]:
        """Load all inventory from database"""
        rows = self.db.fetch_all("SELECT product_id, quantity FROM inventory")
        return {row['product_id']: row['quantity'] for row in rows}
    
    def get_quantity(self, product_id: str) -> int:
        """Get inventory quantity for a product"""
        row = self.db.fetch_one(
            "SELECT quantity FROM inventory WHERE product_id = ?",
            (product_id,)
        )
        return row['quantity'] if row else 0
    
    def set_quantity(self, product_id: str, quantity: int):
        """Set inventory quantity for a product"""
        quantity = max(0, quantity)  # Ensure non-negative
        
        # Check if record exists
        existing = self.db.fetch_one(
            "SELECT product_id FROM inventory WHERE product_id = ?",
            (product_id,)
        )
        
        if existing:
            self.db.execute(
                "UPDATE inventory SET quantity = ? WHERE product_id = ?",
                (quantity, product_id)
            )
        else:
            self.db.execute(
                "INSERT INTO inventory (product_id, quantity) VALUES (?, ?)",
                (product_id, quantity)
            )
    
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
    
    def save_all(self, inventory: Dict[str, int]):
        """Save all inventory (useful for migration)"""
        # Clear existing inventory
        self.db.execute("DELETE FROM inventory")
        # Insert all inventory records
        if inventory:
            self.db.execute_many(
                "INSERT INTO inventory (product_id, quantity) VALUES (?, ?)",
                [(product_id, qty) for product_id, qty in inventory.items()]
            )
