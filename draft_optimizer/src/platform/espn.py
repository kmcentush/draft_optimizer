import os
from typing import Dict, List, Optional, Set, Tuple

from espn_api.football import League as ESPN_League

from draft_optimizer.src.models import BaseLeague, Pick, Player, ProGame, ProTeam, Team

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

    def get_pro_schedule(self) -> Tuple[Dict[int, ProTeam], Dict[int, List[ProGame]]]:
        # Get raw data
        raw = self._espn_league.espn_request.get_pro_schedule()

        # Parse
        teams = raw["settings"]["proTeams"]
        team_objs: Dict[int, ProTeam] = {}
        schedule: Dict[int, List[ProGame]] = {}
        added: Set[ProGame] = set()
        for team in teams:
            if team["id"] != 0:  # FA
                # Make team object
                team_obj = ProTeam(
                    id=team["id"],
                    name=team["name"],
                    abbrev=team["abbrev"].upper(),
                    location=team["location"],
                    bye_week=team["byeWeek"],
                )
                team_objs[team_obj.id] = team_obj

                # Build schedule
                games = team.get("proGamesByScoringPeriod", {})
                for week, week_games in games.items():
                    # Add week if missing
                    if week not in schedule.keys():
                        schedule[week] = []

                    # Loop over games each week (won't necessarily be length 1; ex: rescheduled games)
                    for game in week_games:
                        # Make game object
                        game_obj = ProGame(
                            home_id=game["homeProTeamId"], away_id=game["awayProTeamId"], week=week, date=game["date"]
                        )
                        if game_obj not in added:
                            schedule[week].append(game_obj)
                            added |= {game_obj}

        return team_objs, schedule

    def get_picks(self) -> List[Pick]:
        # Get picks
        espn_picks = self._espn_league.draft
        picks = [
            Pick(round=p.round_num, pick=p.round_pick, player_id=p.playerId, team_id=p.team.team_id) for p in espn_picks
        ]

        return picks

    def get_players(self, max_players: Optional[int] = None) -> Dict[int, Player]:
        # Get player IDs
        player_ids = [k for k in self._espn_league.player_map.keys() if isinstance(k, int)]
        if max_players is not None:
            player_ids = player_ids[0:max_players]

        # Get players
        chunk_size = 500
        espn_players = []
        for i in range(0, len(player_ids), chunk_size):
            chunk = player_ids[i : i + chunk_size]
            chunk_players = self._espn_league.player_info(playerId=chunk)
            if not isinstance(chunk_players, list):
                chunk_players = [chunk_players]
            espn_players += chunk_players
        players = [
            Player(
                id=p.playerId,
                name=p.name,
                position=p.position,
                pro_team=p.proTeam.upper() if p.proTeam != "None" else None,
                points=p.total_points,
                weekly_points={k: v["points"] for k, v in p.stats.items() if "projected_points" not in v.keys()},
                proj_points=p.projected_total_points,
                proj_weekly_points={},
            )
            for p in espn_players
            if p is not None
        ]
        players_dict = {p.id: p for p in players if p is not None}

        return players_dict

    def get_teams(self) -> Dict[int, Team]:
        # Get teams
        espn_teams = self._espn_league.teams
        teams = {
            t.team_id: Team(id=t.team_id, name=t.team_name, owner=t.owner, player_ids=[p.playerId for p in t.roster])
            for t in espn_teams
        }

        return teams
