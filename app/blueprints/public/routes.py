from flask import render_template, request, current_app, jsonify
from app.blueprints.public import bp
from app.db import get_session, close_session
from app.models import models
from sqlalchemy import and_, or_, func, desc
import logging

logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Trang chủ với hero section và sản phẩm nổi bật"""
    session = None
    try:
        session = get_session()
        
        # Lấy các danh mục chính
        categories = session.query(models.Categories).filter(
            models.Categories.is_active == 1,
            models.Categories.parent_id.is_(None)
        ).order_by(models.Categories.sort_order, models.Categories.name).limit(6).all()
        
        # Lấy sản phẩm mới nhất (giả sử có sản phẩm)
        # featured_products = session.query(models.Products).filter(
        #     models.Products.is_active == 1
        # ).order_by(desc(models.Products.created_at)).limit(8).all()
        
        # Lấy một số cửa hàng nổi bật
        featured_stores = session.query(models.Stores).filter(
            models.Stores.is_active == 1
        ).order_by(models.Stores.name).limit(3).all()
        
        return render_template('index.html', 
                             categories=categories,
                             featured_stores=featured_stores)
    except Exception as e:
        logger.error(f"Error in index: {str(e)}")
        return render_template('index.html', 
                             categories=[],
                             featured_stores=[])
    finally:
        if session:
            close_session(session)

@bp.route('/cua-hang')
def stores():
    """Hiển thị danh sách cửa hàng"""
    session = None
    try:
        session = get_session()
        
        # Lấy tham số từ query string
        q = request.args.get('q', '').strip()
        
        # Truy vấn cửa hàng
        query = session.query(models.Stores).filter(models.Stores.is_active == 1)
        
        # Tìm kiếm theo tên cửa hàng
        if q:
            query = query.filter(
                or_(
                    models.Stores.name.contains(q),
                    models.Stores.address.contains(q),
                    models.Stores.phone.contains(q)
                )
            )
        
        stores_list = query.order_by(models.Stores.name).all()
        
        return render_template('stores.html',
                             stores=stores_list,
                             search_query=q)
        
    except Exception as e:
        logger.error(f"Error in stores: {str(e)}")
        return render_template('stores.html',
                             stores=[],
                             search_query='',
                             error="Không thể tải danh sách cửa hàng")
    finally:
        if session:
            close_session(session)

@bp.route('/danh-muc/<slug>')
def category_products(slug):
    """Hiển thị sản phẩm theo danh mục"""
    from flask import redirect, url_for
    # Redirect to products page with category parameter
    return redirect(url_for('public.products', category=slug))

@bp.route('/he-thong-cua-hang')
def store_system():
    """Hiển thị danh sách cửa hàng với tính năng lọc và tìm kiếm"""
    session = None
    try:
        session = get_session()
        
        # Lấy tham số từ query string
        tinh = request.args.get('tinh', '').strip()
        q = request.args.get('q', '').strip()
        
        # Lấy danh sách tỉnh/thành (distinct provinces)
        provinces = session.query(models.Stores.province).filter(
            models.Stores.province.isnot(None),
            models.Stores.province != '',
            models.Stores.is_active == 1
        ).distinct().order_by(models.Stores.province).all()
        province_list = [p[0] for p in provinces if p[0]]
        
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
        
        # Sắp xếp và lấy kết quả
        stores_list = query.order_by(
            models.Stores.city,
            models.Stores.district,
            models.Stores.name
        ).all()
        
        return render_template('stores.html',
                             stores=stores_list,
                             provinces=province_list,
                             selected_province=tinh,
                             search_query=q)
        
    except Exception as e:
        logger.error(f"Error in stores route: {str(e)}")
        current_app.logger.error(f"Error in stores route: {str(e)}")
        return render_template('stores.html',
                             stores=[],
                             provinces=[],
                             selected_province='',
                             search_query='',
                             error="Không thể tải danh sách cửa hàng")
    finally:
        if session:
            close_session(session)

@bp.route('/san-pham')
def products():
    """Hiển thị danh sách sản phẩm với tính năng tìm kiếm"""
    session = None
    try:
        session = get_session()
        
        # Lấy tham số từ query string
        q = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        
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
        products_list = query.limit(50).all()  # Giới hạn 50 sản phẩm
        
        # Lấy danh sách category từ products để tạo filter
        categories_query = session.query(models.Categories).filter(
            models.Categories.is_active == 1
        ).order_by(models.Categories.name)
        categories_list = categories_query.all()
        
        return render_template('products.html',
                             products=products_list,
                             categories=categories_list,
                             search_query=q,
                             selected_category=category)
        
    except Exception as e:
        logger.error(f"Error in products route: {str(e)}")
        current_app.logger.error(f"Error in products route: {str(e)}")
        return render_template('products.html',
                             products=[],
                             categories=[],
                             search_query='',
                             selected_category='',
                             error="Không thể tải danh sách sản phẩm")
    finally:
        if session:
            close_session(session)