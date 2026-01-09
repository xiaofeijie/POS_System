# POS System - Package Diagram Summary

## System Architecture Overview

The POS System follows a **5-layer architecture** with **13 modules** in total:

```
┌─────────────────────────────────────────┐
│         UI Layer (2 modules)            │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ CheckoutUI   │  │  ReturnUI     │   │
│  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Services Layer (4 modules)         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Checkout     │  │   Return     │   │
│  │  Service     │  │   Service    │   │
│  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Inventory    │  │   Payment    │   │
│  │  Service     │  │   Service    │   │
│  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Storage Layer (3 modules)          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │  Product     │  │    Order      │   │
│  │  Storage     │  │   Storage     │   │
│  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐                      │
│  │  Inventory   │                      │
│  │  Storage     │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Database Layer (1 module)           │
│  ┌──────────────┐                      │
│  │  Database    │                      │
│  │  Connection  │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Models Layer (3 modules)          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │   Product    │  │    Order     │   │
│  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐                      │
│  │  OrderItem   │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
```

## Layer Details

### Layer 1: UI Layer (2 modules)
**Responsibility**: User interface and interaction

| Module | Purpose |
|--------|---------|
| CheckoutUI | Handles checkout user interface |
| ReturnUI | Handles return user interface |

**Dependencies**: Services Layer

---

### Layer 2: Services Layer (4 modules)
**Responsibility**: Business logic and workflow

| Module | Purpose |
|--------|---------|
| CheckoutService | Processes checkout operations |
| ReturnService | Processes return operations |
| InventoryService | Manages inventory operations |
| PaymentService | Validates and processes payments |

**Dependencies**: Storage Layer, Models Layer

---

### Layer 3: Storage Layer (3 modules)
**Responsibility**: Data persistence abstraction

| Module | Purpose |
|--------|---------|
| ProductStorage | Manages product data operations |
| OrderStorage | Manages order data operations |
| InventoryStorage | Manages inventory data operations |

**Dependencies**: Database Layer, Models Layer

---

### Layer 4: Database Layer (1 module)
**Responsibility**: Database connection and query execution

| Module | Purpose |
|--------|---------|
| DatabaseConnection | Manages SQLite database connections and queries |

**Dependencies**: None (infrastructure layer)

---

### Layer 5: Models Layer (3 modules)
**Responsibility**: Data structures

| Module | Purpose |
|--------|---------|
| Product | Product data model |
| Order | Order data model |
| OrderItem | Order item data model |

**Dependencies**: None (base layer)

## Module Count Summary

| Layer | Module Count | Modules |
|-------|--------------|---------|
| UI Layer | 2 | CheckoutUI, ReturnUI |
| Services Layer | 4 | CheckoutService, ReturnService, InventoryService, PaymentService |
| Storage Layer | 3 | ProductStorage, OrderStorage, InventoryStorage |
| Database Layer | 1 | DatabaseConnection |
| Models Layer | 3 | Product, Order, OrderItem |
| **Total** | **13** | |

## Dependency Flow

```
UI Layer
  ↓ (depends on)
Services Layer
  ↓ (depends on)
Storage Layer + Models Layer
  ↓ (Storage depends on)
Database Layer
  ↓ (supports)
Models Layer
```

## Design Principles

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility
2. **Dependency Inversion**: Higher layers depend on lower layers, not vice versa
3. **Loose Coupling**: Modules interact through well-defined interfaces
4. **High Cohesion**: Related functionality is grouped within the same layer

