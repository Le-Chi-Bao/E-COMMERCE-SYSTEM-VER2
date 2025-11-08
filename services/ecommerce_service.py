# services/ecommerce_service.py
from models.user import UserModel
from models.product import ProductModel
from models.cart import CartModel
from models.order import OrderModel

class EcommerceService:
    def __init__(self):
        self.user_model = UserModel()
        self.product_model = ProductModel()
        self.cart_model = CartModel()
        self.order_model = OrderModel()
        self.current_user = None
    
    # ========== AUTHENTICATION ==========
    def register_user(self, username, email, password):
        success, message = self.user_model.register_user(username, email, password)
        return message
    
    def login_user(self, username, password):
        success, user_data, message = self.user_model.login_user(username, password)
        if success:
            self.current_user = user_data
        return message
    
    def logout_user(self):
        self.current_user = None
        return "✅ Đã đăng xuất"
    
    def get_current_user(self):
        return self.current_user
    
    # ========== PRODUCT MANAGEMENT ==========
    def get_products(self, category_filter="Tất cả"):
        return self.product_model.get_products(category_filter)  # ← ĐÃ SỬA THÀNH get_products
    
    def get_categories(self):
        return self.product_model.get_categories()
    
    def get_product_by_id(self, product_id):
        return self.product_model.get_product_by_id(product_id)
    
    # ========== CART MANAGEMENT ==========
    def add_to_cart(self, product_id, quantity):
        if not self.current_user:
            return "❌ Vui lòng đăng nhập để thêm vào giỏ hàng"
        
        if quantity <= 0:
            return "❌ Số lượng phải lớn hơn 0"
        
        # Kiểm tra sản phẩm tồn tại
        product = self.get_product_by_id(product_id)
        if not product:
            return "❌ Sản phẩm không tồn tại"
        
        success, message = self.cart_model.add_to_cart(
            self.current_user['user_id'], product_id, quantity
        )
        
        if success:
            return f"✅ Đã thêm {quantity} '{product['name']}' vào giỏ hàng"
        else:
            return message
    
    def get_cart_items(self):
        if not self.current_user:
            return []
        return self.cart_model.get_cart_items(self.current_user['user_id'])
    
    def update_cart_item(self, cart_id, new_quantity):
        if not self.current_user:
            return "❌ Vui lòng đăng nhập"
        
        success, message = self.cart_model.update_cart_item(
            self.current_user['user_id'], cart_id, new_quantity
        )
        
        if success:
            action = "Xóa" if new_quantity <= 0 else "Cập nhật"
            return f"✅ {action} giỏ hàng thành công"
        else:
            return message
    
    def get_cart_total(self):
        if not self.current_user:
            return 0
        return self.cart_model.get_cart_total(self.current_user['user_id'])
    
    def clear_cart(self):
        if not self.current_user:
            return "❌ Vui lòng đăng nhập"
        
        success, message = self.cart_model.clear_cart(self.current_user['user_id'])
        if success:
            return "✅ Đã xóa tất cả sản phẩm trong giỏ hàng"
        else:
            return message
    
    # ========== ORDER MANAGEMENT ==========
    def checkout(self):
        if not self.current_user:
            return "❌ Vui lòng đăng nhập"
        
        cart_items = self.get_cart_items()
        if not cart_items:
            return "❌ Giỏ hàng trống"
        
        total_amount = self.get_cart_total()
        success, order_id, message = self.order_model.create_order(
            self.current_user['user_id'], cart_items, total_amount
        )
        
        if success:
            # Xóa giỏ hàng sau khi tạo đơn hàng thành công
            self.cart_model.clear_cart(self.current_user['user_id'])
            return f"✅ Đặt hàng thành công! Mã đơn: #{order_id}, Tổng: {total_amount:,.0f}₫"
        else:
            return message
    
    def get_user_orders(self):
        if not self.current_user:
            return []
        return self.order_model.get_user_orders(self.current_user['user_id'])
    
    # ========== ADMIN MANAGEMENT ==========
    def get_all_users(self):
        if not self.current_user or self.current_user['username'] not in ['admin', 'admin2']:
            return []
        return self.user_model.get_all_users()
    
    def get_all_products(self):
        if not self.current_user or self.current_user['username'] not in ['admin', 'admin2']:
            return []
        return self.product_model.get_all_products_admin()  # ← ĐÃ SỬA THÀNH get_all_products_admin
    
    def get_all_orders(self):
        if not self.current_user or self.current_user['username'] not in ['admin', 'admin2']:
            return []
        return self.order_model.get_all_orders()
    
    def get_sales_analytics(self):
        if not self.current_user or self.current_user['username'] not in ['admin', 'admin2']:
            return {}
        return self.order_model.get_sales_report()

# Khởi tạo service
ecommerce = EcommerceService()