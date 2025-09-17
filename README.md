# Fuji Store - E-commerce Website

Dự án website thương mại điện tử được phát triển theo tài liệu hướng dẫn Fuji_Student_Functions.md

## Mô tả dự án

Fuji Store là một website bán hàng trực tuyến đầy đủ tính năng với:
- Hệ thống đăng ký/đăng nhập người dùng
- Danh mục sản phẩm và tìm kiếm
- Giỏ hàng và thanh toán (COD)
- Quản lý đơn hàng
- Interface quản trị viên
- Responsive design với Bootstrap 5

## Công nghệ sử dụng

### Backend
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM với automap cho database
- **PyMySQL** - MySQL database connector
- **Flask-JWT-Extended** - JWT authentication
- **bcrypt** - Password hashing
- **Werkzeug** - WSGI utilities

### Frontend
- **Bootstrap 5** - CSS framework
- **JavaScript ES6** - Client-side scripting
- **Bootstrap Icons** - Icon library

### Database
- **MySQL/MariaDB** - Database server
- **fuji.sql** - Database schema

## Cấu trúc dự án

```
fuji_app/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── db.py                 # Database configuration
│   ├── models.py             # SQLAlchemy automap models
│   ├── auth.py               # Authentication utilities
│   └── blueprints/
│       ├── api/              # API endpoints
│       │   ├── __init__.py
│       │   ├── routes.py     # Main API routes
│       │   ├── auth_routes.py
│       │   ├── catalog_routes.py
│       │   ├── cart_routes.py
│       │   ├── order_routes.py
│       │   └── admin_routes.py
│       └── public/           # Public web pages
│           ├── __init__.py
│           ├── routes.py
│           └── templates/
│               ├── base.html
│               ├── index.html
│               ├── products.html
│               └── stores.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
├── config.py                 # App configuration
├── requirements.txt          # Python dependencies
├── wsgi.py                   # WSGI entry point
├── .env                      # Environment variables
├── fuji.sql                  # Database schema
└── README.md                 # This file
```

## Cài đặt và chạy

### 1. Chuẩn bị môi trường

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình database

```bash
# Khởi động MySQL/MariaDB server
# Import database schema
mysql -u root -p < fuji.sql
```

### 3. Cấu hình môi trường

Tạo file `.env` (đã có sẵn):
```
FLASK_APP=wsgi.py
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=mysql+pymysql://root:@localhost/fuji_db
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRES=86400
```

### 4. Chạy ứng dụng

```bash
# Development server
flask run

# Hoặc với Python
python wsgi.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## API Endpoints

### Authentication
- `POST /api/auth/register` - Đăng ký người dùng
- `POST /api/auth/login` - Đăng nhập
- `POST /api/auth/logout` - Đăng xuất
- `GET /api/auth/profile` - Thông tin người dùng
- `PUT /api/auth/profile` - Cập nhật thông tin

### Products & Catalog
- `GET /api/products` - Danh sách sản phẩm (có filter, search)
- `GET /api/products/<slug>` - Chi tiết sản phẩm
- `GET /api/categories` - Danh sách danh mục
- `GET /api/brands` - Danh sách thương hiệu

### Shopping Cart
- `GET /api/cart` - Xem giỏ hàng
- `POST /api/cart/items` - Thêm sản phẩm vào giỏ
- `PUT /api/cart/items/<item_id>` - Cập nhật số lượng
- `DELETE /api/cart/items/<item_id>` - Xóa sản phẩm

### Orders
- `POST /api/orders` - Tạo đơn hàng
- `GET /api/orders` - Danh sách đơn hàng
- `GET /api/orders/<order_id>` - Chi tiết đơn hàng

### Stores
- `GET /api/stores` - Danh sách cửa hàng
- `GET /api/stores/<store_id>` - Chi tiết cửa hàng
- `GET /api/stores/provinces` - Danh sách tỉnh/thành

### Admin (yêu cầu quyền admin)
- `GET /api/admin/users` - Quản lý người dùng
- `POST /api/admin/products` - Tạo sản phẩm
- `PUT /api/admin/products/<id>` - Cập nhật sản phẩm
- `DELETE /api/admin/products/<id>` - Xóa sản phẩm
- `GET /api/admin/orders` - Quản lý đơn hàng
- `PUT /api/admin/orders/<id>/status` - Cập nhật trạng thái đơn hàng

## Tính năng chính

### Người dùng
1. **Đăng ký/Đăng nhập**: Hệ thống authentication với JWT
2. **Duyệt sản phẩm**: Xem danh sách, tìm kiếm, lọc theo danh mục/thương hiệu
3. **Giỏ hàng**: Thêm/xóa/cập nhật sản phẩm
4. **Đặt hàng**: Thanh toán COD (Cash on Delivery)
5. **Quản lý đơn hàng**: Theo dõi trạng thái đơn hàng

### Khách vãng lai
1. **Duyệt sản phẩm**: Xem toàn bộ catalog
2. **Giỏ hàng phiên**: Giỏ hàng lưu trong session
3. **Đặt hàng**: Có thể đặt hàng mà không cần đăng ký

### Admin
1. **Quản lý sản phẩm**: CRUD operations
2. **Quản lý đơn hàng**: Cập nhật trạng thái, xem chi tiết
3. **Quản lý người dùng**: Xem danh sách, cập nhật thông tin

## Database Schema

Database được thiết kế với các bảng chính:
- `users` - Thông tin người dùng
- `products` - Sản phẩm
- `product_variants` - Biến thể sản phẩm
- `categories` - Danh mục
- `brands` - Thương hiệu
- `orders` - Đơn hàng
- `order_items` - Chi tiết đơn hàng
- `cart_items` - Giỏ hàng
- `stores` - Cửa hàng

## Bảo mật

- **Password hashing**: Sử dụng bcrypt
- **JWT Authentication**: Token-based authentication
- **Input validation**: Kiểm tra dữ liệu đầu vào
- **Session management**: Quản lý phiên cho khách vãng lai

## Responsive Design

Website được thiết kế responsive với Bootstrap 5:
- Mobile-first approach
- Tương thích với tất cả thiết bị
- Interface thân thiện người dùng

## Deployment

### Production Setup
1. Cấu hình production database
2. Set FLASK_ENV=production
3. Cấu hình reverse proxy (nginx)
4. Sử dụng WSGI server (gunicorn, uWSGI)

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "wsgi.py"]
```

## Troubleshooting

### Common Issues
1. **Database connection error**: Kiểm tra MySQL server và cấu hình DATABASE_URL
2. **Import error**: Đảm bảo đã cài đặt tất cả dependencies
3. **Template not found**: Kiểm tra đường dẫn templates
4. **API errors**: Kiểm tra JWT token và permissions

### Debug Mode
```bash
export FLASK_DEBUG=True
flask run
```

## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

Dự án này được phát triển cho mục đích học tập.

## Support

Liên hệ hỗ trợ qua:
- Email: support@fujistore.com
- Hotline: 1900-xxxx

---

**Phát triển bởi**: Sinh viên theo hướng dẫn Fuji_Student_Functions.md
**Phiên bản**: 1.0.0
**Ngày cập nhật**: 2024