from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import json, os

from auth import authenticate_user, get_current_user, save_users, load_users, pwd_context

app = FastAPI()
APPLICATIONS_FILE = "applications.json"

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

# --- Login ---
@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": form_data.username, "token_type": "bearer"}

# --- Applications ---
@app.post("/applications/")
def add_application(job_title: str, company: str, date_applied: str, status: str, user: dict = Depends(get_current_user)):
    applications = load_json(APPLICATIONS_FILE, {})
    applications.setdefault(user["username"], [])
    applications[user["username"]].append({
        "job_title": job_title,
        "company": company,
        "date_applied": date_applied,
        "status": status
    })
    save_json(APPLICATIONS_FILE, applications)
    return {"message": "Job application added successfully"}

@app.get("/applications/")
def view_applications(user: dict = Depends(get_current_user)):
    applications = load_json(APPLICATIONS_FILE, {})
    user_apps = applications.get(user["username"], [])
    return {"username": user["username"], "applications": user_apps}
