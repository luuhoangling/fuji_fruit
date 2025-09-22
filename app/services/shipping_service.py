"""
Shipping service for calculating shipping fees and managing shipping rates
"""
from typing import List, Dict, Optional, Tuple
from app.models.shipping_rate import ShippingRate
from sqlalchemy.orm import Session
from decimal import Decimal


class ShippingService:
    """Service for shipping fee calculation and management"""
    
    def __init__(self, session: Session = None):
        self.session = session
    
    def get_shipping_rates_for_location(self, province: str = None, district: str = None, ward: str = None) -> List[ShippingRate]:
        """Get applicable shipping rates for a location"""
        if not self.session:
            return []
            
        query = self.session.query(ShippingRate).filter(
            ShippingRate.is_active == True
        )
        
        # Find rates that match the location or apply nationwide
        applicable_rates = []
        
        for rate in query.all():
            if rate.matches_location(province, district, ward):
                applicable_rates.append(rate)
        
        # Sort by priority (highest first) then by base fee (lowest first)
        applicable_rates.sort(key=lambda r: (-r.priority, r.base_fee))
        
        return applicable_rates
    
    def calculate_shipping_fee(self, province: str = None, district: str = None, ward: str = None, 
                             order_amount: float = 0, weight_kg: float = 1, shipping_method: str = 'standard') -> Dict:
        """
        Calculate shipping fee for given location and order details
        """
        if not self.session:
            return self._get_legacy_shipping(order_amount, province)
            
        applicable_rates = self.get_shipping_rates_for_location(province, district, ward)
        
        if not applicable_rates:
            return self._get_legacy_shipping(order_amount, province)
        
        # Find the best rate for requested method
        selected_rate = None
        for rate in applicable_rates:
            if rate.shipping_method == shipping_method:
                selected_rate = rate
                break
        
        # If no rate found for specific method, use the first (highest priority) rate
        if not selected_rate:
            selected_rate = applicable_rates[0]
        
        # Calculate shipping fee
        shipping_fee = selected_rate.calculate_shipping_fee(order_amount, weight_kg)
        is_free = shipping_fee == 0
        
        # Get all available methods for this location
        available_methods = []
        for rate in applicable_rates:
            method_fee = rate.calculate_shipping_fee(order_amount, weight_kg)
            available_methods.append({
                'id': rate.id,
                'name': rate.name,
                'method': rate.shipping_method,
                'fee': float(method_fee),
                'estimated_delivery': rate.estimated_delivery_text,
                'is_free': method_fee == 0
            })
        
        return {
            'shipping_fee': float(shipping_fee),
            'shipping_rate': selected_rate.to_dict(),
            'is_free': is_free,
            'available_methods': available_methods
        }
    
    def _get_legacy_shipping(self, order_amount: float, province: str = None) -> Dict:
        """Legacy shipping calculation for backward compatibility"""
        # Shipping fee rules (in VND)
        FREE_SHIPPING_THRESHOLD = 500000
        DEFAULT_SHIPPING_FEE = 30000
        
        # Province-based shipping fees
        PROVINCE_SHIPPING_FEES = {
            'Hà Nội': 25000,
            'TP Hồ Chí Minh': 25000,
            'Đà Nẵng': 30000,
            'Hải Phòng': 30000,
            'Cần Thơ': 35000,
        }
        
        # Free shipping for large orders
        if order_amount >= FREE_SHIPPING_THRESHOLD:
            fee = 0
        # Province-specific shipping
        elif province and province in PROVINCE_SHIPPING_FEES:
            fee = PROVINCE_SHIPPING_FEES[province]
        else:
            fee = DEFAULT_SHIPPING_FEE
        
        return {
            'shipping_fee': float(fee),
            'shipping_rate': {
                'name': 'Phí ship mặc định',
                'shipping_method': 'standard',
                'estimated_delivery_text': '2-5 ngày'
            },
            'is_free': fee == 0,
            'available_methods': []
        }
    
    def compute_shipping(self, subtotal: float, province: str = None, district: str = None, ward: str = None) -> float:
        """Legacy method for backward compatibility"""
        result = self.calculate_shipping_fee(province, district, ward, subtotal)
        return result['shipping_fee']
    
    def get_shipping_info(self, subtotal: float, province: str = None) -> Dict:
        """Get detailed shipping information"""
        shipping_fee = self.compute_shipping(subtotal, province)
        FREE_SHIPPING_THRESHOLD = 500000
        
        remaining_for_free = max(0, FREE_SHIPPING_THRESHOLD - subtotal)
        
        return {
            'fee': shipping_fee,
            'is_free': shipping_fee == 0,
            'free_shipping_threshold': FREE_SHIPPING_THRESHOLD,
            'remaining_for_free_shipping': remaining_for_free
        }
    
    def create_shipping_rate(self, rate_data: Dict) -> ShippingRate:
        """Create a new shipping rate"""
        if not self.session:
            raise ValueError("Database session required")
            
        shipping_rate = ShippingRate(**rate_data)
        self.session.add(shipping_rate)
        self.session.flush()  # To get the ID
        return shipping_rate
    
    def update_shipping_rate(self, rate_id: int, rate_data: Dict) -> Optional[ShippingRate]:
        """Update an existing shipping rate"""
        if not self.session:
            return None
            
        shipping_rate = self.session.query(ShippingRate).get(rate_id)
        if not shipping_rate:
            return None
        
        for key, value in rate_data.items():
            if hasattr(shipping_rate, key):
                setattr(shipping_rate, key, value)
        
        return shipping_rate
    
    def delete_shipping_rate(self, rate_id: int) -> bool:
        """Soft delete a shipping rate"""
        if not self.session:
            return False
            
        shipping_rate = self.session.query(ShippingRate).get(rate_id)
        if not shipping_rate:
            return False
        
        shipping_rate.is_active = False
        return True
    
    def get_admin_shipping_rates(self, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int]:
        """Get shipping rates for admin panel with pagination"""
        if not self.session:
            return [], 0
            
        query = self.session.query(ShippingRate)
        
        total = query.count()
        shipping_rates = query.order_by(
            ShippingRate.priority.desc(), 
            ShippingRate.created_at.desc()
        ).offset((page - 1) * per_page).limit(per_page).all()
        
        return [rate.to_dict() for rate in shipping_rates], total


# Global instance for backward compatibility
shipping_service = ShippingService()