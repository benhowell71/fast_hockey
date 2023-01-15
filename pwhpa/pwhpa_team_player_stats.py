from pwhpa.pwhpa_player_stats import pwhpa_player_stats

def pwhpa_team_player_stats(team: str, position: str):
    stats = pwhpa_player_stats(position=position)

    team_stats = stats[stats.team_id == team]

    return team_stats