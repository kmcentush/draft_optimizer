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

    # Get players
    players = league.get_players(max_players=1)
    assert len(players) > 0
