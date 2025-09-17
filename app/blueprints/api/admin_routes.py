"""
Admin API routes for managing products, categories, brands, and orders
"""
from flask import jsonify, request
from app.blueprints.api import bp
from app.db import get_session, close_session
from app.models import models
from app.auth import admin_required
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def make_json_response(data, status=200):
    """Create a JSON response with proper UTF-8 encoding"""
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, status

# ========== CATEGORIES MANAGEMENT ==========

@bp.route('/admin/categories', methods=['GET'])
@admin_required
def admin_get_categories():
    """Get all categories for admin"""
    session_db = None
    try:
        session_db = get_session()
        
        categories = session_db.query(models.Categories).order_by(
            models.Categories.sort_order,
            models.Categories.name
        ).all()
        
        categories_list = []
        for cat in categories:
            categories_list.append({
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'parent_id': cat.parent_id,
                'sort_order': cat.sort_order,
                'is_active': cat.is_active,
                'description': getattr(cat, 'description', ''),
                'created_at': cat.created_at.isoformat() if hasattr(cat, 'created_at') else None
            })
        
        return make_json_response({
            'categories': categories_list
        })
        
    except Exception as e:
        logger.error(f"Admin get categories error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get categories'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/admin/categories', methods=['POST'])
@admin_required
def admin_create_category():
    """Create new category"""
    session_db = None
    try:
        session_db = get_session()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return make_json_response({
                'error': 'name is required'
            }, 400)
        
        # Generate slug from name if not provided
        slug = data.get('slug', data['name'].lower().replace(' ', '-'))
        
        # Check if slug already exists
        existing = session_db.query(models.Categories).filter(
            models.Categories.slug == slug
        ).first()
        
        if existing:
            return make_json_response({
                'error': 'Slug already exists'
            }, 400)
        
        # Create category
        category = models.Categories(
            id=str(uuid.uuid4()),
            name=data['name'],
            slug=slug,
            parent_id=data.get('parent_id'),
            sort_order=data.get('sort_order', 0),
            is_active=data.get('is_active', True),
            description=data.get('description', ''),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session_db.add(category)
        session_db.commit()
        
        return make_json_response({
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug
            }
        }, 201)
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Admin create category error: {str(e)}")
        return make_json_response({
            'error': 'Failed to create category'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

# ========== BRANDS MANAGEMENT ==========

@bp.route('/admin/brands', methods=['GET'])
@admin_required
def admin_get_brands():
    """Get all brands for admin"""
    session_db = None
    try:
        session_db = get_session()
        
        brands = session_db.query(models.Brands).order_by(models.Brands.name).all()
        
        brands_list = []
        for brand in brands:
            brands_list.append({
                'id': brand.id,
                'name': brand.name,
                'slug': getattr(brand, 'slug', ''),
                'logo_url': getattr(brand, 'logo_url', ''),
                'description': getattr(brand, 'description', ''),
                'is_active': brand.is_active,
                'created_at': brand.created_at.isoformat() if hasattr(brand, 'created_at') else None
            })
        
        return make_json_response({
            'brands': brands_list
        })
        
    except Exception as e:
        logger.error(f"Admin get brands error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get brands'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/admin/brands', methods=['POST'])
@admin_required
def admin_create_brand():
    """Create new brand"""
    session_db = None
    try:
        session_db = get_session()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return make_json_response({
                'error': 'name is required'
            }, 400)
        
        # Generate slug from name if not provided
        slug = data.get('slug', data['name'].lower().replace(' ', '-'))
        
        # Create brand
        brand = models.Brands(
            id=str(uuid.uuid4()),
            name=data['name'],
            slug=slug,
            logo_url=data.get('logo_url', ''),
            description=data.get('description', ''),
            is_active=data.get('is_active', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session_db.add(brand)
        session_db.commit()
        
        return make_json_response({
            'message': 'Brand created successfully',
            'brand': {
                'id': brand.id,
                'name': brand.name,
                'slug': brand.slug
            }
        }, 201)
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Admin create brand error: {str(e)}")
        return make_json_response({
            'error': 'Failed to create brand'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

# ========== PRODUCTS MANAGEMENT ==========

@bp.route('/admin/products', methods=['GET'])
@admin_required
def admin_get_products():
    """Get all products for admin"""
    session_db = None
    try:
        session_db = get_session()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        
        # Query products
        query = session_db.query(models.Products).order_by(
            models.Products.created_at.desc()
        )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        products = query.offset(offset).limit(per_page).all()
        
        products_list = []
        for product in products:
            # Get brand info
            brand = None
            if product.brand_id:
                brand = session_db.query(models.Brands).filter(
                    models.Brands.id == product.brand_id
                ).first()
            
            # Get variants count
            variants_count = session_db.query(models.ProductVariants).filter(
                models.ProductVariants.product_id == product.id
            ).count()
            
            products_list.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'sku': product.sku,
                'brand': brand.name if brand else '',
                'brand_id': product.brand_id,
                'is_active': product.is_active,
                'variants_count': variants_count,
                'created_at': product.created_at.isoformat()
            })
        
        return make_json_response({
            'products': products_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        logger.error(f"Admin get products error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get products'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/admin/products', methods=['POST'])
@admin_required
def admin_create_product():
    """Create new product with default variant"""
    session_db = None
    try:
        session_db = get_session()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'brand_id', 'short_desc']
        for field in required_fields:
            if not data.get(field):
                return make_json_response({
                    'error': f'{field} is required'
                }, 400)
        
        # Generate slug from name if not provided
        slug = data.get('slug', data['name'].lower().replace(' ', '-'))
        sku = data.get('sku', f"PRD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
        
        # Create product
        product_id = str(uuid.uuid4())
        product = models.Products(
            id=product_id,
            type_code='simple',
            name=data['name'],
            slug=slug,
            sku=sku,
            brand_id=data['brand_id'],
            short_desc=data['short_desc'],
            description=data.get('description', ''),
            origin_country=data.get('origin_country', 'VN'),
            unit_of_measure=data.get('unit_of_measure', 'piece'),
            size_note=data.get('size_note', ''),
            perishable=data.get('perishable', False),
            is_active=data.get('is_active', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session_db.add(product)
        
        # Create default variant
        variant = models.ProductVariants(
            id=str(uuid.uuid4()),
            product_id=product_id,
            sku=sku + '-DEFAULT',
            name='Default',
            options={},
            size_key='',
            weight_key='',
            list_price=data.get('price', 0),
            compare_at=data.get('compare_at_price'),
            is_active=True,
            sort_order=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session_db.add(variant)
        
        # Create initial stock record
        stock = models.InventoryStocks(
            variant_id=variant.id,
            on_hand=data.get('initial_stock', 0),
            reserved=0,
            updated_at=datetime.utcnow()
        )
        
        session_db.add(stock)
        session_db.commit()
        
        return make_json_response({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'variant_id': variant.id
            }
        }, 201)
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Admin create product error: {str(e)}")
        return make_json_response({
            'error': 'Failed to create product'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

# ========== ORDERS MANAGEMENT ==========

@bp.route('/admin/orders', methods=['GET'])
@admin_required
def admin_get_orders():
    """Get all orders for admin"""
    session_db = None
    try:
        session_db = get_session()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        status_filter = request.args.get('status')
        
        # Query orders
        query = session_db.query(models.Orders).order_by(
            models.Orders.created_at.desc()
        )
        
        # Filter by status if provided
        if status_filter:
            query = query.filter(models.Orders.status_code == status_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        orders = query.offset(offset).limit(per_page).all()
        
        orders_list = []
        for order in orders:
            # Get user info
            user = session_db.query(models.Users).filter(
                models.Users.id == order.user_id
            ).first()
            
            # Get order status
            status = session_db.query(models.OrderStatuses).filter(
                models.OrderStatuses.status_code == order.status_code
            ).first()
            
            orders_list.append({
                'id': order.id,
                'user_name': user.full_name if user else '',
                'user_email': user.email if user else '',
                'status_code': order.status_code,
                'status_label': status.label if status else order.status_code,
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
        logger.error(f"Admin get orders error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get orders'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/admin/orders/<order_id>/status', methods=['PATCH'])
@admin_required
def admin_update_order_status(order_id):
    """Update order status"""
    session_db = None
    try:
        session_db = get_session()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('status_code'):
            return make_json_response({
                'error': 'status_code is required'
            }, 400)
        
        status_code = data['status_code']
        
        # Validate status code exists
        status = session_db.query(models.OrderStatuses).filter(
            models.OrderStatuses.status_code == status_code
        ).first()
        
        if not status:
            return make_json_response({
                'error': 'Invalid status code'
            }, 400)
        
        # Get order
        order = session_db.query(models.Orders).filter(
            models.Orders.id == order_id
        ).first()
        
        if not order:
            return make_json_response({
                'error': 'Order not found'
            }, 404)
        
        # Update status
        order.status_code = status_code
        order.updated_at = datetime.utcnow()
        session_db.commit()
        
        return make_json_response({
            'message': 'Order status updated successfully',
            'order': {
                'id': order.id,
                'status_code': order.status_code,
                'status_label': status.label
            }
        })
        
    except Exception as e:
        if session_db:
            session_db.rollback()
        logger.error(f"Admin update order status error: {str(e)}")
        return make_json_response({
            'error': 'Failed to update order status'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)