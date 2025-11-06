# models/cart.py
from database.connection import DatabaseConnection

class CartModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_to_cart(self, user_id, product_id, quantity):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Kiểm tra sản phẩm đã có trong giỏ chưa
                cursor.execute(
                    "SELECT cart_id, quantity FROM cart WHERE user_id = %s AND product_id = %s",
                    (user_id, product_id)
                )
                existing_item = cursor.fetchone()
                
                if existing_item:
                    # Cập nhật số lượng
                    new_quantity = existing_item[1] + quantity
                    cursor.execute(
                        "UPDATE cart SET quantity = %s WHERE cart_id = %s",
                        (new_quantity, existing_item[0])
                    )
                else:
                    # Thêm mới
                    cursor.execute(
                        "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                        (user_id, product_id, quantity)
                    )
                
                conn.commit()
                return True, "Thêm vào giỏ hàng thành công"
            except Exception as e:
                return False, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, "❌ Lỗi kết nối database"
    
    def get_cart_items(self, user_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT c.cart_id, p.product_id, p.name, p.price, c.quantity, 
                           (p.price * c.quantity) as total_price,
                           p.image_url
                    FROM cart c
                    JOIN products p ON c.product_id = p.product_id
                    WHERE c.user_id = %s
                """, (user_id,))
                
                cart_items = cursor.fetchall()
                return cart_items
            except Exception as e:
                print(f"❌ Lỗi lấy giỏ hàng: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []
    
    def update_cart_item(self, user_id, cart_id, new_quantity):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                if new_quantity <= 0:
                    # Xóa item
                    cursor.execute("DELETE FROM cart WHERE cart_id = %s AND user_id = %s", 
                                 (cart_id, user_id))
                else:
                    # Cập nhật số lượng
                    cursor.execute("UPDATE cart SET quantity = %s WHERE cart_id = %s AND user_id = %s", 
                                 (new_quantity, cart_id, user_id))
                
                conn.commit()
                return True, "Cập nhật giỏ hàng thành công"
            except Exception as e:
                return False, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, "❌ Lỗi kết nối database"
    
    def clear_cart(self, user_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
                conn.commit()
                return True, "Đã xóa giỏ hàng"
            except Exception as e:
                return False, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, "❌ Lỗi kết nối database"
    
    def get_cart_total(self, user_id):
        cart_items = self.get_cart_items(user_id)
        total = sum(item['total_price'] for item in cart_items)
        return total