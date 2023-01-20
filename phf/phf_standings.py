import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from phf.phf_league_info import phf_league_info
from phf.helpers import (
    STANDINGS_COLS,
    FINAL_STANDING_COLS
)

def phf_standings(season: int) -> pd.DataFrame:

    logos = pd.read_csv('phf/logos.csv')

    lg_info = phf_league_info(season=season)
    lg = lg_info[0]
    season_df = lg[lg.single_season == season]
    season_id = season_df.season_id.item()
    league_id = lg_info[3] 
    base_url = "https://web.api.digitalshift.ca/partials/stats/standings/table?division_id=" + str(league_id) + "&league_toggle=division&season_id="
    # base_url = "https://web.api.digitalshift.ca/partials/stats/filters?type=season&id=4667&league_toggle=division"
    full_url = base_url + str(season_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    if season in [2020, 2023]:
        n = 3
    else:
        n = 0

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        soup = BeautifulSoup(data['content'], 'html.parser')

        tbody = soup.find_all('table')[n]
        standings = pd.read_html(str(tbody))[0]
        # standings

        standings['Team'] = standings.Team.str.replace("[0-9]+", "")
        # standings['team_abbrev'] = standings.Team.str[-3:]
        standings['Team'] = standings.Team.str[:-3]
        standings.columns = STANDINGS_COLS
        standings['season'] = season
        standings['team_name'] = np.where(standings.team_name == 'Toronto Toronto', 'Toronto Six', standings.team_name)
        standings = standings.merge(logos, how='left', left_on='team_name', right_on='full_team_name')
        standings['league_id'] = league_id
        standings['season_id'] = season_id
        standings['league'] = 'PHF'

        standings['games_played'] = standings['gp']

        standings = standings[standings.games_played > 0]

        # standings = standings[['team_name',
        #     'league_id',
        #     'season', 'team_id', 'gp', 'wins', 'losses', 'ties', 'points',
        #     'regulation_wins', 'overtime_wins', 'shootout_wins', 'goals_scored',
        #     'goals_allowed', 'goal_differential', 'penalty_minutes', 'next_game', 
        #     'full_team_name', 'team_abbr', 'team_nick',
        #     'team_location', 'team_color1', 'team_color2', 'team_logo']]
        standings = standings[FINAL_STANDING_COLS]

        return standings
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')
