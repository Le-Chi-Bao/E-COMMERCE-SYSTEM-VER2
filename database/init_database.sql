-- database/init_database.sql
-- Tạo database và tables cho Mini E-commerce System

CREATE DATABASE IF NOT EXISTS mini_ecommerce;
USE mini_ecommerce;

-- Bảng người dùng
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng danh mục
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Bảng sản phẩm
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    category_id INT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Bảng giỏ hàng
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Bảng đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Bảng chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Thêm dữ liệu vào bảng
INSERT INTO categories (category_name, description) VALUES 
('Điện thoại', 'Smartphone và điện thoại di động'),
('Laptop', 'Máy tính xách tay'),
('Phụ kiện', 'Phụ kiện điện tử');

INSERT INTO products (name, description, price, stock_quantity, category_id) VALUES
('iPhone 15', 'iPhone 15 128GB', 25000000, 50, 1),
('Samsung Galaxy S24', 'Samsung Galaxy S24 Ultra', 22000000, 30, 1),
('MacBook Air M2', 'MacBook Air 13 inch M2', 32000000, 20, 2),
('Tai nghe AirPods', 'Tai nghe không dây Apple AirPods', 5000000, 100, 3),
('Laptop Dell XPS', 'Laptop Dell XPS 13 inch', 28000000, 15, 2),
('Samsung Galaxy Tab', 'Tablet Samsung Galaxy Tab S9', 15000000, 25, 3);

-- Tạo user mẫu (password đã được hash)
INSERT INTO users (username, email, password) VALUES 
('testuser', 'test@email.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'), -- password: 123456
('admin', 'admin@email.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'); -- password: admin123

-- Tạo index để tối ưu hiệu năng
CREATE INDEX idx_user_cart ON cart(user_id);
CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_order_user ON orders(user_id);