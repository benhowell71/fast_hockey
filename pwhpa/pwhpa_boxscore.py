import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from pwhpa.helpers_pwhpa import (
    process_scores,
    process_offense_players,
    process_defense_players
)

def pwhpa_boxscore(game_id: str):
    # game_id = 'team-sonnet-vs-team-scotiabank'
    base_url = "https://stats.pwhpa.com/event/"
    full_url = base_url + game_id + '/'

    res = requests.get(full_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    tbody = soup.find_all('tbody')

    score_g = pd.DataFrame()

    score = tbody[1].find_all('tr')

    for i in np.arange(0, len(score)):
        score_info = score[i].find_all('td')
        score_g = score_g.append(process_scores(score_info=score_info))
        
    off1 = tbody[2].find_all('tr')
    off2 = tbody[4].find_all('tr')

    off1p = process_offense_players(off_players=off1)
    off2p = process_offense_players(off_players=off2)

    score_g.reset_index(inplace=True, drop=True)
    off1p['team'] = score_g.iloc[0].team
    off2p['team'] = score_g.iloc[1].team

    def1 = tbody[3].find_all('tr')
    def2 = tbody[5].find_all('tr')

    def1p = process_defense_players(off_players=def1)
    def2p = process_defense_players(off_players=def2)

    def1p['team'] = score_g.iloc[0].team
    def2p['team'] = score_g.iloc[1].team

    offense = pd.concat([off1p, off2p])
    defense = pd.concat([def1p, def2p])

    offense['game_id'] = game_id
    defense['game_id'] = game_id

    score_g['game_id'] = game_id

    res = [score_g, offense, defense]

    return res