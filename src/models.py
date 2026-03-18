from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Subject(BaseModel):
    id: str
    title: str
    url: str
    pic: dict
    rating: Optional[dict] = None
    year: Optional[str] = None


class Rating(BaseModel):
    value: Optional[int] = None
    max: int = 5


class MovieMark(BaseModel):
    subject: Subject
    rating: Optional[Rating] = None
    comment: Optional[str] = None
    create_time: str
    status: str = "done"


class DoubanResponse(BaseModel):
    marks: List[MovieMark]
    total: int
