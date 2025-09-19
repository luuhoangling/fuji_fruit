from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.services.stock_service import StockService
from app.services.pricing_service import PricingService
from app.services.order_service import OrderService
from app.services.review_service import ReviewService
from app.services.shipping_service import ShippingService
from app.repositories.category_repo import CategoryRepository
from app.repositories.product_repo import ProductRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.review_repo import ReviewRepository
from app.blueprints.site.forms import ReviewForm, CheckoutForm, LoginForm, RegisterForm
from app.models.user import User
from app.auth import hash_password, check_password
from sqlalchemy.orm import sessionmaker
from app.db import get_db_session
import uuid

site_bp = Blueprint('site', __name__)

# Utility functions
def get_cart_from_session():
    """Get cart items from session with current prices"""
    cart = session.get('cart', {})
    if not cart:
        return [], 0
    
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        pricing_service = PricingService()
        items = []
        subtotal = 0
        
        for product_id, qty in cart.items():
            product = product_repo.get_by_id(int(product_id))
            if product:
                price = pricing_service.get_effective_price(product.id)
                line_total = price * qty
                items.append({
                    'product_id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'image_url': product.image_url,
                    'unit_price': price,
                    'qty': qty,
                    'line_total': line_total
                })
                subtotal += line_total
        
        return items, subtotal
    finally:
        db_session.close()

def get_cart_count():
    """Get total items count in cart"""
    cart = session.get('cart', {})
    return sum(cart.values())

def calculate_shipping_fee(subtotal, province=None):
    """Calculate shipping fee based on subtotal and province"""
    if subtotal >= 300000:  # Free shipping for orders >= 300k
        return 0
    
    # Default shipping rates
    if province and province.lower() in ['hà nội', 'tp.hcm', 'ho chi minh']:
        return 15000
    else:
        return 25000

@site_bp.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        categories = category_repo.get_all_active()
        cart_count = get_cart_count()
        
        return {
            'categories': categories,
            'cart_count': cart_count
        }
    finally:
        db_session.close()

# Routes
@site_bp.route('/')
def home():
    """Home page - categories, new products, sale products"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        product_repo = ProductRepository(db_session)
        pricing_service = PricingService()
        
        categories = category_repo.get_all_active()
        
        # Get 12 newest products
        new_products = product_repo.get_latest_products(limit=12)
        
        # Get 12 products on sale
        sale_products = product_repo.get_products_on_sale(limit=12)
        
        # Add pricing info
        for product in new_products + sale_products:
            product.price = pricing_service.get_effective_price(product.id)
            product.original_price = product.price if not pricing_service.is_on_sale(product.id) else product.price
        
        return render_template('site/home.html',
                             categories=categories,
                             new_products=new_products,
                             sale_products=sale_products)
    finally:
        db_session.close()

@site_bp.route('/c/<slug>')
def category(slug):
    """Category listing with filtering and pagination"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        product_repo = ProductRepository(db_session)
        pricing_service = PricingService()
        
        category = category_repo.get_by_slug(slug)
        if not category:
            flash('Danh mục không tồn tại', 'error')
            return redirect(url_for('site.home'))
        
        # Get query parameters
        q = request.args.get('q', '')
        price_min = request.args.get('price_min', type=int)
        price_max = request.args.get('price_max', type=int)
        sort = request.args.get('sort', 'newest')
        page = request.args.get('page', 1, type=int)
        page_size = 24
        
        # Get products with filters
        products, total = product_repo.get_by_category_with_filters(
            category_id=category.id,
            search_term=q,
            price_min=price_min,
            price_max=price_max,
            sort_by=sort,
            page=page,
            per_page=page_size
        )
        
        # Add pricing info
        for product in products:
            product.price = pricing_service.get_effective_price(product.id)
            product.original_price = product.price if not pricing_service.is_on_sale(product.id) else product.price_original
        
        return render_template('site/category.html',
                             category=category,
                             items=products,
                             total=total,
                             page=page,
                             page_size=page_size,
                             q=q,
                             price_min=price_min,
                             price_max=price_max,
                             sort=sort)
    finally:
        db_session.close()

@site_bp.route('/products')
def products():
    """All products page with filtering and pagination"""
    db_session = get_db_session()
    try:
        category_repo = CategoryRepository(db_session)
        product_repo = ProductRepository(db_session)
        pricing_service = PricingService()
        
        # Get query parameters
        q = request.args.get('q', '')
        category_id = request.args.get('category', type=int)
        price_min = request.args.get('price_min', type=int)
        price_max = request.args.get('price_max', type=int)
        sort = request.args.get('sort', 'newest')
        page = request.args.get('page', 1, type=int)
        page_size = 24
        
        # Get products with filters
        products, total = product_repo.get_all_with_filters(
            search_term=q,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
            sort_by=sort,
            page=page,
            per_page=page_size
        )
        
        # Add pricing info
        for product in products:
            product.price = pricing_service.get_effective_price(product.id)
            product.original_price = product.price if not pricing_service.is_on_sale(product.id) else product.price_original
        
        # Get all categories for filter
        categories = category_repo.get_all_active()
        
        # Get selected category for display
        selected_category = None
        if category_id:
            selected_category = category_repo.get_by_id(category_id)
        
        return render_template('site/products.html',
                             items=products,
                             total=total,
                             page=page,
                             page_size=page_size,
                             q=q,
                             categories=categories,
                             selected_category=selected_category,
                             category_id=category_id,
                             price_min=price_min,
                             price_max=price_max,
                             sort=sort)
    finally:
        db_session.close()

