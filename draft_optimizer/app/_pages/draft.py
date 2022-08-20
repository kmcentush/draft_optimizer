import streamlit as st

from draft_optimizer.app.settings import list_settings, load_settings


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
    num_teams = settings["num_teams"]
    roster_size = settings["roster_size"]
    draft_order = settings["draft_order"]
    draft_picks = settings["draft_picks"]
    teams = [i for i in range(num_teams)]

    # Display pick form
    overall_pick = len(draft_picks)
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

        # Handle picks
        if submit:
            # TODO: save pick
            st.experimental_rerun()

    # Make team tabs
    st.markdown("---")
    teams = [f"Team {t + 1}" for t in teams]
    team_tabs = st.tabs(teams)
    for team, team_tab in enumerate(team_tabs):
        cols = team_tab.columns(2)
        cols[0].markdown("### Roster")
        cols[1].markdown("### Optimal Team")
