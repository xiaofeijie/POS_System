# Database System Documentation

## Overview

The POS System has been upgraded from JSON file storage to SQLite database storage. This provides better performance, data integrity, and scalability.

## Database Structure

The system uses SQLite database (`data/pos_system.db`) with the following tables:

### Tables

1. **products**
   - `product_id` (TEXT, PRIMARY KEY)
   - `name` (TEXT, NOT NULL)
   - `price` (REAL, NOT NULL)
   - `barcode` (TEXT)
   - `category` (TEXT)

2. **orders**
   - `order_id` (TEXT, PRIMARY KEY)
   - `total_amount` (REAL, NOT NULL)
   - `payment_method` (TEXT, NOT NULL)
   - `payment_status` (TEXT, NOT NULL)
   - `created_at` (TEXT, NOT NULL)
   - `status` (TEXT, NOT NULL)

3. **order_items**
   - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - `order_id` (TEXT, FOREIGN KEY → orders.order_id)
   - `product_id` (TEXT, FOREIGN KEY → products.product_id)
   - `quantity` (INTEGER, NOT NULL)
   - `unit_price` (REAL, NOT NULL)

4. **inventory**
   - `product_id` (TEXT, PRIMARY KEY, FOREIGN KEY → products.product_id)
   - `quantity` (INTEGER, NOT NULL)

### Indexes

- `idx_order_items_order_id` on `order_items(order_id)`
- `idx_order_items_product_id` on `order_items(product_id)`
- `idx_products_barcode` on `products(barcode)`
- `idx_orders_created_at` on `orders(created_at)`

## Usage

### Initialization

The database is automatically initialized when you run the main application:

```bash
python main.py
```

Or manually initialize:

```bash
python database/init_db.py
```

### Migration from JSON

If you have existing data in JSON format, you can migrate it to the database:

```bash
python database/migrate_from_json.py
```

This will:
1. Read data from `data/products.json`, `data/orders.json`, and `data/inventory.json`
2. Create the database and tables if they don't exist
3. Import all data into the database
4. Skip duplicate entries (products/orders that already exist)

### Manual Migration

You can also specify custom paths:

```bash
python database/migrate_from_json.py [json_data_dir] [db_path]
```

Example:
```bash
python database/migrate_from_json.py data data/pos_system.db
```

## Code Structure

### Database Module (`database/`)

- `db_connection.py`: Database connection management
- `schema.py`: Table definitions and initialization
- `migrate_from_json.py`: Migration script from JSON to SQLite
- `init_db.py`: Database initialization script

### Storage Layer (`storage/`)

All storage classes have been updated to use SQLite:

- `ProductStorage`: Product data operations
- `OrderStorage`: Order data operations
- `InventoryStorage`: Inventory data operations

The API remains the same, so no changes are needed in the services or UI layers.

## Advantages of Database System

1. **Better Performance**: SQL queries are faster than loading entire JSON files
2. **Data Integrity**: Foreign keys and constraints ensure data consistency
3. **Concurrent Access**: SQLite handles concurrent reads efficiently
4. **Scalability**: Can handle larger datasets more efficiently
5. **Query Capabilities**: Easy to add complex queries in the future
6. **Transactions**: Atomic operations ensure data consistency

## Backup and Restore

### Backup Database

Simply copy the database file:

```bash
# Windows
copy data\pos_system.db data\pos_system_backup.db

# Linux/Mac
cp data/pos_system.db data/pos_system_backup.db
```

### Restore Database

Replace the database file with your backup:

```bash
# Windows
copy data\pos_system_backup.db data\pos_system.db

# Linux/Mac
cp data/pos_system_backup.db data/pos_system.db
```

## Database Browser

You can view and edit the database using SQLite browser tools:

- **DB Browser for SQLite**: https://sqlitebrowser.org/
- **SQLite Studio**: https://sqlitestudio.pl/
- **Command Line**: `sqlite3 data/pos_system.db`

Example SQLite command line usage:

```bash
sqlite3 data/pos_system.db
.tables
SELECT * FROM products;
.quit
```

## Notes

- The database file (`data/pos_system.db`) is excluded from Git (in `.gitignore`)
- JSON files are still supported for migration but are no longer used for runtime storage
- All existing functionality remains the same - only the storage backend has changed
- SQLite is included in Python standard library, no additional packages required
