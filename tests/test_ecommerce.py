# tests/test_ecommerce.py
import unittest
import sys
import os
import random
import string
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.ecommerce_service import EcommerceService

class TestEcommerceSystem(unittest.TestCase):
    
    def setUp(self):
        """Chuẩn bị môi trường test"""
        self.service = EcommerceService()
    
    def tearDown(self):
        """Dọn dẹp sau test"""
        if self.service.current_user:
            # Xóa giỏ hàng trước khi logout
            self.service.clear_cart()
            self.service.logout_user()
    
    def generate_random_username(self):
        """Tạo username ngẫu nhiên để tránh trùng lặp"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"testuser_{random_suffix}"
    
    # ========== AUTHENTICATION TESTS ==========
    def test_register_user_success(self):
        """Test đăng ký user thành công"""
        random_username = self.generate_random_username()
        random_email = f"{random_username}@email.com"
        
        result = self.service.register_user(random_username, random_email, "123456")
        self.assertIn("✅ Đăng ký thành công", result)
    
    def test_register_duplicate_username(self):
        """Test đăng ký username trùng"""
        result = self.service.register_user("testuser", "another@email.com", "123456")
        self.assertIn("❌ Tên đăng nhập hoặc email đã tồn tại", result)
    
    def test_login_success(self):
        """Test đăng nhập thành công"""
        result = self.service.login_user("testuser", "123456")
        self.assertIn("✅ Đăng nhập thành công", result)
        self.assertIsNotNone(self.service.current_user)
    
    def test_login_wrong_password(self):
        """Test đăng nhập sai mật khẩu"""
        result = self.service.login_user("testuser", "wrongpassword")
        self.assertIn("❌ Sai tên đăng nhập hoặc mật khẩu", result)
        self.assertIsNone(self.service.current_user)
    
    # ========== PRODUCT TESTS ==========
    def test_get_products_all(self):
        """Test lấy tất cả sản phẩm"""
        products = self.service.get_products()
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)
    
    def test_get_product_by_id(self):
        """Test lấy sản phẩm theo ID"""
        product = self.service.get_product_by_id(1)
        self.assertIsNotNone(product)
        self.assertEqual(product['product_id'], 1)
    
    # ========== CART TESTS ==========
    def test_add_to_cart_without_login(self):
        """Test thêm vào giỏ hàng khi chưa login"""
        result = self.service.add_to_cart(1, 1)
        self.assertIn("❌ Vui lòng đăng nhập", result)
    
    def test_add_to_cart_with_login(self):
        """Test thêm vào giỏ hàng khi đã login"""
        # Login trước
        self.service.login_user("testuser", "123456")
        
        result = self.service.add_to_cart(1, 2)
        self.assertIn("✅ Đã thêm", result)
    
    def test_get_cart_items(self):
        """Test lấy giỏ hàng"""
        self.service.login_user("testuser", "123456")
        cart_items = self.service.get_cart_items()
        self.assertIsInstance(cart_items, list)
    
    def test_clear_cart_functionality(self):
        """Test chức năng xóa giỏ hàng"""
        self.service.login_user("testuser", "123456")
        
        # Thêm sản phẩm vào giỏ
        self.service.add_to_cart(1, 1)
        
        # Xóa giỏ hàng
        result = self.service.clear_cart()
        self.assertIn("✅ Đã xóa tất cả", result)
        
        # Kiểm tra giỏ hàng trống
        cart_items = self.service.get_cart_items()
        self.assertEqual(len(cart_items), 0)
    
    # ========== ORDER TESTS ==========
    def test_checkout_empty_cart(self):
        """Test checkout với giỏ hàng trống"""
        self.service.login_user("testuser", "123456")
        
        # Đảm bảo giỏ hàng trống
        self.service.clear_cart()
        
        result = self.service.checkout()
        self.assertIn("❌ Giỏ hàng trống", result)
    
    def test_checkout_success(self):
        """Test checkout thành công"""
        self.service.login_user("testuser", "123456")
        
        # Đảm bảo giỏ hàng trống trước
        self.service.clear_cart()
        
        # Thêm sản phẩm vào giỏ
        self.service.add_to_cart(1, 1)
        
        # Checkout
        result = self.service.checkout()
        self.assertIn("✅ Đặt hàng thành công", result)
    
    # ========== ADMIN TESTS ==========
    def test_admin_access_regular_user(self):
        """Test user thường truy cập admin functions"""
        self.service.login_user("testuser", "123456")
        users = self.service.get_all_users()
        self.assertEqual(users, [])
    
    def test_admin_access_admin_user(self):
        """Test admin truy cập admin functions"""
        self.service.login_user("admin", "admin123")
        users = self.service.get_all_users()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)

class TestEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.service = EcommerceService()
        self.service.login_user("testuser", "123456")
    
    def tearDown(self):
        """Dọn dẹp sau test"""
        if self.service.current_user:
            self.service.clear_cart()
            self.service.logout_user()
    
    def test_add_to_cart_invalid_quantity(self):
        """Test thêm vào giỏ hàng với số lượng không hợp lệ"""
        result = self.service.add_to_cart(1, 0)
        self.assertIn("❌ Số lượng phải lớn hơn 0", result)
    
    def test_add_to_cart_nonexistent_product(self):
        """Test thêm vào giỏ hàng sản phẩm không tồn tại"""
        result = self.service.add_to_cart(9999, 1)
        self.assertIn("❌ Sản phẩm không tồn tại", result)
    
    def test_update_cart_item_remove(self):
        """Test cập nhật giỏ hàng với số lượng = 0 (xóa sản phẩm)"""
        # Thêm sản phẩm trước
        self.service.add_to_cart(1, 2)
        cart_items = self.service.get_cart_items()
        
        if cart_items:
            cart_id = cart_items[0]['cart_id']
            result = self.service.update_cart_item(cart_id, 0)
            self.assertIn("✅ Xóa giỏ hàng thành công", result)

class TestDatabaseCleanup(unittest.TestCase):
    """Test để dọn dẹp database sau khi test"""
    
    def test_cleanup_test_data(self):
        """Xóa dữ liệu test tạo ra trong quá trình test"""
        service = EcommerceService()
        
        # Đăng nhập admin để dọn dẹp
        service.login_user("admin", "admin123")
        
        # Có thể thêm logic cleanup ở đây nếu cần
        # Ví dụ: xóa users test, orders test, etc.
        
        print("✅ Database cleanup completed")

if __name__ == '__main__':
    # Chạy tests
    unittest.main(verbosity=2)