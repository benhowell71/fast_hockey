"""ready to test PHF Team Rosters"""
import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime
from tqdm import tqdm

from phf.phf_get_season_id import phf_get_season_id
from phf.phf_league_info import phf_league_info
from phf.helper_functions import phf_get_player_photo

from phf.helpers import (
    ROSTER_NAMES,
    ROSTER_COLUMNS
)

def phf_roster(team: str, season: int) -> pd.DataFrame:
    # team = 'Boston Pride'
    season_id = phf_get_season_id(season=season)
    teams = phf_league_info(season=season)[4]
    team_id = teams[teams.name == team].id.item()
    # teams = pd.read_csv('phf/logos.csv')
    # if season != 2023:
    #     
    # elif season == 2020:
    #     teams = pd.read_csv('phf/id_2020.csv')
    #     team_id = teams[teams.team_name == team].id.item()
    # else:
    #     team_id = teams[teams.full_team_name == team].team_id.item()
    base_url = "https://web.api.digitalshift.ca/partials/stats/team/roster?team_id="
    full_url = base_url + str(team_id)
    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        soup = BeautifulSoup(data['content'], 'html.parser')
        # players = soup.find_all('table')[0]
        names = []
        ids = []
        link = []
        player_data = pd.DataFrame()
        for t in np.arange(0, len(soup.find_all('table'))):
            players = soup.find_all('table')[t]
            players_df = pd.read_html(str(players))[0]

            if len(players_df.dropna(axis='columns', how='all').columns) > 2:
                # players_df = players_df.iloc[:, 0:5]
                players_df = players_df.dropna(axis='columns', how='all')
                for y in tqdm(players.find_all('a', {'class': 'person-inline'})):
                    id = re.search(r"[0-9]+", y["href"])
                    player_id = id.group(0)
                    if player_id not in ids:
                        name = re.search(r">(.*)<", str(y)).group(1)
                        photo_link = phf_get_player_photo(id=player_id)

                        link.append(photo_link)
                        names.append(name)
                        ids.append(player_id)
                        
                player_data = player_data.append(players_df)

        info = pd.DataFrame({
            'Name': names,
            'player_id': ids,
            'player_photo': link
        }).drop_duplicates()

        player_df = player_data.drop_duplicates().reset_index(drop=True).merge(info, how='left', on='Name')

        player_df['is_captain'] = np.where(player_df.Name.str.contains('- C') | player_df.Name.str.contains(' - A'), 1, 0)
        player_df['Name'] = player_df.Name.str.replace('- C', '')
        player_df['Name'] = player_df.Name.str.replace('- A', '')

        if 'Height' in player_df.columns:
            player_df['height'] = player_df['Height'].str.replace("'|\"", '')
            player_df[['feet', 'inches']] = player_df['height'].str.split(' ', expand=True)
            player_df = player_df.drop(columns=['height'])
        else:
            player_df[['feet', 'inches']] = np.nan
            player_df['Height'] = np.nan
        
        if 'Hometown' not in player_df.columns:
            player_df['Hometown'] = np.nan
            player_df = player_df[['#', 'Name', 'POS', 'Height', 'Hometown', 'player_id',
                        'player_photo', 'is_captain', 'feet', 'inches']]

        if 'Birthdate' not in player_df.columns:
            player_df['Birthdate'] = np.nan
            player_df = player_df[['#', 'Name', 'POS', 'Height', 'Hometown', 'player_id',
                        'player_photo', 'is_captain', 'feet', 'inches', 'Birthdate']]

        if 'Country' not in player_df.columns:
            player_df['Country'] = np.nan
            player_df = player_df[['#', 'Name', 'POS', 'Height', 'Hometown', 'player_id',
                        'player_photo', 'is_captain', 'feet', 'inches', 'Birthdate', 'Country']]

        if 'College' not in player_df.columns:
            player_df['College'] = np.nan
            player_df = player_df[['#', 'Name', 'POS', 'Height', 'Birthdate', 'Country', 'Hometown', 'College', 'player_id',
                        'player_photo', 'is_captain', 'feet', 'inches']]

        player_df = player_df[['#', 'Name', 'POS', 'Height', 'Birthdate', 'Country', 'Hometown', 'College', 'player_id',
                        'player_photo', 'is_captain', 'feet', 'inches']]
        player_df.columns = ROSTER_NAMES
        player_df['season'] = season
        player_df['team'] = team
        player_df['team_id'] = team_id
        player_df['season_id'] = season_id
        player_df['league'] = 'PHF'
        player_df['league_id'] = 100
        player_df = player_df[ROSTER_COLUMNS]

        #############################################################
        try:
            staff = soup.find_all('table')[len(soup.find_all('table')) - 1]
            staff = pd.read_html(str(staff))[0]
            if len(staff.columns) == 2:
                staff.columns = ['staff_name', 'staff_role']
            else:
                staff = pd.DataFrame(columns=['staff_name', 'staff_role'])
        except:
            staff = pd.DataFrame(columns=['staff_name', 'staff_role'])

        info = [player_df, staff]
        
        return info
    
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')