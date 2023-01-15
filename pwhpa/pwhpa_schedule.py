import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from pwhpa.helpers_pwhpa import process_game

def pwhpa_schedule():

    full_url = "https://stats.pwhpa.com/calendar/secret-dream-gap-tour-schedule/"

    res = requests.get(full_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    tbody = soup.find_all('tbody')

    g = tbody[0].find_all('tr')

    schedule = pd.DataFrame()
    for i in np.arange(0, len(g)):
        game_info = g[i].find_all('td')
        game_df = process_game(game_info=game_info)

        schedule = schedule.append(game_df)

    # n = 3
    # tbody = soup.find_all('table')[0]
    # schedule = pd.read_html(str(tbody))[0]
    return schedule
