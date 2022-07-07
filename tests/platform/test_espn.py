from draft_optimizer.src.platform.espn import League


def test_league():
    # Specify info
    name = "League"
    league_id = 88497130
    year = 2021

    # Get league
    league = League(name=name, id=league_id, year=year)
    assert league.name == name
    assert league.id == league_id
    assert league.year == year

    # Get pro schedule
    pro_teams, pro_schedule = league.get_pro_schedule()
    assert len(pro_teams) == 32
    assert len(pro_schedule.keys()) == 18

    # Get teams
    teams = league.get_teams()
    assert len(teams) > 0

    # Get picks
    picks = league.get_picks()
    assert len(picks) > 0

    # Get players
    players = league.get_players(max_players=1)
    assert len(players) > 0
