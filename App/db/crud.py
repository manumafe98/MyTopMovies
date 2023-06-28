from sqlalchemy.orm import Session
from db.models.models import Movies, Users
from db.schemas.schemas import MovieCreate, UserCreate

def get_all_movies(db: Session, user_id: int):
    return db.query(Movies).filter(Movies.owner_id == user_id).order_by(Movies.rating.desc()).all()


def get_movie_by_id(db: Session, movie_id: int, user_id: int):
    return db.query(Movies).filter(Movies.owner_id == user_id, Movies.id == movie_id).first()


def get_movie_by_title(db: Session, movie_title: str, user_id: int):
    return db.query(Movies).filter(Movies.owner_id == user_id, Movies.title == movie_title).first()


def create_movie_item(db: Session, movie: MovieCreate, user_id: int):
    db_movie = Movies(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_item(db: Session, movie_id: int, user_id: int):
    movie_to_delete = get_movie_by_id(db=db, movie_id=movie_id, user_id=user_id)
    db.delete(movie_to_delete)
    db.commit()


def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()


def create_user(db: Session, user: UserCreate):
    db_user = Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user