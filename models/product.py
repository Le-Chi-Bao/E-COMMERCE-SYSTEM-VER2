# models/product.py
from database.connection import DatabaseConnection

class ProductModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_products(self, category_filter="Tất cả"):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                
                if category_filter != "Tất cả":
                    cursor.execute("""
                        SELECT p.*, c.category_name 
                        FROM products p 
                        JOIN categories c ON p.category_id = c.category_id 
                        WHERE c.category_name = %s
                    """, (category_filter,))
                else:
                    cursor.execute("""
                        SELECT p.*, c.category_name 
                        FROM products p 
                        JOIN categories c ON p.category_id = c.category_id
                    """)
                
                products = cursor.fetchall()
                return products
            except Exception as e:
                print(f"❌ Lỗi lấy sản phẩm: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []
    
    def get_product_by_id(self, product_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
                return product
            except Exception as e:
                print(f"❌ Lỗi lấy sản phẩm: {e}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None
    
    def get_categories(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT category_name FROM categories")
                categories = [row[0] for row in cursor.fetchall()]
                return ["Tất cả"] + categories
            except Exception as e:
                print(f"❌ Lỗi lấy danh mục: {e}")
                return ["Tất cả", "Điện thoại", "Laptop", "Phụ kiện"]
            finally:
                cursor.close()
                conn.close()
        return ["Tất cả", "Điện thoại", "Laptop", "Phụ kiện"]
    
    def update_stock(self, product_id, quantity):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (quantity, product_id)
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"❌ Lỗi cập nhật tồn kho: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        return False