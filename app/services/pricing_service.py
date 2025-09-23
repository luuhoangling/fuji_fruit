"""Pricing service for handling product prices"""

from app.repositories.product_repo import product_repo
from typing import Optional


class PricingService:
    """Service for pricing logic"""
    
    def get_effective_price(self, product_id: int) -> Optional[float]:
        """Get current effective price for a product"""
        product = product_repo.get_effective_price(product_id)
        return float(product.effective_price) if product else None
    
    def get_effective_price_for_order(self, product_id: int) -> Optional[float]:
        """Get effective price with lock for order creation"""
        return product_repo.get_effective_price_for_update(product_id)
    
    def calculate_savings(self, regular_price: float, sale_price: float) -> dict:
        """Calculate savings amount and percentage"""
        # Ensure both prices are float to avoid decimal/float operation errors
        regular_price = float(regular_price)
        sale_price = float(sale_price)
        
        if sale_price >= regular_price:
            return {'amount': 0, 'percentage': 0}
        
        savings_amount = regular_price - sale_price
        savings_percentage = (savings_amount / regular_price) * 100
        
        return {
            'amount': round(savings_amount, 2),
            'percentage': round(savings_percentage, 1)
        }
    
    def is_on_sale(self, product_id: int) -> bool:
        """Check if product is currently on sale"""
        from datetime import datetime
        
        product = product_repo.get_by_id(product_id)
        if not product or not product.sale_price:
            return False
        
        now = datetime.utcnow()
        sale_active = True
        
        # Check sale start date
        if product.sale_start and product.sale_start > now:
            sale_active = False
        
        # Check sale end date
        if product.sale_end and product.sale_end < now:
            sale_active = False
            
        return sale_active


# Global instance
pricing_service = PricingService()