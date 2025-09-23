-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 23, 2025 at 05:24 PM
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
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` bigint(20) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `parent_id`, `name`, `slug`, `created_at`, `updated_at`, `is_active`) VALUES
(1, NULL, 'Cam', 'cam', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(2, NULL, 'Cherry', 'cherry', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(3, NULL, 'Chôm chôm', 'chom-chom', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(4, NULL, 'Combo/Quà tặng', 'combo-qua-tang', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(5, NULL, 'Dâu tây', 'dau-tay', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(6, NULL, 'Dưa', 'dua', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(7, NULL, 'Hồng', 'hong', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(8, NULL, 'Khác', 'khac', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(9, NULL, 'Kiwi', 'kiwi', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(10, NULL, 'Lê', 'le', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(11, NULL, 'Lựu', 'luu', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(12, NULL, 'Măng cụt', 'mang-cut', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(13, NULL, 'Mận', 'man', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(14, NULL, 'Na', 'na', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(15, NULL, 'Nho', 'nho', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(16, NULL, 'Quýt', 'quyt', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(17, NULL, 'Roi', 'roi', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(18, NULL, 'Sầu riêng', 'sau-rieng', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(19, NULL, 'Thanh long', 'thanh-long', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(20, NULL, 'Táo', 'tao', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(21, NULL, 'Việt quất', 'viet-quat', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(22, NULL, 'Xoài', 'xoai', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1),
(23, NULL, 'Đào', 'ao', '2025-09-19 18:17:09', '2025-09-19 18:17:09', 1);

-- --------------------------------------------------------

--
-- Table structure for table `discounts`
--

CREATE TABLE `discounts` (
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `discount_type` varchar(20) NOT NULL,
  `discount_value` decimal(10,2) NOT NULL,
  `min_order_amount` decimal(10,2) DEFAULT NULL,
  `max_discount_amount` decimal(10,2) DEFAULT NULL,
  `usage_limit` int(11) DEFAULT NULL,
  `usage_limit_per_user` int(11) DEFAULT NULL,
  `used_count` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `id` bigint(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` bigint(20) NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `order_code` varchar(20) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `address` text NOT NULL,
  `province` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `ward` varchar(100) DEFAULT NULL,
  `payment_method` enum('COD','BANK_TRANSFER','MOCK_TRANSFER') NOT NULL DEFAULT 'COD',
  `payment_status` enum('unpaid','paid','transfer_confirmed','mock_paid') NOT NULL DEFAULT 'unpaid',
  `status` enum('pending_payment','waiting_admin_confirmation','shipping','delivered','completed','cancelled','pending','confirmed','fulfilled') NOT NULL DEFAULT 'pending_payment',
  `subtotal` decimal(12,2) DEFAULT NULL,
  `shipping_fee` decimal(12,2) NOT NULL DEFAULT 0.00,
  `discount_amt` decimal(12,2) NOT NULL DEFAULT 0.00,
  `discount_code` varchar(50) DEFAULT NULL,
  `grand_total` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `transfer_confirmed` tinyint(1) NOT NULL DEFAULT 0,
  `transfer_confirmed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `order_code`, `customer_name`, `phone`, `address`, `province`, `district`, `ward`, `payment_method`, `payment_status`, `status`, `subtotal`, `shipping_fee`, `discount_amt`, `discount_code`, `grand_total`, `total_amount`, `created_at`, `transfer_confirmed`, `transfer_confirmed_at`) VALUES
(29, '3', 'FJ-GDNB1X', 'Nguyễn Văn A', '0888666888', '123', '123', '123', '123', 'COD', 'mock_paid', 'fulfilled', 488000.00, 30000.00, 0.00, NULL, 518000.00, 518000.00, '2025-09-23 15:03:14', 0, NULL),
(30, '3', 'FJ-AU7LZP', 'Nguyễn Văn A', '0888666888', '123', '123', '123', '123', 'COD', 'unpaid', 'cancelled', 142000.00, 0.00, 0.00, NULL, 142000.00, 142000.00, '2025-09-23 15:23:18', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_events`
--

CREATE TABLE `order_events` (
  `id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `event_type` enum('placed','payment_confirmed','admin_confirmed','shipping_started','delivered','completed','cancelled','restocked','mock_paid','confirmed','fulfilled','paid') NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_events`
--

INSERT INTO `order_events` (`id`, `order_id`, `event_type`, `note`, `created_at`) VALUES
(57, 29, 'placed', 'Order placed', '2025-09-23 15:03:14'),
(58, 30, 'placed', 'Order placed', '2025-09-23 15:23:18'),
(59, 30, 'cancelled', 'Đơn hàng chuyển từ waiting_admin_confirmation sang cancelled', '2025-09-23 15:23:29');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `qty` int(11) NOT NULL,
  `line_total` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `product_name`, `unit_price`, `qty`, `line_total`) VALUES
