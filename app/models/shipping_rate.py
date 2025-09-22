"""
Shipping rate model for delivery fee management
"""
from app.models import BaseModel
from app.extensions import db
from sqlalchemy import String, Numeric, Boolean, Text, Integer
from decimal import Decimal


class ShippingRate(BaseModel):
    """Shipping rate model for different regions/methods"""
    __tablename__ = 'shipping_rates'
    
    # Basic info
    name = db.Column(String(100), nullable=False)
    description = db.Column(Text, nullable=True)
    
    # Geographic scope
    province = db.Column(String(100), nullable=True)  # Tỉnh/Thành phố
    district = db.Column(String(100), nullable=True)  # Quận/Huyện
    ward = db.Column(String(100), nullable=True)     # Phường/Xã
    
    # Shipping details
    shipping_method = db.Column(String(50), nullable=False, default='standard')  # standard, express, overnight
    base_fee = db.Column(Numeric(10, 2), nullable=False, default=0)
    per_kg_fee = db.Column(Numeric(10, 2), nullable=False, default=0)
    free_shipping_threshold = db.Column(Numeric(10, 2), nullable=True)  # Free shipping if order > threshold
    
    # Delivery time
    estimated_days_min = db.Column(Integer, nullable=False, default=1)
    estimated_days_max = db.Column(Integer, nullable=False, default=3)
    
    # Status
    is_active = db.Column(Boolean, default=True, nullable=False)
    priority = db.Column(Integer, default=0, nullable=False)  # Higher priority shown first
    
    def __repr__(self):
        return f'<ShippingRate {self.name}>'
    
    def calculate_shipping_fee(self, order_amount, weight_kg=1):
        """Calculate shipping fee for given order amount and weight"""
        if not self.is_active:
            return 0
        
        # Check for free shipping
        if self.free_shipping_threshold and order_amount >= self.free_shipping_threshold:
            return 0
        
        # Calculate base fee + weight fee
        total_fee = self.base_fee + (self.per_kg_fee * weight_kg)
        return max(total_fee, 0)
    
    def matches_location(self, province=None, district=None, ward=None):
        """Check if this shipping rate applies to given location"""
        # If shipping rate has no location restrictions, it applies everywhere
        if not self.province and not self.district and not self.ward:
            return True
        
        # Check province match
        if self.province and province:
            if self.province.lower() != province.lower():
                return False
        
        # Check district match
        if self.district and district:
            if self.district.lower() != district.lower():
                return False
        
        # Check ward match
        if self.ward and ward:
            if self.ward.lower() != ward.lower():
                return False
        
        return True
    
    @property
    def estimated_delivery_text(self):
        """Get estimated delivery time as text"""
        if self.estimated_days_min == self.estimated_days_max:
            return f"{self.estimated_days_min} ngày"
        else:
            return f"{self.estimated_days_min}-{self.estimated_days_max} ngày"
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'province': self.province,
            'district': self.district,
            'ward': self.ward,
            'shipping_method': self.shipping_method,
            'base_fee': float(self.base_fee),
            'per_kg_fee': float(self.per_kg_fee),
            'free_shipping_threshold': float(self.free_shipping_threshold) if self.free_shipping_threshold else None,
            'estimated_days_min': self.estimated_days_min,
            'estimated_days_max': self.estimated_days_max,
            'estimated_delivery_text': self.estimated_delivery_text,
            'is_active': self.is_active,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }