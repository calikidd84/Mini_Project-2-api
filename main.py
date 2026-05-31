from contextlib import asynccontextmanager
from typing import List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, SessionLocal, engine

import os
from dotenv import load_dotenv 

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Video Games API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Video Games API is running"}


# -------------------------
# Stats
# -------------------------
@app.get("/stats", response_model=Union[schemas.StatsRead, schemas.FilteredTopGamesStat])
def get_stats(
    publisher_id: Optional[int] = Query(default=None, ge=1),
    console_id: Optional[int] = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    if publisher_id is not None and console_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Use either publisher_id or console_id, not both",
        )

    console_average, console_count = (
        db.query(func.avg(models.Console.fan_rating), func.count(models.Console.fan_rating))
        .filter(models.Console.fan_rating.isnot(None))
        .one()
    )
    game_average, game_count = (
        db.query(func.avg(models.Game.fan_rating), func.count(models.Game.fan_rating))
        .filter(models.Game.fan_rating.isnot(None))
        .one()
    )

    average_game_rating = func.avg(models.Game.fan_rating).label("average_game_rating")
    rated_game_count = func.count(models.Game.fan_rating).label("rated_game_count")
    best_publisher_row = (
        db.query(models.Publisher, average_game_rating, rated_game_count)
        .join(models.Game)
        .filter(models.Game.fan_rating.isnot(None))
        .group_by(models.Publisher.id)
        .order_by(desc(average_game_rating), desc(rated_game_count))
        .first()
    )

    if publisher_id is not None:
        publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
        if not publisher:
            raise HTTPException(status_code=404, detail="Publisher not found")

        top_games = (
            db.query(models.Game)
            .filter(models.Game.publisher_id == publisher.id, models.Game.fan_rating.isnot(None))
            .order_by(desc(models.Game.fan_rating), desc(models.Game.vote_count), models.Game.title)
            .limit(5)
            .all()
        )
        return {
            "filter_type": "publisher",
            "filter_id": publisher.id,
            "name": publisher.name,
            "games": top_games,
        }

    if console_id is not None:
        console = db.query(models.Console).filter(models.Console.id == console_id).first()
        if not console:
            raise HTTPException(status_code=404, detail="Console not found")

        top_games = (
            db.query(models.Game)
            .join(models.Game.consoles)
            .filter(models.Console.id == console.id, models.Game.fan_rating.isnot(None))
            .order_by(desc(models.Game.fan_rating), desc(models.Game.vote_count), models.Game.title)
            .limit(5)
            .all()
        )
        return {
            "filter_type": "console",
            "filter_id": console.id,
            "name": console.name,
            "games": top_games,
        }

    publishers_best_5_games = []
    publishers = db.query(models.Publisher).order_by(models.Publisher.name).all()
    for publisher in publishers:
        top_games = (
            db.query(models.Game)
            .filter(models.Game.publisher_id == publisher.id, models.Game.fan_rating.isnot(None))
            .order_by(desc(models.Game.fan_rating), desc(models.Game.vote_count), models.Game.title)
            .limit(5)
            .all()
        )
        publishers_best_5_games.append({"publisher": publisher, "games": top_games})

    best_console = (
        db.query(models.Console)
        .filter(models.Console.fan_rating.isnot(None))
        .order_by(desc(models.Console.fan_rating), desc(models.Console.vote_count), models.Console.name)
        .first()
    )
    top_game = (
        db.query(models.Game)
        .filter(models.Game.fan_rating.isnot(None))
        .order_by(desc(models.Game.fan_rating), desc(models.Game.vote_count), models.Game.title)
        .first()
    )

    best_publisher = None
    if best_publisher_row:
        publisher, publisher_average, publisher_count = best_publisher_row
        best_publisher = {
            "publisher": publisher,
            "average_game_rating": publisher_average,
            "rated_game_count": publisher_count,
        }

    return {
        "console_ratings": {
            "average_fan_rating": console_average,
            "rated_count": console_count,
        },
        "game_ratings": {
            "average_fan_rating": game_average,
            "rated_count": game_count,
        },
        "publishers_best_5_games": publishers_best_5_games,
        "best_publisher": best_publisher,
        "best_console": best_console,
        "top_game": top_game,
    }


