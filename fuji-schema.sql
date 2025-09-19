-- =========================================
-- FujiShop - Core Database Schema (DDL only)
-- MySQL 8.x / MariaDB 10.x
-- =========================================

-- Safety & defaults
SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- ---------- DROP (idempotent) ----------
DROP VIEW IF EXISTS v_product_rating;
DROP VIEW IF EXISTS v_products_effective_price;

DROP TABLE IF EXISTS order_events;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;

DROP TABLE IF EXISTS product_reviews;
DROP TABLE IF EXISTS product_stock;
DROP TABLE IF EXISTS product_images;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

-- =========================================
-- 1) CATEGORIES
-- =========================================
CREATE TABLE categories (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  parent_id   BIGINT NULL,
  name        VARCHAR(255) NOT NULL,
  slug        VARCHAR(255) UNIQUE,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_cat_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 2) PRODUCTS (giá gốc + giảm giá theo lịch)
-- =========================================
CREATE TABLE products (
  id           BIGINT PRIMARY KEY AUTO_INCREMENT,
  name         VARCHAR(255) NOT NULL,
  slug         VARCHAR(255) UNIQUE,
  short_desc   TEXT,
  image_url    VARCHAR(1024),
  price        DECIMAL(12,2) NOT NULL,     -- giá gốc
  sale_price   DECIMAL(12,2) NULL,         -- giá sale (nếu có)
  sale_start   DATETIME NULL,
  sale_end     DATETIME NULL,
  is_active    TINYINT(1) DEFAULT 1,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FULLTEXT KEY ft_products (name, short_desc),
  KEY idx_products_created (created_at),
  KEY idx_products_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 3) PRODUCT <-> CATEGORY (n-n)
-- =========================================
CREATE TABLE product_categories (
  product_id   BIGINT NOT NULL,
  category_id  BIGINT NOT NULL,
  PRIMARY KEY (product_id, category_id),
  KEY idx_pc_cat (category_id),
  CONSTRAINT fk_pc_product  FOREIGN KEY (product_id)  REFERENCES products(id)   ON DELETE CASCADE,
  CONSTRAINT fk_pc_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 4) PRODUCT IMAGES (tuỳ chọn: album ảnh)
-- =========================================
CREATE TABLE product_images (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  product_id  BIGINT NOT NULL,
  image_url   VARCHAR(1024) NOT NULL,
  alt         VARCHAR(255),
  sort_order  INT DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_pi_prod_sort (product_id, sort_order),
  CONSTRAINT fk_pi_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 5) STOCK (tồn kho 1 kho/1 sản phẩm)
-- =========================================
CREATE TABLE product_stock (
  product_id   BIGINT PRIMARY KEY,
  qty_on_hand  INT NOT NULL DEFAULT 0,
  updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_stock_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_stock_qty ON product_stock(qty_on_hand);

-- =========================================
-- 6) REVIEWS (hiển thị ngay; admin chỉ xoá)
-- =========================================
CREATE TABLE product_reviews (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  product_id  BIGINT NOT NULL,
  user_name   VARCHAR(100) NULL,
  rating      TINYINT NOT NULL,  -- validate 1..5 ở app
  content     TEXT NULL,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_reviews_prod_time (product_id, created_at DESC),
  CONSTRAINT fk_reviews_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 7) ORDERS (đơn + thanh toán giả)
-- =========================================
CREATE TABLE orders (
  id               BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_code       VARCHAR(20) NOT NULL UNIQUE, -- mã tra cứu ngắn (vd: FJ-8X2K9C)
  customer_name    VARCHAR(100) NOT NULL,
  phone            VARCHAR(30)  NOT NULL,
  address          TEXT NOT NULL,
  province         VARCHAR(100) NULL,
  district         VARCHAR(100) NULL,
  ward             VARCHAR(100) NULL,
  payment_method   ENUM('COD','MOCK_TRANSFER') NOT NULL DEFAULT 'COD',
  payment_status   ENUM('unpaid','mock_paid')  NOT NULL DEFAULT 'unpaid',
  status           ENUM('pending','confirmed','fulfilled','cancelled') NOT NULL DEFAULT 'pending',
  -- Tài chính
  subtotal         DECIMAL(12,2) NULL,          -- tổng dòng hàng
  shipping_fee     DECIMAL(12,2) NOT NULL DEFAULT 0,
  discount_amt     DECIMAL(12,2) NOT NULL DEFAULT 0,
  grand_total      DECIMAL(12,2) NOT NULL,      -- = subtotal + shipping - discount
  total_amount     DECIMAL(12,2) NOT NULL,      -- mirror grand_total (dùng cho báo cáo/UI)
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_orders_status_time (status, created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 8) ORDER ITEMS (snapshot giá tại thời điểm đặt)
-- =========================================
CREATE TABLE order_items (
  id           BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id     BIGINT NOT NULL,
  product_id   BIGINT NOT NULL,
  product_name VARCHAR(255) NOT NULL,  -- chụp lại để hiển thị bền vững
  unit_price   DECIMAL(12,2) NOT NULL, -- từ v_products_effective_price lúc đặt
  qty          INT NOT NULL,
  line_total   DECIMAL(12,2) NOT NULL, -- unit_price * qty
  CONSTRAINT fk_oi_order   FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
  CONSTRAINT fk_oi_product FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 9) ORDER EVENTS (timeline "placed / mock_paid / confirmed / fulfilled / cancelled / restocked")
-- =========================================
CREATE TABLE order_events (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id    BIGINT NOT NULL,
  event_type  ENUM('placed','mock_paid','confirmed','fulfilled','cancelled','restocked') NOT NULL,
  note        VARCHAR(255) NULL,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  KEY idx_ev_order_time (order_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- 10) VIEWS
-- =========================================

-- 10.1) Giá hiệu lực (tự áp sale nếu trong khoảng thời gian)
CREATE OR REPLACE VIEW v_products_effective_price AS
SELECT  p.*,
        CASE
          WHEN p.sale_price IS NOT NULL
           AND (p.sale_start IS NULL OR p.sale_start <= NOW())
           AND (p.sale_end   IS NULL OR p.sale_end   >= NOW())
          THEN p.sale_price ELSE p.price
        END AS effective_price
FROM products p
WHERE p.is_active = 1;

-- 10.2) Điểm TB & số review
CREATE OR REPLACE VIEW v_product_rating AS
SELECT product_id,
       AVG(rating) AS avg_rating,
       COUNT(*)    AS review_count
FROM product_reviews
GROUP BY product_id;

-- =========================================
-- 11) SUGGESTED PERMISSIONS (nếu cần phân quyền DB)
-- (tuỳ bạn cấp trên app; phần này chỉ gợi ý, không tạo user)
-- GRANT SELECT,INSERT,UPDATE,DELETE ON yourdb.* TO 'app_user'@'%';
-- GRANT SELECT ON v_products_effective_price TO 'app_user'@'%';
-- GRANT SELECT ON v_product_rating TO 'app_user'@'%';
-- =========================================
