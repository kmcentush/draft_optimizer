import numpy as np
import pandas as pd
import streamlit as st

from draft_optimizer.app.players import load_players
from draft_optimizer.app.settings import list_settings, load_settings, save_settings


def get_possible_picks(draft_picks: np.ndarray, players: pd.DataFrame) -> pd.Series:
    # Reset index
    players = players.reset_index(level=["name", "position", "pro_team"])

    # Exclude picks
    players = players.loc[~players.index.isin(draft_picks)]

    # Build str
    possible_picks = players["name"] + " (" + players["position"] + ", " + players["pro_team"] + ")"
    possible_picks = possible_picks.sort_values()

    return possible_picks


def display():
    # Display title
    st.markdown("# Draft")
    st.sidebar.markdown("---")

    # TODO: go to round/pick (so can revert; will be point-in-time)

    # List settings
    settings_files = list_settings()
    settings_file = st.sidebar.selectbox("Settings", settings_files)
    if settings_file is None:
        st.error("Settings not selected.")
        st.stop()

    # Load settings
    settings = load_settings(settings_file)
    points_mode = settings["points_mode"]
    num_teams = settings["num_teams"]
    roster_size = settings["roster_size"]
    pos_consts = settings["pos_consts"]
    draft_order = np.array(settings["draft_order"], dtype=int)
    draft_picks = np.array(settings["draft_picks"], dtype=int)
    teams = [i for i in range(num_teams)]

    # Load players
    players = load_players(points_mode)
    possible_picks = get_possible_picks(draft_picks, players)

    # Display pick form
    overall_pick = len(draft_picks)
    if overall_pick >= num_teams * roster_size:
        st.markdown("### Draft Concluded")
    else:
        # Get info
        round_num = overall_pick // num_teams + 1
        pick_num = overall_pick % num_teams + 1
        team = draft_order[overall_pick] + 1

        # Display pick options
        with st.form("draft"):
            # Draft section
            cols = st.columns(2)
            cols[0].markdown(f"### Round: {round_num}, Pick: {pick_num}")
            cols[0].markdown(f"On the clock: Team {team}")
            pick = cols[0].selectbox("Player", ["None"] + possible_picks.tolist())

            # Best available section
            cols[1].markdown("### Best Available")
            positions = list(pos_consts.keys())
            pos_tabs = cols[1].tabs(positions)
            for i, pos_tab in enumerate(pos_tabs):
                to_display = players.loc[players.index.get_level_values("position") == positions[i]]
                to_display = to_display.loc[to_display.index.get_level_values("id").isin(possible_picks.index)]
                pos_tab.dataframe(to_display["sum_weeks"].nlargest(25).reset_index())

            # Submit
            submit = cols[0].form_submit_button("Draft")

        # Handle submit
        if submit:
            if pick == "None":
                cols[0].error("No player selected.")
                st.stop()

            # Save pick
            player_id = int(possible_picks[possible_picks == pick].index[0])
            settings["draft_picks"].append(player_id)
            save_settings(settings_file, settings)
            st.experimental_rerun()

    # Make team tabs
    st.markdown("---")
    teams = [f"Team {t + 1}" for t in teams]
    team_tabs = st.tabs(teams)
    for team, team_tab in enumerate(team_tabs):
        # Roster section
        cols = team_tab.columns(2)
        cols[0].markdown("### Roster")
        picks_idx = draft_order == team
        picks_idx = picks_idx[0 : len(draft_picks)]
        picks_ids = draft_picks[picks_idx]
        roster = players.loc[players.index.get_level_values("id").isin(picks_ids)]
        cols[0].dataframe(roster["sum_weeks"].reset_index())

        # Optimizer section
        cols[1].markdown("### Optimal Team")
        # TODO