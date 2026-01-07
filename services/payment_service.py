"""
Payment Service - Handle payment validation and processing
"""
from typing import Dict, Tuple


class PaymentService:
    """Payment service for validating and processing payments"""
    
    VALID_PAYMENT_METHODS = ['cash', 'card', 'alipay', 'wechat']
    
    def validate_payment_method(self, method: str) -> bool:
        """Validate payment method"""
        return method.lower() in self.VALID_PAYMENT_METHODS
    
    def validate_payment_info(self, method: str, amount: float, paid_amount: float = None) -> Tuple[bool, str]:
        """
        Validate payment information
        Returns: (is_valid, error_message)
        """
        if not self.validate_payment_method(method):
            return False, f"Invalid payment method. Valid methods: {', '.join(self.VALID_PAYMENT_METHODS)}"
        
        if amount <= 0:
            return False, "Payment amount must be greater than 0"
        
        if paid_amount is not None:
            if paid_amount < amount:
                return False, f"Insufficient payment. Required: {amount:.2f}, Paid: {paid_amount:.2f}"
        
        return True, ""
    
    def process_payment(self, method: str, amount: float, paid_amount: float = None) -> Dict:
        """
        Process payment
        Returns payment record
        """
        is_valid, error = self.validate_payment_info(method, amount, paid_amount)
        if not is_valid:
            raise ValueError(error)
        
        if paid_amount is None:
            paid_amount = amount
        
        change = paid_amount - amount if paid_amount > amount else 0
        
        return {
            'method': method.lower(),
            'amount': amount,
            'paid_amount': paid_amount,
            'change': change,
            'status': 'paid'
        }

