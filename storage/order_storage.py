"""
Order Storage - JSON file storage for orders
"""
import json
import os
from typing import List, Optional
from models.order import Order
from models.product import Product
from storage.product_storage import ProductStorage


class OrderStorage:
    """Order storage using JSON file"""
    
    def __init__(self, file_path: str = "data/orders.json"):
        """Initialize order storage"""
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
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def load_all(self) -> List[Order]:
        """Load all orders from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Build products dictionary for order reconstruction
                products = self.product_storage.load_all()
                products_dict = {p.product_id: p for p in products}
                return [Order.from_dict(item, products_dict) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_all(self, orders: List[Order]):
        """Save all orders to file"""
        data = [order.to_dict() for order in orders]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        orders = self.load_all()
        for order in orders:
            if order.order_id == order_id:
                return order
        return None
    
    def add(self, order: Order) -> bool:
        """Add a new order"""
        orders = self.load_all()
        # Check if order ID already exists
        if any(o.order_id == order.order_id for o in orders):
            return False
        orders.append(order)
        self.save_all(orders)
        return True
    
    def update(self, order: Order) -> bool:
        """Update an existing order"""
        orders = self.load_all()
        for i, o in enumerate(orders):
            if o.order_id == order.order_id:
                orders[i] = order
                self.save_all(orders)
                return True
        return False

