# POS System - System Sequence Diagrams

## Sequence Diagram 1: Checkout Process

```mermaid
sequenceDiagram
    participant Cashier
    participant Customer
    participant UI as CheckoutUI
    participant Service as CheckoutService
    participant PStorage as ProductStorage
    participant InvService as InventoryService
    participant PayService as PaymentService
    participant OStorage as OrderStorage
    
    Note over Cashier,Customer: Scan and Add Products
    Cashier->>UI: Enter product ID/barcode
    UI->>PStorage: get_by_id(product_id)
    PStorage-->>UI: Product
    UI->>UI: Display product info
    UI->>Cashier: Prompt for quantity
    Cashier->>UI: Enter quantity
    UI->>Service: add_item(product_id, quantity)
    Service->>PStorage: get_by_id(product_id)
    PStorage-->>Service: Product
    Service->>InvService: check_stock(product_id, quantity)
    InvService-->>Service: true/false
    
    alt Stock available
        Service->>Service: Create/update OrderItem
        Service->>Service: calculate_total()
        Service-->>UI: (success, message)
        UI->>UI: display_current_order()
        UI-->>Cashier: Show order details
    else Insufficient stock
        Service-->>UI: (failure, error message)
        UI-->>Cashier: Display error
    end
    
    Note over Cashier,Customer: Process Payment
    Cashier->>UI: Finish adding items
    UI->>UI: display_current_order()
    UI-->>Cashier: Show order total
    Cashier->>UI: Select payment method
    UI->>Customer: Request payment info
    Customer->>UI: Provide payment method/amount
    UI->>Service: process_payment(method, paid_amount)
    Service->>PayService: process_payment(method, amount, paid_amount)
    PayService->>PayService: validate_payment_info()
    PayService-->>Service: payment_info
    
    loop For each item
        Service->>InvService: reduce_stock(product_id, quantity)
        InvService-->>Service: success
    end
    
    Service->>OStorage: add(order)
    OStorage-->>Service: success
    Service-->>UI: (success, order, payment_info)
    UI->>UI: print_receipt(order, payment_info)
    UI-->>Cashier: Display receipt
    UI-->>Customer: Receipt
```

## Sequence Diagram 2: Return Process

```mermaid
sequenceDiagram
    participant Cashier
    participant Customer
    participant UI as ReturnUI
    participant Service as ReturnService
    participant OStorage as OrderStorage
    participant InvService as InventoryService
    
    Note over Cashier,Customer: Find Order
    Customer->>UI: Provide order ID
    Cashier->>UI: Enter order ID
    UI->>Service: find_order(order_id)
    Service->>OStorage: get_by_id(order_id)
    OStorage-->>Service: Order
    Service-->>UI: Order
    UI->>UI: display_order(order)
    UI-->>Cashier: Show order details
    
    Note over Cashier,Customer: Select Return Items
    UI->>Service: get_returnable_items(order)
    Service->>Service: Calculate returnable quantities
    Service-->>UI: returnable_items
    UI-->>Cashier: Display returnable items
    Cashier->>UI: Select item numbers
    UI->>Customer: Request return quantities
    Customer->>UI: Provide quantities
    UI->>UI: select_return_items(order)
    UI-->>Cashier: Show selected items
    UI->>Customer: Request return reason (optional)
    Customer->>UI: Provide reason (optional)
    
    Note over Cashier,Customer: Process Return
    Cashier->>UI: Confirm return
    UI->>Service: process_return(order_id, return_items, reason)
    Service->>Service: Validate return items
    Service->>Service: Calculate refund amount
    
    loop For each return item
        Service->>InvService: add_stock(product_id, quantity)
        InvService-->>Service: success
    end
    
    Service->>Service: Update order status
    Service->>OStorage: update(order)
    OStorage-->>Service: success
    Service-->>UI: (success, return_info)
    UI->>UI: print_return_receipt(return_info)
    UI-->>Cashier: Display return receipt
    UI-->>Customer: Return receipt
```

## Diagram Elements

- **Actors**: Cashier, Customer
- **System Objects**: UI components, Services, Storage components
- **Messages**: Method calls and responses
- **Alt Blocks**: Alternative flows (e.g., stock available vs. insufficient)
- **Loop Blocks**: Iterative operations (e.g., processing multiple items)

