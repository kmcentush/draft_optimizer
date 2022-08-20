import streamlit as st

from draft_optimizer.app.settings import save_settings


def display():
    # Display title
    st.markdown("# Settings")

    # Specify settings
    league_name = st.text_input("League Name", "")
    cols = st.columns(4)
    points_mode = cols[0].radio("Points Mode", ["PPR", "Half PPR"], horizontal=True)
    num_teams = int(cols[1].number_input("Teams", value=12, min_value=6, max_value=12))
    roster_size = int(cols[2].number_input("Roster Size", value=16, min_value=16, max_value=18))

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
            "points_mode": points_mode,
            "num_teams": num_teams,
            "roster_size": roster_size,
            "draft_order": draft_order,
            "draft_picks": [],
        }
        settings_file = f"{league_name}.json"
        save_settings(settings_file, settings)
