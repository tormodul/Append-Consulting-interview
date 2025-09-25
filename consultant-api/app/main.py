from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Consultant API")

class Consultant(BaseModel):
    id: int
    name: str
    skills: List[str]
    load_percent: int

consultants_db = [
    Consultant(id=1, name="Anna K.", skills=["python", "docker", "fastapi"], load_percent=40),
    Consultant(id=2, name="Leo T.", skills=["python", "react", "css"], load_percent=20),
    Consultant(id=3, name="Sofia M.", skills=["python", "aws", "terraform"], load_percent=90),
    Consultant(id=4, name="David B.", skills=["docker", "kubernetes", "aws"], load_percent=100),
]

@app.get("/consultants", response_model=List[Consultant])
def get_consultants():
    """Returns the complete list of hardcoded consultants."""
    return consultants_db