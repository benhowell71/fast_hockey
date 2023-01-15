import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from typing import List

from phf.phf_get_season_id import phf_get_season_id

def phf_league_info(season: int) -> List:
    season_id = phf_get_season_id(season=season)

    base_url = "https://web.api.digitalshift.ca/partials/stats/filters?type=season&id="
    # base_url = "https://web.api.digitalshift.ca/partials/stats/filters?type=season&id=1950&league_toggle=division"
    full_url = base_url + str(season_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        # for x in data:
            # print(x)
        league_info = []

        years = []
        for x in data['season']['options']:
            # print(x)
            year = {}

            doub = x['name'].split('-')

            year['season_id'] = x['id']
            year['season'] = x['name']
            year['single_season'] = int('20' + doub[1])
            year['type'] = x['type']
            year['league_id'] = x['league_id']
            year['points_win'] = x['view_settings']['points']['win']
            year['points_loss'] = x['view_settings']['points']['loss']
            year['points_tie'] = x['view_settings']['points']['tie']
            year['points_otw'] = x['view_settings']['points']['otw']
            year['points_otl'] = x['view_settings']['points']['otl']
            year['points_sow'] = x['view_settings']['points']['sow']
            year['points_sol'] = x['view_settings']['points']['sol']
            years.append(year)

        league = pd.DataFrame(years)
        # take ID from data['division']['options']
        divisions = pd.DataFrame(data['division']['options'])

        if season == 2023:
            division_id = divisions[divisions.name == 'PHF'].id.unique()[0]
        elif season == 2020:
            division_id = divisions[divisions.name == 'NWHL'].id.unique()[0]
        else:
            division_id = pd.DataFrame(data['team']['options']).division_id.unique()[0]

        if 'team' in data:
            teams = pd.DataFrame(data['team']['options'])
        else:
            teams = pd.read_csv('phf/id_2020.csv')
            teams = teams[teams.season == season]
            teams['division_id'] = division_id
        
        teams['name'] = np.where(teams.name == 'Toronto Toronto', 'Toronto Six', teams.name)
        # for x in data:
        #     print(x)
        # league = data['league']['options']
        # data['facility']['options']
        officials = pd.DataFrame(data['official']['options'])
        # data['bracket']['options']

        league_info = [league, divisions, officials, division_id, teams]

        return league_info

    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')