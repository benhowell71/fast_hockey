import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import math

def process_game(game_info) -> pd.DataFrame:

    date_time = game_info[0].text[0:19]
    date = game_info[0].text[19:len(game_info[0].text)]

    home_tm = game_info[1].text.strip()
    away_tm = game_info[3].text.strip()

    if 'am' in game_info[2].text or 'pm' in game_info[2].text:
        start_time = game_info[2].text
        home_score = np.nan
        away_score = np.nan
    else:
        res = game_info[2].text.split('-')
        home_score = int(res[0].strip())
        away_score = int(res[1].strip())
        start_time = np.nan

    location = game_info[4].text
    game_link = game_info[5].find_all('a')[0].get('href')
    game_id = game_link.replace('https://stats.pwhpa.com/event/', '')
    game_id = game_id.replace('/', '')

    winner = np.where(home_score > away_score, home_tm, np.where(away_score > home_score, away_tm, np.where(math.isnan(home_score), np.nan, 'tie'))).item()

    game_df = pd.DataFrame({
        'game_date': [date],
        'game_time': [date_time],
        'game_id': [game_id],
        'winner': [winner],
        'home_team': [home_tm],
        'home_score': [home_score],
        'away_team': [away_tm],
        'away_score': [away_score],
        'start_time': [start_time],
        'location': [location],
        'game_link': [game_link]
    })

    return game_df

def process_member(player_info):

    jersey = player_info[0].text
    name = player_info[1].text
    player_link = player_info[1].find_all('a')[0].get('href')
    names = name.split(' ')
    first_name = names[0]
    last_name = names[1]
    link = player_info[2].find_all('a')[0].get('href')
    team = link.replace('https://stats.pwhpa.com/team/', '')
    team_id = team.replace('/', '')

    position = player_info[3].text
    dob = player_info[4].text
    age = player_info[5].text
    home_town = player_info[6].text
    college = player_info[7].text

    player_df = pd.DataFrame({
        'player_name': [name],
        'first_name': [first_name],
        'last_name': [last_name],
        'team_id': [team_id],
        'position': [position],
        'number': [jersey],
        'date_of_birth': [dob],
        'age': [age],
        'home_town': [home_town],
        'college': [college],
        'player_page': [player_link]
    })

    return player_df

def process_stats(position: str, player_info):

    if position == 'skaters':
        jersey = player_info[0].text
        name = player_info[1].text
        player_link = player_info[1].find_all('a')[0].get('href')
        names = name.split(' ')
        first_name = names[0]
        last_name = names[1]
        link = player_info[2].find_all('a')[0].get('href')
        team = link.replace('https://stats.pwhpa.com/team/', '')
        team_id = team.replace('/', '')

        pos = player_info[3].text

        gp = player_info[4].text
        g = player_info[5].text
        a = player_info[6].text
        pts = player_info[7].text
        pim = player_info[8].text

        player_df = pd.DataFrame({
        'player_name': [name],
        'first_name': [first_name],
        'last_name': [last_name],
        'team_id': [team_id],
        'position': [pos],
        # 'number': [jersey],
        'games_played': [gp],
        'goals': [g],
        'assists': [a],
        'points': [pts],
        'penalty_minutes': [pim]
        })

    elif position == 'goalies':
        jersey = player_info[0].text # this is actually rank
        name = player_info[1].text
        player_link = player_info[1].find_all('a')[0].get('href')
        names = name.split(' ')
        first_name = names[0]
        last_name = names[1]
        link = player_info[2].find_all('a')[0].get('href')
        team = link.replace('https://stats.pwhpa.com/team/', '')
        team_id = team.replace('/', '')

        pos = 'G'
        gp = player_info[3].text
        w = player_info[4].text
        ga = player_info[5].text
        gaa = player_info[6].text
        sa = player_info[7].text
        svs = player_info[8].text
        sv_pct = player_info[9].text
        so = player_info[10].text
        toi = player_info[11].text

        time = toi.split(':')
        mp = np.round(int(time[0]) + (int(time[1]) / 60), 2)  * 60

        player_df = pd.DataFrame({
            'player_name': [name],
            'first_name': [first_name],
            'last_name': [last_name],
            'team_id': [team_id],
            'position': [pos],
            # 'number': [jersey],
            'games_played': [gp],
            'wins': [w],
            'shots_against': [sa],
            'goals_against': [ga],
            'saves': [svs],
            'save_pct': [sv_pct],
            'gaa': [gaa],
            'shutouts': [so],
            'time_on_ice': [toi],
            'minutes_played': [mp]
        })

    return player_df

