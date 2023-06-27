from db.client import  Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship


class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    ranking = Column(Integer, nullable=False)
    review = Column(String, unique=True, nullable=False)
    img_url = Column(String, unique=True, nullable=False)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("User", back_populates="movies")
    

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # movies = relationship("Movies", back_populates="owner")

# TODO make the relationship work after testing the model