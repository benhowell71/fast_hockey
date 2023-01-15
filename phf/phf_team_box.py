import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime
from tqdm import tqdm

from phf.helper_functions import helper_phf_team_box

# from PHF.phf_get_season_id import phf_get_season_id
# from PHF.helper_functions import phf_get_player_photo

def phf_team_box(game_id: int) -> pd.DataFrame:
    # game_id = 420339
    # game_id = 612254 # for shootout
    base_url = "https://web.api.digitalshift.ca/partials/stats/game/play-by-play?game_id="
    full_url = base_url + str(game_id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))
        soup = BeautifulSoup(data['content'], 'html.parser')
        tables = soup.find_all('table')

        team_box = helper_phf_team_box(tables=tables, game_id = game_id)

        return team_box
        
    except:
        print(f'{datetime.now()}: Invalid arguments or season; please try a season from 2016 onwards.\n I.e. If you want data for the 2015-2016 season, please enter 2016 as the season.')