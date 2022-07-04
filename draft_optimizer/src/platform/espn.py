import os
from typing import Dict, Optional

import psutil
from espn_api.football import League as ESPN_League
from pqdm.threads import pqdm

from draft_optimizer.src.models import BaseLeague, Player

# Get env vars
ESPN_S2 = os.getenv("ESPN_FANTASY_S2")
ESPN_SWID = os.getenv("ESPN_FANTASY_SWID")


class League(BaseLeague):
    _espn_league: ESPN_League

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    def __init__(self, **data):
        # Call super (assigns all but private attributes)
        super().__init__(**data)

        # Generate private attributes
        self._espn_league = ESPN_League(league_id=self.id, year=self.year, espn_s2=ESPN_S2, swid=ESPN_SWID)

    def get_players(self, max_players: Optional[int] = None) -> Dict[int, Player]:
        player_ids = [k for k in self._espn_league.player_map.keys() if isinstance(k, int)]
        if max_players is not None:
            player_ids = player_ids[0:max_players]

        # Define helper
        def _get_player(player_id: int) -> Optional[Player]:
            # Get player
            espn_player = self._espn_league.player_info(playerId=player_id)
            player = None
            if espn_player is not None:
                player = Player(
                    id=espn_player.playerId,
                    name=espn_player.name,
                    position=espn_player.position,
                    pro_team=espn_player.proTeam,
                    proj_points=espn_player.projected_total_points,
                )
            return player

        # Get players
        num_threads = psutil.cpu_count() // psutil.cpu_count(logical=False)
        players = pqdm(player_ids, _get_player, n_jobs=num_threads)
        players_dict = {p.id: p for p in players if p is not None}

        return players_dict
