# POS System - UML Package Diagram

This diagram shows the layered architecture of the POS System with packages organized by layers.

```mermaid
graph TB
    subgraph "UI Layer (2 modules)"
        CheckoutUI[CheckoutUI]
        ReturnUI[ReturnUI]
    end
    
    subgraph "Services Layer (4 modules)"
        CheckoutService[CheckoutService]
        ReturnService[ReturnService]
        InventoryService[InventoryService]
        PaymentService[PaymentService]
    end
    
    subgraph "Storage Layer (3 modules)"
        ProductStorage[ProductStorage]
        OrderStorage[OrderStorage]
        InventoryStorage[InventoryStorage]
    end
    
    subgraph "Database Layer (1 module)"
        DatabaseConnection[DatabaseConnection]
    end
    
    subgraph "Models Layer (3 modules)"
        Product[Product]
        Order[Order]
        OrderItem[OrderItem]
    end
    
    %% Layer dependencies
    CheckoutUI --> CheckoutService
    ReturnUI --> ReturnService
    
    CheckoutService --> ProductStorage
    CheckoutService --> OrderStorage
    CheckoutService --> InventoryService
    CheckoutService --> PaymentService
    ReturnService --> OrderStorage
    ReturnService --> InventoryService
    ReturnService --> PaymentService
    InventoryService --> InventoryStorage
    
    ProductStorage --> DatabaseConnection
    OrderStorage --> DatabaseConnection
    OrderStorage --> ProductStorage
    InventoryStorage --> DatabaseConnection
    InventoryStorage -.-> ProductStorage
    
    CheckoutService --> Order
    CheckoutService --> OrderItem
    CheckoutService --> Product
    ReturnService --> Order
    OrderStorage --> Order
    OrderStorage --> Product
    
    Order --> OrderItem
    OrderItem --> Product
    
    style CheckoutUI fill:#e1f5ff
    style ReturnUI fill:#e1f5ff
    style CheckoutService fill:#fff4e1
    style ReturnService fill:#fff4e1
    style InventoryService fill:#fff4e1
    style PaymentService fill:#fff4e1
    style ProductStorage fill:#e8f5e9
    style OrderStorage fill:#e8f5e9
    style InventoryStorage fill:#e8f5e9
    style DatabaseConnection fill:#fff9c4
    style Product fill:#f3e5f5
    style Order fill:#f3e5f5
    style OrderItem fill:#f3e5f5
```

## Layer Structure

### 1. UI Layer (2 modules)
- **CheckoutUI**: User interface for checkout process
- **ReturnUI**: User interface for return process

### 2. Services Layer (4 modules)
- **CheckoutService**: Handles checkout business logic
- **ReturnService**: Handles return business logic
- **InventoryService**: Manages inventory operations
- **PaymentService**: Validates and processes payments

### 3. Storage Layer (3 modules)
- **ProductStorage**: Manages product data operations
- **OrderStorage**: Manages order data operations
- **InventoryStorage**: Manages inventory data operations

**Dependencies**: Database Layer, Models Layer

### 4. Database Layer (1 module)
- **DatabaseConnection**: Manages SQLite database connections and queries

**Dependencies**: None (infrastructure layer)

### 5. Models Layer (3 modules)
- **Product**: Product data model
- **Order**: Order data model
- **OrderItem**: Order item data model

## Dependency Rules

1. **UI Layer** depends only on **Services Layer**
2. **Services Layer** depends on **Storage Layer** and **Models Layer**
3. **Storage Layer** depends on **Database Layer** and **Models Layer**
4. **Database Layer** has no dependencies (infrastructure layer)
5. **Models Layer** has no dependencies (base layer)

## Architecture Pattern

This follows a **Layered Architecture** pattern:
- Clear separation of concerns
- Each layer has a specific responsibility
- Dependencies flow downward (top layers depend on bottom layers)
- Lower layers are independent of higher layers