@site_bp.route('/p/<slug>')
def product_detail(slug):
    """Product detail page"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        review_repo = ReviewRepository(db_session)
        pricing_service = PricingService()
        stock_service = StockService()
        
        product = product_repo.get_by_slug(slug)
        if not product:
            flash('Sản phẩm không tồn tại', 'error')
            return redirect(url_for('site.home'))
        
        # Get pricing info
        product.price = pricing_service.get_effective_price(product.id)
        product.original_price = product.price if not pricing_service.is_on_sale(product.id) else product.price_original
        
        # Get stock info
        stock_info = stock_service.get_stock_info(product.id)
        product.stock = {
            'in_stock': stock_info['in_stock'],
            'qty': stock_info.get('qty_on_hand')
        }
        
        # Get reviews with pagination
        page = request.args.get('page', 1, type=int)
        reviews_data = review_repo.get_by_product_with_pagination(
            product_id=product.id,
            page=page,
            per_page=10
        )
        
        # Create review form
        review_form = ReviewForm()
        
        return render_template('site/product_detail.html',
                             product=product,
                             reviews=reviews_data,
                             review_form=review_form)
    finally:
        db_session.close()

@site_bp.route('/p/<slug>/reviews', methods=['POST'])
def submit_review(slug):
    """Submit product review"""
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        review_service = ReviewService()
        
        product = product_repo.get_by_slug(slug)
        if not product:
            flash('Sản phẩm không tồn tại', 'error')
            return redirect(url_for('site.home'))
        
        form = ReviewForm()
        if form.validate_on_submit():
            try:
                review_service.create_review(
                    product_id=product.id,
                    user_name=form.user_name.data or 'Khách hàng',
                    rating=form.rating.data,
                    content=form.content.data
                )
                flash('Đánh giá của bạn đã được gửi thành công!', 'success')
            except Exception as e:
                flash('Có lỗi xảy ra khi gửi đánh giá', 'error')
        else:
            flash('Vui lòng kiểm tra lại thông tin đánh giá', 'error')
        
        return redirect(url_for('site.product_detail', slug=slug) + '#reviews')
    finally:
        db_session.close()

@site_bp.route('/cart')
def cart():
    """Shopping cart page"""
    items, subtotal = get_cart_from_session()
    return render_template('site/cart.html',
                         items=items,
                         subtotal=subtotal)

@site_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    product_id = request.json.get('product_id')
    qty = request.json.get('qty', 1)
    
    if not product_id:
        return jsonify({'success': False, 'message': 'Thiếu thông tin sản phẩm'})
    
    # Validate product exists and in stock
    db_session = get_db_session()
    try:
        product_repo = ProductRepository(db_session)
        stock_service = StockService()
        
        product = product_repo.get_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại'})
        
        stock_info = stock_service.get_stock_info(product_id)
        if not stock_info['in_stock']:
            return jsonify({'success': False, 'message': 'Sản phẩm đã hết hàng'})
        
        # Add to session cart
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        cart[product_id_str] = cart.get(product_id_str, 0) + qty
        session['cart'] = cart
        
        return jsonify({
            'success': True,
            'message': 'Đã thêm vào giỏ hàng',
            'cart_count': get_cart_count()
        })
    finally:
        db_session.close()

@site_bp.route('/cart/update', methods=['POST'])
def update_cart():
    """Update cart quantities"""
    updates = request.json.get('updates', {})
    
    cart = session.get('cart', {})
    for product_id, qty in updates.items():
        if qty <= 0:
            cart.pop(product_id, None)
        else:
            cart[product_id] = qty
    
    session['cart'] = cart
    
    items, subtotal = get_cart_from_session()
    return jsonify({
        'success': True,
        'subtotal': subtotal,
        'cart_count': get_cart_count()
    })

@site_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    items, subtotal = get_cart_from_session()
    if not items:
        flash('Giỏ hàng trống', 'error')
        return redirect(url_for('site.cart'))
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        db_session = get_db_session()
        try:
            order_service = OrderService()
            
            # Calculate shipping
            shipping_fee = calculate_shipping_fee(subtotal, form.province.data)
            
            # Create order
            order_data = {
                'customer_name': form.customer_name.data,
                'customer_phone': form.phone.data,
                'shipping_address': f"{form.address.data}, {form.ward.data}, {form.district.data}, {form.province.data}",
                'payment_method': form.payment_method.data,
                'items': [{'product_id': item['product_id'], 'qty': item['qty']} for item in items],
                'subtotal': subtotal,
                'shipping_fee': shipping_fee,
                'discount': 0
            }
            
            order = order_service.create_order(**order_data)
            
            # Clear cart
            session.pop('cart', None)
            
            flash('Đặt hàng thành công!', 'success')
            return redirect(url_for('site.order_detail', order_code=order.order_code))
            
        except Exception as e:
            flash('Có lỗi xảy ra khi đặt hàng', 'error')
        finally:
            db_session.close()
    
    # Calculate estimated shipping
    shipping_fee = calculate_shipping_fee(subtotal)
    
    return render_template('site/checkout.html',
                         form=form,
                         items=items,
                         subtotal=subtotal,
                         shipping_fee=shipping_fee,
                         grand_total=subtotal + shipping_fee)

@site_bp.route('/orders/<order_code>')
def order_detail(order_code):
    """Order detail page"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        order_service = OrderService()
        
        order = order_repo.get_by_order_code(order_code)
        if not order:
            flash('Đơn hàng không tồn tại', 'error')
            return redirect(url_for('site.home'))
        
        # Get order timeline
        timeline = order_service.get_order_timeline(order.id)
        
        return render_template('site/order_detail.html',
                             order=order,
                             timeline=timeline)
    finally:
        db_session.close()

