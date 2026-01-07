"""
Product Model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """Product class"""
    product_id: str  # Product ID
    name: str  # Product name
    price: float  # Product price
    barcode: Optional[str] = None  # Barcode (optional)
    category: Optional[str] = None  # Product category (optional)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'barcode': self.barcode,
            'category': self.category
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create Product object from dictionary"""
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            price=data['price'],
            barcode=data.get('barcode'),
            category=data.get('category')
        )

