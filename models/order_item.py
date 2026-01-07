"""
Order Item Model
"""
from dataclasses import dataclass
from .product import Product


@dataclass
class OrderItem:
    """Order Item class"""
    product: Product  # Product
    quantity: int  # Quantity
    unit_price: float  # Unit price
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal"""
        return self.quantity * self.unit_price
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'product_id': self.product.product_id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }
    
    @classmethod
    def from_dict(cls, data: dict, product: Product) -> 'OrderItem':
        """Create OrderItem object from dictionary"""
        return cls(
            product=product,
            quantity=data['quantity'],
            unit_price=data['unit_price']
        )

