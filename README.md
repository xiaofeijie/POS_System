# POS System - Point of Sale

A small supermarket point of sale system developed in Python, implementing checkout and return functionality.

## Features

### Checkout Functionality
- Scan/input products to add to order
- Real-time display of order details and running total
- Support for multiple payment methods (cash, card, Alipay, WeChat)
- Automatic inventory updates
- Receipt generation

### Return Functionality
- Find orders by order ID
- Select items and quantities to return
- Automatic inventory restoration
- Return receipt generation

## Project Structure

```
The POS system/
├── models/              # Data Models Layer
│   ├── product.py      # Product model
│   ├── order.py        # Order model
│   └── order_item.py   # Order item model
│
├── services/            # Business Logic Layer
│   ├── checkout_service.py    # Checkout service
│   ├── return_service.py      # Return service
│   ├── inventory_service.py   # Inventory management service
│   └── payment_service.py     # Payment validation service
│
├── storage/             # Data Storage Layer
│   ├── product_storage.py     # Product data storage
│   ├── order_storage.py       # Order data storage
│   └── inventory_storage.py   # Inventory data storage
│
├── ui/                  # User Interface Layer
│   ├── checkout_ui.py   # Checkout interface
│   └── return_ui.py     # Return interface
│
├── data/                # Data Files Directory
│   ├── products.json    # Product data
│   ├── orders.json      # Order data
│   └── inventory.json   # Inventory data
│
├── main.py              # Main program entry point
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Usage

### Running the System

```bash
python main.py
```

### Operation Flow

#### Checkout Process
1. Select menu option `1` to enter checkout system
2. Enter product ID or barcode to add products
3. Enter product quantity (default: 1)
4. Continue adding products or type `done` to finish
5. Select payment method
6. If paying with cash, enter amount paid
7. System automatically processes payment, updates inventory, and generates receipt

#### Return Process
1. Select menu option `2` to enter return system
2. Enter order ID
3. View order details
4. Select item numbers to return
5. Enter return quantities
6. Enter return reason (optional)
7. Confirm return
8. System automatically processes return, restores inventory, and generates return receipt

## Technical Details

- **Language**: Python 3.x
- **Data Storage**: JSON files (lightweight, suitable for small systems)
- **Interface Type**: Command Line Interface (CLI)
- **Dependencies**: Uses only Python standard library, no additional dependencies required

## Data Initialization

The system automatically creates sample product data on first run, including:
- 8 sample products
- Initial stock of 100 for each product

Data files are saved in the `data/` directory:
- `products.json`: Product information
- `orders.json`: Order records
- `inventory.json`: Inventory information

## Notes

1. Ensure sufficient disk space for data files
2. Regularly backup JSON files in the `data/` directory
3. Product IDs and order IDs must be unique
4. Returns can only include purchased items, and quantities cannot exceed purchase quantities

## Future Enhancements

Consider adding the following features in the future:
- Product management (CRUD operations)
- Inventory alerts
- Sales statistics and reports
- Membership system
- Database support (replace JSON files)
- Graphical User Interface (GUI)
