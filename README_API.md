# FujiShop API - E-commerce REST API

FujiShop API là một REST API hoàn chỉnh cho ứng dụng thương mại điện tử bán trái cây, được xây dựng với Flask, SQLAlchemy và MySQL.

## Tính năng

### Public API (Không cần authentication)
- **Catalog**: Xem danh mục, tìm kiếm sản phẩm với filter và phân trang
- **Product Details**: Xem thông tin chi tiết sản phẩm, giá effective price (tự động áp dụng sale)
- **Reviews**: Đọc và tạo đánh giá sản phẩm (với rate limiting)
- **Orders**: Tạo đơn hàng, xem chi tiết đơn, thanh toán giả lập (mock payment)

### Admin API (Cần JWT authentication)
- **Product Management**: CRUD sản phẩm, quản lý giá sale theo lịch
- **Category Management**: CRUD danh mục
- **Stock Management**: Cập nhật tồn kho
- **Order Management**: Xem, cập nhật trạng thái đơn hàng
- **Review Management**: Xem và xóa đánh giá

## Cài đặt

### 1. Clone và setup environment

```bash
cd fuji_app
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Cấu hình Database

Tạo file `.env`:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/fuji_db?charset=utf8mb4
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=development
```

### 3. Khởi tạo Database

```bash
# Tạo database
python manage.py init-db

# Seed dữ liệu mẫu
python manage.py seed-db
```

### 4. Chạy ứng dụng

```bash
python manage.py
# hoặc
flask run
```

API sẽ chạy tại: `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication
- **Public endpoints**: Không cần authentication
- **Admin endpoints**: Cần JWT token trong header `Authorization: Bearer <token>`

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {...}
  }
}
```

### Pagination
- Query params: `?page=1&page_size=24`
- Response headers: `X-Total-Count`, `X-Page`, `X-Per-Page`, `X-Total-Pages`
- Response meta:
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "page_size": 24,
    "total": 100,
    "pages": 5
  }
}
```

## API Endpoints

### 🔓 Public API

#### Categories
```http
GET /api/v1/categories
```
Trả về cây danh mục với children.

#### Products
```http
GET /api/v1/products?q=táo&category=hoa-qua-nhap-khau&price_min=50000&price_max=200000&sort=price_asc&page=1&page_size=24
```

**Sort options**: `price_asc`, `price_desc`, `newest`, `oldest`, `name_asc`, `name_desc`

**Response**:
```json
{
  "data": [
    {
      "id": 101,
      "name": "Táo Envy",
      "slug": "tao-envy",
      "price": 149000,
      "effective_price": 129000,
      "image_url": "...",
      "in_stock": true,
      "rating": {"avg": 4.7, "count": 35}
    }
  ],
  "meta": {"page": 1, "page_size": 24, "total": 321}
}
```

#### Product Detail
```http
GET /api/v1/products/{slug}
```

**Response**:
```json
{
  "id": 101,
  "name": "Táo Envy",
  "slug": "tao-envy",
  "price": 149000,
  "original_price": 149000,
  "effective_price": 129000,
  "image_url": "...",
  "short_desc": "...",
  "stock": {"in_stock": true, "qty": 42},
  "rating": {"avg": 4.7, "count": 35},
  "images": [".../1.jpg", ".../2.jpg"]
}
```

#### Reviews
```http
GET /api/v1/products/{slug}/reviews?page=1&page_size=10
POST /api/v1/products/{slug}/reviews
```

**Create Review**:
```json
{
  "user_name": "Minh",
  "rating": 5,
  "content": "Táo rất ngon và giòn!"
}
```

#### Orders
```http
POST /api/v1/orders
GET /api/v1/orders/{order_code}
POST /api/v1/orders/{order_code}/mock-pay
```

**Create Order** (với Idempotency-Key header):
```json
{
  "customer": {
    "name": "Nguyễn Văn Minh",
    "phone": "0901234567",
    "address": "123 Đường ABC, Quận 1",
    "province": "TP Hồ Chí Minh",
    "district": "Quận 1",
    "ward": "Phường Bến Nghé"
  },
  "payment_method": "MOCK_TRANSFER",
  "items": [
    {"product_id": 101, "qty": 2},
    {"product_id": 202, "qty": 1}
  ]
}
```

**Response**:
```json
{
  "order_code": "FJ-8X2K9C",
  "status": "pending",
  "payment_status": "unpaid",
  "amounts": {
    "subtotal": 380000,
    "shipping_fee": 30000,
    "discount": 0,
    "grand_total": 410000
  },
  "items": [...]
}
```

### 🔒 Admin API

#### Authentication
```http
POST /api/v1/admin/login
```
```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### Products Management
```http
GET /api/v1/admin/products?search=&page=1
POST /api/v1/admin/products
PUT /api/v1/admin/products/{id}
DELETE /api/v1/admin/products/{id}
PUT /api/v1/admin/products/{id}/sale
```

