# database/config.py
import os

class DatabaseConfig:
    def __init__(self):
        # Sử dụng biến môi trường, fallback về giá trị mặc định
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '120906')
        self.database = os.getenv('DB_NAME', 'mini_ecommerce')
    
    def get_config(self):
        return {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database
        }