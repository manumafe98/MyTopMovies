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
from exceptions import NotAuthenticatedException


SECRET_KEY = os.environ.get("SECRET_KEY")
API_KEY = os.environ.get("API_KEY")
TBD_SEARCH_API = "https://api.themoviedb.org/3/search/movie"
TBD_GET_API = "https://api.themoviedb.org/3/movie/"
IMAGE_PATH = "https://image.tmdb.org/t/p/w500"


router = APIRouter()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET_KEY, "/user/signin", use_cookie=True, custom_exception=NotAuthenticatedException)


def get_db():
    """
    Function to ensure the application is connected to the database.

    Yields:
        db: sqlalchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    """
    Checks the user password with the hashed password in the database.

    Args:
        plain_password (str): User password
        hashed_password (str): User hashed password in db

    Returns:
        bool: Returns true if the password matches with the one in the db and false if not
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hashes the user password with passlib.

    Args:
        password (str): user inputed password

    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)


@manager.user_loader()
def load_user(username: str, db: Session = next(get_db())):
    """
    Search for the user in the database and its used to make sure the user is authenticated,
    before it can acces some endpoints.

    Args:
        username (str): User's username
        db (Session): The database session

    Returns:
        user: returns a user object
    """
    return get_user_by_username(db=db, username=username)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user = Depends(manager), db: Session = Depends(get_db)):
    """
    Renders the home page.

    Args:
        request (Request): The incoming HTTP request object
        user: Current logged user
        db (Session): The database session

    Returns:
        - TemplateResponse: The response containing the rendered "index.html" template with the movies data.
    """
    all_movies = get_all_movies(db=db, user_id=user.id)
    for movie in all_movies:
        ranking = all_movies.index(movie) + 1
        movie_to_edit = get_movie_by_title(db=db, movie_title=movie.title, user_id=user.id)
        movie_to_edit.ranking = ranking
        db.commit()
    return templates.TemplateResponse("index.html", {"request": request, "movies": all_movies, "logged": True})


@router.get("/edit/{movie_id}", response_class=HTMLResponse)
async def edit(movie_id: int, request: Request, user = Depends(manager)):
    """
    Renders the edit page.

    Args:
        movie_id (int): The id of the movie to edit
        request (Request): The incoming HTTP request object
        user : current logged user

    Returns:
        - TemplateResponse: The response containing the rendered "edit.html" template.
    """
    return templates.TemplateResponse("edit.html", {"request": request})


