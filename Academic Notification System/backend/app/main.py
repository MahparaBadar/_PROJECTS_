from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_user, get_user, User  # Adjust import path as per your application structure

import secrets

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://localhost:8502",
    # Add more origins as needed for your frontend applications
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Generate a random secret key
SECRET_KEY = secrets.token_urlsafe(32)

# Configure your application with the secret key
app.secret_key = SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

class UserInDB(BaseModel):
    username: str

class User(BaseModel):
    username: str
    password: str

@app.post("/signup/")
async def signup(user: User):
    hashed_password = get_password_hash(user.password)
    create_user(user.username, hashed_password)
    return {"message": "User created successfully"}

@app.post("/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Notification feature
class Notification(BaseModel):
    title: str
    message: str
    recipient: str


@app.post("/notify/")
async def create_notification(notification: Notification):
    fake_notifications_db.append(notification)
    return {"message": "Notification created successfully"}


fake_notifications_db = []

@app.get("/notifications/", response_model=List[Notification])
async def get_notifications():
    return fake_notifications_db