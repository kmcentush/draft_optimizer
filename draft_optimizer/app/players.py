import ast
import os

import pandas as pd
import streamlit as st

# Specify data directory
DATA_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "data"))


@st.experimental_memo(show_spinner=False)
def load_players(points_mode: str, year: int = 2022) -> pd.DataFrame:
    # Load data
    points_mode = points_mode.lower().replace(" ", "_")
    players_path = os.path.join(DATA_DIR, "production", str(year), f"players_{points_mode}.csv")
    raw = pd.read_csv(players_path, index_col=[0, 1, 2, 3])

    # Explode weekly projections
    raw["proj_weekly_points"] = raw["proj_weekly_points"].fillna("{}").apply(lambda v: ast.literal_eval(v))
    players = raw["proj_weekly_points"].apply(pd.Series, dtype=float)
    players.columns = [f"week{c}" for c in players.columns]

    # Add columns
    players["sum_weeks"] = players.sum(axis=1)
    players["adp"] = players["sum_weeks"].rank(ascending=False)  # TODO: real ADP?

    return players
