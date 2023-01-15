import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from phf.phf_get_season_id import phf_get_season_id
from phf.helpers import (
    PHF_SCHEDULE,
    SCHEDULE_COLUMNS
)

def phf_schedule(season: int):
    # season = 2023
    season_id = phf_get_season_id(season=season)

    base_url = "https://web.api.digitalshift.ca/partials/stats/schedule/table?limit=100&all=true&season_id="
    full_url = base_url + str(season_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:

        res = requests.get(full_url, headers=payload)

        data = json.loads(res.content.decode('utf-8'))
        data = data['content']
        soup = BeautifulSoup(data, 'html.parser')
        tbody = soup.find_all('tbody')
        ng_init = tbody[0]['ng-init']

        ng_init = re.sub(r'ctrl\.schedule=', '', ng_init)

        schedule_data = json.loads(ng_init)

        df = pd.DataFrame()
    
        for i in np.arange(0, len(schedule_data)):
            df = df.append(pd.DataFrame(schedule_data[i]).filter(items=['full'], axis=0))

        df.reset_index(inplace=True, drop=True)

        df['winner'] = np.where(df.home_score > df.away_score, df.home_team, 
                        np.where(df.away_score > df.home_score, df.away_team,
                            np.where((df.home_team == df.away_team) & (df.status == 'Final'), 'Tie',
                                np.where((df.home_team == df.away_team) & (df.status != 'Final'), '', np.nan))))

        df = df.rename(columns={"date_group": "game_date"})
        df = df[PHF_SCHEDULE]

        df['league'] = 'PHF'
        df['season'] = season
        df['game_type'] = df.game_type.str[:1]

        df = df[SCHEDULE_COLUMNS]
        # df.pop('winner')
        # df.insert(6, 'winner', df.pop('winner'))

        return df
    
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')