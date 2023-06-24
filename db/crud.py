from sqlalchemy.orm import Session
from db.models.models import Movies
from db.schemas.schemas import MovieCreate

def get_all_movies(db: Session):
    return db.query(Movies).order_by(Movies.rating.desc()).all()


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Movies).filter(Movies.id == movie_id).first()


def get_movie_by_title(db: Session, movie_title: str):
    return db.query(Movies).filter(Movies.title == movie_title).first()


def create_movie_item(db: Session, movie: MovieCreate):
    db_movie = Movies(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_item(db: Session, movie_id: int):
    movie_to_delete = get_movie_by_id(db=db, movie_id=movie_id)
    db.delete(movie_to_delete)
    db.commit()