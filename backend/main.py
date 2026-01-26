from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from .database import create_db_and_tables, get_session
from .models import Internship
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/internships", response_model=List[Internship])
def read_internships(
    offset: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by_date: bool = True,
    session: Session = Depends(get_session)
):
    query = select(Internship)
    if search:
        query = query.where(
            (Internship.company.contains(search)) | 
            (Internship.role.contains(search)) |
            (Internship.industry.contains(search))
        )
    
    if sort_by_date:
        query = query.order_by(Internship.posted_date.desc())
        
    query = query.offset(offset).limit(limit)
    internships = session.exec(query).all()
    return internships