def process_scores(score_info):

    points = pd.read_csv('pwhpa/points.csv')

    if len(score_info) == 9:
        team = score_info[0].text
        first = score_info[1].text
        second = score_info[2].text
        third = score_info[3].text
        ot = np.nan
        final = score_info[4].text
        ppo = score_info[5].text
        ppg = score_info[6].text
        sog = score_info[7].text
        res = score_info[8].text.lower()
    elif len(score_info) == 10:
        team = score_info[0].text
        first = score_info[1].text
        second = score_info[2].text
        third = score_info[3].text
        ot = score_info[4].text
        final = score_info[5].text
        ppo = score_info[6].text
        ppg = score_info[7].text
        sog = score_info[8].text
        res = score_info[9].text.lower()
    elif len(score_info) == 3:
        team = score_info[0].text
        first = np.nan
        second = np.nan
        third = np.nan
        ot = np.nan
        final = score_info[1].text
        ppo = np.nan
        ppg = np.nan
        sog = np.nan
        res = score_info[2].text.lower()

    score = pd.DataFrame({
        'team': [team],
        'first': [first],
        'second': [second],
        'third': [third],
        'ot': [ot],
        'final': [final],
        'power_play_opps': [ppo],
        'power_play_goals': [ppg],
        'shots_on_goal': [sog],
        'result': [res]
    }).merge(points, how='left', on='result')

    return score

def process_offense(player):
    name = player[1].text
    jersey = player[0].text
    pos = player[2].text
    goals = player[3].text
    assists = player[4].text
    pim = player[5].text

    player_df = pd.DataFrame({
        'player_name': [name],
        'jersey': [jersey],
        'position': [pos],
        'goals': [goals],
        'assists': [assists],
        'penalty_minutes': [pim]
    })

    return player_df

def process_defense(player):
    number = player[0].text
    name = player[1].text
    pos = player[2].text
    winner = player[3].text
    ga = player[4].text
    sa = player[5].text
    sv = player[6].text
    so = player[7].text
    toi = player[8].text

    if sa == '0':
        sv_pct = np.nan
    else:
        sv_pct = round((int(sv) / int(sa)), 3)
        # sv_pct = np.where(int(sa) > 0, (int(sv) / int(sa)), np.nan)

    time = toi.split(':')
    mp = np.round(int(time[0]) + (int(time[1]) / 60), 2)

    dff = pd.DataFrame({
        'player_name': [name],
        'jersey': [number],
        'position': [pos],
        'winner': [winner],
        'goals_allowed': [ga],
        'shots_against': [sa],
        'saves': [sv],
        'save_pct': [sv_pct],
        'gaa': [np.nan],
        'shutout': [so],
        'time_on_ice': [toi],
        'minutes_played': [mp]
    })

    return dff

def process_offense_players(off_players):

    off = pd.DataFrame()

    for i in np.arange(0, len(off_players)):
        player = off_players[i].find_all('td')
        off = off.append(process_offense(player=player))
    
    off['star_of_game'] = off.player_name.str.extract(r'(\d)')
    off = off.astype({'star_of_game': 'float'})
    off['player_name'] = off.player_name.str.replace(r'(\d)', '')
    off['player_name'] = off.player_name.str.strip()

    return off

def process_defense_players(off_players):

    off = pd.DataFrame()

    for i in np.arange(0, len(off_players)):
        player = off_players[i].find_all('td')
        off = off.append(process_defense(player=player))
    
    off['star_of_game'] = off.player_name.str.extract(r'(\d)')
    off = off.astype({'star_of_game': 'float'})
    off['player_name'] = off.player_name.str.replace(r'(\d)', '')
    off['player_name'] = off.player_name.str.strip()
    off['minutes_played'] = off.minutes_played * 60

    return off