import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

def sdhl_standings(season: int) -> pd.DataFrame:

    # base_url = "https://www.sdhl.se/game-stats/teams/result?ssgtUuid=qbO-5Eadc4G0L&count=25"
    full_url = "https://www.sdhl.se/api/sports/league-standings?ssgtUuid=qbO-5Eadc4G0L"

    res = requests.get(full_url)
    # [x for x in data]
    # BeautifulSoup(res.content, 'html.parser')
    data = json.loads(res.content.decode('utf-8'))

    stand = pd.DataFrame(data['leagueStandings'])

    standings = {
        'team_name': [],
        'team_id': [],
        'team_uuid': [],
        'games_played': [],
        'points': [],
        'points_per_game': [],
        'wins': [],
        'losses': [],
        'ties': [],
        'regulation_wins': [],
        'regulation_losses': [],
        'overtime_wins': [],
        'overtime_losses': [],
        'shootout_wins': [],
        'shootout_losses': [],
        'goal_differential': [],
        'goals_scored': [],
        'goals_allowed': []
    }

    for index, rows in stand.iterrows():
        standings['team_name'].append(rows['info']['teamInfo']['teamNames']['long'])
        standings['team_id'].append(rows['info']['id'])
        standings['team_uuid'].append(rows['info']['teamInfo']['teamUuid'])
        standings['games_played'].append(int(rows['GP']))
        standings['points'].append(int(rows['Points']))
        standings['points_per_game'].append(np.round(int(rows['Points']) / int(rows['GP']), 1))
        standings['wins'].append(int(rows['RegW']) + int(rows['SOW']) + int(rows['OTW']))
        standings['losses'].append(int(rows['RegL']) + int(rows['SOL']) + int(rows['OTL']))
        standings['ties'].append(int(rows['RegT']))
        standings['regulation_wins'].append(int(rows['RegW']))
        standings['regulation_losses'].append(int(rows['RegL']))
        standings['overtime_wins'].append(int(rows['OTW']))
        standings['overtime_losses'].append(int(rows['OTL']))
        standings['shootout_wins'].append(int(rows['SOW']))
        standings['shootout_losses'].append(int(rows['SOL']))
        standings['goal_differential'].append(int(rows['Diff']))
        standings['goals_scored'].append(int(rows['G']))
        standings['goals_allowed'].append(int(rows['GA']))

    stand_df = pd.DataFrame(standings)

    stand_df['goals_scored_per_game'] = np.round(stand_df['goals_scored'] / stand_df['games_played'], 1)
    stand_df['goals_allowed_per_game'] = np.round(stand_df['goals_allowed'] / stand_df['games_played'], 1)
