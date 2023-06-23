from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    year: int
    description: str
    rating: float
    ranking: int
    review: str
    img_url: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    # owner_id: int

    class Config:
        orm_mode = True


# class UserBase(BaseModel):
#     email: str
#     username: str

# class UserCreate(UserBase):
#     password: str

# class User(UserBase):
#     id: int
#     movies: list[Movie] = []

#     class Config:
#         orm_mode = True

# TODO uncomment the usermodel and use it after the movie tests