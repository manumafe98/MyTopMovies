from sqlalchemy.orm import Session
from db.models.models import Movies, Users
from db.schemas.schemas import MovieCreate, UserCreate

def get_all_movies(db: Session, user_id: int):
    """
    Retrieve all movies owned by a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        List[Movie]: A list of Movie objects.

    """
    return db.query(Movies).filter(Movies.owner_id == user_id).order_by(Movies.rating.desc()).all()


def get_movie_by_id(db: Session, movie_id: int, user_id: int):
    """
    Retrieve a movie by its ID for a specific user.

    Args:
        db (Session): The database session.
        movie_id (int): The ID of the movie.
        user_id (int): The ID of the user.

    Returns:
        Optional[Movie]: The Movie object if found, None otherwise.

    """
    return db.query(Movies).filter(Movies.owner_id == user_id, Movies.id == movie_id).first()


def get_movie_by_title(db: Session, movie_title: str, user_id: int):
    """
    Retrieve a movie by its title for a specific user.

    Args:
        db (Session): The database session.
        movie_title (str): The title of the movie.
        user_id (int): The ID of the user.

    Returns:
        Optional[Movie]: The Movie object if found, None otherwise.

    """
    return db.query(Movies).filter(Movies.owner_id == user_id, Movies.title == movie_title).first()


def create_movie_item(db: Session, movie: MovieCreate, user_id: int):
    """
    Create a new movie item for a user.

    Args:
        db (Session): The database session.
        movie (MovieCreate): The details of the movie to create.
        user_id (int): The ID of the user.

    Returns:
        Movie: The created Movie object.

    """
    db_movie = Movies(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_item(db: Session, movie_id: int, user_id: int):
    """
    Delete a movie item for a specific user.

    Args:
        db (Session): The database session.
        movie_id (int): The ID of the movie.
        user_id (int): The ID of the user.

    """
    movie_to_delete = get_movie_by_id(db=db, movie_id=movie_id, user_id=user_id)
    db.delete(movie_to_delete)
    db.commit()


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[User]: The User object if found, None otherwise.

    """
    return db.query(Users).filter(Users.username == username).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user.

    Args:
        db (Session): The database session.
        user (UserCreate): The details of the user to create.

    Returns:
        User: The created User object.

    """
    db_user = Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user