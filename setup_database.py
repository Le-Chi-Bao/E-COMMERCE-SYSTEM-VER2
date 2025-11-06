# setup_database.py - Script tự động setup database
import mysql.connector
import os
from database.config import DatabaseConfig
from database.connection import DatabaseConnection

def setup_database():
    print("🚀 Bắt đầu thiết lập database...")
    
    config = DatabaseConfig()
    
    try:
        # Kết nối đến MySQL server (chưa chọn database)
        connection = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password
        )
        
        cursor = connection.cursor()
        
        # Đọc file SQL
        sql_file_path = os.path.join('database', 'init_database.sql')
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Chạy từng câu lệnh SQL
        statements = sql_script.split(';')
        
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
                print(f"✅ Đã thực thi: {statement.strip()[:50]}...")
        
        connection.commit()
        print("🎉 Thiết lập database thành công!")
        print("📊 Database: mini_ecommerce")
        print("📋 Tables: users, products, categories, cart, orders, order_items")
        print("👤 Tài khoản mẫu:")
        print("   - testuser / 123456")
        print("   - admin / admin123")
        
    except Exception as e:
        print(f"❌ Lỗi khi thiết lập database: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
    print("ket noi thanh cong")