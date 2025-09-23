"""
Admin views for management functionality
"""
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app.blueprints.admin import admin_bp
from app.auth import admin_required_web as admin_required, get_current_user
from app.models import Product, Category, Order, User, Discount, ShippingRate
from app.repositories.product_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository 
from app.repositories.order_repo import OrderRepository
from app.services.discount_service import DiscountService
from app.services.shipping_service import ShippingService
from app.db import get_session, close_session
from app.extensions import db, csrf
from datetime import datetime, timedelta
from sqlalchemy import func


@admin_bp.route('/login')
def admin_login():
    """Admin login page - redirect to main login with admin check"""
    from flask import redirect, url_for
    return redirect(url_for('site.login', next=url_for('admin.dashboard')))


@admin_bp.before_request
def check_admin_access():
    """Check admin access for all admin routes except login"""
    from flask import request, redirect, url_for, flash
    
    # Allow access to login page
    if request.endpoint == 'admin.admin_login':
        return
        
    # Check if user is logged in and is admin
    user = get_current_user()
    if not user:
        flash('Vui lòng đăng nhập để tiếp tục', 'error')
        return redirect(url_for('admin.admin_login'))
    
    if not user.is_admin():
        flash('Bạn không có quyền truy cập trang quản trị', 'error')
        return redirect(url_for('site.home'))


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    session_db = get_session()
    try:
        # Get basic statistics
        total_products = session_db.query(Product).count()
        total_orders = session_db.query(Order).count()
        total_users = session_db.query(User).filter(User.role_code == 'customer').count()
        
        # Recent orders (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_orders = session_db.query(Order).filter(
            Order.created_at >= thirty_days_ago
        ).count()
        
        # Total revenue (last 30 days)
        revenue_result = session_db.query(func.sum(Order.grand_total)).filter(
            Order.created_at >= thirty_days_ago,
            Order.status != 'cancelled'
        ).scalar()
        total_revenue = float(revenue_result or 0)
        
        # Recent orders for display
        recent_orders_list = session_db.query(Order).order_by(
            Order.created_at.desc()
        ).limit(10).all()
        
        stats = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'recent_orders': recent_orders,
            'total_revenue': total_revenue,
            'recent_orders_list': recent_orders_list  # Pass the objects directly
        }
        
        return render_template('admin/dashboard.html', stats=stats)
        
    finally:
        close_session(session_db)


@admin_bp.route('/products')
@admin_required
def products():
    """Product management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 20
    
    session_db = get_session()
    try:
        product_repo = ProductRepository(session_db)
        products_data, total = product_repo.get_admin_products(search, page, per_page)
        
        # Get categories for filter/form
        categories = session_db.query(Category).filter(Category.is_active == True).all()
        
        return render_template('admin/products.html', 
                             products=products_data,
                             categories=[cat.to_dict() for cat in categories],
                             total=total,
                             page=page,
                             per_page=per_page,
                             search=search)
    finally:
        close_session(session_db)


@admin_bp.route('/products/create', methods=['GET', 'POST'])
@admin_required
def create_product():
    """Create new product"""
    if request.method == 'GET':
        session_db = get_session()
        try:
            categories = session_db.query(Category).filter(Category.is_active == True).all()
            return render_template('admin/product_form.html', 
                                 categories=[cat.to_dict() for cat in categories],
                                 product=None)
        finally:
            close_session(session_db)
    
    # Handle POST request
    data = request.get_json()
    session_db = get_session()
    try:
        # Create product logic here
        # This would involve ProductRepository.create_product()
        return jsonify({'success': True, 'message': 'Sản phẩm đã được tạo thành công'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit existing product"""
    session_db = get_session()
    try:
        product = session_db.query(Product).get(product_id)
        if not product:
            flash('Không tìm thấy sản phẩm', 'error')
            return redirect(url_for('admin.products'))
        
        if request.method == 'GET':
            categories = session_db.query(Category).filter(Category.is_active == True).all()
            return render_template('admin/product_form.html',
                                 categories=[cat.to_dict() for cat in categories],
                                 product=product.to_dict())
        
        # Handle POST request - update product
        data = request.get_json()
        # Update product logic here
        return jsonify({'success': True, 'message': 'Sản phẩm đã được cập nhật'})
        
    finally:
        close_session(session_db)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    session_db = get_session()
    try:
        product = session_db.query(Product).get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
        
        # Soft delete by setting is_active = False
        product.is_active = False
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Sản phẩm đã được xóa'})
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/discounts')
@admin_required
def discounts():
    """Discount management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 20
    
    session_db = get_session()
    try:
        query = session_db.query(Discount)
        
        if search:
            query = query.filter(
                (Discount.code.ilike(f'%{search}%')) |
                (Discount.name.ilike(f'%{search}%'))
            )
        
        total = query.count()
        discounts = query.order_by(Discount.created_at.desc()).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        return render_template('admin/discounts.html',
                             discounts=[d.to_dict() for d in discounts],
                             total=total,
                             page=page,
                             per_page=per_page,
                             search=search)
    finally:
        close_session(session_db)


@admin_bp.route('/discounts/create', methods=['GET', 'POST'])
@admin_required
def create_discount():
    """Create new discount"""
    if request.method == 'GET':
        return render_template('admin/discount_form.html', discount=None)
    
    # Handle POST request
    data = request.get_json()
    session_db = get_session()
    try:
        # Validate discount code uniqueness
        existing = session_db.query(Discount).filter(Discount.code == data['code']).first()
        if existing:
            return jsonify({'success': False, 'message': 'Mã giảm giá đã tồn tại'}), 400
        
        discount = Discount(
            code=data['code'],
            name=data['name'],
            description=data.get('description', ''),
            discount_type=data['discount_type'],
            discount_value=data['discount_value'],
            min_order_amount=data.get('min_order_amount', 0),
            max_discount_amount=data.get('max_discount_amount'),
            usage_limit=data.get('usage_limit'),
            usage_limit_per_user=data.get('usage_limit_per_user', 1),
            start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
            end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')),
            is_active=data.get('is_active', True)
        )
        
        session_db.add(discount)
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Mã giảm giá đã được tạo thành công'})
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/discounts/<int:discount_id>/delete', methods=['POST'])
@admin_required
def delete_discount(discount_id):
    """Delete discount"""
    session_db = get_session()
    try:
        discount = session_db.query(Discount).get(discount_id)
        if not discount:
            return jsonify({'success': False, 'message': 'Không tìm thấy mã giảm giá'}), 404
        
        # Soft delete by setting is_active = False
        discount.is_active = False
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Mã giảm giá đã được xóa'})
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/shipping-rates')
@admin_required
def shipping_rates():
    """Shipping rate management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    session_db = get_session()
    try:
        query = session_db.query(ShippingRate)
        total = query.count()
        
        shipping_rates = query.order_by(ShippingRate.priority.desc(), ShippingRate.created_at.desc()).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        return render_template('admin/shipping_rates.html',
                             shipping_rates=[sr.to_dict() for sr in shipping_rates],
                             total=total,
                             page=page,
                             per_page=per_page)
    finally:
        close_session(session_db)


