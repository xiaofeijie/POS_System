"""
Migration Script - Migrate data from JSON files to SQLite database
"""
import json
import os
from database.db_connection import DatabaseConnection
from database.schema import create_tables
from storage.product_storage import ProductStorage
from storage.order_storage import OrderStorage
from storage.inventory_storage import InventoryStorage
from models.product import Product


def migrate_products_from_json(json_path: str, product_storage: ProductStorage):
    """Migrate products from JSON file"""
    if not os.path.exists(json_path):
        print(f"Products JSON file not found: {json_path}")
        return 0
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products = [Product.from_dict(item) for item in data]
            
            count = 0
            for product in products:
                if product_storage.add(product):
                    count += 1
                else:
                    print(f"Product {product.product_id} already exists, skipping...")
            
            print(f"Migrated {count} products from JSON")
            return count
    except Exception as e:
        print(f"Error migrating products: {e}")
        return 0


def migrate_orders_from_json(json_path: str, order_storage: OrderStorage):
    """Migrate orders from JSON file"""
    if not os.path.exists(json_path):
        print(f"Orders JSON file not found: {json_path}")
        return 0
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Get all products for order reconstruction
            products = order_storage.product_storage.load_all()
            products_dict = {p.product_id: p for p in products}
            
            from models.order import Order
            orders = [Order.from_dict(item, products_dict) for item in data]
            
            count = 0
            for order in orders:
                if order_storage.add(order):
                    count += 1
                else:
                    print(f"Order {order.order_id} already exists, skipping...")
            
            print(f"Migrated {count} orders from JSON")
            return count
    except Exception as e:
        print(f"Error migrating orders: {e}")
        return 0


def migrate_inventory_from_json(json_path: str, inventory_storage: InventoryStorage):
    """Migrate inventory from JSON file"""
    if not os.path.exists(json_path):
        print(f"Inventory JSON file not found: {json_path}")
        return 0
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            inventory = json.load(f)
            
            count = 0
            for product_id, quantity in inventory.items():
                inventory_storage.set_quantity(product_id, quantity)
                count += 1
            
            print(f"Migrated {count} inventory records from JSON")
            return count
    except Exception as e:
        print(f"Error migrating inventory: {e}")
        return 0


def migrate_all(json_data_dir: str = "data", db_path: str = "data/pos_system.db"):
    """Migrate all data from JSON files to database"""
    print("Starting migration from JSON to SQLite database...")
    print(f"Database path: {db_path}")
    print(f"JSON data directory: {json_data_dir}")
    print("-" * 60)
    
    # Initialize database
    db = DatabaseConnection(db_path)
    create_tables(db)
    print("Database tables created/verified")
    
    # Initialize storage classes
    product_storage = ProductStorage(db)
    order_storage = OrderStorage(db)
    inventory_storage = InventoryStorage(db)
    
    # Migrate products
    products_json = os.path.join(json_data_dir, "products.json")
    product_count = migrate_products_from_json(products_json, product_storage)
    
    # Migrate inventory
    inventory_json = os.path.join(json_data_dir, "inventory.json")
    inventory_count = migrate_inventory_from_json(inventory_json, inventory_storage)
    
    # Migrate orders (should be done after products)
    orders_json = os.path.join(json_data_dir, "orders.json")
    order_count = migrate_orders_from_json(orders_json, order_storage)
    
    print("-" * 60)
    print("Migration completed!")
    print(f"Summary:")
    print(f"  - Products: {product_count}")
    print(f"  - Inventory records: {inventory_count}")
    print(f"  - Orders: {order_count}")


if __name__ == "__main__":
    import sys
    
    json_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "data/pos_system.db"
    
    migrate_all(json_dir, db_path)