(29, 29, 12, 'Cherry Canada', 488000.00, 1, 488000.00),
(30, 30, 10, 'Nho đen sữa Đài Loan', 142000.00, 1, 142000.00);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `short_desc` text DEFAULT NULL,
  `image_url` varchar(1024) DEFAULT NULL,
  `price` decimal(12,2) NOT NULL,
  `sale_price` decimal(12,2) DEFAULT NULL,
  `sale_start` datetime DEFAULT NULL,
  `sale_end` datetime DEFAULT NULL,
  `sale_active` tinyint(1) NOT NULL DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `slug`, `short_desc`, `image_url`, `price`, `sale_price`, `sale_start`, `sale_end`, `sale_active`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Lê quả tươi', 'le-qua-tuoi', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-13-1.png', 99000.00, 69000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(2, 'Roi đỏ An Phước', 'roi-o-an-phuoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-30.png', 129000.00, 100000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(3, 'Hồng táo Jujubin', 'hong-tao-jujubin', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/Thiet-ke-chua-co-ten-7.png', 169000.00, 148000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(4, 'Đào Tuyết Lệ Giang', 'ao-tuyet-le-giang', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/09/z7000739892044_613052488a59c82ee437d56f79f92271.jpg', 129000.00, 99000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(5, 'Chôm chôm Thái Miền Nam', 'chom-chom-thai-mien-nam', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/09/Thiet-ke-chua-co-ten.png', 99000.00, 69000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(6, 'Thanh Long Ruột Đỏ', 'thanh-long-ruot-o', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/09/1.png', 69000.00, 49000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(7, 'Táo Fuji Nam Phi', 'tao-fuji-nam-phi', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/fuji-nam-phi.png', 99000.00, 79000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(8, 'Nho xanh sữa Hàn Quốc', 'nho-xanh-sua-han-quoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1-1.jpeg', 899000.00, 665000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(9, 'Nho đỏ Mỹ', 'nho-o-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/nho-do-my-4.jpg', 249000.00, 197000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(10, 'Nho đen sữa Đài Loan', 'nho-en-sua-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/07/nho-den-sua-dai-loan.png', 169000.00, 142000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(11, 'Chà là Thái Lan', 'cha-la-thai-lan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/08/cha-la-thai-lan-1.png', 199000.00, 144000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(12, 'Cherry Canada', 'cherry-canada', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-1.png', 599000.00, 488000.00, '2025-09-20 15:39:23', '2025-09-30 15:39:23', 1, 1, '2025-09-19 18:17:09', '2025-09-20 15:51:11'),
(13, 'Táo Dazzle Mỹ', 'tao-dazzle-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/02/2-1.jpg', 139000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(14, 'Táo Fuji Newzealand', 'tao-fuji-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/fuji-new.png', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(15, 'SET LỤC BẢO TRĂNG RẰM', 'set-luc-bao-trang-ram', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/537748442_767456776040321_8745635047054036671_n.jpg', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(16, 'SET NGŨ PHÚC TRĂNG RẰM', 'set-ngu-phuc-trang-ram', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/537296695_767456786040320_5892535717461104407_n.jpg', 550000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(17, 'Lê Nâu', 'le-nau', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-12-1.png', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(18, 'Táo Rockit Newzealand', 'tao-rockit-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/tao-rokit.png', 149000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(19, 'Giỏ quà biếu tặng 3', 'gio-qua-bieu-tang-3', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6874712234441_706eb2778621ec19930252443e372347.jpg', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(20, 'KHAY QUẢ BIẾU TẶNG – 08', 'khay-qua-bieu-tang-08', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-15.png', 450000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(21, 'KHAY QUẢ BIẾU TẶNG – 06', 'khay-qua-bieu-tang-06', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-13.png', 480000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(22, 'Giỏ quà biếu tặng 39', 'gio-qua-bieu-tang-39', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6874712946646_d7a6fbb61dbb732a33fb60cee2a587eb.jpg', 900000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(23, 'Giỏ quà biếu tặng 38', 'gio-qua-bieu-tang-38', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/2.png', 3000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(24, 'Giỏ quà biếu tặng 37', 'gio-qua-bieu-tang-37', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6874711379393_93ead9533b69f55c9c62fd07c02ceb49.jpg', 1000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(25, 'KHAY QUẢ BIẾU TẶNG – 05', 'khay-qua-bieu-tang-05', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-12.png', 900000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(26, 'KHAY QUẢ BIẾU TẶNG – 04', 'khay-qua-bieu-tang-04', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-11.png', 850000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(27, 'KHAY QUẢ BIẾU TẶNG – 03', 'khay-qua-bieu-tang-03', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/482032925_637675535685113_4908052050553044721_n.jpg', 550000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(28, 'KHAY QUẢ BIẾU TẶNG – 01', 'khay-qua-bieu-tang-01', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/z6005203646046_7d5f247f9ebda6f46085cd6fb535a9f8.jpg', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(29, 'KHAY QUẢ BIẾU TẶNG – 02', 'khay-qua-bieu-tang-02', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/z6005214138890_be61d6637df059cc459419f7850afba4.jpg', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(30, 'Giỏ quà biếu tặng 36', 'gio-qua-bieu-tang-36', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6874710929655_7476bff5f9a0ca4cd92c42af926c7c08.jpg', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(31, 'Giỏ quà biếu tặng 34', 'gio-qua-bieu-tang-34', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6874713341078_aaedc72d829ac02cf1c0ece176a4dac7.jpg', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(32, 'KHAY QUẢ BIẾU TẶNG – 07', 'khay-qua-bieu-tang-07', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-14.png', 500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(33, 'HỘP ĐỒNG XUÂN 1', 'hop-ong-xuan-1', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/4-banh-Dong-01.png', 390000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(34, 'HỘP V.I.P', 'hop-vip', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319713414_a2f6381f7cd1d1bd39ad2984f94577eb.jpg', 1999000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(35, 'HỘP THĂNG LONG', 'hop-thang-long', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319561095_11e1e49342fc83a0dcfa206aad9b77c3.jpg', 1200000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(36, 'HỘP THĂNG HOA', 'hop-thang-hoa', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318663084_06564be97b5d5d08aaa2a575da7f9fcb.jpg', 920000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(37, 'HỘP SẮC HOA', 'hop-sac-hoa', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318731342_8219536f3723bdbe2255ec13c292a82c.jpg', 580000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(38, 'HỘP QUYẾN RŨ', 'hop-quyen-ru', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318679762_c167cd88ead0b40c92f92d2be9168c7f.jpg', 880000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(39, 'HỘP NỒNG NÀN', 'hop-nong-nan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318679761_3fe863efbadd1ec534f4e51cd919043c.jpg', 520000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(40, 'HỘP NGUYỄN DU PHỐ', 'hop-nguyen-du-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319298738_da8e5d9ebf3ede6abb97d25ab3fc80be.jpg', 690000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(41, 'HỘP NGÔ QUYỀN PHỐ', 'hop-ngo-quyen-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319636985_994c58ac02025d04cbbef8fa43bbc0e6.jpg', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(42, 'HỘP LÝ THƯỜNG KIỆT PHỐ', 'hop-ly-thuong-kiet-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319420182_f3737e3effc9ee76e3030a787617b5b3.jpg', 790000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(43, 'HỘP LÊ THÁNH TÔNG PHỐ', 'hop-le-thanh-tong-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319713415_288ce2fa84525fee25ad5901e0b5bacd.jpg', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(44, 'HỘP HOA NGUYỆT 2', 'hop-hoa-nguyet-2', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318533589_00590b83244c49f3fd295c59c8775451.jpg', 180000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(45, 'HỘP HOA NGUYỆT 1', 'hop-hoa-nguyet-1', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318628210_ea1e75897a4e1d2ed1bebc14dcf359ec-1.jpg', 180000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(46, 'HỘP HÀNG NGANG PHỐ', 'hop-hang-ngang-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319243896_87a49b63b13d2c2d69da5b04038e0409.jpg', 560000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(47, 'HỘP HÀNG MÃ PHỐ', 'hop-hang-ma-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319768343_42ad027217555322c4a1800541e0659d.jpg', 320000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(48, 'HỘP HÀNG KHAY PHỐ', 'hop-hang-khay-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319636984_366f1b6f7a39287ea50ceea3186fe867.jpg', 1200000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(49, 'HỘP HÀNG GAI PHỐ', 'hop-hang-gai-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319111199_51345fcbced700633787d6ca7fde2542.jpg', 560000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(50, 'HỘP HÀNG ĐƯỜNG PHỐ', 'hop-hang-uong-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319224094_69e4e10853c9d458bdb8e2f13025a55f.jpg', 560000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(51, 'HỘP HÀNG ĐÀO PHỐ', 'hop-hang-ao-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319111200_22fd4a0363941690606ef923ba748643.jpg', 560000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(52, 'HỘP HÂN HOAN', 'hop-han-hoan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318592408_4ffe835786f9cbf42efa1613c9585344.jpg', 390000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(53, 'HỘP ĐỒNG XUÂN 3', 'hop-ong-xuan-3', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/4-banh-Dong-03.png', 390000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(54, 'HỘP ĐỒNG XUÂN 2', 'hop-ong-xuan-2', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/4-banh-Dong-02.png', 390000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(55, 'HỘP ĐỒNG XUÂN 4', 'hop-ong-xuan-4', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/4-banh-Dong-04.png', 390000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(56, 'HỘP HÀ THÀNH', 'hop-ha-thanh', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319505738_25c9cead88f49fb800361c489e75f720.jpg', 950000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(57, 'HỘP ĐAM MÊ', 'hop-am-me', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318954160_6bd9f6566343dcfe64c6cb9c3db3bf4a.jpg', 820000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(58, 'HỘP DỊU DÀNG', 'hop-diu-dang', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319021990_ea922f3484c79187f236d85c2c26920b.jpg', 430000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(59, 'HỘP CUỐN HÚT', 'hop-cuon-hut', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318792732_26f08271f6dea362fab9eb8bddb72d5b.jpg', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(60, 'HỘP BIẾN TẤU 2', 'hop-bien-tau-2', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318761601_a3687b8cee8bbc97f15783ff611e45e9.jpg', 350000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(61, 'HỘP BIẾN TẤU 1', 'hop-bien-tau-1', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318875457_79631a50615e36bf7eac7743134e92cb.jpg', 350000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(62, 'HỘP PHAN ĐÌNH PHÙNG PHỐ', 'hop-phan-inh-phung-pho', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925319348126_7214a0643ac7b4488d673ff5c5a3c2eb.jpg', 790000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(63, 'HỘP QUÝ PHÁI', 'hop-quy-phai', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/z6925318564477_f2171550c9c030485fb285f2b80e0915.jpg', 1150000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(64, 'Nho đen Mỹ', 'nho-en-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/nho-den-my.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(65, 'Nho xanh Mỹ', 'nho-xanh-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/nh0-xanh-my.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(66, 'Nho đỏ nội địa Trung', 'nho-o-noi-ia-trung', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/06/6.png', 229000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(67, 'Táo Juliet Pháp', 'tao-juliet-phap', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/09/tao-jiliet.png', 129000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(68, 'Nho ngón tay Mỹ', 'nho-ngon-tay-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/08/2-1.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(69, 'Nho đỏ kẹo Mỹ', 'nho-o-keo-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/07/1-1.jpg', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(70, 'Giỏ quà biếu tặng 32', 'gio-qua-bieu-tang-32', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/3-5.png', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(71, 'GIỎ QUÀ ENVY 02', 'gio-qua-envy-02', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/5.png', 1000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(72, 'Giỏ quà biếu tặng 33', 'gio-qua-bieu-tang-33', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/4.png', 500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(73, 'Giỏ quà biếu tặng 22', 'gio-qua-bieu-tang-22', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6874713115152_e3c5a3b4149e57ed79abceec43c3f004.jpg', 1700000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(74, 'Nho ngón tay Đài Loan', 'nho-ngon-tay-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/07/nho-ngon-tay-dai-loan.png', 229000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(75, 'Kiwi vàng Newzealand', 'kiwi-vang-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-72.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(76, 'Quýt APH', 'quyt-aph', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/GIAI-NHIET-NGAY-HE-33-1.png', 109000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(77, 'Táo Envy Newzealand', 'tao-envy-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Gio-hoa-900-x-900-px-6.png', 179000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(78, 'Táo Envy Mỹ', 'tao-envy-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1-1.jpg', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(79, 'Dưa vàng Lam Sơn', 'dua-vang-lam-son', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/07/518419830_1198219999010571_7143768441460756109_n.jpg', 30000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(80, 'Lựu đỏ', 'luu-o', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/08/4.jpg', 169000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(81, 'Na Thái VIP', 'na-thai-vip', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/07/Thiet-ke-chua-co-ten.png', 79000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(82, 'Thanh long đỏ Việt Nam', 'thanh-long-o-viet-nam', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/07/2-3.jpg', 28000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(83, 'Dưa chấm xuất Nhật', 'dua-cham-xuat-nhat', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/GIAI-NHIET-NGAY-HE-36.png', 89000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(84, 'Kiwi xanh Newzealand', 'kiwi-xanh-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/05/PRODUCT_PHOTOGRAPHY_GREEN_COMBO_SPOON-1.psd.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(85, 'Dưa lê giống Hàn', 'dua-le-giong-han', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/08/z5707194137439_1fef1c4cdbcff9b296fb57ec2012edd5.jpg', 129000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(86, 'SET QUÀ NẮNG MAI', 'set-qua-nang-mai', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/9-Anh-post-gio-qua-02.png', 1200000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(87, 'SET QUÀ NGỌC NGÀ', 'set-qua-ngoc-nga', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/07/9-Anh-post-gio-qua-01.png', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(88, 'Giỏ quà biếu tặng 10', 'gio-qua-bieu-tang-10', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/04/z6712908260758_8949be7d91d72c6cf3b384661ca3c798.jpg', 1300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(89, 'Giỏ Tri Ân', 'gio-tri-an', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/9-Anh-post-gio-qua-06.png', 2300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(90, 'Giỏ quà biếu tặng 26', 'gio-qua-bieu-tang-26', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6736920365005_cee44b5cca01e3bdb88bd552954b191f.jpg', 1300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(91, 'Giỏ Hồng Phát', 'gio-hong-phat', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/9-Anh-post-gio-qua-08.png', 2200000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(92, 'Giỏ Ngọc Lễ', 'gio-ngoc-le', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/9-Anh-post-gio-qua-05.png', 2300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(93, 'Giỏ Hồng Phúc', 'gio-hong-phuc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/9-Anh-post-gio-qua-07.png', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(94, 'Giỏ An Tường', 'gio-an-tuong', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/9-Anh-post-gio-qua-09.png', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(95, 'Giỏ quà Minh Nguyệt', 'gio-qua-minh-nguyet', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/9-Anh-post-gio-qua-04.png', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(96, 'Lê Xanh', 'le-xanh', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/07/z6712923469734_3af086edf48a779e933df38b3fc354ca.jpg', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(97, 'Việt quất Jumbo Mỹ', 'viet-quat-jumbo-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-82.png', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(98, 'Đào dẹt Đài Loan (500g)', 'ao-det-ai-loan-500g', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/09/dao-det-dai-loan.png', 129000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(99, 'Nho đỏ Crimson Úc', 'nho-o-crimson-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/02/482274627_1174838681317856_6420870820821848241_n.jpg', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(100, 'Nho đen Melody Úc', 'nho-en-melody-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/02/2.jpg', 229000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(101, 'Nho sữa Đài Loan', 'nho-sua-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/www.fujifruit.com_.vn-81.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(102, 'Cherry Mỹ', 'cherry-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-2.png', 499000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(103, 'KHAY QUẢ BIẾU TẶNG – 12', 'khay-qua-bieu-tang-12', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/20241119-155404.jpg', 700000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(104, 'KHAY QUẢ BIẾU TẶNG – 16', 'khay-qua-bieu-tang-16', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/z6712848897171_347b018248ad727b7967a282104f387d.jpg', 350000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(105, 'KHAY QUẢ BIẾU TẶNG – 24', 'khay-qua-bieu-tang-24', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/11.png', 600000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(106, 'KHAY QUẢ BIẾU TẶNG – 22', 'khay-qua-bieu-tang-22', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/z6005507859893_9c85b95d63ca26008bd5ed2ba736257e.jpg', 600000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(107, 'Vải U Trứng Hưng Yên', 'vai-u-trung-hung-yen', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/06/1-1.png', 269000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(108, 'Cam vàng Úc', 'cam-vang-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/cam-vang-uc-02.png', 229000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(109, 'Giỏ quà biếu tặng 24', 'gio-qua-bieu-tang-24', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1111.png', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(110, 'Táo Ambrosia Mỹ', 'tao-ambrosia-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-9.png', 125000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(111, 'Táo Ambrosia Newzealand', 'tao-ambrosia-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-10.png', 109000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(112, 'Táo Ambrosia Canada', 'tao-ambrosia-canada', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1-3.jpg', 129000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(113, 'Nho xanh Chile', 'nho-xanh-chile', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/05/nho-xanh-chile.jpg', 229000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(114, 'Măng cụt Thái', 'mang-cut-thai', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/07/1-5.jpg', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(115, 'Nho xanh Sweet Globe Úc', 'nho-xanh-sweet-globe-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/02/Untitled-design-2023-02-07T133644.720.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(116, 'Nho Xanh Frutico Úc', 'nho-xanh-frutico-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/z6341375549035_4395da248e74371d100f31b6e6ab66f9.jpg', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(117, 'Dừa trọc size L', 'dua-troc-size-l', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-29.png', 39000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(118, 'Táo Ever Crisp Mỹ', 'tao-ever-crisp-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/Rosalee-1.jpg', 89000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(119, 'Nho xanh Ấn Độ', 'nho-xanh-an-o', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/05/Thiet-ke-chua-co-ten-5.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(120, 'Mâm quả tài lộc 8', 'mam-qua-tai-loc-8', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/mam-qua-tai-loc-8-1.png', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(121, 'Mâm quả tài lộc 6', 'mam-qua-tai-loc-6', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/mam-qua-tai-loc-6-1.png', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(122, 'KHAY QUẢ BIẾU TẶNG – 20', 'khay-qua-bieu-tang-20', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/z6044204854735_16de2f90c6d87021db58ff6bf6fb500e-1.jpg', 300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(123, 'KHAY QUẢ BIẾU TẶNG – 19', 'khay-qua-bieu-tang-19', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/z6005219638346_fea62ca911e8f81e9c1adb5203e4ffd7.jpg', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(124, 'KHAY QUẢ BIẾU TẶNG – 23', 'khay-qua-bieu-tang-23', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/Anh-chup-man-hinh-2025-05-15-155028.png', 750000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(125, 'Dâu tây Hàn Quốc', 'dau-tay-han-quoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/12-4.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(126, 'Mận ruột đỏ Chile', 'man-ruot-o-chile', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/03/332685115_463095422609911_6438903278111535045_n.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(127, 'Lê Nam Phi', 'le-nam-phi', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/320933909_660125062567171_4058836009108110718_n.jpg', 109000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(128, 'Táo dazzle Newzealand', 'tao-dazzle-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-6.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(129, 'Lựu Peru', 'luu-peru', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-68.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(130, 'Mận ruột đỏ Úc', 'man-ruot-o-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-84.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(131, 'Táo xanh Pháp', 'tao-xanh-phap', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-78.png', 109000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(132, 'Kiwi vàng Đài Loan', 'kiwi-vang-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-74.png', 69000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(133, 'Cam vàng Đài Loan', 'cam-vang-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1-2.jpg', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(134, 'Quýt baby', 'quyt-baby', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6167429749706_a749e04d8814023e6b75834bc0d52d74.jpg', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(135, 'Kiwi vàng Pháp', 'kiwi-vang-phap', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-71.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(136, 'Hồng mật Vân Sơn', 'hong-mat-van-son', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/3-12.png', 169000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(137, 'Na dai Tây Ninh', 'na-dai-tay-ninh', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-18.png', 139000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(138, 'Nho xanh Oliver Úc', 'nho-xanh-oliver-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/www.fujifruit.com_.vn-76.png', 269000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(139, 'Nho đen Hello Úc', 'nho-en-hello-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-69.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(140, 'Giỏ quà biếu tặng 29', 'gio-qua-bieu-tang-29', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/3-2.png', 2500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(141, 'Giỏ quà biếu tặng 17', 'gio-qua-bieu-tang-17', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/2-2.png', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(142, 'Giỏ quà biếu tặng 27', 'gio-qua-bieu-tang-27', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/4-2.png', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(143, 'Giỏ quà biếu tặng 23', 'gio-qua-bieu-tang-23', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/41.png', 1300000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(144, 'Giỏ quà biếu tặng 19', 'gio-qua-bieu-tang-19', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/435256796_403762422409760_4271141863507799447_n.jpg', 1000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(145, 'Giỏ quà biếu tặng 4', 'gio-qua-bieu-tang-4', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/5.png', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(146, 'Giỏ quà biếu tặng 18', 'gio-qua-bieu-tang-18', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/4-1.png', 3000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(147, 'Giỏ quà biếu tặng 8', 'gio-qua-bieu-tang-8', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/04/23.png', 1500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(148, 'Giỏ quà biếu tặng 1', 'gio-qua-bieu-tang-1', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/31.png', 800000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(149, 'Giỏ quà biếu tặng 5', 'gio-qua-bieu-tang-5', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/10.png', 1000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(150, 'Giỏ quà biếu tặng 16', 'gio-qua-bieu-tang-16', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/15-1.png', 950000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(151, 'Giỏ quà biếu tặng 11', 'gio-qua-bieu-tang-11', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/04/2-1.png', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(152, 'Nho đỏ kẹo Úc', 'nho-o-keo-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Blue-Gradient-Modern-Bussiness-Facebook-Cover-1066-×-1600-px-10.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(153, 'Dâu tây Mộc Châu', 'dau-tay-moc-chau', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/02/471732261_583658627753471_9219321597210998021_n.jpg', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(154, 'Việt quất Đài Loan', 'viet-quat-ai-loan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/05/z6442843165973_cb2b23ec2dd96bb96540d0a302690e28.jpg', 49000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(155, 'Táo xanh Mỹ', 'tao-xanh-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/tao-xanh-my.png', 115000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(156, 'Sầu riêng RI6 mini', 'sau-rieng-ri6-mini', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/05/Thiet-ke-chua-co-ten-11.png', 129000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(157, 'Dưa lưới Aladin', 'dua-luoi-aladin', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/www.fujifruit.com_.vn-2023-04-26T132502.668.png', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(158, 'Nho xanh Futico Úc', 'nho-xanh-futico-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/04/www.fujifruit.com_.vn-2023-04-25T195010.809.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(159, 'Táo Queen Newzealand', 'tao-queen-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/tao-queen-new.png', 109000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(160, 'Nho ngón tay Hello Úc', 'nho-ngon-tay-hello-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/02/329130144_900202954558583_1877011328191703864_n.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(161, 'KHAY QUẢ BIẾU TẶNG – 30', 'khay-qua-bieu-tang-30', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/16.png', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(162, 'KHAY QUẢ BIẾU TẶNG – 29', 'khay-qua-bieu-tang-29', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/15.png', 800000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(163, 'KHAY QUẢ BIẾU TẶNG – 28', 'khay-qua-bieu-tang-28', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/13.png', 500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(164, 'KHAY QUẢ BIẾU TẶNG – 26', 'khay-qua-bieu-tang-26', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/22.png', 600000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(165, 'KHAY QUẢ BIẾU TẶNG – 27', 'khay-qua-bieu-tang-27', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/18.png', 400000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(166, 'KHAY QUẢ BIẾU TẶNG – 25', 'khay-qua-bieu-tang-25', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2025/03/17.png', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(167, 'Táo Breeze Newzealand', 'tao-breeze-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-11.png', 125000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(168, 'Nho đen kẹo Úc', 'nho-en-keo-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Nho-den-keo-Uc.png', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(169, 'Lựu Ấn Độ', 'luu-an-o', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/Gio-hoa-900-x-900-px-4.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(170, 'Nho xanh Hydix Nam Phi', 'nho-xanh-hydix-nam-phi', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/05/nho-xanh-nam-ohi.jpg', 349000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(171, 'Cherry Newzealand', 'cherry-newzealand', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-3.png', 599000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(172, 'Cherry Chile', 'cherry-chile', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Thiet-ke-chua-co-ten-1-1.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(173, 'Táo Fuji Mỹ', 'tao-fuji-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/fuji-my.png', 89000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(174, 'Giỏ quà biếu tặng 25', 'gio-qua-bieu-tang-25', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6005508009739_d8664dc5fe4bbf96ff4b72d1a9f941cc.jpg', 2000000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(175, 'Dâu tây Đà Lạt (330g)', 'dau-tay-a-lat-330g', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/08/dau-tay-da-lat-1.png', 169000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(176, 'Giỏ quà biếu tặng 31', 'gio-qua-bieu-tang-31', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z6005249609992_5146ffa8638e5b2097185347da8cb055.jpg', 3500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(177, 'Giỏ quả biếu tặng 21', 'gio-qua-bieu-tang-21', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/1.png', 950000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(178, 'GIỎ QUẢ ENVY', 'gio-qua-envy', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/03/468122138_932815988911374_5791732756503854853_n.jpg', 1200000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(179, 'Giỏ quà biếu tặng 9', 'gio-qua-bieu-tang-9', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/04/2.png', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(180, 'Giỏ quà biếu tặng 13', 'gio-qua-bieu-tang-13', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/3.png', 750000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(181, 'Giỏ quà biếu tặng 6', 'gio-qua-bieu-tang-6', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/06/1.png', 500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(182, 'Nho xanh Peru', 'nho-xanh-peru', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/nho-peru.jpg', 249000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(183, 'Việt quất Peru', 'viet-quat-peru', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/25.png', 79000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(184, 'Dưa lưới xanh TL3', 'dua-luoi-xanh-tl3', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/dua-luoi-xanh-1.jpeg', 59000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(185, 'Nho xanh Hello Úc', 'nho-xanh-hello-uc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/03/Thiet-ke-chua-co-ten-4.png', 299000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(186, 'Lựu đỏ Tunisia', 'luu-o-tunisia', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/2-12.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(187, 'Xoài cát chu Đồng Tháp', 'xoai-cat-chu-ong-thap', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-27.png', 99000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(188, 'Thanh trà Thái Lan', 'thanh-tra-thai-lan', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/03/4-1.png', 269000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(189, 'Hồng giòn Hàn Quốc', 'hong-gion-han-quoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/Untitled-design-20.png', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(190, 'Táo Story Pháp', 'tao-story-phap', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/12/tao.jpg', 89000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(191, 'CHÔM CHÔM NHÃN TIỀN GIANG', 'chom-chom-nhan-tien-giang', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/12/z6167426038678_5dd0a8caadd9c59e1666e214f423a222.jpg', 119000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(192, 'Táo Koru Mỹ', 'tao-koru-my', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/tao-koru-usa.png', 135000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(193, 'Lê Hàn Quốc', 'le-han-quoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2023/01/14d418966069a3cffc5e57088ce1b675b9609951_s2_n2_y2.png', 199000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(194, 'KHAY QUẢ BIẾU TẶNG – 21', 'khay-qua-bieu-tang-21', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/20241119-163226.jpg', 650000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(195, 'KHAY QUẢ BIẾU TẶNG – 17', 'khay-qua-bieu-tang-17', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/20241119-155423.jpg', 400000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(196, 'KHAY QUẢ BIẾU TẶNG – 13', 'khay-qua-bieu-tang-13', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2024/11/20241119-155410.jpg', 500000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(197, 'Cam xoàn loại 1', 'cam-xoan-loai-1', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/cam-xoan.png', 59000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09'),
(198, 'Dưa lê Hàn Quốc', 'dua-le-han-quoc', NULL, 'https://fujifruit.com.vn/wp-content/uploads/2022/12/z4000423355907_9ce087dbce6e9012fc7cfb7a917390dc.jpg', 149000.00, NULL, NULL, NULL, 0, 1, '2025-09-19 18:17:09', '2025-09-19 18:17:09');

-- --------------------------------------------------------

--
-- Table structure for table `product_categories`
--

CREATE TABLE `product_categories` (
  `product_id` bigint(20) NOT NULL,
  `category_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product_categories`
--

INSERT INTO `product_categories` (`product_id`, `category_id`) VALUES
(1, 10),
(2, 17),
(3, 20),
(4, 10),
(5, 3),
(6, 19),
(7, 20),
(8, 15),
(9, 15),
(10, 15),
(11, 8),
(12, 2),
(13, 20),
(14, 20),
(15, 8),
(16, 8),
(17, 10),
(18, 20),
(19, 4),
(20, 8),
(21, 8),
(22, 4),
(23, 4),
(24, 4),
(25, 8),
(26, 8),
(27, 8),
(28, 8),
(29, 8),
(30, 4),
(31, 4),
(32, 8),
(33, 8),
(34, 8),
(35, 8),
(36, 8),
(37, 8),
(38, 8),
(39, 8),
(40, 8),
(41, 8),
(42, 8),
(43, 10),
(44, 8),
(45, 8),
(46, 8),
(47, 8),
(48, 8),
(49, 8),
(50, 8),
(51, 23),
(52, 8),
(53, 8),
(54, 8),
(55, 8),
(56, 8),
(57, 8),
(58, 8),
(59, 8),
(60, 8),
(61, 8),
(62, 8),
(63, 8),
(64, 15),
(65, 15),
(66, 15),
(67, 20),
(68, 15),
(69, 15),
(70, 4),
(71, 4),
(72, 4),
(73, 4),
(74, 15),
(75, 9),
(76, 16),
(77, 20),
(78, 20),
(79, 6),
(80, 11),
(81, 14),
(82, 19),
(83, 6),
(84, 9),
(85, 10),
(86, 8),
(87, 8),
(88, 4),
(89, 8),
(90, 4),
(91, 7),
(92, 10),
(93, 7),
(94, 8),
(95, 4),
(96, 10),
(97, 21),
(98, 23),
(99, 15),
(100, 15),
(101, 15),
(102, 2),
(103, 8),
(104, 8),
(105, 8),
(106, 8),
(107, 8),
(108, 1),
(109, 4),
(110, 20),
(111, 20),
(112, 20),
(113, 15),
(114, 12),
(115, 15),
(116, 15),
(117, 6),
(118, 20),
(119, 15),
(120, 8),
(121, 8),
(122, 8),
(123, 8),
(124, 8),
(125, 5),
(126, 13),
(127, 10),
(128, 20),
(129, 11),
(130, 13),
(131, 20),
(132, 9),
(133, 1),
(134, 16),
(135, 9),
(136, 7),
(137, 14),
(138, 15),
(139, 15),
(140, 4),
(141, 4),
(142, 4),
(143, 4),
(144, 4),
(145, 4),
(146, 4),
(147, 4),
(148, 4),
(149, 4),
(150, 4),
(151, 4),
(152, 15),
(153, 5),
(154, 21),
(155, 20),
(156, 18),
(157, 6),
(158, 15),
(159, 20),
(160, 15),
(161, 8),
(162, 8),
(163, 8),
(164, 8),
(165, 8),
(166, 8),
(167, 20),
(168, 15),
(169, 11),
(170, 15),
(171, 2),
(172, 2),
(173, 20),
(174, 4),
(175, 5),
(176, 4),
(177, 4),
(178, 4),
(179, 4),
(180, 4),
(181, 4),
(182, 15),
(183, 21),
(184, 6),
(185, 15),
(186, 11),
(187, 22),
(188, 8),
(189, 7),
(190, 20),
(191, 3),
(192, 20),
(193, 10),
(194, 8),
(195, 8),
(196, 8),
(197, 1),
(198, 10);

-- --------------------------------------------------------

--
-- Table structure for table `product_images`
--

CREATE TABLE `product_images` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `image_url` varchar(1024) NOT NULL,
  `alt` varchar(255) DEFAULT NULL,
  `sort_order` int(11) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_reviews`
--

CREATE TABLE `product_reviews` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `rating` tinyint(4) NOT NULL,
  `content` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_stock`
--

CREATE TABLE `product_stock` (
  `product_id` bigint(20) NOT NULL,
  `qty_on_hand` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product_stock`
--

INSERT INTO `product_stock` (`product_id`, `qty_on_hand`, `updated_at`) VALUES
(1, 0, '2025-09-20 15:39:24'),
(2, 0, '2025-09-20 15:39:24'),
(3, 0, '2025-09-20 15:39:24'),
(4, 16, '2025-09-20 15:39:24'),
(5, 18, '2025-09-20 15:39:24'),
(6, 36, '2025-09-20 15:39:24'),
(7, 10, '2025-09-20 15:39:24'),
(8, 48, '2025-09-23 16:34:40'),
(9, 43, '2025-09-20 21:23:20'),
(10, 8, '2025-09-23 22:23:18'),
(11, 37, '2025-09-23 16:43:59'),
(12, 30, '2025-09-23 22:03:14'),
(13, 17, '2025-09-20 15:43:42'),
(14, 11, '2025-09-20 15:43:42'),
(15, 56, '2025-09-20 15:43:42'),
(16, 18, '2025-09-20 15:43:42'),
(17, 31, '2025-09-20 15:43:42'),
(18, 38, '2025-09-20 15:43:42'),
(19, 37, '2025-09-20 15:43:42'),
(20, 11, '2025-09-20 15:43:42'),
(21, 49, '2025-09-20 15:43:42'),
(22, 43, '2025-09-20 15:43:42'),
(23, 7, '2025-09-20 15:43:42'),
(24, 14, '2025-09-20 15:43:42'),
(25, 45, '2025-09-20 15:43:42'),
(26, 11, '2025-09-20 15:43:42'),
(27, 25, '2025-09-20 15:43:42'),
(28, 32, '2025-09-20 15:43:42'),
(29, 25, '2025-09-20 15:43:42'),
(30, 26, '2025-09-20 15:43:42'),
(31, 50, '2025-09-20 15:43:42'),
(32, 54, '2025-09-20 15:43:42'),
(33, 0, '2025-09-20 15:43:42'),
(34, 26, '2025-09-20 15:43:42'),
(35, 53, '2025-09-20 15:43:42'),
(36, 14, '2025-09-20 15:43:42'),
(37, 19, '2025-09-20 15:43:42'),
(38, 49, '2025-09-20 15:43:42'),
(39, 16, '2025-09-20 15:43:42'),
(40, 40, '2025-09-20 15:43:42'),
(41, 34, '2025-09-20 15:43:42'),
(42, 47, '2025-09-20 15:43:42'),
(43, 17, '2025-09-20 15:43:42'),
(44, 51, '2025-09-20 15:43:42'),
(45, 30, '2025-09-20 15:43:42'),
(46, 49, '2025-09-20 15:43:42'),
(47, 40, '2025-09-20 15:43:42'),
(48, 47, '2025-09-20 15:43:42'),
(49, 55, '2025-09-20 15:43:42'),
(50, 17, '2025-09-20 15:43:42'),
(51, 30, '2025-09-20 15:43:42'),
(52, 36, '2025-09-20 15:43:42'),
(53, 32, '2025-09-20 15:43:42'),
(54, 48, '2025-09-20 15:43:42'),
(55, 25, '2025-09-20 15:43:42'),
(56, 33, '2025-09-20 15:43:42'),
(57, 28, '2025-09-20 15:43:42'),
(58, 37, '2025-09-20 15:43:42'),
(59, 42, '2025-09-20 15:43:42'),
(60, 39, '2025-09-20 15:43:42'),
(61, 8, '2025-09-20 15:43:42'),
(62, 29, '2025-09-20 15:43:42'),
(63, 5, '2025-09-20 15:43:42'),
(64, 46, '2025-09-20 15:43:42'),
(65, 42, '2025-09-20 15:43:42'),
(66, 13, '2025-09-20 15:43:42'),
(67, 46, '2025-09-20 15:43:42'),
(68, 16, '2025-09-20 15:43:42'),
(69, 52, '2025-09-20 15:43:42'),
(70, 39, '2025-09-20 15:43:42'),
(71, 36, '2025-09-20 15:43:42'),
(72, 56, '2025-09-20 15:43:42'),
(73, 55, '2025-09-20 15:43:42'),
(74, 49, '2025-09-20 15:43:42'),
(75, 17, '2025-09-20 15:43:42'),
(76, 45, '2025-09-20 15:43:42'),
(77, 58, '2025-09-20 15:43:42'),
(78, 38, '2025-09-20 15:43:42'),
(79, 12, '2025-09-20 15:43:42'),
(80, 55, '2025-09-20 15:43:42'),
(81, 10, '2025-09-20 15:43:42'),
(82, 49, '2025-09-20 15:43:42'),
(83, 43, '2025-09-20 15:43:42'),
(84, 6, '2025-09-20 15:43:42'),
(85, 7, '2025-09-20 15:43:42'),
(86, 15, '2025-09-20 15:43:42'),
(87, 49, '2025-09-20 15:43:42'),
(88, 29, '2025-09-20 15:43:42'),
(89, 49, '2025-09-20 15:43:42'),
(90, 41, '2025-09-20 15:43:42'),
(91, 55, '2025-09-20 15:43:42'),
(92, 36, '2025-09-20 15:43:42'),
(93, 11, '2025-09-20 15:43:42'),
(94, 52, '2025-09-20 15:43:42'),
(95, 57, '2025-09-20 15:43:42'),
(96, 12, '2025-09-20 15:43:42'),
(97, 51, '2025-09-20 15:43:42'),
(98, 48, '2025-09-20 15:43:42'),
(99, 24, '2025-09-20 15:43:42'),
(100, 29, '2025-09-20 15:43:42'),
(101, 12, '2025-09-20 15:43:42'),
(102, 26, '2025-09-20 15:43:42'),
(103, 32, '2025-09-20 15:43:42'),
(104, 21, '2025-09-20 15:43:42'),
(105, 60, '2025-09-20 15:43:42'),
(106, 8, '2025-09-20 15:43:42'),
(107, 25, '2025-09-20 15:43:42'),
(108, 39, '2025-09-20 21:48:04'),
(109, 5, '2025-09-20 15:43:42'),
(110, 17, '2025-09-20 15:43:42'),
(111, 8, '2025-09-20 15:43:42'),
(112, 41, '2025-09-20 15:43:42'),
(113, 9, '2025-09-20 15:43:42'),
(114, 30, '2025-09-20 15:43:42'),
(115, 6, '2025-09-20 15:43:42'),
(116, 46, '2025-09-20 15:43:42'),
(117, 39, '2025-09-20 15:43:42'),
(118, 52, '2025-09-20 15:43:42'),
(119, 27, '2025-09-20 15:43:42'),
(120, 29, '2025-09-20 15:43:42'),
(121, 5, '2025-09-20 15:43:42'),
(122, 44, '2025-09-20 15:43:42'),
(123, 35, '2025-09-20 15:43:42'),
(124, 35, '2025-09-20 15:43:42'),
(125, 13, '2025-09-20 15:43:42'),
(126, 8, '2025-09-20 15:43:42'),
(127, 56, '2025-09-20 15:43:42'),
(128, 26, '2025-09-20 15:43:42'),
(129, 14, '2025-09-20 15:43:42'),
(130, 42, '2025-09-20 15:43:42'),
(131, 54, '2025-09-20 15:43:42'),
(132, 26, '2025-09-20 15:43:42'),
(133, 18, '2025-09-20 15:43:42'),
(134, 9, '2025-09-20 15:43:42'),
(135, 42, '2025-09-20 15:43:42'),
(136, 12, '2025-09-20 15:43:42'),
(137, 39, '2025-09-20 15:43:42'),
(138, 44, '2025-09-20 15:43:42'),
(139, 44, '2025-09-20 15:43:42'),
(140, 26, '2025-09-20 15:43:42'),
(141, 48, '2025-09-20 15:43:42'),
(142, 46, '2025-09-20 15:43:42'),
(143, 28, '2025-09-20 15:43:42'),
(144, 51, '2025-09-20 15:43:42'),
(145, 56, '2025-09-20 15:43:42'),
(146, 8, '2025-09-20 15:43:42'),
(147, 39, '2025-09-20 15:43:42'),
(148, 53, '2025-09-20 15:43:42'),
(149, 32, '2025-09-20 15:43:42'),
(150, 52, '2025-09-20 15:43:42'),
(151, 47, '2025-09-20 15:43:42'),
(152, 18, '2025-09-20 15:43:42'),
(153, 57, '2025-09-20 15:43:42'),
(154, 60, '2025-09-20 15:43:42'),
(155, 12, '2025-09-20 15:43:42'),
(156, 43, '2025-09-20 15:43:42'),
(157, 6, '2025-09-20 15:43:42'),
(158, 7, '2025-09-20 15:43:42'),
(159, 14, '2025-09-20 15:43:42'),
(160, 45, '2025-09-20 15:43:42'),
(161, 9, '2025-09-20 15:43:42'),
(162, 20, '2025-09-20 15:43:42'),
(163, 12, '2025-09-20 15:43:42'),
(164, 51, '2025-09-20 15:43:42'),
(165, 47, '2025-09-20 15:43:42'),
(166, 20, '2025-09-20 15:43:42'),
(167, 10, '2025-09-20 15:43:42'),
(168, 44, '2025-09-20 15:43:42'),
(169, 15, '2025-09-20 15:43:42'),
(170, 53, '2025-09-20 15:43:42'),
(171, 45, '2025-09-20 15:43:42'),
(172, 5, '2025-09-20 15:43:42'),
(173, 54, '2025-09-20 15:43:42'),
(174, 26, '2025-09-20 15:43:42'),
(175, 21, '2025-09-20 15:43:42'),
(176, 21, '2025-09-20 15:43:42'),
(177, 39, '2025-09-20 15:43:42'),
(178, 15, '2025-09-20 15:43:42'),
(179, 11, '2025-09-20 15:43:42'),
(180, 59, '2025-09-20 15:43:42'),
(181, 33, '2025-09-20 15:43:42'),
(182, 40, '2025-09-20 15:43:42'),
(183, 41, '2025-09-20 15:43:42'),
(184, 23, '2025-09-20 15:43:42'),
(185, 43, '2025-09-20 15:43:42'),
(186, 29, '2025-09-20 15:43:42'),
(187, 13, '2025-09-20 15:43:42'),
(188, 28, '2025-09-20 15:43:42'),
(189, 39, '2025-09-20 15:43:42'),
(190, 53, '2025-09-20 15:43:42'),
(191, 31, '2025-09-20 15:43:42'),
(192, 49, '2025-09-20 15:43:42'),
(193, 35, '2025-09-20 15:43:42'),
(194, 23, '2025-09-20 15:43:42'),
(195, 7, '2025-09-20 15:43:42'),
(196, 11, '2025-09-22 23:02:00'),
(197, 55, '2025-09-22 22:09:42'),
(198, 7, '2025-09-20 18:25:23');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` smallint(6) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `code`, `name`, `created_at`) VALUES
(1, 'admin', 'Quản trị viên', '2025-09-19 14:06:38'),
(2, 'user', 'Người dùng', '2025-09-19 14:06:38');

-- --------------------------------------------------------

--
-- Table structure for table `shipping_rates`
--

CREATE TABLE `shipping_rates` (
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `ward` varchar(100) DEFAULT NULL,
  `shipping_method` varchar(50) NOT NULL,
  `base_fee` decimal(10,2) NOT NULL,
  `per_kg_fee` decimal(10,2) NOT NULL,
  `free_shipping_threshold` decimal(10,2) DEFAULT NULL,
  `estimated_days_min` int(11) NOT NULL,
  `estimated_days_max` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `priority` int(11) NOT NULL,
  `id` bigint(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `avatar_url` varchar(1024) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `email_verified` tinyint(1) NOT NULL DEFAULT 0,
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password_hash`, `full_name`, `avatar_url`, `is_active`, `email_verified`, `last_login_at`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'admin@example.com', NULL, '$2b$12$l44/x5uss45943vM7PXZzuJER16kGddtMCxso2MyNg7RNSatHr.Fa', 'Administrator', NULL, 1, 1, '2025-09-23 15:03:49', '2025-09-19 14:06:38', '2025-09-23 15:03:49'),
(3, 'nva', 'nva@tn.vn', '0888666888', '$2b$12$l44/x5uss45943vM7PXZzuJER16kGddtMCxso2MyNg7RNSatHr.Fa', 'Nguyễn Văn A', NULL, 1, 0, '2025-09-23 15:04:01', '2025-09-20 09:03:55', '2025-09-23 15:04:01'),
(5, 'nvb', 'nvb@tn.vn', '0888666868', '$2b$12$mUAMmsCBROZLg/8PfqkGgeLMFEhF0f2cEdtwoDpY/.TCa6CcDJSU2', 'Nguyễn Văn B', NULL, 1, 0, '2025-09-22 15:00:54', '2025-09-20 14:22:59', '2025-09-22 15:00:54'),
(6, 'nvc', 'nvc@tn.vn', '0888666866', '$2b$12$IZWs0KhQ5ZMt63A2G0JnVOiaqsNuQ.06TpQR9xbII1oDABvikgCAy', 'Nguyễn Văn C', NULL, 1, 0, '2025-09-20 14:45:12', '2025-09-20 14:45:06', '2025-09-20 14:45:12');

-- --------------------------------------------------------

--
-- Table structure for table `user_discount_usage`
--

CREATE TABLE `user_discount_usage` (
  `user_id` bigint(20) NOT NULL,
  `discount_id` bigint(20) NOT NULL,
  `order_id` varchar(36) DEFAULT NULL,
  `used_at` datetime NOT NULL,
  `id` bigint(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` bigint(20) NOT NULL,
  `role_id` smallint(6) NOT NULL,
  `assigned_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_id`, `role_id`, `assigned_at`) VALUES
(1, 1, '2025-09-19 14:06:38');

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_products_effective_price`
-- (See below for the actual view)
--
CREATE TABLE `v_products_effective_price` (
`id` bigint(20)
,`name` varchar(255)
,`slug` varchar(255)
,`short_desc` text
,`image_url` varchar(1024)
,`price` decimal(12,2)
,`sale_price` decimal(12,2)
,`sale_start` datetime
,`sale_end` datetime
,`is_active` tinyint(1)
,`created_at` datetime
,`updated_at` datetime
,`effective_price` decimal(12,2)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_product_rating`
-- (See below for the actual view)
--
CREATE TABLE `v_product_rating` (
`product_id` bigint(20)
,`avg_rating` decimal(7,4)
,`review_count` bigint(21)
);

-- --------------------------------------------------------

--
-- Structure for view `v_products_effective_price`
--
DROP TABLE IF EXISTS `v_products_effective_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_products_effective_price`  AS SELECT `p`.`id` AS `id`, `p`.`name` AS `name`, `p`.`slug` AS `slug`, `p`.`short_desc` AS `short_desc`, `p`.`image_url` AS `image_url`, `p`.`price` AS `price`, `p`.`sale_price` AS `sale_price`, `p`.`sale_start` AS `sale_start`, `p`.`sale_end` AS `sale_end`, `p`.`is_active` AS `is_active`, `p`.`created_at` AS `created_at`, `p`.`updated_at` AS `updated_at`, CASE WHEN `p`.`sale_price` is not null AND (`p`.`sale_start` is null OR `p`.`sale_start` <= current_timestamp()) AND (`p`.`sale_end` is null OR `p`.`sale_end` >= current_timestamp()) THEN `p`.`sale_price` ELSE `p`.`price` END AS `effective_price` FROM `products` AS `p` WHERE `p`.`is_active` = 1 ;

-- --------------------------------------------------------

--
-- Structure for view `v_product_rating`
--
DROP TABLE IF EXISTS `v_product_rating`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_product_rating`  AS SELECT `product_reviews`.`product_id` AS `product_id`, avg(`product_reviews`.`rating`) AS `avg_rating`, count(0) AS `review_count` FROM `product_reviews` GROUP BY `product_reviews`.`product_id` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `idx_cat_parent` (`parent_id`);

--
-- Indexes for table `discounts`
--
ALTER TABLE `discounts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_discounts_code` (`code`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_code` (`order_code`),
  ADD KEY `idx_orders_status_time` (`status`,`created_at`);

--
-- Indexes for table `order_events`
--
ALTER TABLE `order_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ev_order_time` (`order_id`,`created_at`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_oi_order` (`order_id`),
  ADD KEY `fk_oi_product` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `idx_products_created` (`created_at`),
  ADD KEY `idx_products_price` (`price`);
ALTER TABLE `products` ADD FULLTEXT KEY `ft_products` (`name`,`short_desc`);

--
-- Indexes for table `product_categories`
--
ALTER TABLE `product_categories`
  ADD PRIMARY KEY (`product_id`,`category_id`),
  ADD KEY `idx_pc_cat` (`category_id`);

--
-- Indexes for table `product_images`
--
ALTER TABLE `product_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_pi_prod_sort` (`product_id`,`sort_order`);

--
-- Indexes for table `product_reviews`
--
ALTER TABLE `product_reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_reviews_prod_time` (`product_id`,`created_at`);

--
-- Indexes for table `product_stock`
--
ALTER TABLE `product_stock`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `idx_stock_qty` (`qty_on_hand`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `shipping_rates`
--
ALTER TABLE `shipping_rates`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD KEY `idx_users_active` (`is_active`),
  ADD KEY `idx_users_created` (`created_at`);

--
-- Indexes for table `user_discount_usage`
--
ALTER TABLE `user_discount_usage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_user_discount_usage_user_id` (`user_id`),
  ADD KEY `ix_user_discount_usage_order_id` (`order_id`),
  ADD KEY `ix_user_discount_usage_discount_id` (`discount_id`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `idx_ur_role` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `discounts`
--
ALTER TABLE `discounts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `order_events`
--
ALTER TABLE `order_events`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=199;

--
-- AUTO_INCREMENT for table `product_images`
--
ALTER TABLE `product_images`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_reviews`
--
ALTER TABLE `product_reviews`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `shipping_rates`
--
ALTER TABLE `shipping_rates`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_discount_usage`
--
ALTER TABLE `user_discount_usage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_events`
--
ALTER TABLE `order_events`
  ADD CONSTRAINT `order_events_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_oi_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_oi_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `product_categories`
--
ALTER TABLE `product_categories`
  ADD CONSTRAINT `fk_pc_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pc_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_images`
--
ALTER TABLE `product_images`
  ADD CONSTRAINT `fk_pi_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_reviews`
--
ALTER TABLE `product_reviews`
  ADD CONSTRAINT `fk_reviews_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_stock`
--
ALTER TABLE `product_stock`
  ADD CONSTRAINT `fk_stock_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_discount_usage`
--
ALTER TABLE `user_discount_usage`
  ADD CONSTRAINT `user_discount_usage_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_discount_usage_ibfk_2` FOREIGN KEY (`discount_id`) REFERENCES `discounts` (`id`);

--
-- Constraints for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  ADD CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
