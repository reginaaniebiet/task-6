from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import json, os

from auth import authenticate_user, get_current_user, require_admin, require_customer, save_users, load_users, pwd_context

app = FastAPI()

PRODUCTS_FILE = "products.json"
CART_FILE = "cart.json"

# --- File Helpers ---
def load_json(file, default):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- User Registration ---
@app.post("/register/")
def register(username: str, password: str, role: str = "customer"):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = pwd_context.hash(password)
    users[username] = {"password": hashed_pw, "role": role}
    save_users(users)
    return {"message": f"User {username} registered as {role}"}

# --- Login ---
@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": form_data["username"], "token_type": "bearer"}

# --- Products Endpoints ---
@app.post("/admin/add_product/")
def add_product(name: str, price: float, user=Depends(require_admin)):
    products = load_json(PRODUCTS_FILE, [])
    products.append({"name": name, "price": price})
    save_json(PRODUCTS_FILE, products)
    return {"message": f"Product {name} added"}

@app.get("/products/")
def get_products():
    return load_json(PRODUCTS_FILE, [])

# --- Cart Endpoints ---
@app.post("/cart/add/")
def add_to_cart(product_name: str, user=Depends(require_customer)):
    products = load_json(PRODUCTS_FILE, [])
    if not any(p["name"] == product_name for p in products):
        raise HTTPException(status_code=404, detail="Product not found")
    
    cart = load_json(CART_FILE, {})
    cart.setdefault(user["username"], [])
    cart[user["username"]].append(product_name)
    save_json(CART_FILE, cart)
    return {"message": f"{product_name} added to cart"}

@app.get("/cart/")
def view_cart(user=Depends(require_customer)):
    cart = load_json(CART_FILE, {})
    return {"username": user["username"], "cart": cart.get(user["username"], [])}
