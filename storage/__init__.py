"""
Storage Module
"""
from .product_storage import ProductStorage
from .order_storage import OrderStorage
from .inventory_storage import InventoryStorage

__all__ = ['ProductStorage', 'OrderStorage', 'InventoryStorage']

