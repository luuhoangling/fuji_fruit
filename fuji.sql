-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 16, 2025 at 06:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fuji`
--

-- --------------------------------------------------------

--
-- Table structure for table `addresses`
--

CREATE TABLE `addresses` (
  `id` char(36) NOT NULL,
  `user_id` char(36) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `receiver` varchar(255) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `line1` varchar(255) NOT NULL,
  `line2` varchar(255) DEFAULT NULL,
  `ward` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `postal_code` varchar(32) DEFAULT NULL,
  `country_code` char(2) NOT NULL DEFAULT 'VN',
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `is_default` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `addresses`
--
DELIMITER $$
CREATE TRIGGER `bi_addresses_uuid` BEFORE INSERT ON `addresses` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `blog_categories`
--

CREATE TABLE `blog_categories` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `blog_categories`
--
DELIMITER $$
CREATE TRIGGER `bi_blog_categories_uuid` BEFORE INSERT ON `blog_categories` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `blog_posts`
--

CREATE TABLE `blog_posts` (
  `id` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `excerpt` text DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  `hero_image` varchar(1024) DEFAULT NULL,
  `author_id` char(36) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `blog_posts`
--
DELIMITER $$
CREATE TRIGGER `bi_blog_posts_uuid` BEFORE INSERT ON `blog_posts` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `blog_post_categories`
--

CREATE TABLE `blog_post_categories` (
  `post_id` char(36) NOT NULL,
  `category_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `brands`
--
DELIMITER $$
CREATE TRIGGER `bi_brands_uuid` BEFORE INSERT ON `brands` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `bundles`
--

