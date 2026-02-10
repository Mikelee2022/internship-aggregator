from backend.database import engine, Session
from backend.models import Internship
from sqlmodel import select, func

with Session(engine) as session:
    total = session.exec(select(func.count(Internship.id))).one()
    print(f"Total Internship objects via SQLModel: {total}")
    
    # Check if any have empty company
    empty_company = session.exec(select(func.count(Internship.id)).where(Internship.company == "")).one()
    print(f"Internships with empty company name: {empty_company}")
