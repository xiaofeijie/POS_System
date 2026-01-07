# POS System - Use Case Diagram

```mermaid
graph TB
    Cashier[Cashier]
    Customer[Customer]
    
    subgraph POS["POS System"]
        subgraph Checkout["Checkout"]
            UC1[UC1: Scan Product]
            UC2[UC2: Add Item to Order]
            UC3[UC3: View Order Details]
            UC4[UC4: Process Payment]
            UC5[UC5: Print Receipt]
        end
        
        subgraph Return["Return"]
            UC6[UC6: Find Order]
            UC7[UC7: Select Return Items]
            UC8[UC8: Process Return]
            UC9[UC9: Print Return Receipt]
        end
        
        subgraph Inventory["Inventory"]
            UC10[UC10: Check Stock]
            UC11[UC11: Update Inventory]
        end
    end
    
    Cashier --> UC1
    Cashier --> UC2
    Cashier --> UC3
    Cashier --> UC4
    Cashier --> UC5
    Cashier --> UC6
    Cashier --> UC7
    Cashier --> UC8
    Cashier --> UC9
    
    Customer --> UC4
    Customer --> UC6
    Customer --> UC7
    
    UC1 -.->|include| UC2
    UC2 -.->|include| UC10
    UC2 -.->|extend| UC3
    UC4 -.->|include| UC11
    UC4 -.->|include| UC5
    UC6 -.->|extend| UC3
    UC7 -.->|include| UC6
    UC8 -.->|include| UC11
    UC8 -.->|include| UC9
    
    style Cashier fill:#e1f5ff
    style Customer fill:#fff4e1
    style UC1 fill:#e8f5e9
    style UC2 fill:#e8f5e9
    style UC3 fill:#e8f5e9
    style UC4 fill:#e8f5e9
    style UC5 fill:#e8f5e9
    style UC6 fill:#f3e5f5
    style UC7 fill:#f3e5f5
    style UC8 fill:#f3e5f5
    style UC9 fill:#f3e5f5
    style UC10 fill:#fff9c4
    style UC11 fill:#fff9c4
```

## Use Cases

### Checkout Use Cases
- **UC1: Scan Product** - Cashier scans or enters product ID/barcode
- **UC2: Add Item to Order** - System adds item to current order
- **UC3: View Order Details** - Display current order with running total
- **UC4: Process Payment** - Customer provides payment, system processes it
- **UC5: Print Receipt** - System generates and prints receipt

### Return Use Cases
- **UC6: Find Order** - Customer provides order ID, system finds order
- **UC7: Select Return Items** - Select items and quantities to return
- **UC8: Process Return** - System processes return and updates inventory
- **UC9: Print Return Receipt** - System generates return receipt

### Inventory Use Cases
- **UC10: Check Stock** - Verify product availability
- **UC11: Update Inventory** - Update stock after sale or return

