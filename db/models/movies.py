from pydantic import BaseModel

class Movies(BaseModel):
    title: str
    year: int
    description: str
    rating: float
    ranking: int
    review: str
    img_url: str

