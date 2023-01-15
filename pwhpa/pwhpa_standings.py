import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from pwhpa.pwhpa_columns import (
    STANDINGS_COLS,
    STANDINGS_ORDER
)

def pwhpa_standings():

    logos = pd.read_csv('pwhpa/pwhpa_teams.csv')
    full_url = "https://stats.pwhpa.com/table/sdgt-standings/"
    full_url = "https://stats.pwhpa.com/wp-json/sportspress/v2/tables"

    res = requests.get(full_url)
    data = json.loads(res.content.decode('utf-8'))
    # soup = BeautifulSoup(res.content, 'html.parser')

    # pd.read_html(soup.find_all('tbody')[0])
    standings = pd.DataFrame.from_dict(data[0]['data']).T.reset_index()
    standings = standings.loc[0:3]

    standings['name'] = np.where(standings.name.str.contains('Harvey'), "Harvey's", standings.name)
    standings['strk'] = standings.strk.str.replace('<span style="color:#888888">', '')
    standings['strk'] = standings.strk.str.replace('</span>', '')

    standings = standings.rename(columns={'index': 'team_id'})

    standings = standings[STANDINGS_ORDER]
    standings.columns = STANDINGS_COLS
    standings = standings.astype(
        {
            'team_id': 'int',
            'rank': 'int',
            'gp': 'int',
            'w': 'int',
            'l': 'int',
            'otw': 'int',
            'ot': 'int',
            'pts': 'int',
            'gf': 'int',
            'ga': 'int',
            'goal_diff': 'int',
            'power_play_goals': 'int',
            'power_plays': 'int',
            'power_play_pct': 'float',
            'power_play_goals_allowed': 'int',
            'power_plays_against': 'int',
            'penalty_kill_pct': 'float'
        }
    )

    standings['power_play_pct'] = standings['power_play_pct'] / 100
    standings['penalty_kill_pct'] = standings['penalty_kill_pct'] / 100

    return standings