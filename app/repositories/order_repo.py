"""Order repository"""

from app.repositories import BaseRepository
from app.models import Order, OrderItem, OrderEvent, OrderStatus
from app.extensions import db
from sqlalchemy import desc, or_
from typing import List, Optional, Tuple


class OrderRepository(BaseRepository):
    """Repository for Order operations"""
    
    def __init__(self, db_session=None):
        super().__init__(Order)
        self.db_session = db_session
    
    def get_by_code(self, order_code: str) -> Optional[Order]:
        """Get order by order code"""
        return self.model.query.filter_by(order_code=order_code).first()
    
    def get_by_code_for_update(self, order_code: str) -> Optional[Order]:
        """Get order by code with row lock"""
        return self.model.query.filter_by(order_code=order_code)\
                   .with_for_update().first()
    
    def create_order(self, order_data: dict, items_data: List[dict]) -> Order:
        """Create order with items in transaction"""
        # Create order
        order = Order(**order_data)
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for item_data in items_data:
            item_data['order_id'] = order.id
            item = OrderItem(**item_data)
            db.session.add(item)
        
        return order
    
    def add_event(self, order_id: int, event_type: str, note: str = None):
        """Add event to order timeline"""
        event = OrderEvent(
            order_id=order_id,
            event_type=event_type,
            note=note
        )
        db.session.add(event)
    
    def search_orders(self, 
                     status: str = None,
                     search_query: str = '',
                     page: int = 1,
                     per_page: int = 20) -> Tuple[List[Order], int]:
        """Search orders with filters"""
        query = self.model.query
        
        # Status filter
        if status:
            query = query.filter_by(status=OrderStatus(status))
        
        # Text search in order_code, customer_name, phone
        if search_query:
            query = query.filter(
                or_(
                    Order.order_code.ilike(f'%{search_query}%'),
                    Order.customer_name.ilike(f'%{search_query}%'),
                    Order.phone.ilike(f'%{search_query}%')
                )
            )
        
        query = query.order_by(desc(Order.created_at))
        
        # Get total count
        total = query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        orders = query.offset(offset).limit(per_page).all()
        
        return orders, total
    
    def get_order_detail(self, order_id: int) -> Optional[Order]:
        """Get order with all relations"""
        return self.model.query.options(
            db.joinedload(Order.items),
            db.joinedload(Order.events)
        ).filter_by(id=order_id).first()
    
    def get_orders_by_status(self, status: str, page: int = 1, per_page: int = 20) -> Tuple[List[Order], int]:
        """Get orders by status with pagination"""
        query = self.model.query.filter_by(status=status)
        query = query.order_by(desc(Order.created_at))
        
        # Get total count
        total = query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        orders = query.offset(offset).limit(per_page).all()
        
        return orders, total
    
    def update_order_status(self, order_id: int, new_status: str, note: str = None) -> bool:
        """Update order status and add event"""
        try:
            order = self.get_by_id(order_id)
            if not order:
                return False
            
            old_status = order.status
            order.status = new_status
            
            # Add status change event
            self.add_event(order_id, new_status, note or f"Đơn hàng chuyển từ {old_status} sang {new_status}")
            
            return True
        except Exception:
            return False
    
    def cancel_order(self, order_id: int, note: str = None) -> bool:
        """Cancel order if possible"""
        try:
            order = self.get_by_id(order_id)
            if not order:
                return False
            
            # Only allow cancellation for pending and confirmed orders
            if order.status not in ['pending', 'confirmed']:
                return False
            
            order.status = 'cancelled'
            self.add_event(order_id, 'cancelled', note or "Đơn hàng đã được hủy")
            
            return True
        except Exception:
            return False


class OrderItemRepository(BaseRepository):
    """Repository for OrderItem operations"""
    
    def __init__(self):
        super().__init__(OrderItem)


class OrderEventRepository(BaseRepository):
    """Repository for OrderEvent operations"""
    
    def __init__(self):
        super().__init__(OrderEvent)


# Global instances
order_repo = OrderRepository()
order_item_repo = OrderItemRepository()
order_event_repo = OrderEventRepository()