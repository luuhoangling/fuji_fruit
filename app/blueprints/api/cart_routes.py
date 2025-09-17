"""
Shopping Cart API routes
"""
from flask import jsonify, request, session
from app.blueprints.api import bp
from app.db import get_session, close_session
from app.models import models
from app.auth import get_current_user, get_cart_session
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

def get_or_create_cart(session_db, user=None):
    """Get or create cart for current user/session"""
    cart = None
    
    if user:
        # Logged in user - get user cart
        cart = session_db.query(models.Carts).filter(
            models.Carts.user_id == user.id
        ).first()
        
        if not cart:
            cart = models.Carts(
                id=str(uuid.uuid4()),
                user_id=user.id,
                session_id=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session_db.add(cart)
            session_db.commit()
    else:
        # Guest user - get session cart
        cart_session_id = get_cart_session()
        cart = session_db.query(models.Carts).filter(
            models.Carts.session_id == cart_session_id
        ).first()
        
        if not cart:
            cart = models.Carts(
                id=str(uuid.uuid4()),
                user_id=None,
                session_id=cart_session_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session_db.add(cart)
            session_db.commit()
    
    return cart

@bp.route('/cart', methods=['GET'])
def get_cart():
    """Get current cart contents"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        
        cart = get_or_create_cart(session_db, user)
        
        # Get cart items with product and variant info
        cart_items = session_db.query(models.CartItems).filter(
            models.CartItems.cart_id == cart.id
        ).all()
        
        items_list = []
        total_amount = 0
        
        for item in cart_items:
            # Get product info
            product = session_db.query(models.Products).filter(
                models.Products.id == item.product_id
            ).first()
            
            # Get variant info
            variant = session_db.query(models.ProductVariants).filter(
                models.ProductVariants.id == item.variant_id
            ).first()
            
            # Get product image
            image = session_db.query(models.ProductMedia).filter(
                models.ProductMedia.product_id == product.id
            ).order_by(models.ProductMedia.sort_order).first()
            
            # Get stock info
            stock_info = {'available': 0}
            try:
                stock_result = session_db.execute(
                    text("SELECT available FROM v_variant_stock WHERE variant_id = :variant_id"),
                    {"variant_id": variant.id}
                ).fetchone()
                if stock_result:
                    stock_info['available'] = stock_result[0] or 0
            except:
                pass
            
            line_total = item.unit_price * item.qty
            total_amount += line_total
            
            items_list.append({
                'id': item.id,
                'product_id': product.id,
                'variant_id': variant.id,
                'product_name': product.name,
                'variant_name': variant.name,
                'sku': variant.sku,
                'unit_price': item.unit_price,
                'qty': item.qty,
                'line_total': line_total,
                'image_url': image.url if image else '',
                'available': stock_info['available'],
                'size_key': variant.size_key if hasattr(variant, 'size_key') else '',
                'weight_key': variant.weight_key if hasattr(variant, 'weight_key') else ''
            })
        
        return make_json_response({
            'cart': {
                'id': cart.id,
                'items': items_list,
                'total_amount': total_amount,
                'total_items': len(items_list)
            }
        })
        
    except Exception as e:
        logger.error(f"Get cart error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get cart'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/cart/items', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        data = request.get_json()
        
        # Validate input
        if not data.get('variant_id') or not data.get('qty'):
            return make_json_response({
                'error': 'variant_id and qty are required'
            }, 400)
        
        variant_id = data['variant_id']
        qty = int(data['qty'])
        
        if qty <= 0:
            return make_json_response({
                'error': 'Quantity must be greater than 0'
            }, 400)
        
        # Check if variant exists and get current price
        variant = session_db.query(models.ProductVariants).filter(
            models.ProductVariants.id == variant_id,
            models.ProductVariants.is_active == True
        ).first()
        
        if not variant:
            return make_json_response({
                'error': 'Product variant not found'
            }, 404)
        
        # Check stock availability
        stock_info = {'available': 0}
        try:
            stock_result = session_db.execute(
                text("SELECT available FROM v_variant_stock WHERE variant_id = :variant_id"),
                {"variant_id": variant_id}
            ).fetchone()
            if stock_result:
                stock_info['available'] = stock_result[0] or 0
        except:
            pass
        
        if stock_info['available'] < qty:
            return make_json_response({
                'error': f'Not enough stock. Available: {stock_info["available"]}'
            }, 400)
        
        # Get or create cart
        cart = get_or_create_cart(session_db, user)
        
        # Check if item already exists in cart
        existing_item = session_db.query(models.CartItems).filter(
            models.CartItems.cart_id == cart.id,
            models.CartItems.variant_id == variant_id
        ).first()
        
        if existing_item:
            # Update quantity
            new_qty = existing_item.qty + qty
            if stock_info['available'] < new_qty:
                return make_json_response({
                    'error': f'Not enough stock. Available: {stock_info["available"]}, in cart: {existing_item.qty}'
                }, 400)
            
            existing_item.qty = new_qty
            existing_item.unit_price = variant.list_price  # Update to current price
        else:
            # Create new cart item
            cart_item = models.CartItems(
                id=str(uuid.uuid4()),
                cart_id=cart.id,
                product_id=variant.product_id,
                variant_id=variant_id,
                qty=qty,
                unit_price=variant.list_price,
                added_at=datetime.utcnow()
            )
            session_db.add(cart_item)
        
        # Update cart timestamp
        cart.updated_at = datetime.utcnow()
        session_db.commit()
        
        return make_json_response({
            'message': 'Item added to cart successfully'
        }, 201)
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Add to cart error: {str(e)}")
        return make_json_response({
            'error': 'Failed to add item to cart'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/cart/items/<item_id>', methods=['PATCH'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('qty'):
            return make_json_response({
                'error': 'qty is required'
            }, 400)
        
        qty = int(data['qty'])
        if qty <= 0:
            return make_json_response({
                'error': 'Quantity must be greater than 0'
            }, 400)
        
        # Get cart item
        cart_item = session_db.query(models.CartItems).filter(
            models.CartItems.id == item_id
        ).first()
        
        if not cart_item:
            return make_json_response({
                'error': 'Cart item not found'
            }, 404)
        
        # Verify cart ownership
        cart = session_db.query(models.Carts).filter(
            models.Carts.id == cart_item.cart_id
        ).first()
        
        cart_session_id = get_cart_session()
        if not ((user and cart.user_id == user.id) or (not user and cart.session_id == cart_session_id)):
            return make_json_response({
                'error': 'Access denied'
            }, 403)
        
        # Check stock availability
        stock_info = {'available': 0}
        try:
            stock_result = session_db.execute(
                text("SELECT available FROM v_variant_stock WHERE variant_id = :variant_id"),
                {"variant_id": cart_item.variant_id}
            ).fetchone()
            if stock_result:
                stock_info['available'] = stock_result[0] or 0
        except:
            pass
        
        if stock_info['available'] < qty:
            return make_json_response({
                'error': f'Not enough stock. Available: {stock_info["available"]}'
            }, 400)
        
        # Update quantity
        cart_item.qty = qty
        cart.updated_at = datetime.utcnow()
        session_db.commit()
        
        return make_json_response({
            'message': 'Cart item updated successfully'
        })
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Update cart item error: {str(e)}")
        return make_json_response({
            'error': 'Failed to update cart item'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/cart/items/<item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    """Remove item from cart"""
    session_db = None
    try:
        session_db = get_session()
        user = get_current_user()
        
        # Get cart item
        cart_item = session_db.query(models.CartItems).filter(
            models.CartItems.id == item_id
        ).first()
        
        if not cart_item:
            return make_json_response({
                'error': 'Cart item not found'
            }, 404)
        
        # Verify cart ownership
        cart = session_db.query(models.Carts).filter(
            models.Carts.id == cart_item.cart_id
        ).first()
        
        cart_session_id = get_cart_session()
        if not ((user and cart.user_id == user.id) or (not user and cart.session_id == cart_session_id)):
            return make_json_response({
                'error': 'Access denied'
            }, 403)
        
        # Remove item
        session_db.delete(cart_item)
        cart.updated_at = datetime.utcnow()
        session_db.commit()
        
        return make_json_response({
            'message': 'Item removed from cart successfully'
        })
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Remove cart item error: {str(e)}")
        return make_json_response({
            'error': 'Failed to remove cart item'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)