import requests
from fastapi import FastAPI, Depends, HTTPException
from backend.settings import settings
import google.generativeai as genai  # Import the generativeai module
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the User model
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

# Define the FavoriteCuisine model
class FavoriteCuisine(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    cuisine: str

# Define Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CuisineCreate(BaseModel):
    cuisine: str

# Create the database engine
connection_string = str(settings.DATABASE_URL)
engine = create_engine(connection_string)

# Create the FastAPI app
app = FastAPI()

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Utility functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Define route for user signup
@app.post("/signup/")
def signup(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    with Session(engine) as session:
        db_user = User(username=user.username, hashed_password=hashed_password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return {"message": "User created successfully"}

# Define route for token generation (login)
@app.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.debug(f"Login attempt for username: {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.error("Invalid credentials")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    logger.debug("Login successful")
    return {"access_token": user.username, "token_type": "bearer"}

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

# Define route to add favorite cuisine
@app.post("/favorite_cuisine/")
def add_favorite_cuisine(cuisine: CuisineCreate, current_user: User = Depends(get_current_user)):
    logger.info(f"Adding favorite cuisine: {cuisine.cuisine} for user: {current_user.username}")
    with Session(engine) as session:
        favorite = FavoriteCuisine(user_id=current_user.id, cuisine=cuisine.cuisine)
        session.add(favorite)
        session.commit()
        session.refresh(favorite)
        return favorite

# Define route to get recipe (using Google Custom Search JSON API)
@app.get("/recipe/")
def get_recipe(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        favorite = session.exec(select(FavoriteCuisine).where(FavoriteCuisine.user_id == current_user.id)).first()
        if not favorite:
            raise HTTPException(status_code=404, detail="No favorite cuisine found")

        logger.info(f"Favorite cuisine found: {favorite.cuisine} for user: {current_user.username}")

        # Integrate Google Custom Search JSON API to get recipe
        api_key = settings.GOOGLE_API_KEY
        search_engine_id = settings.SEARCH_ENGINE_ID
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": favorite.cuisine + " recipe",
        }

        logger.info(f"Requesting recipe with URL: {url} and params: {params}")

        response = requests.get(url, params=params)

        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching recipe from API")

        recipe = response.json()

        # Format the recipe details as Markdown
        markdown_response = ""
        for item in recipe.get("items", []):
            title = item.get("title", "No title")
            link = item.get("link", "#")
            snippet = item.get("snippet", "No snippet")
            markdown_response += f"## [{title}]({link})\n"
            markdown_response += f"{snippet}\n\n"

        return {"cuisine": favorite.cuisine, "recipe": markdown_response}

# Define route to generate content using GenerativeAI
@app.get("/generate_content/")
def generate_content(prompt: str):
    response = model.generate_content(prompt)
    return response.text

# Initialize the database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

