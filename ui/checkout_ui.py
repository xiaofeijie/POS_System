"""
Checkout UI - User interface for checkout process
"""
from services.checkout_service import CheckoutService
from storage.product_storage import ProductStorage


class CheckoutUI:
    """Checkout user interface"""
    
    def __init__(self):
        """Initialize checkout UI"""
        self.checkout_service = CheckoutService()
        self.product_storage = ProductStorage()
    
    def display_current_order(self):
        """Display current order details"""
        if self.checkout_service.current_order is None or len(self.checkout_service.current_order.items) == 0:
            print("\nCurrent order is empty")
            return
        
        order = self.checkout_service.current_order
        print("\n" + "="*60)
        print("Current Order Details")
        print("="*60)
        print(f"{'Product Name':<20} {'Qty':<8} {'Unit Price':<12} {'Subtotal':<12}")
        print("-"*60)
        
        for item in order.items:
            print(f"{item.product.name:<20} {item.quantity:<8} ${item.unit_price:<11.2f} ${item.subtotal:<11.2f}")
        
        print("-"*60)
        print(f"{'Total':<40} ${order.total_amount:.2f}")
        print("="*60)
    
    def scan_product(self):
        """Scan or input product"""
        print("\nEnter product ID or barcode (type 'done' to finish adding items):")
        product_input = input("> ").strip()
        
        if product_input.lower() in ['done', 'finish', 'complete']:
            return False
        
        # Try to find product by ID or barcode
        product = self.product_storage.get_by_id(product_input)
        if product is None:
            product = self.product_storage.get_by_barcode(product_input)
        
        if product is None:
            print(f"Product not found: {product_input}")
            return True
        
        # Get quantity
        print(f"Product found: {product.name} (${product.price:.2f})")
        print("Enter quantity (default: 1):")
        quantity_input = input("> ").strip()
        
        try:
            quantity = int(quantity_input) if quantity_input else 1
            if quantity <= 0:
                print("Quantity must be greater than 0")
                return True
        except ValueError:
            print("Invalid quantity")
            return True
        
        # Add to order
        success, message = self.checkout_service.add_item(product.product_id, quantity)
        print(message)
        
        if success:
            self.display_current_order()
        
        return True
    
    def process_payment(self):
        """Process payment"""
        if self.checkout_service.current_order is None or len(self.checkout_service.current_order.items) == 0:
            print("Order is empty, cannot process payment")
            return
        
        total = self.checkout_service.get_current_total()
        print(f"\nOrder Total: ${total:.2f}")
        print("\nSelect payment method:")
        print("1. Cash")
        print("2. Card")
        print("3. Alipay")
        print("4. WeChat")
        
        method_map = {
            '1': 'cash',
            '2': 'card',
            '3': 'alipay',
            '4': 'wechat'
        }
        
        choice = input("> ").strip()
        payment_method = method_map.get(choice, choice.lower())
        
        paid_amount = None
        if payment_method == 'cash':
            print("Enter amount paid:")
            try:
                paid_amount = float(input("> ").strip())
            except ValueError:
                print("Invalid amount")
                return
        
        # Process payment
        success, message, payment_info = self.checkout_service.process_payment(payment_method, paid_amount)
        
        if success:
            print(f"\n✓ {message}")
            order = payment_info['order']
            payment = payment_info['payment']
            
            # Print receipt
            self.print_receipt(order, payment)
        else:
            print(f"\n✗ {message}")
    
    def print_receipt(self, order, payment_info):
        """Print receipt"""
        print("\n" + "="*60)
        print("RECEIPT")
        print("="*60)
        print(f"Order ID: {order.order_id}")
        print(f"Time: {order.created_at}")
        print("-"*60)
        print(f"{'Product Name':<20} {'Qty':<8} {'Unit Price':<12} {'Subtotal':<12}")
        print("-"*60)
        
        for item in order.items:
            print(f"{item.product.name:<20} {item.quantity:<8} ${item.unit_price:<11.2f} ${item.subtotal:<11.2f}")
        
        print("-"*60)
        print(f"{'Total':<40} ${order.total_amount:.2f}")
        print(f"Payment Method: {payment_info['method']}")
        if payment_info.get('paid_amount'):
            print(f"Amount Paid: ${payment_info['paid_amount']:.2f}")
        if payment_info.get('change', 0) > 0:
            print(f"Change: ${payment_info['change']:.2f}")
        print("="*60)
        print("Thank you for your purchase!")
        print("="*60)
    
    def run(self):
        """Run checkout process"""
        print("\n" + "="*60)
        print("Checkout System")
        print("="*60)
        
        # Start new order
        self.checkout_service.start_new_order()
        
        # Add items
        while True:
            if not self.scan_product():
                break
        
        # Check if order has items
        if self.checkout_service.current_order is None or len(self.checkout_service.current_order.items) == 0:
            print("Order cancelled")
            return
        
        # Process payment
        self.process_payment()

