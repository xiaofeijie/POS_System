"""
Order Storage - SQLite database storage for orders
"""
from typing import List, Optional
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from database.db_connection import DatabaseConnection
from storage.product_storage import ProductStorage


class OrderStorage:
    """Order storage using SQLite database"""
    
    def __init__(self, db: DatabaseConnection = None):
        """Initialize order storage"""
        self.db = db or DatabaseConnection()
        self.product_storage = ProductStorage(self.db)
    
    def load_all(self) -> List[Order]:
        """Load all orders from database"""
        orders = []
        order_rows = self.db.fetch_all("SELECT * FROM orders ORDER BY created_at DESC")
        
        for order_row in order_rows:
            order = self._load_order_with_items(order_row['order_id'])
            if order:
                orders.append(order)
        
        return orders
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        order_row = self.db.fetch_one(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id,)
        )
        if not order_row:
            return None
        
        return self._load_order_with_items(order_id)
    
    def _load_order_with_items(self, order_id: str) -> Optional[Order]:
        """Load order with its items"""
        order_row = self.db.fetch_one(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id,)
        )
        if not order_row:
            return None
        
        # Load order items
        item_rows = self.db.fetch_all(
            "SELECT * FROM order_items WHERE order_id = ?",
            (order_id,)
        )
        
        items = []
        for item_row in item_rows:
            product = self.product_storage.get_by_id(item_row['product_id'])
            if product:
                item = OrderItem(
                    product=product,
                    quantity=item_row['quantity'],
                    unit_price=item_row['unit_price']
                )
                items.append(item)
        
        order = Order(
            order_id=order_row['order_id'],
            items=items,
            total_amount=order_row['total_amount'],
            payment_method=order_row['payment_method'],
            payment_status=order_row['payment_status'],
            created_at=order_row['created_at'],
            status=order_row['status']
        )
        return order
    
    def add(self, order: Order) -> bool:
        """Add a new order"""
        # Check if order already exists
        existing = self.get_by_id(order.order_id)
        if existing:
            return False
        
        # Insert order
        self.db.execute(
            """INSERT INTO orders (order_id, total_amount, payment_method, 
               payment_status, created_at, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (order.order_id, order.total_amount, order.payment_method,
             order.payment_status, order.created_at, order.status)
        )
        
        # Insert order items
        if order.items:
            self.db.execute_many(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                   VALUES (?, ?, ?, ?)""",
                [(order.order_id, item.product.product_id, item.quantity, item.unit_price)
                 for item in order.items]
            )
        
        return True
    
    def update(self, order: Order) -> bool:
        """Update an existing order"""
        existing = self.get_by_id(order.order_id)
        if not existing:
            return False
        
        # Update order
        self.db.execute(
            """UPDATE orders 
               SET total_amount = ?, payment_method = ?, payment_status = ?, status = ?
               WHERE order_id = ?""",
            (order.total_amount, order.payment_method,
             order.payment_status, order.status, order.order_id)
        )
        
        # Delete existing items and insert new ones
        self.db.execute("DELETE FROM order_items WHERE order_id = ?", (order.order_id,))
        
        if order.items:
            self.db.execute_many(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                   VALUES (?, ?, ?, ?)""",
                [(order.order_id, item.product.product_id, item.quantity, item.unit_price)
                 for item in order.items]
            )
        
        return True
    
    def save_all(self, orders: List[Order]):
        """Save all orders (useful for migration)"""
        # Clear existing orders
        self.db.execute("DELETE FROM order_items")
        self.db.execute("DELETE FROM orders")
        # Insert all orders
        for order in orders:
            self.add(order)
