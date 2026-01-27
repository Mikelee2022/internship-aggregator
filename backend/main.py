from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select, func
from typing import List, Optional, Dict, Any
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

@app.get("/internships", response_model=Dict[str, Any])
def read_internships(
    offset: int = 0,
    limit: int = 12,
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
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    if sort_by_date:
        query = query.order_by(Internship.posted_date.desc())
        
    query = query.offset(offset).limit(limit)
    internships = session.exec(query).all()
    
    return {
        "items": internships,
        "total": total
    }
