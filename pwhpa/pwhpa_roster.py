import pandas as pd
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

from pwhpa.helpers_pwhpa import process_member

def pwhpa_roster(team: str):

    full_url = "https://stats.pwhpa.com/members/"
    res = requests.get(full_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    img = soup.find_all('section')
    body = soup.find_all('tbody')

    body = body[0].find_all('tr')

    mems = pd.DataFrame()
    for i in np.arange(0, len(body)):
        player_info = body[i].find_all('td')
        player_df = process_member(player_info=player_info)

        mems = mems.append(player_df)

    headshot = img[2].find_all('img')

    links = []
    for i in np.arange(0, len(headshot)):
        links.append(headshot[i].get('src'))

    headshot = pd.DataFrame({
        'player_headshot': links
    })

    player_page = img[2].find_all('a')
    page = []
    for i in np.arange(0, len(player_page)):
        page.append(player_page[i].get('href'))

    page = pd.DataFrame({
        'player_page': page
    }).drop_duplicates().reset_index(drop=True).reset_index()

    headshot_subset = headshot[:len(page)].reset_index()

    photos = headshot_subset.merge(page, how='left', on='index').drop(columns=['index'])

    roster = mems.merge(photos, how='left', on='player_page')

    if team not in ['all', 'All', 'PWHPA']:
        team_roster = mems[mems.team_id == team.lower()]
    else:
        team_roster = mems

    return team_roster