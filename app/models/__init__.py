"""Base model class"""

from app.extensions import db
from datetime import datetime


class BaseModel(db.Model):
    """Base model with common fields"""
    __abstract__ = True
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Import all models to make them available
from .category import Category
from .product import Product, ProductCategory, ProductImage, ProductStock, ProductEffectivePrice, ProductRating
from .review import ProductReview
from .order import Order, OrderItem, OrderEvent, PaymentMethod, PaymentStatus, OrderStatus, EventType
from .user import User
from .discount import Discount
from .shipping_rate import ShippingRate
from .user_discount_usage import UserDiscountUsage

__all__ = [
    'BaseModel', 'Category', 'Product', 'ProductCategory', 'ProductImage', 
    'ProductStock', 'ProductEffectivePrice', 'ProductRating', 'ProductReview',
    'Order', 'OrderItem', 'OrderEvent', 'PaymentMethod', 'PaymentStatus', 
    'OrderStatus', 'EventType', 'User', 'Discount', 'ShippingRate', 'UserDiscountUsage'
]