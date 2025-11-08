# hash_password.py
import hashlib
import sys

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    password = input("Nhập password cần hash: ")

hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"Password: {password}")
print(f"Hash: {hashed}")