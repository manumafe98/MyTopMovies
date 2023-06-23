import os
import requests
from fastapi import Request, Form, APIRouter, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.models.models import Movies, Users
from db.schemas.schemas import MovieCreate, UserCreate

# $env:API_KEY = "38d089808acd67f9a32d59629a4578a8"
API_KEY = os.environ.get("API_KEY")
TBD_SEARCH_API = "https://api.themoviedb.org/3/search/movie"
TBD_GET_API = "https://api.themoviedb.org/3/movie/"
IMAGE_PATH = "https://image.tmdb.org/t/p/w500"


router = APIRouter()
templates = Jinja2Templates(directory="templates")


router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session, skip: int = 0):
    all_movies = db.query(Movies).offset(skip).order_by(Movies.rating.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "movies": all_movies})


router.get("/edit", response_class=HTMLResponse)
async def edit(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})


router.post("/edit", response_class=HTMLResponse)
async def edit_formt(request: Request):
    pass


router.get("/add", response_class=HTMLResponse)
async def add(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


router.post("/add", response_class=HTMLResponse)
async def add_form(request: Request):
    pass


router.get("/get_movie_data")
def get_movie_data(request: Request):
    movie_id = int(request.get("id"))
    pass

# TODO make the post enpoints work and the get_movie_data
# TODO once the main app is working add register and login
# TODO maybe convert the add from a button to a navbar item