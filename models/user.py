# models/user.py
import hashlib
from database.connection import DatabaseConnection

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                hashed_password = self.hash_password(password)
                
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password)
                )
                conn.commit()
                return True, "✅ Đăng ký thành công! Hãy đăng nhập."
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    return False, "❌ Tên đăng nhập hoặc email đã tồn tại"
                return False, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, "❌ Lỗi kết nối database"
    
    def login_user(self, username, password):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                hashed_password = self.hash_password(password)
                
                cursor.execute(
                    "SELECT user_id, username, email FROM users WHERE username = %s AND password = %s",
                    (username, hashed_password)
                )
                user = cursor.fetchone()
                
                if user:
                    user_data = {
                        'user_id': user[0],
                        'username': user[1],
                        'email': user[2]
                    }
                    return True, user_data, f"✅ Đăng nhập thành công! Chào mừng {user[1]}"
                else:
                    return False, None, "❌ Sai tên đăng nhập hoặc mật khẩu"
            except mysql.connector.Error as e:
                return False, None, f"❌ Lỗi: {e}"
            finally:
                cursor.close()
                conn.close()
        return False, None, "❌ Lỗi kết nối database"
    
    def get_user_by_id(self, user_id):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT user_id, username, email FROM users WHERE user_id = %s",
                    (user_id,)
                )
                user = cursor.fetchone()
                return user
            except Exception as e:
                print(f"❌ Lỗi lấy thông tin user: {e}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None