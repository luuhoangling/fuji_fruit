"""Admin API endpoints (JWT authentication required)"""

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api import admin_bp
from app.api.errors import (
    NotFoundError, ValidationAPIError, BusinessLogicError, ConflictError,
    validate_request_json, serialize_response
)
from app.repositories.category_repo import category_repo
from app.repositories.product_repo import product_repo
from app.repositories.review_repo import review_repo
from app.repositories.stock_repo import stock_repo
from app.services.order_service import order_service, OrderError
from app.services.stock_service import stock_service
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema, ProductSaleSchema, ProductQuerySchema
from app.schemas.review import ReviewQuerySchema
from app.schemas.order import OrderQuerySchema, OrderStatusUpdateSchema
from app.schemas.category import CategoryCreateSchema, CategorySchema
from app.utils.pagination import PaginationHelper
from app.utils.slugs import SlugGenerator
from app.extensions import db
import bcrypt


# Authentication
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise ValidationAPIError("Username and password are required")
        
        # Simplified admin auth (in production, use proper user management)
        # Default admin credentials: admin/admin123
        if username == 'admin' and password == 'admin123':
            access_token = create_access_token(identity=username)
            return jsonify({
                'access_token': access_token,
                'user': {
                    'username': username,
                    'role': 'admin'
                }
            })
        else:
            raise ValidationAPIError("Invalid credentials")
    
    except ValidationAPIError:
        raise
    except Exception as e:
        raise BusinessLogicError(f"Login failed: {str(e)}")


# Categories Management
@admin_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_admin_categories():
    """Get all categories for admin"""
    try:
        categories = category_repo.get_all()
        result = [cat.to_dict() for cat in categories]
        return jsonify(result)
    except Exception as e:
        raise BusinessLogicError(f"Failed to fetch categories: {str(e)}")


@admin_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create new category"""
    try:
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(CategoryCreateSchema, request.get_json())
        
        # Generate slug
        name = data['name']
        slug = SlugGenerator.generate_category_slug(
            name, 
            lambda s: category_repo.get_by_slug(s) is not None
        )
        
        # Create category
        category = category_repo.create(
            name=name,
            slug=slug,
            parent_id=data.get('parent_id')
        )
        
        db.session.commit()
        return jsonify(category.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to create category: {str(e)}")


@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update category"""
    try:
        category = category_repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", str(category_id))
        
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(CategoryCreateSchema, request.get_json())
        
        # Update fields
        if 'name' in data:
            category.name = data['name']
            # Regenerate slug if name changed
            category.slug = SlugGenerator.generate_category_slug(
                data['name'],
                lambda s: s != category.slug and category_repo.get_by_slug(s) is not None
            )
        
        if 'parent_id' in data:
            category.parent_id = data['parent_id']
        
        db.session.commit()
        return jsonify(category.to_dict())
        
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to update category: {str(e)}")


