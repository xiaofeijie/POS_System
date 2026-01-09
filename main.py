"""
POS System - Main Entry Point
"""
from ui.checkout_ui import CheckoutUI
from ui.return_ui import ReturnUI
from ui.inventory_ui import InventoryUI
from storage.product_storage import ProductStorage
from storage.inventory_storage import InventoryStorage


def initialize_sample_data():
    """Initialize sample products and inventory for testing"""
    from database.schema import init_database
    
    # Initialize database
    init_database()
    
    product_storage = ProductStorage()
    inventory_storage = InventoryStorage()
    
    # Check if products already exist
    existing_products = product_storage.load_all()
    if len(existing_products) > 0:
        return  # Data already exists
    
    # Sample products
    from models.product import Product
    
    sample_products = [
        Product("P001", "Coca Cola", 3.50, "6901234567890", "Beverage"),
        Product("P002", "Pepsi Cola", 3.50, "6901234567891", "Beverage"),
        Product("P003", "Instant Noodles", 5.00, "6901234567892", "Food"),
        Product("P004", "Cup Noodles", 5.00, "6901234567893", "Food"),
        Product("P005", "Pure Milk", 12.00, "6901234567894", "Dairy"),
        Product("P006", "Fresh Milk", 12.00, "6901234567895", "Dairy"),
        Product("P007", "Oreo Cookies", 8.50, "6901234567896", "Snacks"),
        Product("P008", "Potato Chips", 6.00, "6901234567897", "Snacks"),
    ]
    
    # Add products
    for product in sample_products:
        product_storage.add(product)
        inventory_storage.set_quantity(product.product_id, 100)  # Set initial stock
    
    print("Sample product data initialized")


def show_main_menu():
    """Show main menu"""
    print("\n" + "="*60)
    print("POS System - Point of Sale")
    print("="*60)
    print("1. Checkout")
    print("2. Return")
    print("3. View Inventory")
    print("4. Exit")
    print("="*60)


def main():
    """Main function"""
    # Initialize sample data
    try:
        initialize_sample_data()
    except Exception as e:
        print(f"Error initializing data: {e}")
    
    checkout_ui = CheckoutUI()
    return_ui = ReturnUI()
    inventory_ui = InventoryUI()
    
    while True:
        show_main_menu()
        choice = input("Please select an option (1-4): ").strip()
        
        if choice == '1':
            try:
                checkout_ui.run()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled")
            except Exception as e:
                print(f"\nError occurred: {e}")
        
        elif choice == '2':
            try:
                return_ui.run()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled")
            except Exception as e:
                print(f"\nError occurred: {e}")
        
        elif choice == '3':
            try:
                inventory_ui.run()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled")
            except Exception as e:
                print(f"\nError occurred: {e}")
        
        elif choice == '4':
            print("\nThank you for using POS System. Goodbye!")
            break
        
        else:
            print("\nInvalid selection, please try again")


if __name__ == "__main__":
    main()

