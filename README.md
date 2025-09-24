# 🍓 Fuji Fruit - E-commerce Website

[![Flask](https://img.shields.io/badge/Flask-2.3.3-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

> 🌟 **Fuji Fruit** - Hệ thống thương mại điện tử chuyên bán trái cây tươi ngon, được xây dựng với Flask và MySQL.

## 📖 Mô tả dự án

**Fuji Fruit Store** là một ứng dụng web thương mại điện tử đầy đủ tính năng, được phát triển với Flask framework. Hệ thống cung cấp trải nghiệm mua sắm trực tuyến hoàn chỉnh từ duyệt sản phẩm đến thanh toán và quản lý đơn hàng.

### ✨ Tính năng nổi bật

- 🔐 **Hệ thống xác thực người dùng** - Đăng ký, đăng nhập với JWT
- 🛍️ **Quản lý sản phẩm** - Danh mục, tìm kiếm, lọc thông minh
- 🛒 **Giỏ hàng thông minh** - Session-based cho khách vãng lai
- 💰 **Thanh toán COD** - Thanh toán khi nhận hàng
- 📊 **Admin Dashboard** - Quản lý sản phẩm, đơn hàng, người dùng  
- 📱 **Responsive Design** - Tương thích mọi thiết bị
- 🔒 **Bảo mật cao** - Hash password, JWT tokens, CSRF protection

## 🛠️ Công nghệ sử dụng

### Backend Stack
- **[Flask 2.3.3](https://flask.palletsprojects.com/)** - Web framework chính
- **[SQLAlchemy 2.0.23](https://www.sqlalchemy.org/)** - ORM với automap models
- **[PyMySQL 1.1.0](https://pypi.org/project/PyMySQL/)** - MySQL database connector
- **[Flask-JWT-Extended 4.5.3](https://flask-jwt-extended.readthedocs.io/)** - JWT authentication
- **[bcrypt 4.0.1](https://pypi.org/project/bcrypt/)** - Password hashing
- **[Flask-Limiter 3.5.0](https://flask-limiter.readthedocs.io/)** - Rate limiting
- **[Marshmallow 3.21.3](https://marshmallow.readthedocs.io/)** - Serialization/validation

### Frontend Stack  
- **[Bootstrap 5.3.0](https://getbootstrap.com/)** - CSS framework
- **[Bootstrap Icons](https://icons.getbootstrap.com/)** - Icon library
- **[Font Awesome 6.0](https://fontawesome.com/)** - Additional icons
- **JavaScript ES6** - Client-side interactions

### Database & DevOps
- **[MySQL 8.0+](https://www.mysql.com/)** - Primary database
- **[Gunicorn 21.2.0](https://gunicorn.org/)** - WSGI HTTP Server
- **[Flask-Migrate 4.0.5](https://flask-migrate.readthedocs.io/)** - Database migrations

## 📁 Cấu trúc Project

```
fuji_app/
├── 📁 app/                           # Ứng dụng chính
│   ├── __init__.py                   # Flask app factory  
│   ├── auth.py                       # Authentication utilities
│   ├── db.py                         # Database configuration
│   ├── extensions.py                 # Flask extensions
│   ├── 📁 api/                       # REST API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                   # Auth API routes
│   │   ├── errors.py                 # Error handlers
│   │   └── public.py                 # Public API routes
│   ├── 📁 blueprints/                # Web interface blueprints
│   │   ├── 📁 admin/                 # Admin dashboard
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   └── 📁 site/                  # Public website
│   │       ├── __init__.py
│   │       ├── forms.py              # WTForms
│   │       └── views.py
│   ├── 📁 models/                    # Database models
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── order.py
│   │   ├── product.py
│   │   ├── review.py
│   │   └── user.py
│   ├── 📁 repositories/              # Data access layer
│   │   ├── category_repo.py
│   │   ├── order_repo.py
│   │   └── product_repo.py
│   ├── 📁 schemas/                   # Marshmallow schemas
│   │   ├── category.py
│   │   ├── order.py
│   │   └── product.py
│   ├── 📁 services/                  # Business logic
│   │   ├── order_service.py
│   │   ├── pricing_service.py
│   │   └── stock_service.py
│   ├── 📁 static/                    # Static assets
│   │   ├── css/custom.css
│   │   └── js/
│   ├── 📁 templates/                 # Jinja2 templates
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── 📁 admin/                 # Admin templates
│   │   ├── 📁 site/                  # Public templates
│   │   └── 📁 _partials/             # Template partials
│   └── 📁 utils/                     # Utility functions
│       ├── avatar_utils.py
│       ├── pagination.py
│       └── slugs.py
├── config.py                         # App configuration
├── init_db.py                        # Database initialization
├── manage.py                         # Management commands
├── requirements.txt                  # Python dependencies
├── wsgi.py                          # WSGI entry point
├── .env                             # Environment variables
└── README.md                        # Documentation
```

## 🚀 Cài đặt và Triển khai

### 📋 Yêu cầu hệ thống

- **Python**: 3.8+ 
- **MySQL**: 8.0+ hoặc MariaDB 10.4+
- **Node.js**: 16+ (tùy chọn, cho dev tools)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/fuji-fruit.git
cd fuji-fruit
```

### 2️⃣ Thiết lập Python Environment

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac/Git Bash
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Cài đặt dependencies
pip install -r requirements.txt
```

### 3️⃣ Cấu hình Database

**Tạo database MySQL:**
```sql
CREATE DATABASE fuji CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fuji_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON fuji.* TO 'fuji_user'@'localhost';
FLUSH PRIVILEGES;
```

**Khởi tạo database:**
```bash
# Sử dụng script khởi tạo
python init_db.py

# Hoặc với Flask CLI
flask db upgrade
```

### 4️⃣ Cấu hình Environment

Sao chép và điều chỉnh file môi trường:
```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-super-secret-key-here

# Database Configuration
DATABASE_URL=mysql+pymysql://fuji_user:your_password@localhost:3306/fuji?charset=utf8mb4

# JWT Configuration  
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Optional: Redis for rate limiting
# REDIS_URL=redis://localhost:6379/0
```

### 5️⃣ Chạy ứng dụng

**Development Mode:**
```bash
# Với Flask CLI
flask run

# Hoặc với Python
python wsgi.py

# Với management script
python manage.py
```

**Production Mode:**
```bash
# Với Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

🌐 **Ứng dụng sẽ chạy tại:** http://localhost:5000

### 6️⃣ Tài khoản Admin mặc định

```
Username: admin
Password: 666666
```

## 📚 API Documentation

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/register` | Đăng ký tài khoản mới | ❌ |
| `POST` | `/api/v1/auth/login` | Đăng nhập người dùng | ❌ |
| `POST` | `/api/v1/auth/logout` | Đăng xuất | ✅ |
| `GET` | `/api/v1/auth/profile` | Thông tin người dùng | ✅ |
| `PUT` | `/api/v1/auth/profile` | Cập nhật thông tin | ✅ |

### 🛍️ Products & Catalog

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/products` | Danh sách sản phẩm + filter/search | ❌ |
| `GET` | `/api/v1/products/{slug}` | Chi tiết sản phẩm | ❌ |
| `GET` | `/api/v1/categories` | Danh sách danh mục | ❌ |
| `GET` | `/api/v1/brands` | Danh sách thương hiệu | ❌ |

### 🛒 Shopping Cart

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/cart` | Xem giỏ hàng | ❌ (Session) |
| `POST` | `/api/v1/cart/items` | Thêm sản phẩm | ❌ |
| `PUT` | `/api/v1/cart/items/{id}` | Cập nhật số lượng | ❌ |
| `DELETE` | `/api/v1/cart/items/{id}` | Xóa sản phẩm | ❌ |

### 📦 Orders Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/orders` | Tạo đơn hàng mới | ❌ |
| `GET` | `/api/v1/orders` | Danh sách đơn hàng | ✅ |
| `GET` | `/api/v1/orders/{id}` | Chi tiết đơn hàng | ✅ |

### 🏪 Stores & Locations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/stores` | Danh sách cửa hàng | ❌ |
| `GET` | `/api/v1/stores/{id}` | Chi tiết cửa hàng | ❌ |
| `GET` | `/api/v1/stores/provinces` | Danh sách tỉnh/thành | ❌ |

### 👨‍💼 Admin Endpoints (Requires Admin Role)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/admin/users` | Quản lý người dùng |
| `POST` | `/api/v1/admin/products` | Tạo sản phẩm mới |
| `PUT` | `/api/v1/admin/products/{id}` | Cập nhật sản phẩm |
| `DELETE` | `/api/v1/admin/products/{id}` | Xóa sản phẩm |
| `GET` | `/api/v1/admin/orders` | Quản lý đơn hàng |
| `PUT` | `/api/v1/admin/orders/{id}/status` | Cập nhật trạng thái |

### 🔍 API Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { ... }
  }
}
```

## ⭐ Tính năng chính

### 👤 Người dùng đã đăng ký
- ✅ **Hệ thống xác thực**: Đăng ký/đăng nhập với JWT tokens
- 🔍 **Tìm kiếm thông minh**: Lọc theo danh mục, thương hiệu, giá
- 🛒 **Giỏ hàng cá nhân**: Lưu trữ persistent, đồng bộ thiết bị
- 💳 **Thanh toán COD**: Thanh toán khi nhận hàng
- 📋 **Quản lý đơn hàng**: Theo dõi trạng thái, lịch sử mua hàng
- 👨‍💼 **Hồ sơ cá nhân**: Cập nhật thông tin, đổi mật khẩu

### 🚶‍♂️ Khách vãng lai
- 🌐 **Duyệt sản phẩm**: Xem toàn bộ catalog không cần đăng ký
- 🛍️ **Giỏ hàng session**: Lưu tạm trong phiên làm việc
- 📦 **Đặt hàng nhanh**: Checkout mà không cần tạo tài khoản
- 🔄 **Chuyển đổi dễ dàng**: Có thể đăng ký bất cứ lúc nào

### 👨‍💻 Quản trị viên
- 📊 **Dashboard tổng quan**: Thống kê bán hàng, đơn hàng
- 🏷️ **Quản lý sản phẩm**: CRUD operations, quản lý danh mục
- 📦 **Quản lý đơn hàng**: Cập nhật trạng thái, xử lý đơn hàng
- 👥 **Quản lý người dùng**: Xem thông tin, phân quyền
- 📈 **Báo cáo**: Doanh thu, sản phẩm bán chạy

## 🗄️ Database Schema

### Cấu trúc Database
Database được thiết kế với kiến trúc **SQLAlchemy Automap** để tự động ánh xạ từ schema có sẵn:

| Bảng | Mô tả | Quan hệ |
|------|-------|---------|
| `users` | Thông tin người dùng, authentication | 1-N với orders |
| `products` | Sản phẩm chính | N-M với categories |
| `product_stock` | Quản lý tồn kho | 1-1 với products |
| `categories` | Danh mục sản phẩm | N-M với products |
| `orders` | Đơn hàng | 1-N với order_items |
| `order_items` | Chi tiết đơn hàng | N-1 với orders |
| `cart_items` | Giỏ hàng | N-1 với users |
| `reviews` | Đánh giá sản phẩm | N-1 với products |

### 🔐 Bảo mật

| Tính năng | Công nghệ | Mô tả |
|-----------|-----------|-------|
| **Password Hashing** | bcrypt 4.0.1 | Hash password với salt |
| **JWT Authentication** | Flask-JWT-Extended | Token-based auth |
| **CSRF Protection** | Flask-WTF | Chống cross-site request forgery |
| **Rate Limiting** | Flask-Limiter | Giới hạn request để chống spam |
| **Input Validation** | Marshmallow | Validate dữ liệu đầu vào |
| **Session Security** | Flask Sessions | Secure session cho guest users |

### 📱 Responsive Design

- ✅ **Mobile-First**: Thiết kế ưu tiên mobile
- ✅ **Bootstrap 5.3**: Framework CSS hiện đại  
- ✅ **Cross-Browser**: Tương thích mọi trình duyệt
- ✅ **Performance**: Tối ưu tốc độ tải trang
- ✅ **Accessibility**: Hỗ trợ người khuyết tật

<div align="center">

**Phát triển với ❤️ Linh đẹp trai vcl**

⭐ **Đừng quên star repo nếu project hữu ích!** ⭐

**Version**: 2.0.0 | **Updated**: September 2025

</div>