@admin_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete category"""
    try:
        category = category_repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", str(category_id))
        
        # Check if category has children
        children = category_repo.get_children(category_id)
        if children:
            raise ConflictError("Cannot delete category with child categories")
        
        # Check if category has products
        if category.products:
            raise ConflictError("Cannot delete category with products")
        
        category_repo.delete(category)
        db.session.commit()
        
        return '', 204
        
    except (NotFoundError, ConflictError):
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to delete category: {str(e)}")


# Products Management
@admin_bp.route('/products', methods=['GET'])
@jwt_required()
def get_admin_products():
    """Get products for admin with stock info"""
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        page, page_size = PaginationHelper.validate_pagination_params(page, page_size)
        
        products, total = product_repo.get_admin_products(search, page, page_size)
        
        response_data = PaginationHelper.paginate_data(products, page, page_size, total)
        response = jsonify(response_data)
        return PaginationHelper.add_pagination_headers(response, page, page_size, total)
        
    except Exception as e:
        raise BusinessLogicError(f"Failed to fetch products: {str(e)}")


@admin_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product"""
    try:
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(ProductCreateSchema, request.get_json())
        
        # Generate slug
        name = data['name']
        slug = SlugGenerator.generate_product_slug(
            name,
            lambda s: product_repo.get_by_slug(s) is not None
        )
        
        # Create product
        product = product_repo.create(
            name=name,
            slug=slug,
            short_desc=data.get('short_desc'),
            price=data['price'],
            sale_price=data.get('sale_price'),
            sale_start=data.get('sale_start'),
            sale_end=data.get('sale_end'),
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
        
        # Add categories
        category_ids = data.get('category_ids', [])
        for cat_id in category_ids:
            category = category_repo.get_by_id(cat_id)
            if category:
                product.categories.append(category)
        
        # Initialize stock
        stock_repo.set_stock(product.id, 0)
        
        db.session.commit()
        return jsonify(product.to_dict(include_relations=True)), 201
        
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to create product: {str(e)}")


@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product"""
    try:
        product = product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(ProductUpdateSchema, request.get_json())
        
        # Update fields
        for field in ['name', 'short_desc', 'price', 'sale_price', 'sale_start', 'sale_end', 'image_url', 'is_active']:
            if field in data:
                setattr(product, field, data[field])
        
        # Update slug if name changed
        if 'name' in data:
            product.slug = SlugGenerator.generate_product_slug(
                data['name'],
                lambda s: s != product.slug and product_repo.get_by_slug(s) is not None
            )
        
        # Update categories
        if 'category_ids' in data:
            product.categories.clear()
            for cat_id in data['category_ids']:
                category = category_repo.get_by_id(cat_id)
                if category:
                    product.categories.append(category)
        
        db.session.commit()
        return jsonify(product.to_dict(include_relations=True))
        
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to update product: {str(e)}")


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete product"""
    try:
        product = product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        product_repo.delete(product)
        db.session.commit()
        
        return '', 204
        
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to delete product: {str(e)}")


@admin_bp.route('/products/<int:product_id>/sale', methods=['PUT'])
@jwt_required()
def set_product_sale(product_id):
    """Set product sale pricing"""
    try:
        product = product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(ProductSaleSchema, request.get_json())
        
        # Validate sale price vs regular price
        if data['sale_price'] >= product.price:
            raise ValidationAPIError("Sale price must be less than regular price")
        
        # Update sale fields
        product.sale_price = data['sale_price']
        product.sale_start = data.get('sale_start')
        product.sale_end = data.get('sale_end')
        
        db.session.commit()
        return jsonify(product.to_dict())
        
    except (NotFoundError, ValidationAPIError):
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to set sale price: {str(e)}")


# Stock Management
@admin_bp.route('/stock/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product_stock(product_id):
    """Update product stock"""
    try:
        product = product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = request.get_json()
        qty_on_hand = data.get('qty_on_hand')
        
        if qty_on_hand is None or not isinstance(qty_on_hand, int) or qty_on_hand < 0:
            raise ValidationAPIError("qty_on_hand must be a non-negative integer")
        
        stock_info = stock_service.update_stock(product_id, qty_on_hand)
        return jsonify(stock_info)
        
    except (NotFoundError, ValidationAPIError):
        raise
    except Exception as e:
        raise BusinessLogicError(f"Failed to update stock: {str(e)}")


# Reviews Management
@admin_bp.route('/reviews', methods=['GET'])
@jwt_required()
def get_admin_reviews():
    """Get reviews for admin panel"""
    try:
        product_id = request.args.get('product_id', type=int)
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        page, page_size = PaginationHelper.validate_pagination_params(page, page_size)
        
        reviews, total = review_repo.get_admin_reviews(product_id, page, page_size)
        
        # Format reviews for admin
        review_data = []
        for review in reviews:
            review_dict = review.to_dict()
            if review.product:
                review_dict['product_name'] = review.product.name
            review_data.append(review_dict)
        
        response_data = PaginationHelper.paginate_data(review_data, page, page_size, total)
        response = jsonify(response_data)
        return PaginationHelper.add_pagination_headers(response, page, page_size, total)
        
    except Exception as e:
        raise BusinessLogicError(f"Failed to fetch reviews: {str(e)}")


@admin_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete review"""
    try:
        review = review_repo.get_by_id(review_id)
        if not review:
            raise NotFoundError("Review", str(review_id))
        
        review_repo.delete(review)
        db.session.commit()
        
        return '', 204
        
    except NotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise BusinessLogicError(f"Failed to delete review: {str(e)}")


# Orders Management
@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_admin_orders():
    """Get orders for admin panel"""
    try:
        status = request.args.get('status')
        search_query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        page, page_size = PaginationHelper.validate_pagination_params(page, page_size)
        
        orders, total = order_service.search_orders(status, search_query, page, page_size)
        
        response_data = PaginationHelper.paginate_data(orders, page, page_size, total)
        response = jsonify(response_data)
        return PaginationHelper.add_pagination_headers(response, page, page_size, total)
        
    except Exception as e:
        raise BusinessLogicError(f"Failed to fetch orders: {str(e)}")


@admin_bp.route('/orders/<order_code>', methods=['GET'])
@jwt_required()
def get_admin_order_detail(order_code):
    """Get detailed order info for admin"""
    try:
        order = order_service.get_order_by_code(order_code)
        return jsonify(order)
        
    except OrderError as e:
        if "not found" in str(e):
            raise NotFoundError("Order", order_code)
        raise BusinessLogicError(str(e))


@admin_bp.route('/orders/<order_code>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_code):
    """Update order status"""
    try:
        if not request.is_json:
            raise ValidationAPIError("Request must be JSON")
        
        data = validate_request_json(OrderStatusUpdateSchema, request.get_json())
        
        order = order_service.update_order_status(order_code, data['status'])
        return jsonify(order)
        
    except OrderError as e:
        if "not found" in str(e):
            raise NotFoundError("Order", order_code)
        raise BusinessLogicError(str(e))
    except Exception as e:
        raise BusinessLogicError(f"Failed to update order status: {str(e)}")


@admin_bp.route('/orders/<order_code>/mock-pay', methods=['PUT'])
@jwt_required()
def admin_mock_pay_order(order_code):
    """Admin mark order as mock paid"""
    try:
        order = order_service.mock_pay(order_code)
        return jsonify(order)
        
    except OrderError as e:
        if "not found" in str(e):
            raise NotFoundError("Order", order_code)
        raise BusinessLogicError(str(e))


# Admin health check
@admin_bp.route('/health', methods=['GET'])
@jwt_required()
def admin_health_check():
    """Admin API health check"""
    user = get_jwt_identity()
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'api': '/api/v1/admin',
        'user': user
    })