@admin_bp.route('/shipping-rates/create', methods=['GET', 'POST'])
@admin_required
def create_shipping_rate():
    """Create new shipping rate"""
    if request.method == 'GET':
        return render_template('admin/shipping_rate_form.html', shipping_rate=None)
    
    # Handle POST request
    data = request.get_json()
    session_db = get_session()
    try:
        shipping_rate = ShippingRate(
            name=data['name'],
            description=data.get('description', ''),
            province=data.get('province'),
            district=data.get('district'),
            ward=data.get('ward'),
            shipping_method=data.get('shipping_method', 'standard'),
            base_fee=data['base_fee'],
            per_kg_fee=data.get('per_kg_fee', 0),
            free_shipping_threshold=data.get('free_shipping_threshold'),
            estimated_days_min=data.get('estimated_days_min', 1),
            estimated_days_max=data.get('estimated_days_max', 3),
            is_active=data.get('is_active', True),
            priority=data.get('priority', 0)
        )
        
        session_db.add(shipping_rate)
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Phí ship đã được tạo thành công'})
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/shipping-rates/<int:rate_id>/delete', methods=['POST'])
@admin_required
def delete_shipping_rate(rate_id):
    """Delete shipping rate"""
    session_db = get_session()
    try:
        shipping_rate = session_db.query(ShippingRate).get(rate_id)
        if not shipping_rate:
            return jsonify({'success': False, 'message': 'Không tìm thấy phí ship'}), 404
        
        # Soft delete by setting is_active = False
        shipping_rate.is_active = False
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Phí ship đã được xóa'})
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/orders')
@admin_required
def orders():
    """Order management page"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    per_page = 20
    
    session_db = get_session()
    try:
        order_repo = OrderRepository(session_db)
        orders, total = order_repo.get_orders_for_admin(page, per_page, status)
        
        return render_template('admin/orders.html',
                             orders=orders,
                             total=total,
                             page=page,
                             per_page=per_page,
                             status=status)
    finally:
        close_session(session_db)


@admin_bp.route('/orders/<int:order_id>')
@admin_required
def order_detail(order_id):
    """Order detail page"""
    session_db = get_session()
    try:
        order = session_db.query(Order).get(order_id)
        if not order:
            flash('Không tìm thấy đơn hàng', 'error')
            return redirect(url_for('admin.orders'))
        
        return render_template('admin/order_detail.html', order=order.to_dict(include_relations=True))
        
    finally:
        close_session(session_db)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@csrf.exempt
@admin_required
def update_order_status(order_id):
    """Update order status via AJAX"""
    session_db = get_session()
    try:
        # Get order
        order = session_db.query(Order).get(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Không tìm thấy đơn hàng'}), 404

        # Get new status from request
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'}), 400
        
        new_status = data['status']
        
        # Validate status
        valid_statuses = ['pending', 'waiting_admin_confirmation', 'confirmed', 'fulfilled', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'message': 'Trạng thái không hợp lệ'}), 400
        
        # Update order status using repository
        order_repo = OrderRepository(session_db)
        success = order_repo.update_order_status(order_id, new_status)
        
        if success:
            session_db.commit()
            status_text = {
                'pending': 'chờ xử lý',
                'waiting_admin_confirmation': 'chờ xác nhận',
                'confirmed': 'đã xác nhận',
                'fulfilled': 'đã hoàn thành',
                'cancelled': 'đã hủy'
            }
            return jsonify({
                'success': True, 
                'message': f'Đơn hàng đã được cập nhật thành {status_text.get(new_status, new_status)}'
            })
        else:
            return jsonify({'success': False, 'message': 'Không thể cập nhật trạng thái đơn hàng'}), 400
            
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        close_session(session_db)


@admin_bp.route('/orders/<order_code>/confirm', methods=['POST'])
@csrf.exempt
@admin_required
def confirm_order(order_code):
    """Admin confirms order (moves from pending to confirmed)"""
    session_db = get_session()
    try:
        order = session_db.query(Order).filter_by(order_code=order_code).first()
        if not order:
            return jsonify({'success': False, 'error': 'Không tìm thấy đơn hàng'}), 404
        
        if order.status not in ['pending', 'waiting_admin_confirmation']:
            return jsonify({'success': False, 'error': f'Đơn hàng đang ở trạng thái {order.status}, không thể xác nhận'}), 400
        
        # Update order status to confirmed
        order.status = 'confirmed'
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Đã xác nhận đơn hàng!'})
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        close_session(session_db)


@admin_bp.route('/orders/<order_code>/mark-fulfilled', methods=['POST'])
@csrf.exempt
@admin_required
def mark_fulfilled(order_code):
    """Admin marks order as fulfilled (processing completed)"""
    session_db = get_session()
    try:
        order = session_db.query(Order).filter_by(order_code=order_code).first()
        if not order:
            return jsonify({'success': False, 'error': 'Không tìm thấy đơn hàng'}), 404
        
        if order.status != 'confirmed':
            return jsonify({'success': False, 'error': f'Đơn hàng đang ở trạng thái {order.status}, không thể đánh dấu hoàn thành'}), 400
        
        # Update order status to fulfilled
        order.status = 'fulfilled'
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Đã đánh dấu đơn hàng hoàn thành!'})
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        close_session(session_db)

# DEPRECATED: Admin mark delivered route - no longer needed
# Users now confirm receipt directly from fulfilled status
"""
@admin_bp.route('/orders/<order_code>/mark-delivered', methods=['POST'])
@csrf.exempt
@admin_required
def mark_delivered(order_code):
    \"\"\"Admin marks order as delivered\"\"\"
    session_db = get_session()
    try:
        order = session_db.query(Order).filter_by(order_code=order_code).first()
        if not order:
            return jsonify({'success': False, 'error': 'Không tìm thấy đơn hàng'}), 404
        
        if order.status != 'fulfilled':
            return jsonify({'success': False, 'error': f'Đơn hàng đang ở trạng thái {order.status}, không thể đánh dấu đã giao'}), 400
        
        # Mark as delivered by setting transfer_confirmed = True
        from datetime import datetime
        order.transfer_confirmed = True
        order.transfer_confirmed_at = datetime.utcnow()
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Đã đánh dấu đơn hàng đã giao hàng!'})
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        close_session(session_db)
"""


# DEPRECATED: Admin mark received route - no longer needed  
# Users now confirm receipt directly from fulfilled status
"""
@admin_bp.route('/orders/<order_code>/mark-received', methods=['POST'])
@admin_bp.route('/orders/<order_code>/mark-received', methods=['POST'])
@csrf.exempt
@admin_required
def mark_received(order_code):
    \"\"\"Admin marks that customer has received the order\"\"\"
    session_db = get_session()
    try:
        order = session_db.query(Order).filter_by(order_code=order_code).first()
        if not order:
            return jsonify({'success': False, 'error': 'Không tìm thấy đơn hàng'}), 404
        
        if order.status != 'fulfilled' or not order.transfer_confirmed:
            return jsonify({'success': False, 'error': 'Đơn hàng chưa được giao, không thể xác nhận đã nhận'}), 400
        
        # For COD orders, mark payment as completed when customer receives
        if order.payment_method == 'COD':
            order.payment_status = 'mock_paid'
        
        session_db.commit()
        
        return jsonify({'success': True, 'message': 'Đã xác nhận khách hàng đã nhận hàng!'})
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        close_session(session_db)
"""