# database/config.py
class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'  # THAY ĐỔI THEO MYSQL CỦA BẠN
        self.password = '120906'  # THAY ĐỔI THEO MYSQL CỦA BẠN
        self.database = 'mini_ecommerce'
    
    def get_config(self):
        return {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database
        }