"""
Return UI - User interface for return process
"""
from services.return_service import ReturnService


class ReturnUI:
    """Return user interface"""
    
    def __init__(self):
        """Initialize return UI"""
        self.return_service = ReturnService()
    
    def display_order(self, order):
        """Display order details"""
        print("\n" + "="*60)
        print("Order Details")
        print("="*60)
        print(f"Order ID: {order.order_id}")
        print(f"Order Time: {order.created_at}")
        print(f"Order Status: {order.status}")
        print(f"Payment Status: {order.payment_status}")
        print("-"*60)
        print(f"{'Product Name':<20} {'Qty':<8} {'Unit Price':<12} {'Subtotal':<12}")
        print("-"*60)
        
        for item in order.items:
            print(f"{item.product.name:<20} {item.quantity:<8} ${item.unit_price:<11.2f} ${item.subtotal:<11.2f}")
        
        print("-"*60)
        print(f"{'Total':<40} ${order.total_amount:.2f}")
        print("="*60)
    
    def select_return_items(self, order):
        """Select items to return"""
        returnable_items = self.return_service.get_returnable_items(order)
        
        print("\nSelect items to return:")
        print("-"*60)
        
        valid_items = []
        for idx, item_info in enumerate(returnable_items, 1):
            item = item_info['item']
            can_return = item_info['can_return']
            max_qty = item_info['returnable_quantity']
            
            if can_return:
                print(f"{idx}. {item.product.name} (Purchased: {item.quantity}, Returnable: {max_qty})")
                valid_items.append((idx, item_info))
            else:
                print(f"{idx}. {item.product.name} (Purchased: {item.quantity}, Returnable: 0) - Already returned")
        
        if len(valid_items) == 0:
            print("No items available for return")
            return {}
        
        print("\nEnter item numbers to return (separate multiple with commas, e.g., 1,2):")
        selection = input("> ").strip()
        
        return_items = {}
        
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            for idx in indices:
                # Find the item
                item_info = None
                for num, info in valid_items:
                    if num == idx:
                        item_info = info
                        break
                
                if item_info is None:
                    print(f"Invalid item number: {idx}")
                    continue
                
                item = item_info['item']
                max_qty = item_info['returnable_quantity']
                
                print(f"\n{item.product.name} - Enter return quantity (max: {max_qty}):")
                qty_input = input("> ").strip()
                
                try:
                    qty = int(qty_input)
                    if qty <= 0:
                        print("Quantity must be greater than 0")
                        continue
                    if qty > max_qty:
                        print(f"Return quantity cannot exceed {max_qty}")
                        continue
                    
                    return_items[item.product.product_id] = qty
                except ValueError:
                    print("Invalid quantity")
                    continue
        
        except ValueError:
            print("Invalid input")
            return {}
        
        return return_items
    
    def process_return(self):
        """Process return"""
        print("\n" + "="*60)
        print("Return System")
        print("="*60)
        
        # Get order ID
        print("\nEnter order ID:")
        order_id = input("> ").strip()
        
        # Find order
        order = self.return_service.find_order(order_id)
        if order is None:
            print(f"Order not found: {order_id}")
            return
        
        # Display order
        self.display_order(order)
        
        # Check if can return
        if order.status == 'returned':
            print("\nThis order has already been fully returned")
            return
        
        # Select return items
        return_items = self.select_return_items(order)
        
        if len(return_items) == 0:
            print("No items selected for return")
            return
        
        # Get return reason (optional)
        print("\nEnter return reason (optional, press Enter to skip):")
        reason = input("> ").strip()
        
        # Confirm
        print("\nConfirm return? (y/n):")
        confirm = input("> ").strip().lower()
        if confirm != 'y':
            print("Return cancelled")
            return
        
        # Process return
        success, message, return_info = self.return_service.process_return(
            order_id, return_items, reason
        )
        
        if success:
            print(f"\n✓ {message}")
            self.print_return_receipt(return_info)
        else:
            print(f"\n✗ {message}")
    
    def print_return_receipt(self, return_info):
        """Print return receipt"""
        print("\n" + "="*60)
        print("RETURN RECEIPT")
        print("="*60)
        print(f"Order ID: {return_info['order_id']}")
        print(f"Return Time: {return_info['return_time']}")
        if return_info.get('reason'):
            print(f"Return Reason: {return_info['reason']}")
        print("-"*60)
        print(f"{'Product Name':<20} {'Return Qty':<12} {'Refund Amount':<12}")
        print("-"*60)
        
        for item_info in return_info['items']:
            item = item_info['item']
            qty = item_info['quantity']
            refund = item_info['refund_amount']
            print(f"{item.product.name:<20} {qty:<12} ${refund:.2f}")
        
        print("-"*60)
        print(f"{'Total Refund':<32} ${return_info['return_amount']:.2f}")
        print("="*60)
        print("Return processed successfully")
        print("="*60)
    
    def run(self):
        """Run return process"""
        self.process_return()