**Set Sale**:
```json
{
  "sale_price": 119000,
  "sale_start": "2025-09-20T00:00:00",
  "sale_end": "2025-09-30T23:59:59"
}
```

#### Stock Management
```http
PUT /api/v1/admin/stock/{product_id}
```
```json
{
  "qty_on_hand": 120
}
```

#### Orders Management
```http
GET /api/v1/admin/orders?status=pending&q=&page=1
GET /api/v1/admin/orders/{order_code}
PUT /api/v1/admin/orders/{order_code}/status
PUT /api/v1/admin/orders/{order_code}/mock-pay
```

**Update Status**:
```json
{
  "status": "confirmed"
}
```

## Ví dụ cURL

### Tìm kiếm sản phẩm
```bash
curl "http://localhost:5000/api/v1/products?q=táo&price_min=50000&sort=price_asc&page=1&page_size=24"
```

### Tạo đơn hàng với idempotency
```bash
curl -X POST "http://localhost:5000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 0e8b3f02-9d5a-4e0a-b2e3-6d5f4b4a1bcd" \
  -d '{
    "customer": {
      "name": "Nguyễn Văn Minh",
      "phone": "0901234567",
      "address": "123 Đường ABC",
      "province": "Hà Nội"
    },
    "payment_method": "MOCK_TRANSFER",
    "items": [{"product_id": 1, "qty": 2}]
  }'
```

### Mock payment
```bash
curl -X POST "http://localhost:5000/api/v1/orders/FJ-8X2K9C/mock-pay"
```

### Admin login
```bash
curl -X POST "http://localhost:5000/api/v1/admin/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Cập nhật tồn kho (cần JWT)
```bash
curl -X PUT "http://localhost:5000/api/v1/admin/stock/1" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"qty_on_hand": 120}'
```

## Features Details

### 🎯 Business Logic
- **Effective Pricing**: Tự động áp dụng sale price trong khoảng thời gian
- **Stock Management**: Lock và trừ kho khi tạo đơn, hoàn kho khi hủy
- **Shipping Calculator**: Miễn phí ship cho đơn >500k, phí theo tỉnh thành
- **Order Lifecycle**: pending → confirmed → fulfilled (hoặc cancelled)

### 🔧 Technical Features
- **Rate Limiting**: 5 reviews/phút per IP
- **Idempotency**: Tránh duplicate orders với UUID key
- **Pagination**: Meta info và headers
- **Validation**: Marshmallow schemas
- **Error Handling**: Standardized JSON error responses
- **Database Views**: `v_products_effective_price`, `v_product_rating`

### 📊 Database Schema
- **Categories**: Hierarchical với parent/children
- **Products**: Sale pricing theo lịch, nhiều ảnh
- **Stock**: Separate table cho inventory
- **Orders**: Snapshot giá + timeline events
- **Reviews**: Public reviews, admin có thể xóa

## Development

### Commands
```bash
# Reset database
python manage.py reset-db

# Init database
python manage.py init-db

# Seed sample data
python manage.py seed-db
```

### Project Structure
```
app/
├── models/          # SQLAlchemy models
├── schemas/         # Marshmallow validation
├── repositories/    # Database access layer
├── services/        # Business logic
├── api/            # REST endpoints
└── utils/          # Helpers (pagination, slugs, etc.)
```

### Configuration
- `config.py`: Database, JWT, rate limiting config
- `extensions.py`: Flask extensions setup
- `manage.py`: CLI commands và application runner

## Production Notes

1. **Database**: Sử dụng MySQL 8.x với proper indexing
2. **Caching**: Implement Redis cho idempotency và rate limiting
3. **Authentication**: Thay thế hardcoded admin credentials
4. **Logging**: Setup proper logging với file rotation
5. **Monitoring**: Add health checks và metrics
6. **Security**: HTTPS, CORS, input sanitization
7. **Performance**: Database connection pooling, query optimization

---

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

**API Version**: v1.0.0
**Framework**: Flask 2.3.3 + SQLAlchemy 2.0.23