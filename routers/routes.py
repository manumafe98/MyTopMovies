import os
import requests
from fastapi import APIRouter
from sqlalchemy.orm import Session
from db.models.models import Movies, Users
from db.schemas.schemas import MovieCreate, UserCreate

# $env:API_KEY = "38d089808acd67f9a32d59629a4578a8"
API_KEY = os.environ.get("API_KEY")
TBD_SEARCH_API = "https://api.themoviedb.org/3/search/movie"
TBD_GET_API = "https://api.themoviedb.org/3/movie/"
IMAGE_PATH = "https://image.tmdb.org/t/p/w500"

router = APIRouter()


router.get("/")
async def home():
    pass