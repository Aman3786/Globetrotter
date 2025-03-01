from fastapi import FastAPI, HTTPException, Depends, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, Any
import random
import json
import uuid


# SQLite Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./globetrotter.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    score = Column(Integer, default=0)
    
class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    country = Column(String)
    clues = Column(JSON)
    fun_fact = Column(JSON)
    trivia = Column(JSON)
    
class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(String, primary_key=True,index=True)
    inviter_id = Column(Integer)
    inviter_score = Column(Integer)
    
# Create tables
Base.metadata.create_all(bind=engine)



# Seed initial data
def seed_database():
    db = SessionLocal()
    try:
        if db.query(Destination).count() == 0:
            with open("data.json") as f:
                destinations = json.load(f)
                for dest in destinations:
                    db.add(Destination(**dest))
            db.commit()
            print("DataBase INFO: Data Added to Database...")
    finally:
        db.close()
seed_database()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")


       
       
       
        
# Pydantic Validation Models
class UserCreate(BaseModel):
    username: str
    
class VerifyRequest(BaseModel):
    answer: str
    user_id: Optional[int] = None




# Game Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/game")
async def get_game_question(db: Session = Depends(get_db)):
    # Get random destination
    destination = db.query(Destination).order_by(func.random()).first()
    # Get 3 wrong answers
    wrong_destinations = db.query(Destination)\
        .filter(Destination.id != destination.id)\
        .order_by(func.random())\
        .limit(3)\
        .all()
    options = [destination] + [d for d in wrong_destinations]
    random.shuffle(options)
    return {
        "destination_id": destination.id,
        "clues": destination.clues,
        "options": options
    }
    

@app.post("/api/verify/{destination_id}")
async def verify_answer(
    destination_id: int,
    request: VerifyRequest,
    db: Session = Depends(get_db)
):
    destination = db.query(Destination)\
        .filter(Destination.id == destination_id)\
        .first()
        
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    is_correct = request.answer.strip().lower() == destination.city.lower()
    result = {
        "correct": is_correct,
        "fun_fact": destination.fun_fact
    }
    
    print(request)
    if request.user_id:
        user = db.query(User).filter(User.id == request.user_id).first()
        print(user)
        if user:
            if is_correct:
                user.score += 1
            db.commit()
            result["new_score"] = user.score
            
    print(result)
        
    return result
    
    
# User Endpoints
@app.post("/api/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    return {
        "id": new_user.id,
        "username": new_user.username,
        "score": new_user.score
    }


# Challenge Endpoints
@app.post("/api/challenges/{inviter_id}")
async def create_challenge(inviter_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == inviter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.refresh(user)
    challenge = Challenge(
        id=str(uuid.uuid4()),
        inviter_id=user.id,
        inviter_score=user.score
    )
    db.add(challenge)
    db.commit()
    return {"challenge_id": challenge.id}


@app.get("/challenges",response_class=HTMLResponse)
async def get_challenge(request:Request, challenge_id: str, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    inviter = db.query(User).filter(User.id == challenge.inviter_id).first()
    return templates.TemplateResponse("index.html", {
        "request":request,
        "challenge":True,
        "inviter": inviter,
        "score": inviter.score
    })