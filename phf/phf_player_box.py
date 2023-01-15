import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from phf.phf_schedule import phf_schedule
from phf.helpers import (
    GAME_STAT_COLUMNS,
    GAME_FINAL_STAT_COLUMNS
)

def phf_player_box(game_id: int):
    # game_id = 420339

    base_url = "https://web.api.digitalshift.ca/partials/stats/game/team-stats?game_id="
    full_url = base_url + str(game_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        data = data['content']
        soup = BeautifulSoup(data, 'html.parser')

        tms = []
        names = []
        ids = []
        for x in soup.find_all('a', href = True):
            # print(x)
            if re.search(r"stats", x["href"]):
                names.append(re.search(r">(.*)<", str(x)).group(1))
                ids.append(re.search(r"[0-9]+", str(x['href'])).group(0))
            else:
                # x = str(x)
                tms.append(re.search(r">(.*)<", str(x)).group(1))

        info = pd.DataFrame({
            'player_name': names,
            'player_id': ids
        }).drop_duplicates().reset_index(drop = True)

        away_tm = tms[0]
        home_tm = tms[1]

        # len(soup.find_all('table'))
        away_skaters = soup.find_all('table')[1]
        away_skaters_df = pd.read_html(str(away_skaters))[0]
        away_skaters_df['team'] = away_tm
        away_goalies = soup.find_all('table')[3]
        away_goalies_df = pd.read_html(str(away_goalies))[0]
        away_goalies_df['team'] = away_tm

        home_skaters = soup.find_all('table')[5]
        home_skaters_df = pd.read_html(str(home_skaters))[0]
        home_skaters_df['team'] = home_tm
        home_goalies = soup.find_all('table')[7]
        home_goalies_df = pd.read_html(str(home_goalies))[0]
        home_goalies_df['team'] = home_tm

        skaters = pd.concat([home_skaters_df, away_skaters_df])
        goalies = pd.concat([home_goalies_df, away_goalies_df])

        if len(skaters) > 0:
            skaters['Name'] = skaters.Name.str.replace("#\w+", "")

            skaters.columns = GAME_STAT_COLUMNS
            skaters = skaters.merge(info, how='left', on='player_name')

            skaters['game_id'] = game_id
            skaters['shot_pct'] = np.round(skaters['goals'] / skaters['shots_on_goal'], 3)

            skaters = skaters[GAME_FINAL_STAT_COLUMNS]
        else:
            skaters = pd.DataFrame(columns=GAME_FINAL_STAT_COLUMNS)
        
        if len(goalies) > 0:
            goalies['Name'] = goalies.Name.str.replace("#\w+", "")
            goalies = goalies.merge(info, how='left', left_on='Name', right_on='player_name')
            goalies = goalies.rename(columns={
                '#': 'jersey',
                'SA': 'shots_against',
                'GA': 'goals_allowed',
                'Sv': 'saves',
                'Sv%': 'save_pct',
                # 'MP': 'minutes_played',
                'PIM': 'penalty_minutes',
                'G': 'goals',
                'A': 'assists'
            })

            goalies[['minutes', 'seconds']] = goalies.MP.str.split(':', expand=True)
            goalies['minutes_played'] = np.round(goalies['seconds'].astype(int) / 60, 2) + goalies['minutes'].astype(int)
            goalies['time_on_ice'] = goalies.MP

            goalies['game_id'] = game_id

            goalies = goalies[['player_name', 'player_id', 'team', 'jersey', 'game_id', 'time_on_ice', 'minutes_played', 
                        'shots_against', 'saves', 'goals_allowed', 'save_pct', 'penalty_minutes', 'goals', 'assists']]
        else:
            goalies = pd.DataFrame(columns=['player_name', 'player_id', 'team', 'jersey', 'game_id', 'time_on_ice', 'minutes_played', 
                        'shots_against', 'saves', 'goals_allowed', 'save_pct', 'penalty_minutes', 'goals', 'assists'])

        return [skaters, goalies]
    
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')