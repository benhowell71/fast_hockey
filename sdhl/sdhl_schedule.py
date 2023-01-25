import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

def sdhl_schedule(season: int) -> pd.DataFrame:
    # base_url = "https://www.sdhl.se/api/sports/season-series-game-types-filter"
    # full_url = "https://www.sdhl.se/api/sports/season-series-game-types-filter" # this returns the ID for the schedule URL
    full_url = "https://www.sdhl.se/api/sports/game-info?seasonUuid=qbN-XMFfjGVt&seriesUuid=qQ9-f438G8BXP&gameTypeUuid=qQ9-af37Ti40B&gamePlace=all&played=all"

    res = requests.get(full_url)
    data = json.loads(res.content.decode("utf-8"))
    games = pd.DataFrame(data["gameInfo"])

    # data["ssgtUuid"]

    schedule = {
        'season_id': [],
        'league': [],
        'league_id': [],
        'game_id': [],
        'game_date': [],
        'game_time': [],
        'status': [],
        'winner': [],
        'home_score': [],
        'away_score': [],
        'overtime': [],
        'shootout': [],
        'home_team_id': [],
        'home_team_short': [],
        'home_team': [],
        'away_team_id': [],
        'away_team_short': [],
        'away_team': [],
        'facility_id': [],
        'facility': []
    }

    for index, rows in games.iterrows():
        schedule['season_id'].append(data['ssgtUuid'])
        schedule['game_id'].append(rows['uuid'])
        schedule['game_date'].append(rows['date'])
        schedule['game_time'].append(rows['time'])
        schedule['status'].append('Final' if rows['state'] == 'post-game' else 'Not Started')

        winner = rows['homeTeamInfo']['names']['full'] if rows['homeTeamInfo']['status'] == 'WIN' else rows['awayTeamInfo']['names']['full']    
        schedule['winner'].append('nan' if rows['state'] == 'pre-game' else winner)

        schedule['home_team_id'].append(rows['homeTeamInfo']['uuid'])
        schedule['home_team_short'].append(rows['homeTeamInfo']['code'])
        schedule['home_team'].append(rows['homeTeamInfo']['names']['full'])
        schedule['home_score'].append(rows['homeTeamInfo']['score'])

        # rows['awayTeamInfo']['status']
        schedule['away_team_id'].append(rows['awayTeamInfo']['uuid'])
        schedule['away_team_short'].append(rows['awayTeamInfo']['code'])
        schedule['away_team'].append(rows['awayTeamInfo']['names']['full'])
        schedule['away_score'].append(rows['awayTeamInfo']['score'])

        schedule['overtime'].append(1 if rows['overtime'] else 0)
        schedule['shootout'].append(1 if rows['shootout'] else 0)

        schedule['facility_id'].append(rows['venueInfo']['uuid'])
        schedule['facility'].append(rows['venueInfo']['name'])

        schedule['league_id'].append(rows['seriesInfo']['uuid'])
        schedule['league'].append(rows['seriesInfo']['code'])

    schedule_df = pd.DataFrame(schedule)
    schedule_df.winner.value_counts()
    # pd.DataFrame.from_dict()
    # pd.DataFrame(data["teamList"])
    # data["ssgtUuid"] # okay, this returns the ID for a season
