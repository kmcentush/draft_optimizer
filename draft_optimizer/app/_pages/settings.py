import streamlit as st


def display():
    # Display title
    st.markdown("# Settings")

    # Specify settings
    with st.form("settings"):
        cols = st.columns(4)
        points_mode = cols[0].radio("Points Mode", ["PPR", "Half PPR"], horizontal=True)
        num_teams = int(cols[1].number_input("Teams", value=12, min_value=6, max_value=12))
        roster_size = int(cols[2].number_input("Roster Size", value=16, min_value=16, max_value=18))
        submit = st.form_submit_button("Apply")

    if submit:
        # Update state
        st.session_state["points_mode"] = points_mode
        st.session_state["num_teams"] = num_teams
        st.session_state["roster_size"] = roster_size