@router.post("/edit/{movie_id}", response_class=HTMLResponse)
async def edit_form(movie_id: int, request: Request, db: Session = Depends(get_db),
                    rating: float = Form(...), review: str = Form(...), user = Depends(manager)):
    """
    Handles the form submission in the edit page.

    Args:
        movie_id (int): The id of the movie to edit
        request (Request): The incoming HTTP request object
        db (Session): The database session
        rating (float): The rating submitted in the form
        review (str): The review submitted in the form
        user: Current logged user

    Returns:
        - RedirectResponse: A redirect response to the home page.
    """
    movie_to_update = get_movie_by_id(db=db, movie_id=movie_id, user_id=user.id)
    movie_to_update.rating = rating
    movie_to_update.review = review
    db.commit()
    return RedirectResponse(router.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/add", response_class=HTMLResponse)
async def add(request: Request, user = Depends(manager)):
    """
    Renders the add page.

    Args:
        request (Request): The incoming HTTP request object
        user: Current user logged

    Returns:
        TemplateResponse: The response containing the rendered "add.html" template.
    """
    return templates.TemplateResponse("add.html", {"request": request, "logged": True})
    

@router.post("/add", response_class=HTMLResponse)
async def add_form(request: Request, movie_title: str = Form(...), user = Depends(manager)):
    """
    Handles the form submission in the add page.

    Args:
        request (Request): The incoming HTTP request object
        movie_title (str): The movie title submitted in the form
        user : Current user logged

    Returns:
        TemplateResponse: The response containing the rendered "select.html" template with the matched movie data.
    """
    response = requests.get(TBD_SEARCH_API, params={"api_key": API_KEY, "query": movie_title})
    output = response.json()
    data = output["results"]
    return templates.TemplateResponse("select.html", {"request": request, "matched_movies": data, "logged": True})


@router.get("/delete/{movie_id}", response_class=HTMLResponse)
async def delete(movie_id: int, db: Session = Depends(get_db), user = Depends(manager)):
    """
    Deletes the movie selected by te user.

    Args:
        movie_id (int): The id of the movie to delete
        db (Session): The database session
        user: Current logged user

    Returns:
        RedirectResponse: A redirect response to the home page.
    """
    delete_movie_item(db=db, movie_id=movie_id, user_id=user.id)
    return RedirectResponse(router.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/get_movie_data/{movie_id}", response_class=HTMLResponse)
async def get_movie_data(movie_id: int, request: Request, db: Session = Depends(get_db), user = Depends(manager)):
    """
    Gets all the information of the movie and adds it to the database.

    Args:
        movie_id (int): The movie id
        request (Request): The incoming HTTP request object
        db (Session): The database session
        user: Current user logged

    Returns:
        RedirectResponse: A redirect response to the edit page.
    """
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
    create_movie_item(db=db, movie=new_record, user_id=user.id)
    get_movie = get_movie_by_title(db=db, movie_title=output["original_title"], user_id=user.id)
    get_id = get_movie.id
    return RedirectResponse(router.url_path_for("edit_form", movie_id=get_id), 
                            status_code=status.HTTP_303_SEE_OTHER)


@router.get("/user/signup", response_class=HTMLResponse)
async def register(request: Request):
    """
    Renders the signup page.

    Args:
        request (Request): The incoming HTTP request object

    Returns:
        TemplateResponse: The response containing the rendered "register.html" template.
    """
    return templates.TemplateResponse("register.html", {"request": request, "exists": True})


@router.post("/user/signup", response_class=HTMLResponse)
async def register_form(request: Request, db: Session = Depends(get_db),  
                        username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """
    Handles the form submission in the signup page.

    Args:
        request (Request): The incoming HTTP request object
        db (Session): The database session
        username (str): The username submitted in the form
        email (str): The email submitted in the form
        password (str): The password submitted in the form

    Returns:
        TemplateResponse: To the login if the user already exists
        RedirectResponse: A redirect response to the login page
    """
    db_user = get_user_by_username(db=db, username=username)
    if db_user:
        return templates.TemplateResponse("login.html", {"request": request, "exists": True})

    new_user = UserCreate(username=username, email=email, password=get_password_hash(password))
    success = create_user(db=db, user=new_user)

    if success:
        return RedirectResponse(router.url_path_for("login"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/user/signin", response_class=HTMLResponse)
async def login(request: Request):
    """
    Renders the signin page.

    Args:
        request (Request): The incoming HTTP request object

    Returns:
        TemplateResponse: The response containing the rendered "login.html" template.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/user/signin", response_class=HTMLResponse)
async def login_form(request: Request, db: Session = Depends(get_db), data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles the form submission in the signin page.

    Args:
        request (Request):  The incoming HTTP request object
        db (Session): The database session
        data (OAuth2PasswordRequestForm): The Oauth2 authentication form

    Returns:
        RedirectResponse: If the login is succesfull redirects the user to the home page.
        TemplateResponse: If the user password is incorrect returns the "login.html" rendered template with an error.
        TemplateResponse: If the user don't exist returns the "register.html" rendered template with an error.
    """
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


@router.get("/logout")
async def logout(user = Depends(manager)):
    """
    Logs out the current user.

    Args:
        user: User to be logged out

    Returns:
        RedirectResponse: A redirect response to the login page.
    """
    response = RedirectResponse(router.url_path_for("login"), status_code= status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access-token")
    return response


@router.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    """
    Renders the forgot password page.

    Args:
        request (Request): The incoming HTTP request object

    Returns:
        TemplateResponse: The response containing the rendered "forgot_password.html" template.
    """
    return templates.TemplateResponse("forgot_password.html", {"request": request, "old_password": True})


@router.post("/forgot_password", response_class=HTMLResponse)
async def forgot_password_form(request: Request, db: Session = Depends(get_db),
                               username: str = Form(...), old_password: str = Form(...),
                               new_password: str = Form(...), confirm_password: str = Form(...)):
    """
    Handles the form submission in the forgot password page.

    Args:
        request (Request): The incoming HTTP request object
        db (Session): The database session
        username (str): The username submitted in the form
        old_password (str):The old_password submitted in the form
        new_password (str): The new_password submitted in the form
        confirm_password (str): The confirm_password submitted in the form

    Returns:
        RedirectResponse: Redirects to the login page if the password change was succesfull
        TemplateResponse: If the old password doesn't match the one in the db renders the forgot_password with an error
        TemplateResponse: If the new password doesn't match the confirmation renders the forgot_password with an error
    """
    user = get_user_by_username(db=db, username=username)
    if verify_password(old_password, user.password):
        if new_password == confirm_password:
            new_pass = get_password_hash(new_password)
            user.password = new_pass
            db.commit()
            return RedirectResponse(router.url_path_for("login"), status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("forgot_password.html", {"request": request,
                                                                       "old_password": True, 
                                                                       "passwords_not_match": True})

    return templates.TemplateResponse("forgot_password.html", {"request": request, "old_password": False})


# TODO add password requirements
# TODO improve the whole app visually
