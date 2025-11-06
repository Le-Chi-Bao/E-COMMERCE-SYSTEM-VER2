# test_config.py
from database.config import DatabaseConfig

config = DatabaseConfig()
print("Config object:", config)
print("Config dict:", config.get_config())