
# Đặc tả Chức năng – Website Bán Hàng (Student Level)
**Phiên bản:** 1.0 • **Ngày:** 2025-09-17 16:07:03 (GMT+7)  
**CSDL:** import từ `fuji.sql` (MariaDB ≥ 10.4)

> Mục tiêu: Thiết kế chức năng **tối thiểu cần có** cho một website bán hàng, phục vụ đồ án sinh viên. **Không cần SEO, không cần deploy**, không hỗ trợ nhượng quyền & hệ thống cửa hàng. Sử dụng schema sẵn trong `fuji.sql`.

---

## 1) Phạm vi chức năng (MVP)
### 1.1 Khách truy cập (Guest)
- Xem trang chủ (sản phẩm mới/bán chạy – hardcode hoặc query đơn giản).
- Duyệt **Danh mục** → xem **Danh sách sản phẩm** (phân trang, sắp xếp theo giá/tên).
- **Tìm kiếm** theo tên sản phẩm (LIKE hoặc FULLTEXT nếu đã có).
- **Trang chi tiết sản phẩm**: ảnh, mô tả ngắn/dài, **biến thể** (size/weight), giá, tồn khả dụng.
- **Thêm vào giỏ** (session‑based).

### 1.2 Người dùng đã đăng nhập (Customer)
- **Đăng ký/Đăng nhập/Đăng xuất**.
- **Giỏ hàng**: xem/cập nhật số lượng/xóa item.
- **Thanh toán (Checkout)**: nhập địa chỉ nhận hàng, chọn **COD** (mặc định); hiển thị tổng tiền.
- **Xem lịch sử đơn hàng** và chi tiết đơn hàng.

### 1.3 Quản trị (Admin – đơn giản)
- CRUD **Danh mục, Thương hiệu**.
- CRUD **Sản phẩm** + **Biến thể** + **Ảnh**.
- Quản lý **Đơn hàng**: xem → đổi trạng thái (*pending → confirmed → fulfilled → cancelled/refunded*).
- (Tùy chọn) **Mã giảm giá**: tạo/áp dụng ở checkout.

> **Không làm**: nhượng quyền, hệ thống cửa hàng, nhận tại cửa hàng (pickup), tồn kho theo chi nhánh.

---

## 2) Mô hình dữ liệu (theo `fuji.sql`)
Sử dụng trực tiếp các bảng có sẵn (UUID `CHAR(36)`). Các bảng chính dùng trong MVP:

- **Tài khoản**: `users(id, email, password_hash, full_name, phone, role_code)`; `roles(role_code)`.
- **Catalog**:  
  - `categories(id, parent_id, name, slug, sort_order, ...)`  
  - `brands(id, name)`  
  - `products(id, type_code, name, slug, sku, brand_id, short_desc, description, origin_country, unit_of_measure, size_note, perishable, ...)`  
  - `product_variants(id, product_id, sku, name, options(JSON), size_key, weight_key, list_price, compare_at, is_active, ...)`  
  - `product_media(id, product_id, url, alt_text, sort_order)`  
  - `product_categories(product_id, category_id)`  
  - (Tồn kho) `inventory_stocks(variant_id, on_hand, reserved, updated_at)` → **gộp theo variant** để lấy available = on_hand - reserved.
- **Giỏ & Đơn**:  
  - `carts(id, user_id, session_id, created_at, updated_at)`  
  - `cart_items(id, cart_id, product_id, variant_id, qty, unit_price, added_at)`  
  - `orders(id, user_id, status_code, fulfillment_method, billing_address_id, shipping_address_id, subtotal, discount_total, shipping_fee, tax_total, grand_total, currency, note, created_at, updated_at)`  
  - `order_items(id, order_id, product_id, variant_id, name, unit_price, qty, line_total)`  
  - `order_statuses(status_code)` (seed: pending/confirmed/fulfilled/cancelled/refunded)  
  - `payment_methods(method_code, label)` (seed: cod)  
  - `payment_transactions(id, order_id, method_code, amount, status, provider_ref, created_at)` (**để 'created' cho COD**)
- **Địa chỉ**: `addresses(id, user_id, receiver, phone, line1, ward, district, city, province, postal_code, country_code, is_default, lat, lng)`
- **Ưu đãi (tuỳ chọn)**: `coupons(code, discount_type, amount, min_order, starts_at, ends_at, usage_limit, used_count)`

> **Không dùng** trong MVP: `stores`, `store_hours`, `fulfillment_methods='pickup'`, `leads` (nhượng quyền).

**View gợi ý (tồn kho toàn cục):**
```sql
CREATE OR REPLACE VIEW v_variant_stock AS
SELECT variant_id,
       COALESCE(SUM(on_hand),0)   AS on_hand,
       COALESCE(SUM(reserved),0)  AS reserved,
       COALESCE(SUM(on_hand) - SUM(reserved),0) AS available
FROM inventory_stocks
GROUP BY variant_id;
```

---

