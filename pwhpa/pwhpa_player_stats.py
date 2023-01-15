import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from pwhpa.helpers_pwhpa import process_stats

def pwhpa_player_stats(position: str):

    if position == 'skaters':
        full_url = "https://stats.pwhpa.com/list/scoring-leaders/"
    elif position == 'goalies':
        full_url = "https://stats.pwhpa.com/list/goaltending/"

    res = requests.get(full_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    tbody = soup.find_all('tbody')

    rows = tbody[0].find_all('tr')

    stats = pd.DataFrame()
    for i in np.arange(0, len(rows)):
        player_info = rows[i].find_all('td')
        pstats = process_stats(position=position, player_info=player_info)

        stats = stats.append(pstats)

    return stats
