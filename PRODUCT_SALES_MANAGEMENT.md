# Hệ thống quản lý khuyến mãi sản phẩm - Fuji Fruit

## Tổng quan

Hệ thống quản lý khuyến mãi sản phẩm cho phép admin thiết lập và quản lý giá khuyến mãi cho từng sản phẩm một cách độc lập, khác với hệ thống mã giảm giá (discount codes).

## Các tính năng chính

### 1. Quản lý khuyến mãi sản phẩm
- **Đường dẫn**: `/admin/product-sales`
- **Mô tả**: Giao diện chính để quản lý khuyến mãi cho tất cả sản phẩm
- **Chức năng**:
  - Xem danh sách sản phẩm với thông tin giá gốc, giá khuyến mãi, phần trăm giảm
  - Lọc theo danh mục, trạng thái khuyến mãi
  - Tìm kiếm theo tên sản phẩm
  - Phân trang

### 2. Thiết lập khuyến mãi cho sản phẩm
- **Chức năng**: Thiết lập giá khuyến mãi, thời gian bắt đầu và kết thúc
- **Validation**:
  - Giá khuyến mãi phải > 0
  - Giá khuyến mãi phải < giá gốc
  - Ngày kết thúc phải sau ngày bắt đầu
- **API**: `POST /admin/product-sales/{product_id}/set-sale`

### 3. Xóa khuyến mãi sản phẩm
- **Chức năng**: Xóa hoàn toàn thông tin khuyến mãi của sản phẩm
- **API**: `POST /admin/product-sales/{product_id}/remove-sale`

### 4. Hành động hàng loạt (Bulk Actions)
- **Kích hoạt khuyến mãi**: Kích hoạt cho các sản phẩm đã có giá khuyến mãi
- **Tạm dừng khuyến mãi**: Tạm dừng khuyến mãi (không xóa giá khuyến mãi)
- **Xóa khuyến mãi**: Xóa hoàn toàn thông tin khuyến mãi
- **API**: `POST /admin/product-sales/bulk-actions`

### 5. Cập nhật trạng thái tự động
- **Chức năng**: Tự động kích hoạt/tạm dừng khuyến mãi dựa trên thời gian
- **API**: `POST /admin/product-sales/auto-update`
- **Thực thi**: Tự động chạy khi vào dashboard admin

### 6. Thống kê khuyến mãi
- **Hiển thị trên dashboard**: 
  - Số sản phẩm đang khuyến mãi
  - Số sản phẩm có giá khuyến mãi
  - Số khuyến mãi chờ kích hoạt
  - Số khuyến mãi đã hết hạn
- **API**: `GET /admin/product-sales/statistics`

## Cấu trúc Database

### Bảng `products`
Các trường liên quan đến khuyến mãi:
- `price`: Giá gốc (bắt buộc)
- `sale_price`: Giá khuyến mãi (nullable)
- `sale_start`: Thời gian bắt đầu khuyến mãi (nullable)
- `sale_end`: Thời gian kết thúc khuyến mãi (nullable)
- `sale_active`: Trạng thái khuyến mãi (boolean, default: false)

## Service Layer

### ProductSaleService
**File**: `app/services/product_sale_service.py`

**Các phương thức chính**:
- `set_product_sale()`: Thiết lập khuyến mãi
- `remove_product_sale()`: Xóa khuyến mãi
- `activate_product_sale()`: Kích hoạt khuyến mãi
- `deactivate_product_sale()`: Tạm dừng khuyến mãi
- `bulk_*()`: Các hành động hàng loạt
- `auto_update_sale_status()`: Cập nhật trạng thái tự động
- `get_sale_statistics()`: Lấy thống kê
- `is_sale_valid()`: Kiểm tra khuyến mãi có hợp lệ không
- `get_current_price()`: Lấy giá hiện tại (ưu tiên giá khuyến mãi)

## Templates

### product_sales.html
**File**: `app/templates/admin/product_sales.html`

**Tính năng**:
- Hiển thị danh sách sản phẩm với thông tin khuyến mãi
- Form lọc và tìm kiếm
- Modal thiết lập khuyến mãi
- Checkbox chọn hàng loạt
- JavaScript xử lý AJAX calls

## Menu Navigation

Menu admin đã được cập nhật để bao gồm:
- **Quản lý sản phẩm**: Quản lý thông tin sản phẩm cơ bản
- **Khuyến mãi sản phẩm**: Quản lý giá khuyến mãi cho từng sản phẩm
- **Mã giảm giá**: Quản lý discount codes (tách biệt)

## Phân biệt với Discount Codes

| Khuyến mãi sản phẩm | Mã giảm giá |
|---------------------|-------------|
| Áp dụng trực tiếp cho sản phẩm | Áp dụng cho đơn hàng |
| Hiển thị giá đã giảm | Giảm giá khi checkout |
| Không cần nhập mã | Cần nhập mã giảm giá |
| Quản lý theo sản phẩm | Quản lý theo mã code |
| Hiển thị công khai | Có thể riêng tư |

## Workflow sử dụng

1. **Thiết lập khuyến mãi mới**:
   - Truy cập `/admin/product-sales`
   - Tìm sản phẩm cần thiết lập
   - Click "Thiết lập KM"
   - Nhập giá khuyến mãi và thời gian (nếu có)
   - Lưu

2. **Quản lý khuyến mãi hàng loạt**:
   - Chọn nhiều sản phẩm bằng checkbox
   - Chọn hành động từ menu bulk actions
   - Xác nhận thực hiện

3. **Theo dõi thống kê**:
   - Xem thống kê trên dashboard admin
   - Sử dụng API để lấy thống kê chi tiết

4. **Cập nhật tự động**:
   - Hệ thống tự động cập nhật khi vào dashboard
   - Có thể gọi manual qua API

## Lưu ý kỹ thuật

- Sử dụng `ProductSaleService` cho mọi thao tác liên quan đến khuyến mãi
- Validation được thực hiện ở cả frontend và backend
- Hỗ trợ múi giờ UTC cho datetime
- Sử dụng CSRF protection cho các POST requests
- Error handling chi tiết với thông báo tiếng Việt
- Responsive design tương thích mobile

## Extension trong tương lai

- Khuyến mãi theo danh mục
- Khuyến mãi theo quantity (mua nhiều giảm nhiều)
- Thông báo email khi khuyến mãi sắp hết hạn
- Export báo cáo khuyến mãi
- Lịch sử thay đổi giá khuyến mãi