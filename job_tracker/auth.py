from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import json, os

USERS_FILE = "users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Load/save users ---
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Authentication ---
def authenticate_user(username: str, password: str):
    users = load_users()
    user = users.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return {"username": username}

# --- Get current user dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    users = load_users()
    user = users.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return {"username": token}
