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
    
    # ========== ADMIN METHODS ==========
    def get_all_orders(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT o.*, u.username, 
                           (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) as item_count
                    FROM orders o 
                    JOIN users u ON o.user_id = u.user_id
                    ORDER BY o.created_at DESC
                """)
                
                orders = cursor.fetchall()
                return orders
            except Exception as e:
                print(f"❌ Lỗi lấy tất cả đơn hàng: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []
    
    def get_sales_report(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                
                # Tổng doanh thu
                cursor.execute("SELECT SUM(total_amount) as total_revenue FROM orders WHERE status != 'cancelled'")
                total_revenue = cursor.fetchone()['total_revenue'] or 0
                
                # Tổng số đơn hàng
                cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
                total_orders = cursor.fetchone()['total_orders']
                
                # Số lượng user
                cursor.execute("SELECT COUNT(*) as total_users FROM users")
                total_users = cursor.fetchone()['total_users']
                
                # Đơn hàng theo trạng thái
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM orders 
                    GROUP BY status
                """)
                orders_by_status = cursor.fetchall()
                
                # Top sản phẩm bán chạy
                cursor.execute("""
                    SELECT p.name, SUM(oi.quantity) as total_sold
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    GROUP BY p.product_id, p.name
                    ORDER BY total_sold DESC
                    LIMIT 5
                """)
                top_products = cursor.fetchall()
                
                report = {
                    'total_revenue': float(total_revenue),
                    'total_orders': total_orders,
                    'total_users': total_users,
                    'orders_by_status': orders_by_status,
                    'top_products': top_products,
                    'average_order_value': float(total_revenue / total_orders) if total_orders > 0 else 0
                }
                
                return report
            except Exception as e:
                print(f"❌ Lỗi tạo báo cáo: {e}")
                return {}
            finally:
                cursor.close()
                conn.close()
        return {}