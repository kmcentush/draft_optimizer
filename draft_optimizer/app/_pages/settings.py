import streamlit as st

from draft_optimizer.app.settings import save_settings


def display():
    # Display title
    st.markdown("# Settings")

    # Specify settings
    league_name = st.text_input("League Name", "")
    cols = st.columns(3)
    year = int(cols[0].number_input("Year", value=2022, min_value=2020, max_value=2030))
    league_id = cols[1].text_input("League ID (optional)", "")
    platform = cols[2].radio("Platform (optional)", [None, "ESPN", "Sleeper"], horizontal=True)
    cols = st.columns(4)
    points_mode = cols[0].radio("Points Mode", ["PPR", "Half PPR"], horizontal=True)
    num_teams = int(cols[1].number_input("Teams", value=12, min_value=6, max_value=12))
    roster_size = int(cols[2].number_input("Roster Size", value=16, min_value=16, max_value=18))

    # Specify position constraints
    pos_consts = {}
    with st.expander("Position Limits"):
        default_max = {"QB": 2, "RB": 6, "WR": 6, "TE": 4, "K": 1, "D/ST": 2}
        default_min = {"QB": 1, "RB": 2, "WR": 2, "TE": 2, "K": 1, "D/ST": 1}
        limit_options = list(range(1, 7))
        cols = st.columns(2)
        for i, pos in enumerate(default_max.keys()):
            pos_const = cols[i % 2].select_slider(pos, limit_options, (default_min[pos], default_max[pos]))
            pos_consts[pos] = (int(pos_const[0]), int(pos_const[1]))

    # Specify draft order
    with st.expander("Draft Order"):
        # Get default draft order (snake)
        teams = list(range(num_teams))
        default_draft_order = []
        for i in range(roster_size):
            if i % 2 == 0:
                default_draft_order += teams
            else:
                default_draft_order += teams[::-1]

        # Loop over rounds
        draft_order = []
        for i in range(roster_size // 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                # Display draft order
                draft_round = i * 4 + j
                col.markdown(f"Round {draft_round}")
                for k in range(num_teams):
                    pick_idx = draft_round * num_teams + k
                    team = col.number_input(
                        f"Pick {k + 1}",
                        value=default_draft_order[pick_idx] + 1,
                        min_value=1,
                        max_value=num_teams,
                        step=1,
                        key=f"draft_{pick_idx}",
                    )
                    draft_order.append(int(team - 1))

    # Handle submit
    submit = st.button("Save")
    if submit:
        # Handle errors
        if league_name == "":
            st.error("League name not specified.")
            st.stop()

        # Save output
        settings = {
            "league_name": league_name,
            "year": year,
            "league_id": None if league_id == "" else league_id,
            "platform": None if platform == "None" else platform,
            "points_mode": points_mode,
            "num_teams": num_teams,
            "roster_size": roster_size,
            "pos_consts": pos_consts,
            "draft_order": draft_order,
            "draft_picks": [],
        }
        settings_file = f"{league_name}.json"
        save_settings(settings_file, settings)
