from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import uvicorn

DATABASE_URL = "sqlite:///./game.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class GameDB(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    icon = Column(String)
    play_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

class ScoreDB(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, index=True)
    player_name = Column(String, index=True)
    score = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="小游戏乐园 API", version="1.0.0")

@app.get("/")
def root():
    return {"status": "ok", "message": "小游戏乐园 API", "version": "1.0.0"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreCreate(BaseModel):
    game_id: int
    player_name: str
    score: int

class ScoreResponse(BaseModel):
    id: int
    game_id: int
    player_name: str
    score: int
    created_at: datetime

class GameResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    play_count: int
    rating: int
    created_at: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/games", response_model=list[GameResponse])
def get_games(db: Session = Depends(get_db)):
    games = db.query(GameDB).all()
    return games

@app.get("/api/games/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post("/api/score", response_model=ScoreResponse)
def submit_score(score_data: ScoreCreate, db: Session = Depends(get_db)):
    game = db.query(GameDB).filter(GameDB.id == score_data.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.play_count += 1
    new_score = ScoreDB(
        game_id=score_data.game_id,
        player_name=score_data.player_name,
        score=score_data.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@app.get("/api/leaderboard")
def get_leaderboard(game_id: int = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(ScoreDB)
    if game_id:
        query = query.filter(ScoreDB.game_id == game_id)
    scores = query.order_by(ScoreDB.score.desc()).limit(limit).all()
    return scores

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)