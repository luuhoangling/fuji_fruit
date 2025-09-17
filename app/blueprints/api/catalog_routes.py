"""
Catalog API routes for products, categories, and brands
"""
from flask import jsonify, request
from app.blueprints.api import bp
from app.db import get_session, close_session
from app.models import models
from sqlalchemy import and_, or_, func, text
import logging

logger = logging.getLogger(__name__)

def make_json_response(data, status=200):
    """Create a JSON response with proper UTF-8 encoding"""
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, status

@bp.route('/categories')
def get_categories():
    """Get all categories with hierarchical structure"""
    session_db = None
    try:
        session_db = get_session()
        
        # Get all active categories
        categories = session_db.query(models.Categories).filter(
            models.Categories.is_active == True
        ).order_by(
            models.Categories.sort_order,
            models.Categories.name
        ).all()
        
        # Convert to hierarchical structure
        categories_dict = {}
        root_categories = []
        
        # First pass: create all category objects
        for cat in categories:
            categories_dict[cat.id] = {
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'parent_id': cat.parent_id,
                'sort_order': cat.sort_order,
                'description': getattr(cat, 'description', ''),
                'children': []
            }
        
        # Second pass: build hierarchy
        for cat in categories:
            if cat.parent_id and cat.parent_id in categories_dict:
                categories_dict[cat.parent_id]['children'].append(categories_dict[cat.id])
            else:
                root_categories.append(categories_dict[cat.id])
        
        return make_json_response({
            'categories': root_categories
        })
        
    except Exception as e:
        logger.error(f"Categories error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get categories'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/brands')
def get_brands():
    """Get all brands"""
    session_db = None
    try:
        session_db = get_session()
        
        brands = session_db.query(models.Brands).filter(
            models.Brands.is_active == True
        ).order_by(models.Brands.name).all()
        
        brands_list = []
        for brand in brands:
            brands_list.append({
                'id': brand.id,
                'name': brand.name,
                'slug': getattr(brand, 'slug', ''),
                'logo_url': getattr(brand, 'logo_url', ''),
                'description': getattr(brand, 'description', '')
            })
        
        return make_json_response({
            'brands': brands_list
        })
        
    except Exception as e:
        logger.error(f"Brands error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get brands'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/products')
def get_products():
    """Get products with filtering, sorting, and pagination"""
    session_db = None
    try:
        session_db = get_session()
        
        # Get query parameters
        category = request.args.get('category', '').strip()
        q = request.args.get('q', '').strip()
        brand = request.args.get('brand', '').strip()
        sort = request.args.get('sort', 'name').strip()
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 12)), 50)  # Max 50 items per page
        
        # Build base query
        query = session_db.query(models.Products).filter(
            models.Products.is_active == True
        )
        
        # Filter by category
        if category:
            query = query.join(models.ProductCategories).filter(
                models.ProductCategories.category_id == category
            )
        
        # Filter by brand
        if brand:
            query = query.filter(models.Products.brand_id == brand)
        
        # Search by name or description
        if q:
            search_conditions = or_(
                models.Products.name.contains(q),
                models.Products.short_desc.contains(q),
                models.Products.description.contains(q),
                models.Products.sku.contains(q)
            )
            query = query.filter(search_conditions)
        
        # Apply sorting
        if sort == 'name':
            query = query.order_by(models.Products.name)
        elif sort == 'name_desc':
            query = query.order_by(models.Products.name.desc())
        elif sort == 'created_at':
            query = query.order_by(models.Products.created_at.desc())
        else:
            query = query.order_by(models.Products.created_at.desc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        products = query.offset(offset).limit(per_page).all()
        
        # Format response
        products_list = []
        for product in products:
            # Get primary variant with stock info
            variant = session_db.query(models.ProductVariants).filter(
                models.ProductVariants.product_id == product.id,
                models.ProductVariants.is_active == True
            ).first()
            
            # Get stock info using raw SQL for the view
            stock_info = {'available': 0}
            if variant:
                try:
                    stock_result = session_db.execute(
                        text("SELECT available FROM v_variant_stock WHERE variant_id = :variant_id"),
                        {"variant_id": variant.id}
                    ).fetchone()
                    if stock_result:
                        stock_info['available'] = stock_result[0] or 0
                except:
                    pass
            
            # Get primary image
            image = session_db.query(models.ProductMedia).filter(
                models.ProductMedia.product_id == product.id
            ).order_by(models.ProductMedia.sort_order).first()
            
            products_list.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'sku': product.sku,
                'short_desc': product.short_desc,
                'brand_id': product.brand_id,
                'unit_of_measure': product.unit_of_measure,
                'image_url': image.url if image else '',
                'price': variant.list_price if variant else 0,
                'compare_at_price': variant.compare_at if variant else None,
                'available': stock_info['available'],
                'variant_id': variant.id if variant else None
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
        logger.error(f"Products error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get products'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)

@bp.route('/products/<product_slug>')
def get_product_detail(product_slug):
    """Get detailed product information including variants"""
    session_db = None
    try:
        session_db = get_session()
        
        # Get product
        product = session_db.query(models.Products).filter(
            models.Products.slug == product_slug,
            models.Products.is_active == True
        ).first()
        
        if not product:
            return make_json_response({
                'error': 'Product not found'
            }, 404)
        
        # Get brand info
        brand = None
        if product.brand_id:
            brand = session_db.query(models.Brands).filter(
                models.Brands.id == product.brand_id
            ).first()
        
        # Get variants with stock info
        variants = session_db.query(models.ProductVariants).filter(
            models.ProductVariants.product_id == product.id,
            models.ProductVariants.is_active == True
        ).order_by(models.ProductVariants.sort_order).all()
        
        variants_list = []
        for variant in variants:
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
            
            variants_list.append({
                'id': variant.id,
                'sku': variant.sku,
                'name': variant.name,
                'options': variant.options if hasattr(variant, 'options') else {},
                'size_key': variant.size_key,
                'weight_key': variant.weight_key,
                'list_price': variant.list_price,
                'compare_at': variant.compare_at,
                'available': stock_info['available']
            })
        
        # Get product images
        images = session_db.query(models.ProductMedia).filter(
            models.ProductMedia.product_id == product.id
        ).order_by(models.ProductMedia.sort_order).all()
        
        images_list = []
        for image in images:
            images_list.append({
                'id': image.id,
                'url': image.url,
                'alt_text': image.alt_text,
                'sort_order': image.sort_order
            })
        
        # Get categories
        categories = session_db.query(models.Categories).join(
            models.ProductCategories
        ).filter(
            models.ProductCategories.product_id == product.id
        ).all()
        
        categories_list = []
        for category in categories:
            categories_list.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug
            })
        
        return make_json_response({
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'sku': product.sku,
                'short_desc': product.short_desc,
                'description': product.description,
                'origin_country': product.origin_country,
                'unit_of_measure': product.unit_of_measure,
                'size_note': product.size_note,
                'perishable': product.perishable,
                'brand': {
                    'id': brand.id,
                    'name': brand.name
                } if brand else None,
                'variants': variants_list,
                'images': images_list,
                'categories': categories_list
            }
        })
        
    except Exception as e:
        logger.error(f"Product detail error: {str(e)}")
        return make_json_response({
            'error': 'Failed to get product details'
        }, 500)
    finally:
        if session_db:
            close_session(session_db)