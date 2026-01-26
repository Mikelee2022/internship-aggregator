from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Internship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    role: str
    location: str
    industry: str = "Technology"
    ai_label: bool = False
    summary: Optional[str] = None
    requirements: Optional[str] = None
    salary: Optional[str] = None
    deadline: Optional[datetime] = None
    international_score: Optional[int] = Field(default=5, description="1-10 score indicating friendliness to international students")
    logo_url: Optional[str] = None
    url: str
    posted_date: datetime = Field(default_factory=datetime.utcnow)
