# Hệ thống Đăng nhập và Đăng ký - Fuji Fruit

## Tổng quan
Hệ thống authentication đã được tích hợp thành công vào ứng dụng Fuji Fruit, bao gồm các tính năng:

- Đăng ký tài khoản mới
- Đăng nhập/Đăng xuất
- Quản lý phiên đăng nhập
- Trang thông tin cá nhân
- Bảo mật mật khẩu với bcrypt

## Các tính năng chính

### 1. Đăng ký tài khoản
- **URL:** `/register`
- **Thông tin yêu cầu:**
  - Tên đăng nhập (bắt buộc, 3-20 ký tự)
  - Email (bắt buộc, duy nhất)
  - Họ và tên (tùy chọn)
  - Số điện thoại (tùy chọn)
  - Mật khẩu (bắt buộc, tối thiểu 6 ký tự)
  - Xác nhận mật khẩu
  - Đồng ý điều khoản

### 2. Đăng nhập
- **URL:** `/login`
- **Thông tin đăng nhập:**
  - Email
  - Mật khẩu
  - Tùy chọn "Ghi nhớ đăng nhập"

### 3. Thông tin cá nhân
- **URL:** `/profile`
- Hiển thị thông tin chi tiết của user
- Trạng thái tài khoản
- Thời gian tham gia và đăng nhập lần cuối

### 4. Đăng xuất
- **URL:** `/logout`
- Xóa phiên đăng nhập và redirect về trang chủ

## Cấu trúc Database

### Bảng `users`
```sql
- id (bigint, auto_increment, primary key)
- username (varchar(100), unique, not null)
- email (varchar(255), unique)
- phone (varchar(30), unique)
- password_hash (varchar(255), not null)
- full_name (varchar(150))
- avatar_url (varchar(1024))
- is_active (tinyint(1), default 1)
- email_verified (tinyint(1), default 0)
- last_login_at (datetime)
- created_at (datetime, default current_timestamp)
- updated_at (datetime, default current_timestamp on update)
```

## Tích hợp với UI

### Navbar
- Hiển thị links "Đăng nhập" và "Đăng ký" khi chưa đăng nhập
- Hiển thị dropdown menu với tên user và các tùy chọn khi đã đăng nhập:
  - Thông tin cá nhân
  - Đăng xuất

### Session Management
- Lưu trữ thông tin user trong Flask session:
  - `user_id`: ID của user
  - `user_email`: Email của user
  - `user_name`: Tên hiển thị của user

## Tài khoản test

Đã tạo sẵn tài khoản test để kiểm tra:
- **Email:** test@fuji.com
- **Password:** 123456

## Bảo mật

### Mã hóa mật khẩu
- Sử dụng thư viện `bcrypt` để hash mật khẩu
- Salt được tự động tạo cho mỗi mật khẩu

### Validation
- Kiểm tra tính duy nhất của username và email
- Validation form với Flask-WTF
- CSRF protection

### Session Security
- Session timeout được cấu hình
- Secure session cookies

## Cách sử dụng

### 1. Khởi động ứng dụng
```bash
python -m flask run --debug
```

### 2. Truy cập các trang
- Trang chủ: http://localhost:5000/
- Đăng nhập: http://localhost:5000/login
- Đăng ký: http://localhost:5000/register
- Profile: http://localhost:5000/profile (cần đăng nhập)

### 3. Test workflow
1. Truy cập trang đăng ký và tạo tài khoản mới
2. Hoặc sử dụng tài khoản test đã có sẵn để đăng nhập
3. Kiểm tra navbar hiển thị tên user
4. Truy cập trang profile
5. Đăng xuất và kiểm tra session được xóa

## Files được tạo/chỉnh sửa

### Models
- `app/models/user.py` - User model
- `app/models/__init__.py` - Import User model

### Forms
- `app/blueprints/site/forms.py` - LoginForm, RegisterForm

### Views
- `app/blueprints/site/views.py` - Authentication routes

### Templates
- `app/templates/site/login.html` - Trang đăng nhập
- `app/templates/site/register.html` - Trang đăng ký
- `app/templates/site/profile.html` - Trang thông tin cá nhân
- `app/templates/_partials/navbar.html` - Cập nhật navbar

### Utils
- `create_test_user.py` - Script tạo user test
- `check_table.py` - Script kiểm tra cấu trúc database

## Tính năng sẽ phát triển thêm

1. **Email verification** - Xác thực email qua link
2. **Password reset** - Đặt lại mật khẩu qua email
3. **Profile editing** - Chỉnh sửa thông tin cá nhân
4. **Social login** - Đăng nhập qua Google, Facebook
5. **Two-factor authentication** - Bảo mật 2 lớp
6. **User roles** - Phân quyền người dùng

## Lưu ý

- Đảm bảo database đã được khởi tạo với `python init_db.py`
- Cấu hình SECRET_KEY trong config để bảo mật session
- Trong production, nên sử dụng HTTPS cho các trang authentication
- Cần cấu hình rate limiting để tránh brute force attacks