# Cập nhật thuật ngữ trạng thái đơn hàng

## Thay đổi thực hiện

Đã cập nhật thuật ngữ trạng thái đơn hàng để phù hợp và rõ ràng hơn:

### 1. Trạng thái `fulfilled` (đã hoàn thành công việc shop)
**Trước:** "Đã hoàn thành" hoặc "Đã hoàn thành - Chờ xác nhận nhận hàng"
**Sau:** "Đang giao hàng" (khi chưa xác nhận) hoặc "Đã giao hàng" (khi đã xác nhận)

### 2. Trạng thái `completed` (khách hàng đã xác nhận nhận hàng)
**Trước:** "Hoàn thành" hoặc "Đã hoàn thành"
**Sau:** "Đã giao hàng"

## Files đã cập nhật

### 1. Templates - User Interface
- `app/templates/site/_order_helpers.html` - Macro hiển thị trạng thái cho user
- `app/templates/site/my_orders.html` - Tab navigation và empty messages
- `app/templates/site/order_detail.html` - Event timeline text

### 2. Templates - Admin Interface  
- `app/templates/admin/_order_helpers.html` - Macro hiển thị trạng thái và button text
- `app/templates/admin/orders.html` - Filter dropdown và confirm dialogs
- `app/templates/admin/order_detail.html` - Event display text
- `app/templates/admin/user_detail.html` - Status names mapping

### 3. Backend Logic
- `app/utils/order_helpers.py` - Status display functions
- `app/blueprints/admin/views.py` - Success/error messages

## Kết quả

### Cho người dùng (Customer):
- Tab "Đang giao hàng": Hiển thị đơn hàng đang được vận chuyển
- Tab "Đã giao hàng": Hiển thị đơn hàng đã được giao và xác nhận

### Cho admin:
- Button "Giao hàng": Bắt đầu vận chuyển đơn hàng (từ confirmed → fulfilled)
- Status "Đang giao hàng": Đơn hàng đang được vận chuyển
- Status "Đã giao hàng": Đơn hàng đã hoàn tất

### Flow mới rõ ràng hơn:
```
pending → confirmed → fulfilled (Đang giao hàng) → completed (Đã giao hàng)
```

Thay đổi này giúp thuật ngữ phù hợp hơn với thực tế và dễ hiểu hơn cho cả admin và khách hàng.