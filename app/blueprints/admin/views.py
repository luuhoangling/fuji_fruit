"""
Admin views for management functionality
"""
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app.blueprints.admin import admin_bp
from app.auth import admin_required_web as admin_required, get_current_user
from app.models import Product, Category, Order, User
from app.models.product import ProductStock
from app.repositories.product_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository 
from app.repositories.order_repo import OrderRepository
from app.services.product_sale_service import ProductSaleService
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
        
        # Total revenue (last 30 days) - only completed orders
        revenue_result = session_db.query(func.sum(Order.grand_total)).filter(
            Order.created_at >= thirty_days_ago,
            Order.status == 'completed'
        ).scalar()
        total_revenue = float(revenue_result or 0)
        
        # Recent orders for display
        recent_orders_list = session_db.query(Order).order_by(
            Order.created_at.desc()
        ).limit(10).all()
        
        # Get sale statistics
        sale_service = ProductSaleService(session_db)
        sale_stats = sale_service.get_sale_statistics()
        
        # Auto update sale status
        sale_service.auto_update_sale_status()
        
        stats = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'recent_orders': recent_orders,
            'total_revenue': total_revenue,
            'recent_orders_list': recent_orders_list,  # Pass the objects directly
            'sale_stats': sale_stats
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
@csrf.exempt
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
    if not data:
        return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'}), 400
    
    session_db = get_session()
    try:
        # Validate required fields
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Tên sản phẩm là bắt buộc'}), 400
        
        if not data.get('price'):
            return jsonify({'success': False, 'message': 'Giá sản phẩm là bắt buộc'}), 400
        
        # Create new product
        product = Product(
            name=data['name'],
            short_desc=data.get('short_desc'),
            price=float(data['price']),
            sale_price=float(data['sale_price']) if data.get('sale_price') else None,
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
        
        # Generate slug from name
        from app.utils.slugs import slugify
        product.slug = slugify(product.name)
        
        session_db.add(product)
        session_db.flush()  # Get the ID
        
        # Add categories if provided
        if data.get('categories'):
            category_ids = [int(cat_id) for cat_id in data['categories']]
            categories = session_db.query(Category).filter(Category.id.in_(category_ids)).all()
            product.categories = categories
        
        # Create initial stock record
        qty_on_hand = int(data.get('qty_on_hand', 0))
        stock = ProductStock(
            product_id=product.id,
            qty_on_hand=qty_on_hand
        )
        session_db.add(stock)
        
        session_db.commit()
        return jsonify({'success': True, 'message': 'Sản phẩm đã được tạo thành công'})
        
    except ValueError as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': 'Dữ liệu giá không hợp lệ'}), 400
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': f'Lỗi tạo sản phẩm: {str(e)}'}), 500
    finally:
        close_session(session_db)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@csrf.exempt
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
            product_dict = product.to_dict(include_relations=True)
            
            # Ensure stock data is included
            if not product_dict.get('stock') and product.stock:
                product_dict['stock'] = product.stock.to_dict()
            elif not product_dict.get('stock'):
                product_dict['stock'] = {'qty_on_hand': 0, 'in_stock': False}
                
            return render_template('admin/product_form.html',
                                 categories=[cat.to_dict() for cat in categories],
                                 product=product_dict)
        
        # Handle POST request - update product
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'}), 400
        
        try:
            # Update basic fields
            if 'name' in data:
                product.name = data['name']
            if 'short_desc' in data:
                product.short_desc = data['short_desc']
            if 'price' in data:
                product.price = float(data['price'])
            if 'sale_price' in data and data['sale_price']:
                product.sale_price = float(data['sale_price'])
            else:
                product.sale_price = None
            if 'image_url' in data:
                product.image_url = data['image_url']
            if 'is_active' in data:
                product.is_active = bool(data['is_active'])
            
            # Update categories
            if 'categories' in data:
                category_ids = [int(cat_id) for cat_id in data['categories']] if data['categories'] else []
                categories = session_db.query(Category).filter(Category.id.in_(category_ids)).all()
                product.categories = categories
            
            # Update stock
            if 'qty_on_hand' in data:
                if product.stock:
                    product.stock.qty_on_hand = int(data['qty_on_hand'])
                else:
                    # Create stock record if doesn't exist
                    stock = ProductStock(
                        product_id=product.id,
                        qty_on_hand=int(data['qty_on_hand'])
                    )
                    session_db.add(stock)
            
            session_db.commit()
            return jsonify({'success': True, 'message': 'Sản phẩm đã được cập nhật thành công'})
            
        except ValueError as e:
            session_db.rollback()
            return jsonify({'success': False, 'message': 'Dữ liệu giá không hợp lệ'}), 400
        except Exception as e:
            session_db.rollback()
            return jsonify({'success': False, 'message': f'Lỗi cập nhật sản phẩm: {str(e)}'}), 500
        
    finally:
        close_session(session_db)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@csrf.exempt
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
            flash('Không tìm thấy đ�n hàng', 'error')
            return redirect(url_for('admin.orders'))
        
        # Pass the order object directly instead of converting to dict
        # This preserves datetime objects for template strftime usage
        return render_template('admin/order_detail.html', order=order)
        
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


@admin_bp.route('/product-sales')
@admin_required
def product_sales():
    """Product sale management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', '', type=str)
    sale_status = request.args.get('sale_status', '', type=str)
    per_page = 20
    
    session_db = get_session()
    try:
        query = session_db.query(Product).filter(Product.is_active == True)
        
        # Search filter
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        # Category filter
        if category_id:
            query = query.join(Product.categories).filter(Category.id == category_id)
        
        # Sale status filter
        if sale_status == 'on_sale':
            query = query.filter(Product.sale_active == True)
        elif sale_status == 'not_on_sale':
            query = query.filter(Product.sale_active == False)
        
        total = query.count()
        products = query.order_by(Product.name).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        # Get categories for filter
        categories = session_db.query(Category).filter(Category.is_active == True).all()
        
        return render_template('admin/product_sales.html',
                             products=[p.to_dict(include_relations=True) for p in products],
                             categories=[cat.to_dict() for cat in categories],
                             total=total,
                             page=page,
                             per_page=per_page,
                             search=search,
                             category_id=category_id,
                             sale_status=sale_status)
    finally:
        close_session(session_db)


@admin_bp.route('/product-sales/<int:product_id>/set-sale', methods=['POST'])
@csrf.exempt
@admin_required
def set_product_sale(product_id):
    """Set sale price for a product"""
    data = request.get_json()
    session_db = get_session()
    try:
        sale_service = ProductSaleService(session_db)
        
        sale_price = data.get('sale_price')
        sale_start = data.get('sale_start')
        sale_end = data.get('sale_end')
        
        # Parse dates
        start_date = None
        end_date = None
        
        if sale_start:
            try:
                start_date = datetime.fromisoformat(sale_start.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'success': False, 'message': 'Định dạng ngày bắt đầu không hợp lệ'}), 400
        
        if sale_end:
            try:
                end_date = datetime.fromisoformat(sale_end.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'success': False, 'message': 'Định dạng ngày kết thúc không hợp lệ'}), 400
        
        # Update product using service
        product = sale_service.set_product_sale(product_id, sale_price, start_date, end_date)
        
        return jsonify({
            'success': True, 
            'message': 'Đã thiết lập giá khuyến mãi thành công',
            'product': product.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra: ' + str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/product-sales/<int:product_id>/remove-sale', methods=['POST'])
@csrf.exempt
@admin_required
def remove_product_sale(product_id):
    """Remove sale price from a product"""
    session_db = get_session()
    try:
        sale_service = ProductSaleService(session_db)
        product = sale_service.remove_product_sale(product_id)
        
        return jsonify({
            'success': True, 
            'message': 'Đã xóa giá khuyến mãi thành công',
            'product': product.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra: ' + str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/product-sales/bulk-actions', methods=['POST'])
@csrf.exempt
@admin_required
def bulk_sale_actions():
    """Bulk actions for product sales"""
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    action = data.get('action')
    
    if not product_ids:
        return jsonify({'success': False, 'message': 'Không có sản phẩm nào được chọn'}), 400
    
    session_db = get_session()
    try:
        sale_service = ProductSaleService(session_db)
        
        if action == 'remove_sale':
            count = sale_service.bulk_remove_sales(product_ids)
            return jsonify({
                'success': True, 
                'message': f'Đã xóa giá khuyến mãi cho {count} sản phẩm'
            })
        
        elif action == 'activate_sale':
            count = sale_service.bulk_activate_sales(product_ids)
            return jsonify({
                'success': True, 
                'message': f'Đã kích hoạt khuyến mãi cho {count} sản phẩm'
            })
        
        elif action == 'deactivate_sale':
            count = sale_service.bulk_deactivate_sales(product_ids)
            return jsonify({
                'success': True, 
                'message': f'Đã tạm dừng khuyến mãi cho {count} sản phẩm'
            })
        
        else:
            return jsonify({'success': False, 'message': 'Hành động không hợp lệ'}), 400
            
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra: ' + str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/product-sales/auto-update', methods=['POST'])
@csrf.exempt
@admin_required
def auto_update_sales():
    """Auto update product sale status based on dates"""
    session_db = get_session()
    try:
        sale_service = ProductSaleService(session_db)
        updated_count = sale_service.auto_update_sale_status()
        
        return jsonify({
            'success': True, 
            'message': f'Đã cập nhật trạng thái cho {updated_count} sản phẩm',
            'updated_count': updated_count
        })
        
    except Exception as e:
        session_db.rollback()
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra: ' + str(e)}), 400
    finally:
        close_session(session_db)


@admin_bp.route('/product-sales/statistics')
@admin_required
def sale_statistics():
    """Get sale statistics"""
    session_db = get_session()
    try:
        sale_service = ProductSaleService(session_db)
        stats = sale_service.get_sale_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Có lỗi xảy ra: ' + str(e)}), 400
    finally:
        close_session(session_db)