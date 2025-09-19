from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.stock_service import StockService
from app.services.pricing_service import PricingService
from app.services.order_service import OrderService
from app.services.review_service import ReviewService
from app.repositories.category_repo import CategoryRepository
from app.repositories.product_repo import ProductRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.review_repo import ReviewRepository
from app.repositories.stock_repo import StockRepository
from app.blueprints.admin.forms import ProductForm, StockForm, CategoryForm, OrderStatusForm
from app.db import get_db_session
from sqlalchemy.orm import sessionmaker

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        product_repo = ProductRepository(db_session)
        stock_service = StockService()
        
        # Recent orders
        recent_orders = order_repo.get_recent_orders(limit=10)
        
        # Low stock products
        low_stock_products = stock_service.get_low_stock_products(threshold=10)
        
        # Stats
        stats = {
            'total_orders': order_repo.count_orders(),
            'pending_orders': order_repo.count_orders_by_status('pending'),
            'total_products': product_repo.count_products(),
            'low_stock_count': len(low_stock_products)
        }
        
        return render_template('admin/dashboard.html',
                             recent_orders=recent_orders,
                             low_stock_products=low_stock_products,
                             stats=stats)
    finally:
        db_session.close()

# Products Management
@admin_bp.route('/products')
def products():
    """List all products"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        pricing_service = PricingService()
        
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        products, total = product_repo.search_products(
            search_term=search,
            page=page,
            per_page=per_page
        )
        
        # Add pricing info
        for product in products:
            product.effective_price = pricing_service.get_effective_price(product.id)
            product.on_sale = pricing_service.is_on_sale(product.id)
        
        return render_template('admin/products.html',
                             products=products,
                             total=total,
                             page=page,
                             per_page=per_page,
                             search=search)
    finally:
        db_session.close()

@admin_bp.route('/products/new', methods=['GET', 'POST'])
def product_new():
    """Create new product"""
    form = ProductForm()
    
    if form.validate_on_submit():
        db_session = get_db_session()
        try:
            product_repo = ProductRepository(db_session)
            
            product_data = {
                'name': form.name.data,
                'slug': form.slug.data,
                'short_desc': form.short_desc.data,
                'image_url': form.image_url.data,
                'price': form.price.data,
                'is_active': form.is_active.data,
                'sale_price': form.sale_price.data,
                'sale_start': form.sale_start.data,
                'sale_end': form.sale_end.data
            }
            
            product = product_repo.create(**product_data)
            flash('Sản phẩm đã được tạo thành công', 'success')
            return redirect(url_for('admin.products'))
            
        except Exception as e:
            flash('Có lỗi xảy ra khi tạo sản phẩm', 'error')
        finally:
            db_session.close()
    
    return render_template('admin/product_form.html', form=form, action='new')

@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def product_edit(id):
    """Edit product"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        product = product_repo.get_by_id(id)
        
        if not product:
            flash('Sản phẩm không tồn tại', 'error')
            return redirect(url_for('admin.products'))
        
        form = ProductForm(obj=product)
        
        if form.validate_on_submit():
            try:
                form.populate_obj(product)
                db_session.commit()
                flash('Sản phẩm đã được cập nhật', 'success')
                return redirect(url_for('admin.products'))
            except Exception as e:
                flash('Có lỗi xảy ra khi cập nhật sản phẩm', 'error')
                db_session.rollback()
        
        return render_template('admin/product_form.html', form=form, product=product, action='edit')
    finally:
        db_session.close()

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
def product_delete(id):
    """Delete product"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        product = product_repo.get_by_id(id)
        
        if not product:
            flash('Sản phẩm không tồn tại', 'error')
        else:
            product_repo.delete(id)
            flash('Sản phẩm đã được xóa', 'success')
    except Exception as e:
        flash('Có lỗi xảy ra khi xóa sản phẩm', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for('admin.products'))

# Stock Management
@admin_bp.route('/stock/<int:product_id>', methods=['GET', 'POST'])
def stock_manage(product_id):
    """Manage product stock"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        stock_service = StockService()
        
        product = product_repo.get_by_id(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'error')
            return redirect(url_for('admin.products'))
        
        # Get current stock
        stock_info = stock_service.get_stock_info(product_id)
        
        form = StockForm()
        if form.validate_on_submit():
            try:
                stock_service.update_stock(product_id, form.qty_on_hand.data)
                flash('Tồn kho đã được cập nhật', 'success')
                return redirect(url_for('admin.products'))
            except Exception as e:
                flash('Có lỗi xảy ra khi cập nhật tồn kho', 'error')
        else:
            # Pre-populate form with current stock
            form.qty_on_hand.data = stock_info.get('qty_on_hand', 0)
        
        return render_template('admin/stock_form.html', 
                             form=form, 
                             product=product, 
                             stock_info=stock_info)
    finally:
        db_session.close()

# Categories Management
@admin_bp.route('/categories')
def categories():
    """List all categories"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        categories = category_repo.get_all_with_hierarchy()
        
        return render_template('admin/categories.html', categories=categories)
    finally:
        db_session.close()

@admin_bp.route('/categories/new', methods=['GET', 'POST'])
def category_new():
    """Create new category"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        form = CategoryForm()
        
        # Get parent categories for dropdown
        categories = category_repo.get_all_active()
        form.parent_id.choices = [(0, 'Không có danh mục cha')] + [(c.id, c.name) for c in categories]
        
        if form.validate_on_submit():
            try:
                category_data = {
                    'name': form.name.data,
                    'slug': form.slug.data,
                    'parent_id': form.parent_id.data if form.parent_id.data > 0 else None
                }
                
                category = category_repo.create(**category_data)
                flash('Danh mục đã được tạo thành công', 'success')
                return redirect(url_for('admin.categories'))
                
            except Exception as e:
                flash('Có lỗi xảy ra khi tạo danh mục', 'error')
        
        return render_template('admin/category_form.html', form=form, action='new')
    finally:
        db_session.close()

