import os
from typing import List

import pandas as pd
import streamlit as st

from draft_optimizer.src.platform.espn import League as ESPNLeague
from draft_optimizer.src.utils import DATA_DIR


@st.experimental_memo(show_spinner=False)
def load_players(points_mode: str, year: int) -> pd.DataFrame:
    # Load data
    points_mode = points_mode.lower().replace(" ", "_")
    players_path = os.path.join(DATA_DIR, "production", str(year), f"players_{points_mode}.csv")
    players = pd.read_csv(players_path)
    players["id"] = players["id"].astype(str)
    players = players.set_index(["id", "name", "position", "pro_team"])

    return players


def sync_picks(league_id: str, platform: str, year: int) -> List[str]:
    picks: List[str] = []
    if platform == "ESPN":  # note: ESPN picks don't update mid-draft
        league = ESPNLeague(id=league_id, year=year)
        pick_objs = league.get_picks()
        picks = [str(p.player_id) for p in pick_objs]

    return picks