# -------------------------
# Publishers
# -------------------------
@app.get("/publishers", response_model=List[schemas.PublisherRead])
def get_publishers(db: Session = Depends(get_db)):
    return db.query(models.Publisher).all()


@app.get("/publishers/{publisher_id}", response_model=schemas.PublisherRead)
def get_publisher(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


@app.post("/publishers", response_model=schemas.PublisherRead, status_code=status.HTTP_201_CREATED)
def create_publisher(publisher: schemas.PublisherCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Publisher).filter(models.Publisher.name == publisher.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Publisher already exists")

    db_publisher = models.Publisher(**publisher.model_dump())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@app.put("/publishers/{publisher_id}", response_model=schemas.PublisherRead)
def update_publisher(publisher_id: int, publisher_update: schemas.PublisherUpdate, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    update_data = publisher_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(publisher, key, value)

    db.commit()
    db.refresh(publisher)
    return publisher


@app.delete("/publishers/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_publisher(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    db.delete(publisher)
    db.commit()
    return None


# -------------------------
# Consoles
# -------------------------
@app.get("/consoles", response_model=List[schemas.ConsoleRead])
def get_consoles(db: Session = Depends(get_db)):
    return db.query(models.Console).all()


@app.get("/consoles/{console_id}", response_model=schemas.ConsoleRead)
def get_console(console_id: int, db: Session = Depends(get_db)):
    console = db.query(models.Console).filter(models.Console.id == console_id).first()
    if not console:
        raise HTTPException(status_code=404, detail="Console not found")
    return console


@app.post("/consoles", response_model=schemas.ConsoleRead, status_code=status.HTTP_201_CREATED)
def create_console(console: schemas.ConsoleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Console).filter(models.Console.name == console.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Console already exists")

    db_console = models.Console(**console.model_dump())
    db.add(db_console)
    db.commit()
    db.refresh(db_console)
    return db_console


@app.put("/consoles/{console_id}", response_model=schemas.ConsoleRead)
def update_console(console_id: int, console_update: schemas.ConsoleUpdate, db: Session = Depends(get_db)):
    console = db.query(models.Console).filter(models.Console.id == console_id).first()
    if not console:
        raise HTTPException(status_code=404, detail="Console not found")

    update_data = console_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(console, key, value)

    db.commit()
    db.refresh(console)
    return console


@app.delete("/consoles/{console_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_console(console_id: int, db: Session = Depends(get_db)):
    console = db.query(models.Console).filter(models.Console.id == console_id).first()
    if not console:
        raise HTTPException(status_code=404, detail="Console not found")

    db.delete(console)
    db.commit()
    return None


# -------------------------
# Games
# -------------------------
@app.get("/games", response_model=List[schemas.GameRead])
def get_games(db: Session = Depends(get_db)):
    return db.query(models.Game).all()


@app.get("/games/{game_id}", response_model=schemas.GameRead)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post("/games", response_model=schemas.GameRead, status_code=status.HTTP_201_CREATED)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == game.publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=400, detail="Publisher does not exist")

    consoles = []
    if game.console_ids:
        consoles = db.query(models.Console).filter(models.Console.id.in_(game.console_ids)).all()
        if len(consoles) != len(set(game.console_ids)):
            raise HTTPException(status_code=400, detail="One or more consoles do not exist")

    game_data = game.model_dump(exclude={"console_ids"})
    db_game = models.Game(**game_data)
    db_game.consoles = consoles

    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@app.put("/games/{game_id}", response_model=schemas.GameRead)
def update_game(game_id: int, game_update: schemas.GameUpdate, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    update_data = game_update.model_dump(exclude_unset=True)

    if "publisher_id" in update_data:
        publisher = db.query(models.Publisher).filter(models.Publisher.id == update_data["publisher_id"]).first()
        if not publisher:
            raise HTTPException(status_code=400, detail="Publisher does not exist")

    if "console_ids" in update_data:
        console_ids = update_data.pop("console_ids")
        if console_ids is not None:
            consoles = db.query(models.Console).filter(models.Console.id.in_(console_ids)).all()
            if len(consoles) != len(set(console_ids)):
                raise HTTPException(status_code=400, detail="One or more consoles do not exist")
            game.consoles = consoles

    for key, value in update_data.items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


@app.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(game)
    db.commit()
    return None
