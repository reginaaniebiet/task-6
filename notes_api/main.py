from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import json, os

from auth import authenticate_user, create_access_token, get_current_user, load_users, save_users, pwd_context

app = FastAPI()
NOTES_FILE = "notes.json"

# --- Helpers to load/save JSON ---
def load_json(file, default):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)
    with open(file, "r") as f:
        content = f.read().strip()
        if not content:
            return default
        return json.loads(content)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- User Registration ---
@app.post("/register/")
def register(username: str, password: str):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = pwd_context.hash(password)
    users[username] = {"password": hashed_pw}
    save_users(users)
    return {"message": f"User {username} registered successfully"}

# --- Login to get JWT ---
@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Notes Endpoints ---
@app.post("/notes/")
def add_note(title: str, content: str, user: dict = Depends(get_current_user)):
    notes = load_json(NOTES_FILE, {})
    notes.setdefault(user["username"], [])
    notes[user["username"]].append({
        "title": title,
        "content": content,
        "date": str(__import__("datetime").datetime.utcnow())
    })
    save_json(NOTES_FILE, notes)
    return {"message": "Note added successfully"}

@app.get("/notes/")
def view_notes(user: dict = Depends(get_current_user)):
    notes = load_json(NOTES_FILE, {})
    user_notes = notes.get(user["username"], [])
    return {"username": user["username"], "notes": user_notes}
