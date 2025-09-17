from flask import jsonify, request, current_app
from app.blueprints.api import bp
from app.db import get_session, close_session
from app.models import models
from sqlalchemy import and_, or_
import logging

logger = logging.getLogger(__name__)

def make_json_response(data, status=200):
    """Create a JSON response with proper UTF-8 encoding"""
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, status

@bp.route('/stores')
def api_stores():
    """API endpoint trả JSON danh sách cửa hàng"""
    session = None
    try:
        session = get_session()
        
        # Lấy tham số từ query string
        tinh = request.args.get('tinh', '').strip()
        q = request.args.get('q', '').strip()
        
        # Xây dựng truy vấn stores
        query = session.query(models.Stores).filter(models.Stores.is_active == 1)
        
        # Lọc theo tỉnh/thành
        if tinh:
            query = query.filter(models.Stores.province == tinh)
        
        # Tìm kiếm theo từ khóa
        if q:
            search_conditions = or_(
                models.Stores.name.contains(q),
                models.Stores.line1.contains(q),
                models.Stores.district.contains(q),
                models.Stores.city.contains(q),
                models.Stores.hotline.contains(q),
                models.Stores.store_phone.contains(q)
            )
            query = query.filter(search_conditions)
        
        # Lấy kết quả
        stores_list = query.order_by(
            models.Stores.city,
            models.Stores.district,
            models.Stores.name
        ).all()
        
        # Chuyển đổi thành JSON
        stores_data = []
        for store in stores_list:
            # Tạo địa chỉ đầy đủ
            address_parts = [store.line1]
            if store.ward:
                address_parts.append(store.ward)
            if store.district:
                address_parts.append(store.district)
            if store.city:
                address_parts.append(store.city)
            if store.province:
                address_parts.append(store.province)
            full_address = ', '.join(address_parts)
            
            store_data = {
                'id': store.id,
                'name': store.name,
                'hotline': store.hotline,
                'store_phone': store.store_phone,
                'map_url': store.map_url,
                'zalo_url': store.zalo_url,
                'full_address': full_address,
                'line1': store.line1,
                'ward': store.ward,
                'district': store.district,
                'city': store.city,
                'province': store.province,
                'lat': float(store.lat) if store.lat else None,
                'lng': float(store.lng) if store.lng else None,
                'is_active': bool(store.is_active),
                'created_at': store.created_at.isoformat() if store.created_at else None
            }
            stores_data.append(store_data)
        
        return make_json_response({
            'success': True,
            'count': len(stores_data),
            'data': stores_data
        })
        
    except Exception as e:
        logger.error(f"Error in api_stores: {str(e)}")
        return make_json_response({
            'success': False,
            'error': 'Không thể tải danh sách cửa hàng'
        }, 500)
    finally:
        if session:
            close_session(session)

@bp.route('/stores/<store_id>/hours')
def api_store_hours(store_id):
    """API endpoint trả giờ mở cửa của cửa hàng"""
    session = None
    try:
        session = get_session()
        
        # Kiểm tra store tồn tại
        store = session.query(models.Stores).filter(
            models.Stores.id == store_id,
            models.Stores.is_active == 1
        ).first()
        
        if not store:
            return make_json_response({
                'success': False,
                'error': 'Không tìm thấy cửa hàng'
            }, 404)
        
        # Lấy giờ mở cửa
        hours = session.query(models.StoreHours).filter(
            models.StoreHours.store_id == store_id
        ).order_by(models.StoreHours.dow).all()
        
        # Chuyển đổi thành JSON
        hours_data = []
        for hour in hours:
            hour_data = {
                'dow': hour.dow,  # Day of week (0=Sunday, 1=Monday, etc.)
                'open_time': str(hour.open_time) if hour.open_time else None,
                'close_time': str(hour.close_time) if hour.close_time else None
            }
            hours_data.append(hour_data)
        
        return make_json_response({
            'success': True,
            'store_id': store_id,
            'store_name': store.name,
            'hours': hours_data
        })
        
    except Exception as e:
        logger.error(f"Error in api_store_hours: {str(e)}")
        return make_json_response({
            'success': False,
            'error': 'Không thể tải giờ mở cửa'
        }, 500)
    finally:
        if session:
            close_session(session)

@bp.route('/products/search')
def api_products_search():
    """API endpoint tìm kiếm sản phẩm"""
    session = None
    try:
        session = get_session()
        
        # Lấy tham số từ query string
        q = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        limit = min(int(request.args.get('limit', 50)), 100)  # Tối đa 100 sản phẩm
        
        # Sử dụng view v_products_search để tìm kiếm
        query = session.query(models.VProductsSearch)
        
        # Tìm kiếm theo từ khóa
        if q:
            search_conditions = or_(
                models.VProductsSearch.name.contains(q),
                models.VProductsSearch.text.contains(q),
                models.VProductsSearch.categories.contains(q)
            )
            query = query.filter(search_conditions)
        
        # Lọc theo category
        if category:
            query = query.filter(models.VProductsSearch.categories.contains(category))
        
        # Lấy kết quả
        products_list = query.limit(limit).all()
        
        # Chuyển đổi thành JSON
        products_data = []
        for product in products_list:
            product_data = {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'categories': product.categories,
                'text': product.text
            }
            products_data.append(product_data)
        
        return make_json_response({
            'success': True,
            'count': len(products_data),
            'query': q,
            'category': category,
            'data': products_data
        })
        
    except Exception as e:
        logger.error(f"Error in api_products_search: {str(e)}")
        return make_json_response({
            'success': False,
            'error': 'Không thể tìm kiếm sản phẩm'
        }, 500)
    finally:
        if session:
            close_session(session)