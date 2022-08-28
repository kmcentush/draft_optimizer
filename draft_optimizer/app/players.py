import os

import pandas as pd
import streamlit as st

from draft_optimizer.src.utils import DATA_DIR


@st.experimental_memo(show_spinner=False)
def load_players(points_mode: str, year: int = 2022) -> pd.DataFrame:
    # Load data
    points_mode = points_mode.lower().replace(" ", "_")
    players_path = os.path.join(DATA_DIR, "production", str(year), f"players_{points_mode}_v2.csv")
    players = pd.read_csv(players_path, index_col=[0, 1, 2, 3])

    return players
