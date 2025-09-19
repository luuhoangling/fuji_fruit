"""Shipping service for calculating shipping fees"""

from typing import Dict


class ShippingService:
    """Service for shipping calculations"""
    
    # Shipping fee rules (in VND)
    FREE_SHIPPING_THRESHOLD = 500000  # Free shipping for orders > 500k VND
    DEFAULT_SHIPPING_FEE = 30000      # Default shipping fee
    
    # Province-based shipping fees
    PROVINCE_SHIPPING_FEES = {
        'Hà Nội': 25000,
        'TP Hồ Chí Minh': 25000,
        'Đà Nẵng': 30000,
        'Hải Phòng': 30000,
        'Cần Thơ': 35000,
    }
    
    def compute_shipping(self, subtotal: float, province: str = None) -> float:
        """Calculate shipping fee based on subtotal and province"""
        
        # Free shipping for large orders
        if subtotal >= self.FREE_SHIPPING_THRESHOLD:
            return 0.0
        
        # Province-specific shipping
        if province and province in self.PROVINCE_SHIPPING_FEES:
            return float(self.PROVINCE_SHIPPING_FEES[province])
        
        # Default shipping fee
        return float(self.DEFAULT_SHIPPING_FEE)
    
    def get_shipping_info(self, subtotal: float, province: str = None) -> Dict:
        """Get detailed shipping information"""
        shipping_fee = self.compute_shipping(subtotal, province)
        
        remaining_for_free = max(0, self.FREE_SHIPPING_THRESHOLD - subtotal)
        
        return {
            'fee': shipping_fee,
            'is_free': shipping_fee == 0,
            'free_shipping_threshold': self.FREE_SHIPPING_THRESHOLD,
            'remaining_for_free_shipping': remaining_for_free
        }


# Global instance
shipping_service = ShippingService()