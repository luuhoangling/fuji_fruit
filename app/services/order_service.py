"""Order service for managing orders and transactions"""

import string
import random
from app.repositories.order_repo import order_repo
from app.repositories.product_repo import product_repo
from app.services.pricing_service import pricing_service
from app.services.shipping_service import shipping_service
from app.services.stock_service import stock_service, OutOfStockError
from app.models import PaymentMethod, PaymentStatus, OrderStatus, EventType
from app.extensions import db
from typing import Dict, List, Tuple


class OrderError(Exception):
    """Base exception for order-related errors"""
    pass


class OrderService:
    """Service for order management"""
    
    def generate_order_code(self) -> str:
        """Generate unique order code like FJ-8X2K9C"""
        while True:
            # Generate 6 random alphanumeric characters
            code_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order_code = f"FJ-{code_part}"
            
            # Check if code already exists
            if not order_repo.get_by_code(order_code):
                return order_code
    
    def create_order(self, payload: Dict, idempotency_key: str = None) -> Dict:
        """Create new order with stock reservation"""
        
        # Check idempotency (simplified - in production use Redis/DB)
        # For now, just proceed with order creation
        
        try:
            with db.session.begin():
                # Validate and prepare data
                customer = payload['customer']
                payment_method = PaymentMethod(payload['payment_method'])
                items = payload['items']
                
                # Generate order code
                order_code = self.generate_order_code()
                
                # Create order record
                order_data = {
                    'order_code': order_code,
                    'customer_name': customer['name'],
                    'phone': customer['phone'],
                    'address': customer['address'],
                    'province': customer.get('province'),
                    'district': customer.get('district'),
                    'ward': customer.get('ward'),
                    'payment_method': payment_method,
                    'payment_status': PaymentStatus.UNPAID,
                    'status': OrderStatus.PENDING
                }
                
                # Process order items
                items_data = []
                subtotal = 0
                
                for item in items:
                    product_id = item['product_id']
                    qty = item['qty']
                    
                    # Get product and effective price
                    product = product_repo.get_by_id(product_id)
                    if not product or not product.is_active:
                        raise OrderError(f"Product {product_id} not found or inactive")
                    
                    effective_price = pricing_service.get_effective_price_for_order(product_id)
                    if effective_price is None:
                        raise OrderError(f"Could not get price for product {product_id}")
                    
                    # Reserve stock
                    try:
                        stock_service.reserve_stock(product_id, qty)
                    except OutOfStockError as e:
                        raise OrderError(f"Insufficient stock for {product.name}: requested {e.requested}, available {e.available}")
                    
                    # Calculate line total
                    line_total = effective_price * qty
                    subtotal += line_total
                    
                    # Prepare item data
                    items_data.append({
                        'product_id': product_id,
                        'product_name': product.name,
                        'unit_price': effective_price,
                        'qty': qty,
                        'line_total': line_total
                    })
                
                # Calculate shipping
                shipping_fee = shipping_service.compute_shipping(subtotal, customer.get('province'))
                
                # Calculate totals
                discount_amt = 0  # No discounts for now
                grand_total = subtotal + shipping_fee - discount_amt
                
                # Update order data with totals
                order_data.update({
                    'subtotal': subtotal,
                    'shipping_fee': shipping_fee,
                    'discount_amt': discount_amt,
                    'grand_total': grand_total,
                    'total_amount': grand_total
                })
                
                # Create order with items
                order = order_repo.create_order(order_data, items_data)
                
                # Add initial event
                order_repo.add_event(order.id, EventType.PLACED.value, "Order placed")
                
                db.session.commit()
                
                # Return order response
                return self._format_order_response(order)
                
        except Exception as e:
            db.session.rollback()
            raise OrderError(f"Failed to create order: {str(e)}")
    
    def get_order_by_code(self, order_code: str) -> Dict:
        """Get order details by order code"""
        order = order_repo.get_by_code(order_code)
        if not order:
            raise OrderError(f"Order {order_code} not found")
        
        return self._format_order_detail_response(order)
    
    def mock_pay(self, order_code: str) -> Dict:
        """Mark order as mock paid"""
        try:
            with db.session.begin():
                order = order_repo.get_by_code_for_update(order_code)
                if not order:
                    raise OrderError(f"Order {order_code} not found")
                
                if order.payment_status == PaymentStatus.MOCK_PAID:
                    return self._format_order_response(order)
                
                # Update payment status
                order.payment_status = PaymentStatus.MOCK_PAID
                order_repo.add_event(order.id, EventType.MOCK_PAID.value, "User marked as paid")
                
                # Auto-confirm if still pending
                if order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.CONFIRMED
                    order_repo.add_event(order.id, EventType.CONFIRMED.value, "Auto-confirm after mock pay")
                
                db.session.commit()
                return self._format_order_response(order)
                
        except Exception as e:
            db.session.rollback()
            raise OrderError(f"Failed to process payment: {str(e)}")
    
    def update_order_status(self, order_code: str, new_status: str) -> Dict:
        """Update order status (admin function)"""
        try:
            with db.session.begin():
                order = order_repo.get_by_code_for_update(order_code)
                if not order:
                    raise OrderError(f"Order {order_code} not found")
                
                old_status = order.status
                new_status_enum = OrderStatus(new_status)
                
                # Validate status transition
                if old_status == OrderStatus.FULFILLED and new_status_enum != OrderStatus.FULFILLED:
                    raise OrderError("Cannot change status of fulfilled order")
                
                # Update status
                order.status = new_status_enum
                
                # Handle stock restoration for cancelled orders
                if new_status_enum == OrderStatus.CANCELLED and old_status != OrderStatus.CANCELLED:
                    for item in order.items:
                        stock_service.release_stock(item.product_id, item.qty)
                    order_repo.add_event(order.id, EventType.RESTOCKED.value, "Inventory restored after cancel")
                
                # Add status change event
                order_repo.add_event(order.id, new_status_enum.value, f"Status changed from {old_status.value} to {new_status}")
                
                db.session.commit()
                return self._format_order_response(order)
                
        except Exception as e:
            db.session.rollback()
            raise OrderError(f"Failed to update status: {str(e)}")
    
    def search_orders(self, status: str = None, query: str = '', page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int]:
        """Search orders with filters"""
        orders, total = order_repo.search_orders(status, query, page, per_page)
        
        return [self._format_order_response(order) for order in orders], total
    
    def _format_order_response(self, order) -> Dict:
        """Format order for API response"""
        return {
            'order_code': order.order_code,
            'status': order.status.value,
            'payment_status': order.payment_status.value,
            'amounts': {
                'subtotal': float(order.subtotal) if order.subtotal else None,
                'shipping_fee': float(order.shipping_fee),
                'discount': float(order.discount_amt),
                'grand_total': float(order.grand_total)
            },
            'items': [
                {
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'unit_price': float(item.unit_price),
                    'qty': item.qty,
                    'line_total': float(item.line_total)
                }
                for item in order.items
            ]
        }
    
    def _format_order_detail_response(self, order) -> Dict:
        """Format detailed order for API response"""
        response = self._format_order_response(order)
        
        # Add customer info and events
        response.update({
            'customer': {
                'name': order.customer_name,
                'phone': order.phone,
                'address': order.address,
                'province': order.province,
                'district': order.district,
                'ward': order.ward
            },
            'payment_method': order.payment_method.value,
            'events': [
                {
                    'type': event.event_type.value,
                    'time': event.created_at.isoformat() if event.created_at else None,
                    'note': event.note
                }
                for event in order.events
            ],
            'created_at': order.created_at.isoformat() if order.created_at else None
        })
        
        return response


# Global instance
order_service = OrderService()