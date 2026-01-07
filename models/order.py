"""
Order Model
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from .order_item import OrderItem


@dataclass
class Order:
    """Order class"""
    order_id: str  # Order ID
    items: List[OrderItem] = field(default_factory=list)  # Order items
    total_amount: float = 0.0  # Total amount
    payment_method: str = ""  # Payment method (cash, card, etc.)
    payment_status: str = "pending"  # Payment status (pending, paid, refunded)
    created_at: str = ""  # Creation time
    status: str = "completed"  # Order status (completed, returned, partial_returned)
    
    def __post_init__(self):
        """Initialize creation time if not provided"""
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_total(self):
        """Calculate total amount from items"""
        self.total_amount = sum(item.subtotal for item in self.items)
        return self.total_amount
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'order_id': self.order_id,
            'items': [item.to_dict() for item in self.items],
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict, products_dict: dict) -> 'Order':
        """Create Order object from dictionary"""
        from .order_item import OrderItem
        
        items = []
        for item_data in data['items']:
            product_id = item_data['product_id']
            if product_id in products_dict:
                product = products_dict[product_id]
                item = OrderItem.from_dict(item_data, product)
                items.append(item)
        
        order = cls(
            order_id=data['order_id'],
            items=items,
            total_amount=data['total_amount'],
            payment_method=data['payment_method'],
            payment_status=data['payment_status'],
            created_at=data['created_at'],
            status=data['status']
        )
        return order

