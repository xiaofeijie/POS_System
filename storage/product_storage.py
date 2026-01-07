"""
Product Storage - JSON file storage for products
"""
import json
import os
from typing import List, Optional
from models.product import Product


class ProductStorage:
    """Product storage using JSON file"""
    
    def __init__(self, file_path: str = "data/products.json"):
        """Initialize product storage"""
        self.file_path = file_path
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
    
    def load_all(self) -> List[Product]:
        """Load all products from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Product.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_all(self, products: List[Product]):
        """Save all products to file"""
        data = [product.to_dict() for product in products]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        products = self.load_all()
        for product in products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        """Get product by barcode"""
        products = self.load_all()
        for product in products:
            if product.barcode == barcode:
                return product
        return None
    
    def add(self, product: Product) -> bool:
        """Add a new product"""
        products = self.load_all()
        # Check if product ID already exists
        if any(p.product_id == product.product_id for p in products):
            return False
        products.append(product)
        self.save_all(products)
        return True
    
    def update(self, product: Product) -> bool:
        """Update an existing product"""
        products = self.load_all()
        for i, p in enumerate(products):
            if p.product_id == product.product_id:
                products[i] = product
                self.save_all(products)
                return True
        return False
    
    def delete(self, product_id: str) -> bool:
        """Delete a product"""
        products = self.load_all()
        products = [p for p in products if p.product_id != product_id]
        if len(products) < len(self.load_all()):
            self.save_all(products)
            return True
        return False

