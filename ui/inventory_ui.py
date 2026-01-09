"""
Inventory UI - User interface for viewing inventory
"""
from services.inventory_service import InventoryService
from storage.product_storage import ProductStorage


class InventoryUI:
    """Inventory user interface"""
    
    def __init__(self):
        """Initialize inventory UI"""
        self.inventory_service = InventoryService()
        self.product_storage = ProductStorage()
    
    def display_all_inventory(self):
        """Display all inventory with product details"""
        print("\n" + "="*70)
        print("Inventory Status")
        print("="*70)
        print(f"{'Product ID':<12} {'Product Name':<25} {'Stock':<10} {'Status':<15}")
        print("-"*70)
        
        # Get all products
        products = self.product_storage.load_all()
        
        if len(products) == 0:
            print("No products found in system")
            print("="*70)
            return
        
        # Get inventory for each product
        inventory_data = []
        for product in products:
            stock = self.inventory_service.get_stock(product.product_id)
            status = "In Stock" if stock > 0 else "Out of Stock"
            if stock > 0 and stock < 10:
                status = "Low Stock"
            
            inventory_data.append({
                'product': product,
                'stock': stock,
                'status': status
            })
        
        # Sort by product ID
        inventory_data.sort(key=lambda x: x['product'].product_id)
        
        # Display inventory
        for item in inventory_data:
            product = item['product']
            stock = item['stock']
            status = item['status']
            print(f"{product.product_id:<12} {product.name:<25} {stock:<10} {status:<15}")
        
        print("-"*70)
        
        # Summary
        total_products = len(inventory_data)
        in_stock = sum(1 for item in inventory_data if item['stock'] > 0)
        out_of_stock = sum(1 for item in inventory_data if item['stock'] == 0)
        low_stock = sum(1 for item in inventory_data if 0 < item['stock'] < 10)
        total_items = sum(item['stock'] for item in inventory_data)
        
        print(f"Summary:")
        print(f"  Total Products: {total_products}")
        print(f"  In Stock: {in_stock}")
        print(f"  Out of Stock: {out_of_stock}")
        print(f"  Low Stock (<10): {low_stock}")
        print(f"  Total Items: {total_items}")
        print("="*70)
    
    def display_product_inventory(self, product_id: str):
        """Display inventory for a specific product"""
        product = self.product_storage.get_by_id(product_id)
        if product is None:
            print(f"Product not found: {product_id}")
            return
        
        stock = self.inventory_service.get_stock(product_id)
        status = "In Stock" if stock > 0 else "Out of Stock"
        if stock > 0 and stock < 10:
            status = "Low Stock"
        
        print("\n" + "="*60)
        print("Product Inventory Details")
        print("="*60)
        print(f"Product ID: {product.product_id}")
        print(f"Product Name: {product.name}")
        print(f"Price: ${product.price:.2f}")
        if product.category:
            print(f"Category: {product.category}")
        print(f"Current Stock: {stock}")
        print(f"Status: {status}")
        print("="*60)
    
    def search_inventory(self):
        """Search inventory by product ID or name"""
        print("\nEnter product ID to view details (or press Enter to view all):")
        search_input = input("> ").strip()
        
        if not search_input:
            self.display_all_inventory()
        else:
            # Try product ID first
            product = self.product_storage.get_by_id(search_input)
            if product:
                self.display_product_inventory(search_input)
            else:
                # Try searching by name (partial match)
                products = self.product_storage.load_all()
                matching = [p for p in products if search_input.lower() in p.name.lower()]
                
                if len(matching) == 0:
                    print(f"No product found matching: {search_input}")
                elif len(matching) == 1:
                    self.display_product_inventory(matching[0].product_id)
                else:
                    print(f"\nFound {len(matching)} matching products:")
                    print("-"*60)
                    for p in matching:
                        stock = self.inventory_service.get_stock(p.product_id)
                        print(f"{p.product_id} - {p.name} (Stock: {stock})")
                    print("-"*60)
                    print("\nEnter product ID to view details:")
                    product_id = input("> ").strip()
                    if product_id:
                        self.display_product_inventory(product_id)
    
    def run(self):
        """Run inventory viewing process"""
        print("\n" + "="*60)
        print("Inventory Management")
        print("="*60)
        self.search_inventory()
