from db.client import  Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship


class Movies(Base):
    """
    Model representing movies in the database.

    Attributes:
        id (int): The unique identifier for the movie.
        title (str): The title of the movie.
        year (int): The release year of the movie.
        description (str): The description or summary of the movie.
        rating (float): The rating of the movie.
        ranking (int): The ranking of the movie.
        review (str): A review or comment about the movie.
        img_url (str): The URL of the movie's image.
        owner_id (int): The ID of the user who owns the movie.
        owner (Users): The relationship to the owner user object.

    """
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    ranking = Column(Integer, nullable=False)
    review = Column(String, unique=True, nullable=False)
    img_url = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="movies")
    

class Users(Base):
    """
    Model representing users in the database.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        movies (List[Movies]): The list of movies owned by the user.

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    movies = relationship("Movies", back_populates="owner")
