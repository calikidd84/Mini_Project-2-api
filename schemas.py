from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ConsoleBase(BaseModel):
    name: str
    manufacturer: str
    release_year: Optional[int] = None
    fan_rating: Optional[float] = Field(default=None, ge=1, le=10)
    vote_count: int = Field(default=0, ge=0)


class ConsoleCreate(ConsoleBase):
    pass


class ConsoleUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    release_year: Optional[int] = None
    fan_rating: Optional[float] = Field(default=None, ge=1, le=10)
    vote_count: Optional[int] = Field(default=None, ge=0)


class ConsoleRead(ConsoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PublisherBase(BaseModel):
    name: str
    country: Optional[str] = None
    founded_year: Optional[int] = None


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None


class PublisherRead(PublisherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GameBase(BaseModel):
    title: str
    genre: str
    release_year: Optional[int] = None
    publisher_id: int
    fan_rating: Optional[float] = Field(default=None, ge=1, le=10)
    vote_count: int = Field(default=0, ge=0)


class GameCreate(GameBase):
    console_ids: List[int] = []


class GameUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    publisher_id: Optional[int] = None
    fan_rating: Optional[float] = Field(default=None, ge=1, le=10)
    vote_count: Optional[int] = Field(default=None, ge=0)
    console_ids: Optional[List[int]] = None


class GameRead(GameBase):
    id: int
    publisher: PublisherRead
    consoles: List[ConsoleRead] = []

    model_config = ConfigDict(from_attributes=True)


class RatingAverageStat(BaseModel):
    average_fan_rating: Optional[float] = None
    rated_count: int


class PublisherRatingStat(BaseModel):
    publisher: PublisherRead
    average_game_rating: Optional[float] = None
    rated_game_count: int


class PublisherTopGamesStat(BaseModel):
    publisher: PublisherRead
    games: List[GameRead]


class FilteredTopGamesStat(BaseModel):
    filter_type: str
    filter_id: int
    name: str
    games: List[GameRead]


class StatsRead(BaseModel):
    console_ratings: RatingAverageStat
    game_ratings: RatingAverageStat
    publishers_best_5_games: List[PublisherTopGamesStat]
    best_publisher: Optional[PublisherRatingStat] = None
    best_console: Optional[ConsoleRead] = None
    top_game: Optional[GameRead] = None
