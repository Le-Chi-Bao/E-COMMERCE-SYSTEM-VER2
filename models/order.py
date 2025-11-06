# models/order.py
from database.connection import DatabaseConnection

class OrderModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_order(self, user_id, cart_items, total_amount):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Tạo đơn hàng
                cursor.execute(
                    "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, 'pending')",
                    (user_id, total_amount)
                )
                order_id = cursor.lastrowid
                
                # Thêm items vào order_items
                for item in cart_items:
                    cursor.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                        (order_id, item['product_id'], item['quantity'], item['price'])
                    )
                
                conn.commit()
                return True, order_id, "Tạo đơn hàng thành công"
            except Exception as e:
                return False, None, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, None, "❌ Lỗi kết nối database"
    
    def get_user_orders(self, user_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT o.*, 
                           (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) as item_count
                    FROM orders o 
                    WHERE o.user_id = %s 
                    ORDER BY o.created_at DESC
                """, (user_id,))
                
                orders = cursor.fetchall()
                return orders
            except Exception as e:
                print(f"❌ Lỗi lấy đơn hàng: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []
    
    def get_order_details(self, order_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT oi.*, p.name, p.image_url
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = %s
                """, (order_id,))
                
                order_items = cursor.fetchall()
                return order_items
            except Exception as e:
                print(f"❌ Lỗi lấy chi tiết đơn hàng: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []