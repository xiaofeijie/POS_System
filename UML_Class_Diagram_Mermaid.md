# POS System - UML Class Diagram (Mermaid)

```mermaid
classDiagram
    %% Models Layer
    class Product {
        +str product_id
        +str name
        +float price
        +str barcode
        +str category
        +to_dict() dict
        +from_dict(data) Product
    }
    
    class Order {
        +str order_id
        +List~OrderItem~ items
        +float total_amount
        +str payment_method
        +str payment_status
        +str created_at
        +str status
        +calculate_total() float
        +to_dict() dict
        +from_dict(data, products_dict) Order
    }
    
    class OrderItem {
        +Product product
        +int quantity
        +float unit_price
        +subtotal float
        +to_dict() dict
        +from_dict(data, product) OrderItem
    }
    
    %% Services Layer
    class CheckoutService {
        -ProductStorage product_storage
        -OrderStorage order_storage
        -InventoryService inventory_service
        -PaymentService payment_service
        -Order current_order
        +start_new_order() Order
        +add_item(product_id, quantity) Tuple
        +remove_item(product_id) bool
        +update_item_quantity(product_id, quantity) Tuple
        +get_current_total() float
        +process_payment(payment_method, paid_amount) Tuple
        +cancel_order()
    }
    
    class ReturnService {
        -OrderStorage order_storage
        -InventoryService inventory_service
        -PaymentService payment_service
        +find_order(order_id) Order
        +get_returnable_items(order) List
        +process_return(order_id, return_items, reason) Tuple
    }
    
    class InventoryService {
        -InventoryStorage storage
        +get_stock(product_id) int
        +check_stock(product_id, quantity) bool
        +reduce_stock(product_id, quantity) bool
        +add_stock(product_id, quantity)
        +set_stock(product_id, quantity)
    }
    
    class PaymentService {
        +List VALID_PAYMENT_METHODS
        +validate_payment_method(method) bool
        +validate_payment_info(method, amount, paid_amount) Tuple
        +process_payment(method, amount, paid_amount) Dict
    }
    
    %% Database Layer
    class DatabaseConnection {
        -str db_path
        +get_connection() Connection
        +get_cursor() contextmanager
        +execute(query, params) cursor
        +execute_many(query, params_list) cursor
        +fetch_one(query, params) Row
        +fetch_all(query, params) list
    }
    
    %% Storage Layer
    class ProductStorage {
        -DatabaseConnection db
        +load_all() List~Product~
        +save_all(products)
        +get_by_id(product_id) Product
        +get_by_barcode(barcode) Product
        +add(product) bool
        +update(product) bool
        +delete(product_id) bool
    }
    
    class OrderStorage {
        -DatabaseConnection db
        -ProductStorage product_storage
        +load_all() List~Order~
        +save_all(orders)
        +get_by_id(order_id) Order
        +add(order) bool
        +update(order) bool
    }
    
    class InventoryStorage {
        -DatabaseConnection db
        -ProductStorage product_storage
        +load_all() Dict
        +save_all(inventory)
        +get_quantity(product_id) int
        +set_quantity(product_id, quantity)
        +add_quantity(product_id, quantity)
        +reduce_quantity(product_id, quantity) bool
        +has_stock(product_id, quantity) bool
    }
    
    %% UI Layer
    class CheckoutUI {
        -CheckoutService checkout_service
        -ProductStorage product_storage
        +display_current_order()
        +scan_product() bool
        +process_payment()
        +print_receipt(order, payment_info)
        +run()
    }
    
    class ReturnUI {
        -ReturnService return_service
        +display_order(order)
        +select_return_items(order) Dict
        +process_return()
        +print_return_receipt(return_info)
        +run()
    }
    
    %% Relationships
    Order "1" *-- "*" OrderItem : contains
    OrderItem "*" --> "1" Product : references
    
    CheckoutService --> ProductStorage : uses
    CheckoutService --> OrderStorage : uses
    CheckoutService --> InventoryService : uses
    CheckoutService --> PaymentService : uses
    CheckoutService ..> Order : creates/manages
    
    ReturnService --> OrderStorage : uses
    ReturnService --> InventoryService : uses
    ReturnService --> PaymentService : uses
    ReturnService ..> Order : processes
    
    InventoryService --> InventoryStorage : uses
    
    ProductStorage --> DatabaseConnection : uses
    OrderStorage --> DatabaseConnection : uses
    OrderStorage --> ProductStorage : uses
    InventoryStorage --> DatabaseConnection : uses
    InventoryStorage ..> ProductStorage : references
    
    CheckoutUI --> CheckoutService : uses
    CheckoutUI --> ProductStorage : uses
    
    ReturnUI --> ReturnService : uses
```

## Legend

- **Composition** (`*--`): Order contains OrderItems
- **Association** (`-->`): OrderItem references Product
- **Dependency** (`-->` or `..>`): Service uses Storage, UI uses Service

## Layer Description

1. **Models**: Core data structures (Product, Order, OrderItem)
2. **Services**: Business logic (Checkout, Return, Inventory, Payment)
3. **Storage**: Data persistence (JSON file storage)
4. **UI**: User interface (CheckoutUI, ReturnUI)

