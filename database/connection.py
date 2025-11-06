# database/connection.py
import mysql.connector
from .config import DatabaseConfig

class DatabaseConnection:
    def __init__(self):
        self.config = DatabaseConfig()
    
    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config.get_config())
            return connection
        except Exception as e:
            print(f"❌ Lỗi kết nối MySQL: {e}")
            return None
    
    def test_connection(self):
        conn = self.get_connection()
        if conn:
            conn.close()
            return True
        return False