# models/article.py
from typing import TypedDict, Optional

class Article(TypedDict):
    """
    Represents the structured data for a single article.
    """
    title: str
    author: Optional[str]
    publication_date: Optional[str]
    content: str
    url: Optional[str]