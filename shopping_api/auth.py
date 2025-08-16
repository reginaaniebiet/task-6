from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import json, os

USERS_FILE = "users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Utilities ---
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Authentication ---
def authenticate_user(username: str, password: str):
    users = load_users()
    user = users.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return {"username": username, "role": user["role"]}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    users = load_users()
    user = users.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return {"username": token, "role": user["role"]}

# --- Role Check Dependencies ---
def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user

def require_customer(user: dict = Depends(get_current_user)):
    if user["role"] not in ["admin", "customer"]:
        raise HTTPException(status_code=403, detail="Customers only")
    return user
