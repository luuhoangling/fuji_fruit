"""Order related models"""

from app.extensions import db
from datetime import datetime
from enum import Enum


class PaymentMethod(Enum):
    COD = 'COD'
    MOCK_TRANSFER = 'MOCK_TRANSFER'


class PaymentStatus(Enum):
    UNPAID = 'unpaid'
    MOCK_PAID = 'mock_paid'


class OrderStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    FULFILLED = 'fulfilled'
    CANCELLED = 'cancelled'


class EventType(Enum):
    PLACED = 'placed'
    MOCK_PAID = 'mock_paid'
    CONFIRMED = 'confirmed'
    FULFILLED = 'fulfilled'
    CANCELLED = 'cancelled'
    RESTOCKED = 'restocked'


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    # Define columns exactly matching database schema
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), nullable=True)  # UUID for authenticated users
    order_code = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    province = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    ward = db.Column(db.String(100), nullable=True)
    
    payment_method = db.Column(db.String(20), default='COD', nullable=False)
    payment_status = db.Column(db.String(20), default='unpaid', nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Note: No updated_at column in database schema
    
    # Financial fields
    subtotal = db.Column(db.Numeric(12, 2), nullable=True)
    shipping_fee = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    discount_amt = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    discount_code = db.Column(db.String(50), nullable=True)  # Applied discount code
    grand_total = db.Column(db.Numeric(12, 2), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    events = db.relationship('OrderEvent', backref='order', cascade='all, delete-orphan', 
                           order_by='OrderEvent.created_at.desc()')
    
    def __repr__(self):
        return f'<Order {self.order_code}>'
    
    def to_dict(self, include_relations=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'order_code': self.order_code,
            'customer_name': self.customer_name,
            'phone': self.phone,
            'address': self.address,
            'province': self.province,
            'district': self.district,
            'ward': self.ward,
            'payment_method': self.payment_method,  # Already string now
            'payment_status': self.payment_status,  # Already string now
            'status': self.status,  # Already string now
            'amounts': {
                'subtotal': float(self.subtotal) if self.subtotal else None,
                'shipping_fee': float(self.shipping_fee),
                'discount': float(self.discount_amt),
                'grand_total': float(self.grand_total)
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result['items'] = [item.to_dict() for item in self.items]
            result['events'] = [event.to_dict() for event in self.events]
            
        return result


class OrderItem(db.Model):
    """Order item model"""
    __tablename__ = 'order_items'
    
    # Define columns explicitly to match database schema  
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Numeric(12, 2), nullable=False)
    # Note: No created_at or updated_at columns to match database schema
    
    # Relationship to product (for reference)
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'unit_price': float(self.unit_price),
            'qty': self.qty,
            'line_total': float(self.line_total)
        }


class OrderEvent(db.Model):
    """Order event model for timeline tracking"""
    __tablename__ = 'order_events'
    
    # Define columns exactly matching database schema
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'), nullable=False)
    event_type = db.Column(db.String(20), nullable=False)  # String instead of Enum
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Note: No updated_at column to match database schema
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,  # Already string
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }