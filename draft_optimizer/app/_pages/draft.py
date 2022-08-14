import streamlit as st


def display():
    # Display title
    st.markdown("# Draft")

    # Get state
    if "num_teams" not in st.session_state:
        st.error("Settings not applied.")
        st.stop()
    num_teams = st.session_state["num_teams"]
    roster_size = st.session_state["roster_size"]

    # Get draft order (snake)
    teams = list(range(num_teams))
    draft_order = []
    for i in range(roster_size):
        if i % 2 == 0:
            draft_order += teams
        else:
            draft_order += teams[::-1]

    # Display pick form
    if "overall_pick" not in st.session_state:
        st.session_state["overall_pick"] = 0
    overall_pick = st.session_state["overall_pick"]
    if overall_pick >= num_teams * roster_size:
        st.markdown("### Draft Concluded")
    else:
        round_num = overall_pick // num_teams + 1
        pick_num = overall_pick % num_teams + 1
        team = draft_order[overall_pick] + 1
        with st.form("draft"):
            cols = st.columns(2)
            cols[0].markdown(f"### Round: {round_num}, Pick: {pick_num}")
            cols[0].markdown(f"On the clock: Team {team}")
            cols[1].markdown("### Best Available")
            submit = st.form_submit_button("Draft")

        # TODO: go to round/pick (so can revert; will be point-in-time)

        # Handle picks
        if submit:
            st.session_state["overall_pick"] += 1
            st.experimental_rerun()

    # Make team tabs
    st.markdown("---")
    teams = [f"Team {t + 1}" for t in teams]
    team_tabs = st.tabs(teams)
    for team, team_tab in enumerate(team_tabs):
        cols = team_tab.columns(2)
        cols[0].markdown("### Roster")
        cols[1].markdown("### Optimal Team")
