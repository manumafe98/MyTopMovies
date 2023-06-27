import os
import requests
from fastapi import Request, Form, APIRouter, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.schemas.schemas import MovieCreate, UserCreate, User
from sqlalchemy.orm import Session
from db.client import engine, Base, SessionLocal
from db.crud import get_all_movies, get_movie_by_title, delete_movie_item, get_movie_by_id, create_movie_item
from db.crud import create_user, get_user_by_username
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from passlib.context import CryptContext

# API_KEY = "38d089808acd67f9a32d59629a4578a8"
SECRET_KEY = "217e937592f0ea3c1975629980430a541c3c690b6c55fd8beff9a49bec86d16f"
API_KEY = os.environ.get("API_KEY")
TBD_SEARCH_API = "https://api.themoviedb.org/3/search/movie"
TBD_GET_API = "https://api.themoviedb.org/3/movie/"
IMAGE_PATH = "https://image.tmdb.org/t/p/w500"

router = APIRouter()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET_KEY, "/user/signin", use_cookie=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@manager.user_loader()
def load_user(username: str, db: Session = next(get_db())):
    return get_user_by_username(db=db, username=username)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user = Depends(manager), db: Session = Depends(get_db)):
    all_movies = get_all_movies(db=db)
    for movie in all_movies:
        ranking = all_movies.index(movie) + 1
        movie_to_edit = get_movie_by_title(db=db, movie_title=movie.title)
        movie_to_edit.ranking = ranking
        db.commit()
    return templates.TemplateResponse("index.html", {"request": request, "movies": all_movies})


@router.get("/edit/{movie_id}", response_class=HTMLResponse)
async def edit(movie_id: int, request: Request, user = Depends(manager)):
    return templates.TemplateResponse("edit.html", {"request": request})


@router.post("/edit/{movie_id}", response_class=HTMLResponse)
async def edit_form(movie_id: int, request: Request, db: Session = Depends(get_db),
                    rating: float = Form(...), review: str = Form(...)):
    movie_to_update = get_movie_by_id(db=db, movie_id=movie_id)
    movie_to_update.rating = rating
    movie_to_update.review = review
    db.commit()
    return RedirectResponse(router.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/add", response_class=HTMLResponse)
async def add(request: Request, user = Depends(manager)):
    return templates.TemplateResponse("add.html", {"request": request})
    

@router.post("/add", response_class=HTMLResponse)
async def add_form(request: Request, movie_title: str = Form(...)):
    response = requests.get(TBD_SEARCH_API, params={"api_key": API_KEY, "query": movie_title})
    output = response.json()
    data = output["results"]
    return templates.TemplateResponse("select.html", {"request": request, "matched_movies": data})


@router.get("/delete/{movie_id}", response_class=HTMLResponse)
async def delete(movie_id: int, db: Session = Depends(get_db), user = Depends(manager)):
    delete_movie_item(db=db, movie_id=movie_id)
    return RedirectResponse(router.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/get_movie_data/{movie_id}", response_class=HTMLResponse)
def get_movie_data(movie_id: int, request: Request, db: Session = Depends(get_db), user = Depends(manager)):
    movie_api_url = f"{TBD_GET_API}/{movie_id}"
    response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
    output = response.json()
    new_record = MovieCreate(title=output["original_title"],
                             description=output["overview"],
                             year=output["release_date"].split("-")[0],
                             img_url=f"{IMAGE_PATH}{output['poster_path']}",
                             rating=1.0,
                             ranking=1,
                             review=" ")
    create_movie_item(db=db, movie=new_record)
    get_movie = get_movie_by_title(db=db, movie_title=output["original_title"])
    get_id = get_movie.id
    return RedirectResponse(router.url_path_for("edit_form", movie_id=get_id), 
                            status_code=status.HTTP_303_SEE_OTHER)


@router.get("/user/signup", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/user/signup", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db),  
                  username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    db_user = get_user_by_username(db=db, username=username)
    if db_user:
        return templates.TemplateResponse("register.html", {"request": request, "exists": True})

    new_user = UserCreate(username=username, email=email, password=get_password_hash(password))
    success = create_user(db=db, user=new_user)

    if success:
        return RedirectResponse(router.url_path_for("login"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/user/signin", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/user/signin", response_class=HTMLResponse)
def login_form(request: Request, db: Session = Depends(get_db), data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(db=db, username=data.username)
    if user:
        is_password_correct = verify_password(data.password, user.password)
        if is_password_correct:
            token = manager.create_access_token(data={'sub': data.username})
            response = RedirectResponse(router.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
            manager.set_cookie(response, token)
            return response
        
        else:
            return templates.TemplateResponse("login.html", {"request": request, "bad_password": True})
    
    return templates.TemplateResponse("register.html", {"request": request, "exists": False})

# TODO make the database relational now that the login works
# TODO add some error messages to the login/register forms
# TODO dockerize the app
# TODO maybe improve the forms visualization (thats not a primary goal right now)