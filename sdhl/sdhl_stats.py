import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

def sdhl_stats() -> pd.DataFrame:

    base_url = "https://www.sdhl.se/api/statistics/stat-info/players_summary?ssgtUuid=qbO-5Eadc4G0L&count=500"
    full_url = "https://www.sdhl.se/api/statistics/stat-info/players_summary?ssgtUuid=qbO-5Eadc4G0L&count=500"

    res = requests.get(full_url)

    data = json.loads(res.content.decode('utf-8'))
    df = pd.DataFrame(data)
    stats_df = pd.json_normalize(df['stats'])

    stats_dict = {
        'first_name': [],
        'last_name': [],
        'player_id': [],
        'position': [],
        'team_id': [],
        'date_of_birth': [],
        'games_played': [],
        'total_points': [],
        'goals': [],
        'assists': [],
        'shots_on_goal': [],
        'points_per_game': [],
        'game_winning_goals': [],
        'plus': [],
        'minus': [],
        'plus_minus': [],
        'penalty_minutes': [],
        'blocks': [],
        'hits': [],
        'time_on_ice': []
    }

    for i in np.arange(0, len(stats_df.columns)):

        player = stats_df[i].to_dict()[0]
        
        stats_dict['first_name'].append(player['info.firstName'])
        stats_dict['last_name'].append(player['info.lastName'])
        stats_dict['player_id'].append(player['PlayerId'])
        stats_dict['position'].append(player['info.position'])
        stats_dict['team_id'].append(player['TeamId'])
        stats_dict['date_of_birth'].append(player['info.birthdate'])
        stats_dict['games_played'].append(player['GP'])
        stats_dict['total_points'].append(player['TP'])
        stats_dict['goals'].append(player['G'])
        stats_dict['assists'].append(player['A'])
        stats_dict['shots_on_goal'].append(player['SOG'])
        stats_dict['points_per_game'].append(player['PPG'])
        stats_dict['game_winning_goals'].append(player['GWG'])
        stats_dict['plus'].append(player['Plus'])
        stats_dict['minus'].append(player['Minus'])
        stats_dict['plus_minus'].append(player['PlusMinus'])
        stats_dict['penalty_minutes'].append(player['PIM'])
        stats_dict['blocks'].append(player['BkS'])
        stats_dict['hits'].append(player['Hits'])
        stats_dict['time_on_ice'].append(player['TOIGP'])
    
    stats_results = pd.DataFrame(stats_dict)
    
    teams = df['teams'].item()
    sdhl_teams = {
        'team_name': [],
        'team_abb': [],
        'team_id': [],
        'team_uuid': [],
        'team_nationality': [],
        'team_code': [],
        'team_logo': [],
        'team_url': [],
        'team_founded': []
    }

    for i in teams:
        sdhl_teams['team_name'].append(teams[i]['teamNames']['long'])
        sdhl_teams['team_abb'].append(teams[i]['teamNames']['short'])
        sdhl_teams['team_id'].append(i)
        sdhl_teams['team_uuid'].append(teams[i]['uuid'])
        sdhl_teams['team_nationality'].append(teams[i]['nationality'])
        sdhl_teams['team_code'].append(teams[i]['teamCode'])
        sdhl_teams['team_logo'].append(teams[i]['teamMedia'])
        sdhl_teams['team_url'].append(teams[i]['publicUrl'])
        sdhl_teams['team_founded'].append(teams[i]['teamInfo']['founded'] if 'founded' in teams[i]['teamInfo'] else None)

    team_df = pd.DataFrame(sdhl_teams)
    
    players = df['players'].item()

    player_df = {
        'first_name': [],
        'last_name': [],
        'full_name': [],
        'player_id': [],
        'player_uuid': [],
        'date_of_birth': [],
        'team_uuid': [],
        'jersey': [],
        'nationality': [],
        'weight': [],
        'height': [],
        'handedness': [],
        'captain': [],
        'player_photo': []
    }
    
    for i in players:
        player_list = players[i]
        team_id = [x for x in player_list['teamPlayers']][0] if len(player_list['teamPlayers']) > 0 else None
        player_df['first_name'].append(player_list['firstName'] if 'firstName' in player_list else None)
        player_df['last_name'].append(player_list['lastName'] if 'lastName' in player_list else None)
        player_df['full_name'].append(player_list['fullName'] if 'fullName' in player_list else None)
        player_df['player_id'].append(i)
        player_df['player_uuid'].append(player_list['uuid'] if 'uuid' in player_list else None)
        player_df['date_of_birth'].append(player_list['dateOfBirth'][:10] if 'dateOfBirth' in player_list else None)
        player_df['team_uuid'].append(team_id)
        player_df['jersey'].append(player_list['teamPlayers'][team_id]['defaultJersey'] if len(player_list['teamPlayers']) > 0 and 'defaultJersey' in player_list['teamPlayers'][team_id] else None)
        player_df['nationality'].append(player_list['nationality'] if 'nationality' in player_list else None)
        player_df['height'].append(player_list['height'] if 'height' in player_list else None)
        player_df['weight'].append(player_list['weight'] if 'weight' in player_list else None)
        player_df['handedness'].append(player_list['shoots'][:1].upper() if 'shoots' in player_list else None)
        player_df['captain'].append(player_list['teamPlayers'][team_id]['captain'] if len(player_list['teamPlayers']) > 0 and 'captain' in player_list['teamPlayers'][team_id] else None)
        player_df['player_photo'].append(player_list['renderedLatestPortrait']['url'] if 'renderedLatestPortrait' in player_list else 'https://sportality.cdn.s8y.se/default-images/player/default-no-gender_grey.png')

    player_info = pd.DataFrame(player_df)