@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
def category_edit(id):
    """Edit category"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        category = category_repo.get_by_id(id)
        
        if not category:
            flash('Danh mục không tồn tại', 'error')
            return redirect(url_for('admin.categories'))
        
        form = CategoryForm(obj=category)
        
        # Get parent categories for dropdown (exclude self and children)
        categories = category_repo.get_all_active()
        valid_parents = [c for c in categories if c.id != id]
        form.parent_id.choices = [(0, 'Không có danh mục cha')] + [(c.id, c.name) for c in valid_parents]
        
        if form.validate_on_submit():
            try:
                form.populate_obj(category)
                if form.parent_id.data == 0:
                    category.parent_id = None
                db_session.commit()
                flash('Danh mục đã được cập nhật', 'success')
                return redirect(url_for('admin.categories'))
            except Exception as e:
                flash('Có lỗi xảy ra khi cập nhật danh mục', 'error')
                db_session.rollback()
        
        return render_template('admin/category_form.html', form=form, category=category, action='edit')
    finally:
        db_session.close()

@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
def category_delete(id):
    """Delete category"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        category = category_repo.get_by_id(id)
        
        if not category:
            flash('Danh mục không tồn tại', 'error')
        else:
            category_repo.delete(id)
            flash('Danh mục đã được xóa', 'success')
    except Exception as e:
        flash('Có lỗi xảy ra khi xóa danh mục', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for('admin.categories'))

# Reviews Management
@admin_bp.route('/reviews')
def reviews():
    """List all reviews"""
    db_session = get_db_session()
    try:
        review_repo = ReviewRepository(db_session)
        
        product_id = request.args.get('product_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        if product_id:
            reviews_data = review_repo.get_by_product_with_pagination(
                product_id=product_id,
                page=page,
                per_page=per_page
            )
        else:
            reviews_data = review_repo.get_all_with_pagination(
                page=page,
                per_page=per_page
            )
        
        return render_template('admin/reviews.html',
                             reviews=reviews_data,
                             page=page,
                             per_page=per_page,
                             product_id=product_id)
    finally:
        db_session.close()

@admin_bp.route('/reviews/<int:id>/delete', methods=['POST'])
def review_delete(id):
    """Delete review"""
    db_session = get_db_session()
    try:
        review_service = ReviewService()
        review_service.delete_review(id)
        flash('Đánh giá đã được xóa', 'success')
    except Exception as e:
        flash('Có lỗi xảy ra khi xóa đánh giá', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for('admin.reviews'))

# Orders Management
@admin_bp.route('/orders')
def orders():
    """List all orders"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        orders, total = order_repo.get_orders_with_filters(
            status=status,
            page=page,
            per_page=per_page
        )
        
        return render_template('admin/orders.html',
                             orders=orders,
                             total=total,
                             page=page,
                             per_page=per_page,
                             status=status)
    finally:
        db_session.close()

@admin_bp.route('/orders/<int:id>')
def order_detail(id):
    """Admin order detail"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        order_service = OrderService()
        
        order = order_repo.get_by_id(id)
        if not order:
            flash('Đơn hàng không tồn tại', 'error')
            return redirect(url_for('admin.orders'))
        
        # Get order timeline
        timeline = order_service.get_order_timeline(order.id)
        
        # Status form
        status_form = OrderStatusForm()
        status_form.status.data = order.status
        
        return render_template('admin/order_detail.html',
                             order=order,
                             timeline=timeline,
                             status_form=status_form)
    finally:
        db_session.close()

@admin_bp.route('/orders/<int:id>/status', methods=['POST'])
def order_update_status(id):
    """Update order status"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        order_service = OrderService()
        
        order = order_repo.get_by_id(id)
        if not order:
            flash('Đơn hàng không tồn tại', 'error')
            return redirect(url_for('admin.orders'))
        
        form = OrderStatusForm()
        if form.validate_on_submit():
            try:
                order_service.update_order_status(id, form.status.data)
                flash('Trạng thái đơn hàng đã được cập nhật', 'success')
            except Exception as e:
                flash('Có lỗi xảy ra khi cập nhật trạng thái', 'error')
        
        return redirect(url_for('admin.order_detail', id=id))
    finally:
        db_session.close()

@admin_bp.route('/orders/<int:id>/mock-pay', methods=['POST'])
def order_mock_pay(id):
    """Process mock payment for order"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        order_service = OrderService()
        
        order = order_repo.get_by_id(id)
        if not order:
            flash('Đơn hàng không tồn tại', 'error')
            return redirect(url_for('admin.orders'))
        
        try:
            order_service.process_mock_payment(id)
            flash('Đã xử lý thanh toán thành công', 'success')
        except Exception as e:
            flash('Có lỗi xảy ra khi xử lý thanh toán', 'error')
        
        return redirect(url_for('admin.order_detail', id=id))
    finally:
        db_session.close()