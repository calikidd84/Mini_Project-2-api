from sqlalchemy import Column, ForeignKey, Integer, String, Table, CheckConstraint, Numeric
from sqlalchemy.orm import relationship

from database import Base


game_consoles = Table(
    "game_consoles",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True),
    Column("console_id", Integer, ForeignKey("consoles.id"), primary_key=True),
)


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    country = Column(String, nullable=True)
    founded_year = Column(Integer, nullable=True)

    games = relationship("Game", back_populates="publisher", cascade="all, delete")


class Game(Base):
    __tablename__ = "games"

    __table_args__ = (
        CheckConstraint("fan_rating >= 1 AND fan_rating <= 10", name="games_fan_rating_range"),
        CheckConstraint("vote_count >= 0", name="games_vote_count_nonnegative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    genre = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    fan_rating = Column(Numeric(3, 1), nullable=True)
    vote_count = Column(Integer, nullable=False, default=0)

    publisher = relationship("Publisher", back_populates="games")
    consoles = relationship("Console", secondary=game_consoles, back_populates="games")


class Console(Base):
    __tablename__ = "consoles"

    __table_args__ = (
        CheckConstraint("fan_rating >= 1 AND fan_rating <= 10", name="consoles_fan_rating_range"),
        CheckConstraint("vote_count >= 0", name="consoles_vote_count_nonnegative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    manufacturer = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    fan_rating = Column(Numeric(3, 1), nullable=True)
    vote_count = Column(Integer, nullable=False, default=0)

    games = relationship("Game", secondary=game_consoles, back_populates="consoles")