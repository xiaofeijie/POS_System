"""
Product Storage - SQLite database storage for products
"""
from typing import List, Optional
from models.product import Product
from database.db_connection import DatabaseConnection


class ProductStorage:
    """Product storage using SQLite database"""
    
    def __init__(self, db: DatabaseConnection = None):
        """Initialize product storage"""
        self.db = db or DatabaseConnection()
    
    def load_all(self) -> List[Product]:
        """Load all products from database"""
        rows = self.db.fetch_all("SELECT * FROM products")
        return [self._row_to_product(row) for row in rows]
    
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        row = self.db.fetch_one(
            "SELECT * FROM products WHERE product_id = ?",
            (product_id,)
        )
        return self._row_to_product(row) if row else None
    
    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        """Get product by barcode"""
        row = self.db.fetch_one(
            "SELECT * FROM products WHERE barcode = ?",
            (barcode,)
        )
        return self._row_to_product(row) if row else None
    
    def add(self, product: Product) -> bool:
        """Add a new product"""
        # Check if product already exists
        existing = self.get_by_id(product.product_id)
        if existing:
            return False
        
        self.db.execute(
            """INSERT INTO products (product_id, name, price, barcode, category)
               VALUES (?, ?, ?, ?, ?)""",
            (product.product_id, product.name, product.price,
             product.barcode, product.category)
        )
        return True
    
    def update(self, product: Product) -> bool:
        """Update an existing product"""
        existing = self.get_by_id(product.product_id)
        if not existing:
            return False
        
        self.db.execute(
            """UPDATE products 
               SET name = ?, price = ?, barcode = ?, category = ?
               WHERE product_id = ?""",
            (product.name, product.price, product.barcode,
             product.category, product.product_id)
        )
        return True
    
    def delete(self, product_id: str) -> bool:
        """Delete a product"""
        existing = self.get_by_id(product_id)
        if not existing:
            return False
        
        self.db.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        return True
    
    def save_all(self, products: List[Product]):
        """Save all products (useful for migration, but not efficient for large datasets)"""
        # Clear existing products
        self.db.execute("DELETE FROM products")
        # Insert all products
        if products:
            self.db.execute_many(
                """INSERT INTO products (product_id, name, price, barcode, category)
                   VALUES (?, ?, ?, ?, ?)""",
                [(p.product_id, p.name, p.price, p.barcode, p.category) for p in products]
            )
    
    def _row_to_product(self, row) -> Optional[Product]:
        """Convert database row to Product object"""
        if not row:
            return None
        return Product(
            product_id=row['product_id'],
            name=row['name'],
            price=row['price'],
            barcode=row['barcode'],
            category=row['category']
        )
