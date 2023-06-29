from pydantic import BaseModel, EmailStr

class MovieBase(BaseModel):
    """
    Schema representing the base movie data.

    Attributes:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        description (str): The description or summary of the movie.
        rating (float): The rating of the movie.
        ranking (int): The ranking of the movie.
        review (str): A review or comment about the movie.
        img_url (str): The URL of the movie's image.

    """
    title: str
    year: int
    description: str
    rating: float
    ranking: int
    review: str
    img_url: str

class MovieCreate(MovieBase):
    """
    Schema representing the data for creating a movie.

    Inherits:
        MovieBase

    """
    pass

class Movie(MovieBase):
    """
    Schema representing a movie with additional properties.

    Inherits:
        MovieBase

    Attributes:
        id (int): The unique identifier for the movie.
        owner_id (int): The ID of the user who owns the movie.

    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    Schema representing the base user data.

    Attributes:
        email (EmailStr): The email address of the user.
        username (str): The username of the user.

    """
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """
    Schema representing the data for creating a user.

    Inherits:
        UserBase

    Attributes:
        password (str): The password of the user.

    """
    password: str

class User(UserBase):
    """
    Schema representing a user with additional properties.

    Inherits:
        UserBase

    Attributes:
        id (int): The unique identifier for the user.
        movies (List[Movie]): The list of movies owned by the user.

    """
    id: int
    movies: list[Movie] = []

    class Config:
        orm_mode = True