@site_bp.route('/orders/<order_code>/mock-pay', methods=['POST'])
def mock_pay(order_code):
    """Mock payment for transfer orders"""
    db_session = get_db_session()
    try:
        order_repo = OrderRepository(db_session)
        order_service = OrderService()
        
        order = order_repo.get_by_order_code(order_code)
        if not order:
            flash('Đơn hàng không tồn tại', 'error')
            return redirect(url_for('site.home'))
        
        if order.payment_method != 'MOCK_TRANSFER':
            flash('Phương thức thanh toán không hợp lệ', 'error')
            return redirect(url_for('site.order_detail', order_code=order_code))
        
        if order.payment_status != 'unpaid':
            flash('Đơn hàng đã được thanh toán', 'info')
            return redirect(url_for('site.order_detail', order_code=order_code))
        
        # Process mock payment
        order_service.process_mock_payment(order.id)
        
        flash('Xác nhận thanh toán thành công!', 'success')
        return redirect(url_for('site.order_detail', order_code=order_code))
        
    except Exception as e:
        flash('Có lỗi xảy ra khi xử lý thanh toán', 'error')
        return redirect(url_for('site.order_detail', order_code=order_code))


# Authentication routes
@site_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    form = LoginForm()
    
    if form.validate_on_submit():
        db_session = get_db_session()
        try:
            user = db_session.query(User).filter_by(email=form.email.data).first()
            
            if user and check_password(form.password.data, user.password_hash):
                if not user.is_active:
                    flash('Tài khoản đã bị vô hiệu hóa', 'error')
                    return render_template('site/login.html', form=form)
                
                # Update last login
                user.update_last_login()
                db_session.commit()
                
                # Store user in session
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_name'] = user.display_name
                
                if form.remember_me.data:
                    session.permanent = True
                
                flash(f'Chào mừng {user.full_name}!', 'success')
                
                # Redirect to next page or home
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('site.home'))
            else:
                flash('Email hoặc mật khẩu không đúng', 'error')
                
        except Exception as e:
            flash('Có lỗi xảy ra khi đăng nhập', 'error')
        finally:
            db_session.close()
    
    return render_template('site/login.html', form=form)


@site_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        db_session = get_db_session()
        try:
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hash_password(form.password.data),
                full_name=form.full_name.data or None,
                phone=form.phone.data or None,
                is_active=True,
                email_verified=False
            )
            
            db_session.add(user)
            db_session.commit()
            
            flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
            return redirect(url_for('site.login'))
            
        except Exception as e:
            db_session.rollback()
            flash('Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.', 'error')
        finally:
            db_session.close()
    
    return render_template('site/register.html', form=form)


@site_bp.route('/logout')
def logout():
    """Logout user"""
    user_name = session.get('user_name', 'Bạn')
    session.clear()
    flash(f'Tạm biệt {user_name}!', 'info')
    return redirect(url_for('site.home'))


@site_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem thông tin cá nhân', 'warning')
        return redirect(url_for('site.login'))
    
    db_session = get_db_session()
    try:
        user = db_session.query(User).filter_by(id=session['user_id']).first()
        if not user:
            session.clear()
            flash('Phiên đăng nhập đã hết hạn', 'warning')
            return redirect(url_for('site.login'))
        
        return render_template('site/profile.html', user=user)
    finally:
        db_session.close()