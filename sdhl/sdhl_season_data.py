import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

def sdhl_seasons() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    this returns the seasonUuid values for each year
    there's a separate ssgtUuid

    this also returns the uuid for regular season vs playoffs

    Returns
    -------
    season_data: dataframe containing the season IDs for the schedule
        - the league ID is the series ID for the SDHL
        - seriesUuid is the league ID
        - seasonUuid argument
        - we will have 200 as a league common key
    
    game_type_data: dataframe containing IDs for each game type
        - gameTypeUuid argument
    """
    full_url = "https://www.sdhl.se/api/sports/season-series-game-types-filter" # this returns the ID for the schedule URL
    res = requests.get(full_url)
    data = json.loads(res.content.decode("utf-8"))
    szn = pd.DataFrame(data["season"])

    seasons = {
        'league': [],
        'league_id': [],
        'league_common_key': [],
        'season_id': [],
        'season_code': [],
        'season': [],
        'created_at': [],
        'modified_at': []
    }

    for index, rows in szn.iterrows():
        seasons['league'].append("SDHL")
        seasons['league_id'].append(data['series'][0]['uuid'])
        seasons['league_common_key'].append(200)
        seasons['season_id'].append(rows['uuid'])
        seasons['season_code'].append(rows['code'])
        seasons['season'].append(rows['names'][0]['translation'])
        seasons['created_at'].append(rows['createdAt'])
        seasons['modified_at'].append(rows['lastModified'])

    season_data = pd.DataFrame(seasons)

    game_types = pd.DataFrame(data['gameType'])

    game_type_ids = {
        'game_type_id': [],
        'game_type': [],
        'game_code': [],
        'game_series': [],
        'game_sdhl': []
    }

    for index, rows in game_types.iterrows():
        game_type_ids['game_type_id'].append(rows['uuid'])
        game_type_ids['game_code'].append(rows['code'])
        game_type_ids['game_sdhl'].append(rows['names'][0]['translation'])
        game_type_ids['game_series'].append(rows['names'][1]['translation'] if len(rows['names']) > 1 else None)

        if rows['code'] == 'playoff': 
            c = 'P'
        elif rows['code'] == 'regular':
            c = 'R'
        else:
            c = 'E'
        
        game_type_ids['game_type'].append(c)
    
    game_type_data = pd.DataFrame(game_type_ids)

    return season_data, game_type_data