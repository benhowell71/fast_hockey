from phf.phf_league_info import phf_league_info

import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from phf.helpers import (
    STAT_COLUMNS,
    FINAL_STAT_COLUMNS,
    GOALIE_COL,
    FINAL_GOALIE_COLUMNS
)

def phf_leaders(player_type: str, season: int, season_type = 'Regular Season') -> pd.DataFrame:
    # season = 2023
    lg_info = phf_league_info(season=season)
    lg = lg_info[0]
    season_df = lg[lg.single_season == season]
    season_id = season_df.season_id.item()
    league_id = lg_info[3] # 13893 for 2023
    season_type = season_type.replace(' ', '+')
    
    if player_type == 'skaters': 
        player_type = 'players'

    base_url = "https://web.api.digitalshift.ca/partials/stats/leaders/table?player_type="
    full_url = base_url + player_type + "&division_id=" + str(league_id) + "&game_type=" + str(season_type) + "&season_id=" + str(season_id) + "&limit=350&all=true"

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))

        data = data['content']
        soup = BeautifulSoup(data, 'html.parser')
        tbody = soup.find_all('table')[0]
        stats = pd.read_html(str(tbody))[0]

        names = []
        ids = []
        for y in tbody.find_all('a', {'class': 'person-inline'}):
            id = re.search(r"[0-9]+", y["href"])
            player_id = id.group(0)
            name = re.search(r">(.*)<", str(y)).group(1)
            names.append(name)
            ids.append(player_id)

        info = pd.DataFrame({
            'player_name': names,
            'player_id': ids
        })

        stats['Name'] = stats.Name.str.replace("#\w+", "")

        if player_type == 'players':

            stats.columns = STAT_COLUMNS
            stats = stats.merge(info, how='left', on='player_name')

            stats[['faceoff_won', 'faceoff_lost']] = stats.faceoff_record.str.split(' - ', expand=True)

            stats['season_type'] = season_type.lower().replace('+', '_')
            stats['season'] = season
            stats['season_id'] = season_id
            stats['division_id'] = league_id
            stats['league'] = 'PHF'

            stats = stats[FINAL_STAT_COLUMNS]
        elif player_type == 'goalies':

            stats[['minutes', 'seconds']] = stats.MP.str.split(':', expand=True)
            stats['minutes_played'] = np.round(stats['seconds'].astype(int) / 60, 2) + stats['minutes'].astype(int)

            stats.columns = GOALIE_COL
            stats = stats.merge(info, how='left', on='player_name')

            stats['season_type'] = season_type.lower().replace('+', '_')
            stats['season'] = season
            stats['season_id'] = season_id
            stats['division_id'] = league_id
            stats['league'] = 'PHF'
            stats['position'] = 'G'

            stats = stats[FINAL_GOALIE_COLUMNS]
        else:
            print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season. And enter either players or goalies.')

        return stats
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')