## 3) Màn hình & Form (UI mức đồ án)
1. **Trang chủ**: block danh mục (top), list 8 sản phẩm mới (ORDER BY created_at DESC LIMIT 8).  
2. **Danh mục**: breadcrumb, tiêu đề danh mục, lưới sản phẩm (ảnh, tên, giá, nút Thêm giỏ), phân trang, sort (price asc/desc, name).  
3. **Chi tiết SP**: gallery ảnh, tên, brand, giá (nếu có biến thể → dropdown size/weight → cập nhật giá), mô tả ngắn/dài, số lượng, Thêm giỏ; hiển thị Còn hàng nếu `available>0`.  
4. **Giỏ hàng**: bảng item {ảnh | tên | biến thể | đơn giá | số lượng | thành tiền}; tổng phụ; nút Tiếp tục thanh toán.  
5. **Đăng ký/Đăng nhập**: email, mật khẩu (hash Bcrypt), tên.  
6. **Checkout**: form địa chỉ giao hàng (receiver, phone, line1, ward/district/city, province), chọn Thanh toán COD, ghi chú đơn; hiển thị `subtotal + shipping_fee + discount - tax = grand_total`.  
7. **Xác nhận đặt hàng**: hiển thị mã đơn (id), trạng thái ban đầu `pending`.  
8. **Tài khoản > Đơn hàng**: danh sách & chi tiết đơn (items, tổng tiền, trạng thái).  
9. **Admin**:  
   - Sản phẩm: danh sách → thêm/sửa/xóa sản phẩm & biến thể & ảnh.  
   - Danh mục/Thương hiệu: CRUD.  
   - Đơn hàng: xem chi tiết → cập nhật `status_code` (pending→confirmed→fulfilled / cancelled / refunded).  
   - (Tùy chọn) Coupon: CRUD.

---

## 4) Luồng nghiệp vụ chính

### 4.1 Thêm vào giỏ (session‑based)
1. Nếu chưa có `carts.session_id` → tạo mới; nếu đã đăng nhập → gắn `user_id`.  
2. Lấy `unit_price` từ `product_variants.list_price` (hoặc `products` nếu simple).  
3. Kiểm tra `v_variant_stock.available >= qty`.  
4. Ghi `cart_items` (nếu đã tồn tại variant trong giỏ → cộng `qty`).

### 4.2 Checkout (COD)
1. Người dùng đăng nhập → chọn/nhập `addresses`.  
2. Tính `subtotal` = Σ `unit_price * qty`.  
3. Áp `coupons` (nếu dùng) → cập nhật `discount_total`.  
4. Tính `grand_total = subtotal - discount_total + shipping_fee + tax_total`.  
5. Tạo `orders` (`status_code='pending'`, `fulfillment_method='delivery'`).  
6. Ghi `order_items` snapshot giá và số lượng.  
7. Ghi `payment_transactions` (`method_code='cod'`, `status='created'`).  
8. (Tuỳ chọn) Trừ `reserved` trong `inventory_stocks` để giữ hàng; khi admin `confirmed` → trừ `on_hand`, giảm `reserved`.

### 4.3 Cập nhật trạng thái đơn (Admin)
- `pending → confirmed` (đã chốt) → `fulfilled` (đã giao).  
- Huỷ: `cancelled` hoặc `refunded`.

---

## 5) API đề xuất (REST, tối giản)
**Auth** (JWT/Session tuỳ thuận tiện):
- `POST /auth/register` → body: email, password, full_name, phone  
- `POST /auth/login` → body: email, password  
- `POST /auth/logout`

**Catalog**:
- `GET /categories` → cây/flat list
- `GET /products?category=&q=&sort=&page=`  
- `GET /products/:slug` → chi tiết + biến thể + `available` (join `v_variant_stock`)

**Cart**:
- `GET /cart` (dựa session_id)
- `POST /cart/items` → {variant_id, qty}
- `PATCH /cart/items/:id` → {qty}
- `DELETE /cart/items/:id`

**Checkout/Orders**:
- `POST /checkout` → {shipping_address, note, coupon_code?} → trả `order_id`
- `GET /orders` (của user hiện tại)
- `GET /orders/:id`

**Admin**:
- `POST/PUT/DELETE /admin/products` (+ variants, media)
- `GET /admin/orders` / `GET /admin/orders/:id`
- `PATCH /admin/orders/:id/status` → {status_code}
- (Tùy chọn) `POST/PUT/DELETE /admin/coupons`

> Với đồ án sinh viên: cho phép **COD** là đủ, không cần tích hợp cổng thanh toán.

---

## 6) Ràng buộc & Quy tắc đơn giản
- Tạo **biến thể mặc định** cho sản phẩm đơn giản để thống nhất luồng (mọi thứ đều theo `variant_id`).  
- Không bán vượt tồn: `available >= qty`.  
- `unit_price` được **snapshot** tại thời điểm thêm giỏ & tạo đơn.  
- Chỉ dùng **VND**, `tax_total=0` (đồ án), `shipping_fee` có thể cấu hình cố định (ví dụ 25.000đ).

---

## 7) Tiêu chí nghiệm thu (MVP)
- Đăng ký/Đăng nhập hoạt động; mật khẩu được băm.  
- Duyệt danh mục, xem sản phẩm, tìm kiếm, chi tiết biến thể.  
- Thêm giỏ, cập nhật số lượng, xoá; tổng tiền đúng.  
- Checkout tạo đơn **COD** thành công; xem được lịch sử đơn.  
- Admin CRUD sản phẩm/biến thể/ảnh; cập nhật trạng thái đơn.  
- Không có trang/route nào về nhượng quyền hoặc hệ thống cửa hàng.

---

## 8) Gợi ý công nghệ (tự chọn cho đồ án)
- **Backend**: Laravel / NestJS / Express; ORM: Eloquent / TypeORM / Prisma (MySQL).  
- **Frontend**: React (Vite) hoặc Next.js (SSR đơn giản).  
- **Auth**: JWT (localStorage) hoặc Cookie Session.  
- **Storage ảnh**: lưu đường dẫn tĩnh (thư mục `uploads/`).

