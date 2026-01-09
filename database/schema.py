"""
Database Schema - SQL table definitions
"""
from .db_connection import DatabaseConnection


def create_tables(db: DatabaseConnection):
    """Create all database tables"""
    
    # Products table
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            barcode TEXT,
            category TEXT
        )
    """)
    
    # Orders table
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            total_amount REAL NOT NULL DEFAULT 0.0,
            payment_method TEXT NOT NULL DEFAULT '',
            payment_status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'completed'
        )
    """)
    
    # Order items table
    db.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    # Inventory table
    db.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            product_id TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    # Create indexes for better performance
    db.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at)")


def init_database(db_path: str = "data/pos_system.db"):
    """Initialize database with tables"""
    db = DatabaseConnection(db_path)
    create_tables(db)
    return db
