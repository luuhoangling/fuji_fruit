"""
Discount model for coupon and promotion management
"""
from app.models import BaseModel
from app.extensions import db
from sqlalchemy import String, Numeric, DateTime, Boolean, Text, Integer
from datetime import datetime
from decimal import Decimal


class Discount(BaseModel):
    """Discount/Coupon model"""
    __tablename__ = 'discounts'
    
    # Basic info
    code = db.Column(String(50), unique=True, nullable=False, index=True)
    name = db.Column(String(100), nullable=False)
    description = db.Column(Text, nullable=True)
    
    # Discount details
    discount_type = db.Column(String(20), nullable=False, default='percentage')  # 'percentage' or 'fixed'
    discount_value = db.Column(Numeric(10, 2), nullable=False)  # Percentage (0-100) or fixed amount
    
    # Usage limits
    min_order_amount = db.Column(Numeric(10, 2), nullable=True, default=0)
    max_discount_amount = db.Column(Numeric(10, 2), nullable=True)
    usage_limit = db.Column(Integer, nullable=True)  # Total usage limit
    usage_limit_per_user = db.Column(Integer, nullable=True, default=1)
    used_count = db.Column(Integer, default=0, nullable=False)
    
    # Validity
    start_date = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(DateTime, nullable=False)
    is_active = db.Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Discount {self.code}>'
    
    @property
    def is_valid(self):
        """Check if discount is currently valid"""
        now = datetime.utcnow()
        return (
            self.is_active and 
            self.start_date <= now <= self.end_date and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def can_apply_to_order(self, order_amount, user_usage_count=0):
        """Check if discount can be applied to an order"""
        if not self.is_valid:
            return False, "Mã giảm giá không hợp lệ hoặc đã hết hạn"
        
        if order_amount < self.min_order_amount:
            return False, f"Đơn hàng phải có giá trị tối thiểu {self.min_order_amount:,.0f}đ"
        
        if self.usage_limit_per_user and user_usage_count >= self.usage_limit_per_user:
            return False, "Bạn đã sử dụng hết lượt áp dụng mã này"
        
        return True, "OK"
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if not self.is_valid:
            return 0
        
        if self.discount_type == 'percentage':
            discount = order_amount * (self.discount_value / 100)
        else:  # fixed
            discount = self.discount_value
        
        # Apply max discount limit if set
        if self.max_discount_amount and discount > self.max_discount_amount:
            discount = self.max_discount_amount
        
        return min(discount, order_amount)  # Can't discount more than order amount
    
    def increment_usage(self):
        """Increment usage count"""
        self.used_count += 1
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': float(self.discount_value),
            'min_order_amount': float(self.min_order_amount or 0),
            'max_discount_amount': float(self.max_discount_amount) if self.max_discount_amount else None,
            'usage_limit': self.usage_limit,
            'usage_limit_per_user': self.usage_limit_per_user,
            'used_count': self.used_count,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'is_valid': self.is_valid,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }