import datetime
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel


class Pick(BaseModel):
    round: int
    pick: int
    team_id: int
    player_id: int


class Player(BaseModel):
    id: int
    name: str
    position: str
    pro_team: Optional[str]
    proj_points: float


class ProGame(BaseModel):
    home_id: int
    away_id: int
    week: int
    date: datetime.date

    def __hash__(self) -> int:
        return hash(repr(self))


class ProTeam(BaseModel):
    id: int
    name: str
    abbrev: str
    location: str
    bye_week: int


class Team(BaseModel):
    id: int
    name: str
    owner: str
    player_ids: List[int]


class BaseLeague(BaseModel):
    id: int
    year: int
    name: Optional[str] = None

    def get_pro_schedule(self) -> Tuple[Dict[int, ProTeam], Dict[int, List[ProGame]]]:  # pragma: no cover
        raise NotImplementedError

    def get_picks(self) -> List[Pick]:  # pragma: no cover
        raise NotImplementedError

    def get_players(self, max_players: Optional[int] = None) -> Dict[int, Player]:  # pragma: no cover
        raise NotImplementedError

    def get_teams(self) -> Dict[int, Team]:  # pragma: no cover
        raise NotImplementedError
