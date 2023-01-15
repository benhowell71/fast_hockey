import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime
from tqdm import tqdm

# from phf.phf_get_season_id import phf_get_season_id
# from phf.helper_functions import phf_get_player_photo
from phf.phf_league_info import phf_league_info

from phf.helpers import (
    TEAM_SKATER_COLS,
    FINAL_STAT_COLUMNS,
    TEAM_GOALIE_COLS,
    FINAL_GOALIE_COLUMNS
)

def phf_team_stats(team: str, season: int) -> pd.DataFrame:
    # team = 'Boston Pride'
    # season_id = phf_get_season_id(season=season)

    # teams = pd.read_csv('phf/logos.csv')
    # team_id = teams[teams.full_team_name == team].team_id.item()
    lg = phf_league_info(season=season)
    szn_id = lg[0]
    szn_id = szn_id[szn_id.single_season == season].season_id.item()
    teams = lg[4]
    team_id = teams[teams.name == team].id.item()

    base_url = "https://web.api.digitalshift.ca/partials/stats/team/stats?team_id="
    full_url = base_url + str(team_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        soup = BeautifulSoup(data['content'], 'html.parser')

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

        rs_skaters = pd.read_html(str(soup.find_all('table')[1]))[0]
        rs_goalies = pd.read_html(str(soup.find_all('table')[3]))[0]

        rs_skaters['season_type'] = 'regular_season'
        rs_goalies['season_type'] = 'regular_season'

        if len(soup.find_all('table')) > 6:
            po_skaters = pd.read_html(str(soup.find_all('table')[5]))[0]
            po_goalies = pd.read_html(str(soup.find_all('table')[7]))[0]

            po_skaters['season_type'] = 'playoffs'
            po_goalies['season_type'] = 'playoffs'

            skaters = pd.concat([rs_skaters, po_skaters])
            goalies = pd.concat([rs_goalies, po_goalies])
        elif len(soup.find_all('table')) == 6:
            inactive = pd.read_html(str(soup.find_all('table')[5]))[0]
            inactive['season_type'] = 'regular_season_inactive'
            skaters = pd.concat([rs_skaters, inactive])
            goalies = rs_goalies
        else:
            skaters = rs_skaters
            goalies = rs_goalies

        skaters['Name'] = skaters.Name.str.replace("#\w+", "")
        goalies['Name'] = goalies.Name.str.replace("#\w+", "")

        skaters = skaters.rename(columns={'Name': 'player_name'}).merge(info, how='left', on='player_name')
        goalies = goalies.rename(columns={'Name': 'player_name'}).merge(info, how='left', on='player_name')

        skaters[['faceoff_won', 'faceoff_lost']] = skaters['FoW/L'].str.split(' - ', expand=True)
        skaters['team'] = team
        skaters.columns = TEAM_SKATER_COLS
        skaters['season'] = season
        skaters['season_id'] = szn_id
        skaters['division_id'] = teams.division_id.unique()[0]
        skaters['league'] = 'PHF'
        skaters['league_id'] = 100
        skaters['team_id'] = team_id

        skaters = skaters[FINAL_STAT_COLUMNS]

        goalies[['minutes', 'seconds']] = goalies.MP.str.split(':', expand=True)
        goalies['minutes_played'] = np.round(goalies['seconds'].astype(int) / 60, 2) + goalies['minutes'].astype(int)
        goalies['team'] = team

        goalies.columns = TEAM_GOALIE_COLS
        # goalies = goalies.merge(info, how='left', on='player_name')

        goalies['season'] = season
        goalies['season_id'] = szn_id
        goalies['division_id'] = teams.division_id.unique()[0]
        goalies['league'] = 'PHF'
        goalies['league_id'] = 100
        goalies['position'] = 'G'
        goalies['team_id'] = team_id

        goalies = goalies[FINAL_GOALIE_COLUMNS]

        return [skaters, goalies]

    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')