"""
User discount usage tracking model
"""
from app.models import BaseModel
from app.extensions import db
from sqlalchemy import String, Integer, BigInteger, ForeignKey, DateTime
from datetime import datetime


class UserDiscountUsage(BaseModel):
    """Track discount usage by users"""
    __tablename__ = 'user_discount_usage'
    
    user_id = db.Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    discount_id = db.Column(BigInteger, ForeignKey('discounts.id'), nullable=False, index=True)
    order_id = db.Column(String(36), nullable=True, index=True)  # No FK constraint due to type mismatch
    
    # Usage tracking
    used_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='discount_usages')
    discount = db.relationship('Discount', backref='user_usages')
    # Note: No direct relationship with Order due to type mismatch
    
    def __repr__(self):
        return f'<UserDiscountUsage user_id={self.user_id} discount_id={self.discount_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'discount_id': self.discount_id,
            'order_id': self.order_id,
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }