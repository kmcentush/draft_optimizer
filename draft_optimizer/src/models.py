from typing import Dict, Optional

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    position: str
    pro_team: str
    proj_points: float


class BaseLeague(BaseModel):
    id: int
    year: int
    name: Optional[str] = None

    # def get_draft(self) -> List[Pick]:  # pragma: no cover
    #     raise NotImplementedError

    def get_players(self, max_players: Optional[int] = None) -> Dict[int, Player]:  # pragma: no cover
        raise NotImplementedError

    # def get_teams(self) -> Dict[int, Team]:  # pragma: no cover
    #     raise NotImplementedError