CREATE TABLE `bundles` (
  `product_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bundle_items`
--

CREATE TABLE `bundle_items` (
  `id` char(36) NOT NULL,
  `bundle_id` char(36) NOT NULL,
  `component_product_id` char(36) NOT NULL,
  `component_variant_id` char(36) DEFAULT NULL,
  `quantity` decimal(10,3) NOT NULL DEFAULT 1.000,
  `unit_label` varchar(32) DEFAULT NULL,
  `price_override` decimal(14,2) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `bundle_items`
--
DELIMITER $$
CREATE TRIGGER `bi_bundle_items_uuid` BEFORE INSERT ON `bundle_items` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `carts`
--

CREATE TABLE `carts` (
  `id` char(36) NOT NULL,
  `user_id` char(36) DEFAULT NULL,
  `session_id` varchar(128) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `carts`
--
DELIMITER $$
CREATE TRIGGER `bi_carts_uuid` BEFORE INSERT ON `carts` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `id` char(36) NOT NULL,
  `cart_id` char(36) NOT NULL,
  `product_id` char(36) NOT NULL,
  `variant_id` char(36) DEFAULT NULL,
  `qty` int(11) NOT NULL,
  `unit_price` decimal(14,2) NOT NULL,
  `added_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `cart_items`
--
DELIMITER $$
CREATE TRIGGER `bi_cart_items_uuid` BEFORE INSERT ON `cart_items` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` char(36) NOT NULL,
  `parent_id` char(36) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `parent_id`, `name`, `slug`, `description`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES
('36261e75-9318-11f0-b4db-0897987972b5', NULL, 'Quà tặng trái cây', 'qua-tang-trai-cay', 'Giỏ/khay/mâm quà biếu', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24'),
('36262d20-9318-11f0-b4db-0897987972b5', NULL, 'Giỏ hoa quả biếu tặng', 'gio-hoa-qua-bieu-tang', 'Giỏ quà', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24'),
('36262df3-9318-11f0-b4db-0897987972b5', NULL, 'Mâm quả thắp hương', 'mam-qua-thap-huong', 'Mâm quả cúng', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24'),
('36262e61-9318-11f0-b4db-0897987972b5', NULL, 'Hoa quả nhập khẩu', 'hoa-qua-nhap-khau', 'Cherry, Táo, Nho, Lê, Cam/Quýt...', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24'),
('36262ed3-9318-11f0-b4db-0897987972b5', NULL, 'Cherry', 'cherry', 'Các loại cherry nhập khẩu', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24'),
('36262f36-9318-11f0-b4db-0897987972b5', NULL, 'Hoa quả nội địa', 'hoa-qua-noi-dia', 'Trái cây Việt Nam theo mùa', 0, 1, '2025-09-16 23:14:24', '2025-09-16 23:14:24');

--
-- Triggers `categories`
--
DELIMITER $$
CREATE TRIGGER `bi_categories_uuid` BEFORE INSERT ON `categories` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `coupons`
--

CREATE TABLE `coupons` (
  `id` char(36) NOT NULL,
  `code` varchar(64) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `type` varchar(32) NOT NULL,
  `value` decimal(14,2) NOT NULL,
  `starts_at` datetime DEFAULT NULL,
  `ends_at` datetime DEFAULT NULL,
  `min_order` decimal(14,2) DEFAULT NULL,
  `max_redemption` int(11) DEFAULT NULL,
  `redeemed_count` int(11) NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `coupons`
--
DELIMITER $$
CREATE TRIGGER `bi_coupons_uuid` BEFORE INSERT ON `coupons` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `fulfillment_methods`
--

CREATE TABLE `fulfillment_methods` (
  `method_code` varchar(32) NOT NULL,
  `label` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fulfillment_methods`
--

INSERT INTO `fulfillment_methods` (`method_code`, `label`) VALUES
('delivery', 'Delivery'),
('pickup', 'In‑store Pickup');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_stocks`
--

CREATE TABLE `inventory_stocks` (
  `variant_id` char(36) NOT NULL,
  `store_id` char(36) NOT NULL,
  `on_hand` int(11) NOT NULL DEFAULT 0,
  `reserved` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leads`
--

CREATE TABLE `leads` (
  `id` char(36) NOT NULL,
  `lead_type` varchar(32) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `desired_store` char(36) DEFAULT NULL,
  `status` varchar(32) NOT NULL DEFAULT 'new',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `leads`
--
DELIMITER $$
CREATE TRIGGER `bi_leads_uuid` BEFORE INSERT ON `leads` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `loyalty_accounts`
--

CREATE TABLE `loyalty_accounts` (
  `user_id` char(36) NOT NULL,
  `points` bigint(20) NOT NULL DEFAULT 0,
  `tier` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `loyalty_transactions`
--

CREATE TABLE `loyalty_transactions` (
  `id` char(36) NOT NULL,
  `user_id` char(36) NOT NULL,
  `order_id` char(36) DEFAULT NULL,
  `delta_points` int(11) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `loyalty_transactions`
--
DELIMITER $$
CREATE TRIGGER `bi_loyalty_transactions_uuid` BEFORE INSERT ON `loyalty_transactions` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` char(36) NOT NULL,
  `order_no` varchar(32) DEFAULT NULL,
  `user_id` char(36) DEFAULT NULL,
  `status_code` varchar(32) NOT NULL,
  `fulfillment_method` varchar(32) NOT NULL,
  `pickup_store_id` char(36) DEFAULT NULL,
  `billing_address_id` char(36) DEFAULT NULL,
  `shipping_address_id` char(36) DEFAULT NULL,
  `subtotal` decimal(14,2) NOT NULL DEFAULT 0.00,
  `discount_total` decimal(14,2) NOT NULL DEFAULT 0.00,
  `shipping_fee` decimal(14,2) NOT NULL DEFAULT 0.00,
  `tax_total` decimal(14,2) NOT NULL DEFAULT 0.00,
  `grand_total` decimal(14,2) NOT NULL DEFAULT 0.00,
  `currency` char(3) NOT NULL DEFAULT 'VND',
  `note` text DEFAULT NULL,
  `placed_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `orders`
--
DELIMITER $$
CREATE TRIGGER `bi_orders_uuid` BEFORE INSERT ON `orders` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `order_coupons`
--

CREATE TABLE `order_coupons` (
  `order_id` char(36) NOT NULL,
  `coupon_id` char(36) NOT NULL,
  `amount` decimal(14,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` char(36) NOT NULL,
  `order_id` char(36) NOT NULL,
  `product_id` char(36) NOT NULL,
  `variant_id` char(36) DEFAULT NULL,
  `item_name` varchar(255) NOT NULL,
  `unit_label` varchar(32) DEFAULT NULL,
  `options` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`options`)),
  `qty` int(11) NOT NULL,
  `unit_price` decimal(14,2) NOT NULL,
  `line_total` decimal(14,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `order_items`
--
DELIMITER $$
CREATE TRIGGER `bi_order_items_uuid` BEFORE INSERT ON `order_items` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `order_statuses`
--

CREATE TABLE `order_statuses` (
  `status_code` varchar(32) NOT NULL,
  `sort_order` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_statuses`
--

INSERT INTO `order_statuses` (`status_code`, `sort_order`) VALUES
('cancelled', 90),
('confirmed', 20),
('fulfilled', 30),
('pending', 10),
('refunded', 80);

-- --------------------------------------------------------

--
-- Table structure for table `pages`
--

CREATE TABLE `pages` (
  `id` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `content` longtext DEFAULT NULL,
  `seo_title` varchar(255) DEFAULT NULL,
  `seo_desc` varchar(255) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `pages`
--
DELIMITER $$
CREATE TRIGGER `bi_pages_uuid` BEFORE INSERT ON `pages` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `payment_methods`
--

CREATE TABLE `payment_methods` (
  `method_code` varchar(32) NOT NULL,
  `label` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment_methods`
--

INSERT INTO `payment_methods` (`method_code`, `label`) VALUES
('bank_transfer', 'Bank Transfer'),
('cod', 'Cash on Delivery'),
('online', 'Online Payment');

-- --------------------------------------------------------

--
-- Table structure for table `payment_transactions`
--

CREATE TABLE `payment_transactions` (
  `id` char(36) NOT NULL,
  `order_id` char(36) NOT NULL,
  `method_code` varchar(32) NOT NULL,
  `provider` varchar(64) DEFAULT NULL,
  `amount` decimal(14,2) NOT NULL,
  `status` varchar(32) NOT NULL,
  `txn_ref` varchar(128) DEFAULT NULL,
  `payload` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`payload`)),
  `paid_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `payment_transactions`
--
DELIMITER $$
CREATE TRIGGER `bi_payment_transactions_uuid` BEFORE INSERT ON `payment_transactions` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` char(36) NOT NULL,
  `type_code` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  `brand_id` char(36) DEFAULT NULL,
  `short_desc` text DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `origin_country` varchar(64) DEFAULT NULL,
  `unit_of_measure` varchar(32) NOT NULL DEFAULT 'kg',
  `size_note` varchar(255) DEFAULT NULL,
  `perishable` tinyint(1) NOT NULL DEFAULT 1,
  `shelf_life_days` int(11) DEFAULT NULL,
  `season_start_month` tinyint(4) DEFAULT NULL,
  `season_end_month` tinyint(4) DEFAULT NULL,
  `attributes_schema` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`attributes_schema`)),
  `specs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`specs`)),
  `tax_rate` decimal(5,2) DEFAULT 0.00,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `products`
--
DELIMITER $$
CREATE TRIGGER `bi_products_uuid` BEFORE INSERT ON `products` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `product_categories`
--

CREATE TABLE `product_categories` (
  `product_id` char(36) NOT NULL,
  `category_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_media`
--

CREATE TABLE `product_media` (
  `id` char(36) NOT NULL,
  `product_id` char(36) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `alt_text` varchar(255) DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT 0,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `product_media`
--
DELIMITER $$
CREATE TRIGGER `bi_product_media_uuid` BEFORE INSERT ON `product_media` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `product_types`
--

CREATE TABLE `product_types` (
  `type_code` varchar(32) NOT NULL,
  `label` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_types`
--

INSERT INTO `product_types` (`type_code`, `label`) VALUES
('bundle', 'Bundle'),
('simple', 'Simple'),
('variable', 'Variable');

-- --------------------------------------------------------

--
-- Table structure for table `product_variants`
--

CREATE TABLE `product_variants` (
  `id` char(36) NOT NULL,
  `product_id` char(36) NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `options` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`options`)),
  `size_key` varchar(64) GENERATED ALWAYS AS (json_unquote(json_extract(`options`,'$.size'))) STORED,
  `weight_key` varchar(64) GENERATED ALWAYS AS (json_unquote(json_extract(`options`,'$.weight'))) STORED,
  `barcode` varchar(100) DEFAULT NULL,
  `weight_kg` decimal(8,3) DEFAULT NULL,
  `cost_price` decimal(14,2) DEFAULT NULL,
  `list_price` decimal(14,2) NOT NULL,
  `compare_at` decimal(14,2) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `product_variants`
--
DELIMITER $$
CREATE TRIGGER `bi_product_variants_uuid` BEFORE INSERT ON `product_variants` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `redirects`
--

CREATE TABLE `redirects` (
  `id` char(36) NOT NULL,
  `from_path` varchar(255) NOT NULL,
  `to_path` varchar(255) NOT NULL,
  `http_status` int(11) NOT NULL DEFAULT 301,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `redirects`
--
DELIMITER $$
CREATE TRIGGER `bi_redirects_uuid` BEFORE INSERT ON `redirects` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_code` varchar(32) NOT NULL,
  `label` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_code`, `label`) VALUES
('admin', 'Administrator'),
('customer', 'Customer'),
('staff', 'Staff');

-- --------------------------------------------------------

--
-- Table structure for table `shipments`
--

CREATE TABLE `shipments` (
  `id` char(36) NOT NULL,
  `order_id` char(36) NOT NULL,
  `courier` varchar(64) DEFAULT NULL,
  `service` varchar(64) DEFAULT NULL,
  `tracking_no` varchar(128) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `shipped_at` datetime DEFAULT NULL,
  `delivered_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `shipments`
--
DELIMITER $$
CREATE TRIGGER `bi_shipments_uuid` BEFORE INSERT ON `shipments` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `stores`
--

CREATE TABLE `stores` (
  `id` char(36) NOT NULL,
  `code` varchar(64) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `hotline` varchar(50) DEFAULT NULL,
  `store_phone` varchar(50) DEFAULT NULL,
  `zalo_url` varchar(512) DEFAULT NULL,
  `map_url` varchar(512) DEFAULT NULL,
  `line1` varchar(255) NOT NULL,
  `ward` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `stores`
--
DELIMITER $$
CREATE TRIGGER `bi_stores_uuid` BEFORE INSERT ON `stores` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `store_hours`
--

CREATE TABLE `store_hours` (
  `store_id` char(36) NOT NULL,
  `dow` tinyint(4) NOT NULL,
  `open_time` time NOT NULL,
  `close_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` char(36) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `role_code` varchar(32) NOT NULL DEFAULT 'customer',
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `bi_users_uuid` BEFORE INSERT ON `users` FOR EACH ROW BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN SET NEW.id = UUID(); END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `variant_price_history`
--

CREATE TABLE `variant_price_history` (
  `variant_id` char(36) NOT NULL,
  `valid_from` datetime NOT NULL,
  `list_price` decimal(14,2) NOT NULL,
  `compare_at` decimal(14,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_products_search`
-- (See below for the actual view)
--
CREATE TABLE `v_products_search` (
`id` char(36)
,`name` varchar(255)
,`slug` varchar(255)
,`text` longtext
,`categories` mediumtext
);

-- --------------------------------------------------------

--
-- Structure for view `v_products_search`
--
DROP TABLE IF EXISTS `v_products_search`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_products_search`  AS SELECT `p`.`id` AS `id`, `p`.`name` AS `name`, `p`.`slug` AS `slug`, concat(coalesce(`p`.`short_desc`,''),' ',coalesce(`p`.`description`,'')) AS `text`, group_concat(`c`.`name` order by `c`.`name` ASC separator ', ') AS `categories` FROM ((`products` `p` left join `product_categories` `pc` on(`pc`.`product_id` = `p`.`id`)) left join `categories` `c` on(`c`.`id` = `pc`.`category_id`)) GROUP BY `p`.`id` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_addr_user` (`user_id`);

--
-- Indexes for table `blog_categories`
--
ALTER TABLE `blog_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `blog_posts`
--
ALTER TABLE `blog_posts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `fk_bp_author` (`author_id`);
ALTER TABLE `blog_posts` ADD FULLTEXT KEY `ft_blog_text` (`title`,`content`,`excerpt`);

--
-- Indexes for table `blog_post_categories`
--
ALTER TABLE `blog_post_categories`
  ADD PRIMARY KEY (`post_id`,`category_id`),
  ADD KEY `fk_bpc_cat` (`category_id`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `bundles`
--
ALTER TABLE `bundles`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `bundle_items`
--
ALTER TABLE `bundle_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_bi_b` (`bundle_id`),
  ADD KEY `fk_bi_cp` (`component_product_id`),
  ADD KEY `fk_bi_cv` (`component_variant_id`);

--
-- Indexes for table `carts`
--
ALTER TABLE `carts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_carts_session` (`session_id`),
  ADD KEY `fk_cart_user` (`user_id`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_ci_cart` (`cart_id`),
  ADD KEY `fk_ci_prod` (`product_id`),
  ADD KEY `fk_ci_var` (`variant_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `fk_cat_parent` (`parent_id`);

--
-- Indexes for table `coupons`
--
ALTER TABLE `coupons`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `fulfillment_methods`
--
ALTER TABLE `fulfillment_methods`
  ADD PRIMARY KEY (`method_code`);

--
-- Indexes for table `inventory_stocks`
--
ALTER TABLE `inventory_stocks`
  ADD PRIMARY KEY (`variant_id`,`store_id`),
  ADD KEY `fk_inv_s` (`store_id`);

--
-- Indexes for table `leads`
--
ALTER TABLE `leads`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_lead_store` (`desired_store`);

--
-- Indexes for table `loyalty_accounts`
--
ALTER TABLE `loyalty_accounts`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `loyalty_transactions`
--
ALTER TABLE `loyalty_transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_lt_user` (`user_id`),
  ADD KEY `fk_lt_order` (`order_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_no` (`order_no`),
  ADD KEY `fk_order_user` (`user_id`),
  ADD KEY `fk_order_status` (`status_code`),
  ADD KEY `fk_order_fm` (`fulfillment_method`),
  ADD KEY `fk_order_pickup` (`pickup_store_id`),
  ADD KEY `fk_order_bill` (`billing_address_id`),
  ADD KEY `fk_order_ship` (`shipping_address_id`);

--
-- Indexes for table `order_coupons`
--
ALTER TABLE `order_coupons`
  ADD PRIMARY KEY (`order_id`,`coupon_id`),
  ADD KEY `fk_oc_coupon` (`coupon_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_oi_order` (`order_id`),
  ADD KEY `fk_oi_prod` (`product_id`),
  ADD KEY `fk_oi_var` (`variant_id`);

--
-- Indexes for table `order_statuses`
--
ALTER TABLE `order_statuses`
  ADD PRIMARY KEY (`status_code`);

--
-- Indexes for table `pages`
--
ALTER TABLE `pages`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `payment_methods`
--
ALTER TABLE `payment_methods`
  ADD PRIMARY KEY (`method_code`);

--
-- Indexes for table `payment_transactions`
--
ALTER TABLE `payment_transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pay_order` (`order_id`),
  ADD KEY `fk_pay_method` (`method_code`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `fk_prod_type` (`type_code`),
  ADD KEY `fk_prod_brand` (`brand_id`);
ALTER TABLE `products` ADD FULLTEXT KEY `ft_products_text` (`name`,`description`);

--
-- Indexes for table `product_categories`
--
ALTER TABLE `product_categories`
  ADD PRIMARY KEY (`product_id`,`category_id`),
  ADD KEY `fk_pc_c` (`category_id`);

--
-- Indexes for table `product_media`
--
ALTER TABLE `product_media`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_media_p` (`product_id`);

--
-- Indexes for table `product_types`
--
ALTER TABLE `product_types`
  ADD PRIMARY KEY (`type_code`);

--
-- Indexes for table `product_variants`
--
ALTER TABLE `product_variants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `idx_variant_size` (`size_key`),
  ADD KEY `idx_variant_weight` (`weight_key`),
  ADD KEY `fk_var_p` (`product_id`);

--
-- Indexes for table `redirects`
--
ALTER TABLE `redirects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `from_path` (`from_path`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_code`);

--
-- Indexes for table `shipments`
--
ALTER TABLE `shipments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_ship_order` (`order_id`);

--
-- Indexes for table `stores`
--
ALTER TABLE `stores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `store_hours`
--
ALTER TABLE `store_hours`
  ADD PRIMARY KEY (`store_id`,`dow`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_users_role` (`role_code`);

--
-- Indexes for table `variant_price_history`
--
ALTER TABLE `variant_price_history`
  ADD PRIMARY KEY (`variant_id`,`valid_from`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `addresses`
--
ALTER TABLE `addresses`
  ADD CONSTRAINT `fk_addr_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `blog_posts`
--
ALTER TABLE `blog_posts`
  ADD CONSTRAINT `fk_bp_author` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `blog_post_categories`
--
ALTER TABLE `blog_post_categories`
  ADD CONSTRAINT `fk_bpc_cat` FOREIGN KEY (`category_id`) REFERENCES `blog_categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_bpc_post` FOREIGN KEY (`post_id`) REFERENCES `blog_posts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bundles`
--
ALTER TABLE `bundles`
  ADD CONSTRAINT `fk_bun_p` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bundle_items`
--
ALTER TABLE `bundle_items`
  ADD CONSTRAINT `fk_bi_b` FOREIGN KEY (`bundle_id`) REFERENCES `bundles` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_bi_cp` FOREIGN KEY (`component_product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `fk_bi_cv` FOREIGN KEY (`component_variant_id`) REFERENCES `product_variants` (`id`);

--
-- Constraints for table `carts`
--
ALTER TABLE `carts`
  ADD CONSTRAINT `fk_cart_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `fk_ci_cart` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_ci_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `fk_ci_var` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`);

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `fk_cat_parent` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `inventory_stocks`
--
ALTER TABLE `inventory_stocks`
  ADD CONSTRAINT `fk_inv_s` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_inv_v` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `leads`
--
ALTER TABLE `leads`
  ADD CONSTRAINT `fk_lead_store` FOREIGN KEY (`desired_store`) REFERENCES `stores` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `loyalty_accounts`
--
ALTER TABLE `loyalty_accounts`
  ADD CONSTRAINT `fk_loyal_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `loyalty_transactions`
--
ALTER TABLE `loyalty_transactions`
  ADD CONSTRAINT `fk_lt_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_lt_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_order_bill` FOREIGN KEY (`billing_address_id`) REFERENCES `addresses` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_order_fm` FOREIGN KEY (`fulfillment_method`) REFERENCES `fulfillment_methods` (`method_code`),
  ADD CONSTRAINT `fk_order_pickup` FOREIGN KEY (`pickup_store_id`) REFERENCES `stores` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_order_ship` FOREIGN KEY (`shipping_address_id`) REFERENCES `addresses` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_order_status` FOREIGN KEY (`status_code`) REFERENCES `order_statuses` (`status_code`),
  ADD CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `order_coupons`
--
ALTER TABLE `order_coupons`
  ADD CONSTRAINT `fk_oc_coupon` FOREIGN KEY (`coupon_id`) REFERENCES `coupons` (`id`),
  ADD CONSTRAINT `fk_oc_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_oi_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_oi_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `fk_oi_var` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`);

--
-- Constraints for table `payment_transactions`
--
ALTER TABLE `payment_transactions`
  ADD CONSTRAINT `fk_pay_method` FOREIGN KEY (`method_code`) REFERENCES `payment_methods` (`method_code`),
  ADD CONSTRAINT `fk_pay_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_prod_brand` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_prod_type` FOREIGN KEY (`type_code`) REFERENCES `product_types` (`type_code`);

--
-- Constraints for table `product_categories`
--
ALTER TABLE `product_categories`
  ADD CONSTRAINT `fk_pc_c` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pc_p` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_media`
--
ALTER TABLE `product_media`
  ADD CONSTRAINT `fk_media_p` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_variants`
--
ALTER TABLE `product_variants`
  ADD CONSTRAINT `fk_var_p` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `shipments`
--
ALTER TABLE `shipments`
  ADD CONSTRAINT `fk_ship_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `store_hours`
--
ALTER TABLE `store_hours`
  ADD CONSTRAINT `fk_store_hours_store` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_role` FOREIGN KEY (`role_code`) REFERENCES `roles` (`role_code`);

--
-- Constraints for table `variant_price_history`
--
ALTER TABLE `variant_price_history`
  ADD CONSTRAINT `fk_vph_v` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
