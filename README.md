🛒 MINI E-COMMERCE SYSTEM
Hệ thống mua sắm trực tuyến được xây dựng với Python, Gradio và MySQL, triển khai bằng Docker.

🔐 Bảo mật quan trọng
Thay đổi mật khẩu mặc định trước khi sử dụng:

Tạo file .env trong thư mục MINI E-COMMERCE SYSTEM:

env
DB_PASSWORD=mat_khau_moi_cua_ban

Hệ thống sẽ tự động sử dụng mật khẩu từ file .env
🚀 Tính năng
👤 Quản lý người dùng: Đăng ký, đăng nhập, phân quyền

🛍️ Quản lý sản phẩm: Danh mục, tìm kiếm, lọc sản phẩm

🛒 Giỏ hàng: Thêm/xóa sản phẩm, thanh toán

📦 Quản lý đơn hàng: Theo dõi đơn hàng, lịch sử mua hàng

👑 Quản trị: Quản lý users, products, orders, báo cáo doanh thu

📋 Yêu cầu hệ thống
Docker

Docker Compose

2.5GB RAM trống

Port 8866 và 3307 trống

🛠️ Cài đặt & Chạy ứng dụng
### Cách 1: Chạy tự động (Recommended)

#### Clone project
git clone <repository-url>
cd MINI-ECOMMERCE-SYSTEM

#### Thay đổi mật khẩu mặc định trước khi sử dụng
Tạo file .env trong thư mục MINI E-COMMERCE SYSTEM:

DB_PASSWORD=mat_khau_moi_cua_ban

#### Chạy toàn bộ hệ thống
docker compose up -d

Truy cập: http://localhost:8866

### Cách 2: Chạy từng bước (Nếu gặp lỗi)
#### 1. Chạy database trước
docker compose up -d mysql

#### 2. Chờ database khởi động (60 giây)
timeout 60

#### 3. Khởi tạo database
docker compose run --rm app python setup_database.py

#### 4. Chạy ứng dụng
docker compose up -d app

#### 5. Kiểm tra trạng thái
docker compose logs app

### 🔧 Thông tin kết nối
#### Ứng dụng
URL: http://localhost:8866

Port: 8866

#### Database (MySQL)
Host: localhost

Port: 3307

Database: mini_ecommerce

Username: root

Password: (theo file .env hoặc mặc định: 120906)

👤 Tài khoản mẫu
Username	  Password	    Vai trò
admin	      admin123	    Quản trị viên
testuser	  123456	    Người dùng thường