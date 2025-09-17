"""
Checkout and Orders API routes
"""
from flask import jsonify, request
from app.blueprints.api import bp
from app.db import get_session, close_session
from app.models import models
from app.auth import get_current_user, login_required, get_cart_session
from sqlalchemy import text
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def make_json_response(data, status=200):
    """Create a JSON response with proper UTF-8 encoding"""
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, status

@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """Create order from cart (COD only)"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['shipping_address']
        for field in required_fields:
            if not data.get(field):
                return make_json_response({
                    'error': f'{field} is required'
                }, 400)
        
        shipping_address = data['shipping_address']
        note = data.get('note', '')
        coupon_code = data.get('coupon_code')
        
        # Validate shipping address fields
        address_fields = ['receiver', 'phone', 'line1', 'ward', 'district', 'city', 'province']
        for field in address_fields:
            if not shipping_address.get(field):
                return make_json_response({
                    'error': f'shipping_address.{field} is required'
                }, 400)
        
        # Get user's cart
        cart = session_db.query(models.Carts).filter(
            models.Carts.user_id == user.id
        ).first()
        
        if not cart:
            return make_json_response({
                'error': 'Cart is empty'
            }, 400)
        
        # Get cart items
        cart_items = session_db.query(models.CartItems).filter(
            models.CartItems.cart_id == cart.id
        ).all()
        
        if not cart_items:
            return make_json_response({
                'error': 'Cart is empty'
            }, 400)
        
        # Validate stock and calculate totals
        subtotal = 0
        order_items_data = []
        
        for item in cart_items:
            # Get variant and product info
            variant = session_db.query(models.ProductVariants).filter(
                models.ProductVariants.id == item.variant_id
            ).first()
            
            product = session_db.query(models.Products).filter(
                models.Products.id == item.product_id
            ).first()
            
            if not variant or not product:
                return make_json_response({
                    'error': f'Product variant not found: {item.variant_id}'
                }, 400)
            
            # Check stock
            stock_info = {'available': 0}
            try:
                stock_result = session_db.execute(
                    text("SELECT available FROM v_variant_stock WHERE variant_id = :variant_id"),
                    {"variant_id": item.variant_id}
                ).fetchone()
                if stock_result:
                    stock_info['available'] = stock_result[0] or 0
            except:
                pass
            
            if stock_info['available'] < item.qty:
                return make_json_response({
                    'error': f'Not enough stock for {product.name}. Available: {stock_info["available"]}'
                }, 400)
            
            line_total = item.unit_price * item.qty
            subtotal += line_total
            
            order_items_data.append({
                'product_id': item.product_id,
                'variant_id': item.variant_id,
                'name': f"{product.name} - {variant.name}",
                'unit_price': item.unit_price,
                'qty': item.qty,
                'line_total': line_total
            })
        
        # Apply coupon if provided
        discount_total = 0
        if coupon_code:
            coupon = session_db.query(models.Coupons).filter(
                models.Coupons.code == coupon_code,
                models.Coupons.is_active == True,
                models.Coupons.starts_at <= datetime.utcnow(),
                models.Coupons.ends_at >= datetime.utcnow()
            ).first()
            
            if coupon:
                # Check usage limit
                if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                    return make_json_response({
                        'error': 'Coupon usage limit exceeded'
                    }, 400)
                
                # Check minimum order
                if coupon.min_order and subtotal < coupon.min_order:
                    return make_json_response({
                        'error': f'Minimum order amount for this coupon is {coupon.min_order}'
                    }, 400)
                
                # Calculate discount
                if coupon.discount_type == 'percentage':
                    discount_total = min(subtotal * coupon.amount / 100, coupon.max_discount or subtotal)
                elif coupon.discount_type == 'fixed':
                    discount_total = min(coupon.amount, subtotal)
            else:
                return make_json_response({
                    'error': 'Invalid or expired coupon code'
                }, 400)
        
        # Calculate totals
        shipping_fee = 25000  # Fixed shipping fee for Vietnam
        tax_total = 0  # No tax for student project
        grand_total = subtotal - discount_total + shipping_fee + tax_total
        
        # Create shipping address
        address_id = str(uuid.uuid4())
        address = models.Addresses(
            id=address_id,
            user_id=user.id,
            receiver=shipping_address['receiver'],
            phone=shipping_address['phone'],
            line1=shipping_address['line1'],
            line2=shipping_address.get('line2', ''),
            ward=shipping_address['ward'],
            district=shipping_address['district'],
            city=shipping_address['city'],
            province=shipping_address['province'],
            postal_code=shipping_address.get('postal_code', ''),
            country_code='VN',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session_db.add(address)
        
        # Create order
        order_id = str(uuid.uuid4())
        order = models.Orders(
            id=order_id,
            user_id=user.id,
            status_code='pending',
            fulfillment_method='delivery',
            billing_address_id=address_id,
            shipping_address_id=address_id,
            subtotal=subtotal,
            discount_total=discount_total,
            shipping_fee=shipping_fee,
            tax_total=tax_total,
            grand_total=grand_total,
            currency='VND',
            note=note,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session_db.add(order)
        
        # Create order items
        for item_data in order_items_data:
            order_item = models.OrderItems(
                id=str(uuid.uuid4()),
                order_id=order_id,
                product_id=item_data['product_id'],
                variant_id=item_data['variant_id'],
                name=item_data['name'],
                unit_price=item_data['unit_price'],
                qty=item_data['qty'],
                line_total=item_data['line_total']
            )
            session_db.add(order_item)
        
        # Create payment transaction (COD)
        payment = models.PaymentTransactions(
            id=str(uuid.uuid4()),
            order_id=order_id,
            method_code='cod',
            amount=grand_total,
            status='created',
            provider_ref='',
            created_at=datetime.utcnow()
        )
        session_db.add(payment)
        
        # Update coupon usage
        if coupon_code and discount_total > 0:
            coupon.used_count = (coupon.used_count or 0) + 1
        
        # Reserve stock (optional - for simple implementation, we can skip this)
        # In a real system, you'd want to reserve stock when order is created
        
        # Clear cart
        for item in cart_items:
            session_db.delete(item)
        
        session_db.commit()
        
        return make_json_response({
            'message': 'Order created successfully',
            'order': {
                'id': order_id,
                'status': 'pending',
                'subtotal': subtotal,
                'discount_total': discount_total,
                'shipping_fee': shipping_fee,
                'tax_total': tax_total,
                'grand_total': grand_total,
                'currency': 'VND',
                'payment_method': 'COD'
            }
        }, 201)
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Checkout error: {str(e)}")
        return make_json_response({
            'error': 'Checkout failed'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """Get user's orders"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 50)
        
        # Query user's orders
        query = session_db.query(models.Orders).filter(
            models.Orders.user_id == user.id
        ).order_by(models.Orders.created_at.desc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        orders = query.offset(offset).limit(per_page).all()
        
        orders_list = []
        for order in orders:
            # Get order status
            status = session_db.query(models.OrderStatuses).filter(
                models.OrderStatuses.status_code == order.status_code
            ).first()
            
            orders_list.append({
                'id': order.id,
                'status_code': order.status_code,
                'status_label': status.label if status else order.status_code,
                'subtotal': order.subtotal,
                'discount_total': order.discount_total,
                'shipping_fee': order.shipping_fee,
                'grand_total': order.grand_total,
                'currency': order.currency,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat()
            })
        
        return make_json_response({
            'orders': orders_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        logger.error(f"Get orders error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get orders'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/orders/<order_id>', methods=['GET'])
@login_required
def get_order_detail(order_id):
    """Get order details"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        
        # Get order
        order = session_db.query(models.Orders).filter(
            models.Orders.id == order_id,
            models.Orders.user_id == user.id
        ).first()
        
        if not order:
            return make_json_response({
                'error': 'Order not found'
            }, 404)
        
        # Get order status
        status = session_db.query(models.OrderStatuses).filter(
            models.OrderStatuses.status_code == order.status_code
        ).first()
        
        # Get shipping address
        shipping_address = session_db.query(models.Addresses).filter(
            models.Addresses.id == order.shipping_address_id
        ).first()
        
        # Get order items
        order_items = session_db.query(models.OrderItems).filter(
            models.OrderItems.order_id == order_id
        ).all()
        
        items_list = []
        for item in order_items:
            # Get product image
            image = session_db.query(models.ProductMedia).filter(
                models.ProductMedia.product_id == item.product_id
            ).order_by(models.ProductMedia.sort_order).first()
            
            items_list.append({
                'id': item.id,
                'product_id': item.product_id,
                'variant_id': item.variant_id,
                'name': item.name,
                'unit_price': item.unit_price,
                'qty': item.qty,
                'line_total': item.line_total,
                'image_url': image.url if image else ''
            })
        
        # Get payment info
        payment = session_db.query(models.PaymentTransactions).filter(
            models.PaymentTransactions.order_id == order_id
        ).first()
        
        return make_json_response({
            'order': {
                'id': order.id,
                'status_code': order.status_code,
                'status_label': status.label if status else order.status_code,
                'fulfillment_method': order.fulfillment_method,
                'subtotal': order.subtotal,
                'discount_total': order.discount_total,
                'shipping_fee': order.shipping_fee,
                'tax_total': order.tax_total,
                'grand_total': order.grand_total,
                'currency': order.currency,
                'note': order.note,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat(),
                'shipping_address': {
                    'receiver': shipping_address.receiver,
                    'phone': shipping_address.phone,
                    'line1': shipping_address.line1,
                    'line2': shipping_address.line2,
                    'ward': shipping_address.ward,
                    'district': shipping_address.district,
                    'city': shipping_address.city,
                    'province': shipping_address.province,
                    'postal_code': shipping_address.postal_code
                } if shipping_address else None,
                'items': items_list,
                'payment': {
                    'method_code': payment.method_code,
                    'amount': payment.amount,
                    'status': payment.status
                } if payment else None
            }
        })
        
    except Exception as e:
        logger.error(f"Get order detail error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get order details'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)