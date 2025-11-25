import requests

BASE_URL = "https://socialmediaapp-fwkn.onrender.com/api"

# Test Registration
register_data = {
    "username": "yvonne",
    "password": "StrongPassword123",
    "email": "yvonne@example.com"
}

response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
print("=== REGISTER ===")
print("Status code:", response.status_code)
print("Response text:", response.text, "\n")  # <--- use .text instead of .json()

# Test Login
login_data = {
    "username": "yvonne",
    "password": "StrongPassword123"
}

response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
print("=== LOGIN ===")
print("Status code:", response.status_code)
print("Response text:", response.text, "\n")
