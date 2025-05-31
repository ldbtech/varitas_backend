from pydantic import BaseModel

class Article(BaseModel):
    title: str
    source: str
    author: str
    published_at: str 
    description: str
    refrence_url: str
