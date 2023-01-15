import requests
import json
import re

import pandas as pd
import numpy as np

from phf.helpers import (
    START_NAMES,
    IN_PROG_NAMES,
    REG_NAMES,
    OT_ONLY_NAMES,
    SHOOTOUT_SCORING_INIT_NAMES,
    SHOOTOUT_NAMES,
    SHOOTOUT_SHOT_INIT_NAMES,
    SHOOTOUT_SHOT_NAMES
)

def phf_get_player_photo(id: int):
    # id = 627750
    base_url = "https://web.api.digitalshift.ca/partials/stats/player?player_id="
    full_url = base_url + str(id)

    payload = {
        'Authorization': 'ticket="4dM1QOOKk-PQTSZxW_zfXnOgbh80dOGK6eUb_MaSl7nUN0_k4LxLMvZyeaYGXQuLyWBOQhY8Q65k6_uwMu6oojuO"'
    }

    try:
        res = requests.get(full_url, headers=payload)
        data = json.loads(res.content.decode('utf-8'))

        link = re.search("https://img.shiftstats.com/dcd7c2ef-0bf7-4a7e-a22f-e1e1a76f936c/person-photo_url(.*?).png", str(data['content'])).group(0)

    except:
        link = np.nan
    
    return link

def helper_phf_team_box(tables, game_id):

    n = len(tables)
    df = pd.read_html(str(tables[n - 1]))[0]
    shot = pd.read_html(str(tables[n - 2]))[0]
    score = pd.read_html(str(tables[n - 3]))[0]

    if len(score.columns) == 3:
        score.columns = START_NAMES
        score['period_2_scoring'] = np.nan
        score['period_3_scoring'] = np.nan
        score['overtime_scoring'] = np.nan
        score['shootout_made_scoring'] = np.nan
        score['shootout_missed_scoring'] = np.nan
        score = score[SHOOTOUT_NAMES]

        shot.columns = [x.replace('_scoring', '_shots') for x in START_NAMES]
        shot['period_2_shots'] = np.nan
        shot['overtime_shots'] = np.nan
        shot['shootout_made_shots'] = np.nan
        shot['shootout_missed_shots'] = np.nan
        shot = shot[SHOOTOUT_SHOT_INIT_NAMES]
        shot = shot[SHOOTOUT_SHOT_NAMES]
    elif len(score.columns) == 4:
        score.columns = IN_PROG_NAMES
        score['period_3_scoring'] = np.nan
        score['overtime_scoring'] = np.nan
        score['shootout_made_scoring'] = np.nan
        score['shootout_missed_scoring'] = np.nan
        score = score[SHOOTOUT_NAMES]

        shot.columns = [x.replace('_scoring', '_shots') for x in IN_PROG_NAMES]
        shot['period_3_shots'] = np.nan
        shot['overtime_shots'] = np.nan
        shot['shootout_made_shots'] = np.nan
        shot['shootout_missed_shots'] = np.nan
        shot = shot[SHOOTOUT_SHOT_INIT_NAMES]
        shot = shot[SHOOTOUT_SHOT_NAMES]
    elif len(score.columns) == 5:
        score.columns = REG_NAMES
        score['overtime_scoring'] = np.nan
        score['shootout_made_scoring'] = np.nan
        score['shootout_missed_scoring'] = np.nan
        score[SHOOTOUT_NAMES]

        shot.columns = [x.replace('_scoring', '_shots') for x in REG_NAMES]
        shot['overtime_shots'] = np.nan
        shot['shootout_made_shots'] = np.nan
        shot['shootout_missed_shots'] = np.nan
        shot = shot[SHOOTOUT_SHOT_INIT_NAMES]
        shot = shot[SHOOTOUT_SHOT_NAMES]
    elif len(score.columns) == 6:
        score.columns = OT_ONLY_NAMES
        score['shootout_made_scoring'] = np.nan
        score['shootout_missed_scoring'] = np.nan
        score = score[SHOOTOUT_NAMES]

        shot.columns = [x.replace('_scoring', '_shots') for x in OT_ONLY_NAMES]
        shot['shootout_made_shots'] = np.nan
        shot['shootout_missed_shots'] = np.nan
        shot = shot[SHOOTOUT_SHOT_INIT_NAMES]
        shot = shot[SHOOTOUT_SHOT_NAMES]
    elif len(score.columns) == 7:
        score[['emp', 'shootout_score', 'shootout_rec']] = score.SO.str.split('', expand=True, n=2)
        score['shootout_rec'] = score.shootout_rec.str.replace('(', '')
        score['shootout_rec'] = score.shootout_rec.str.replace(')', '')
        score[['shootout_made', 'shootout_missed']] = score.shootout_rec.str.split(' - ', expand=True)
        score = score.drop(columns=['emp'])

        score = score[['Scoring', '1st', '2nd', '3rd', 'OT', 'shootout_made', 'shootout_missed', 'T']]
        score.columns = SHOOTOUT_NAMES

        shot.columns = [x.replace('_scoring', '_shots') for x in OT_ONLY_NAMES]
        shot['shootout_made_shots'] = np.nan
        shot['shootout_missed_shots'] = np.nan
        shot = shot[SHOOTOUT_SHOT_INIT_NAMES]
        shot = shot[SHOOTOUT_SHOT_NAMES]
        
    # TM_COLS = df.drop(columns=['Team Stats']).columns.tolist()
    df = df.T
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index()

    df.columns = ['team', 'power_plays', 'power_play_pct', 'penalty_minutes',
                  'faceoff_win_pct', 'blocks', 'takeaways', 'giveaways']

    df[['successful_power_plays', 'power_play_opportunities']] = df.power_plays.str.split(expand=True, pat=' / ')

    df['game_id'] = game_id

    df = df[[
        'team',
        'game_id',
        'successful_power_plays',
        'power_play_opportunities',
        'power_plays',
        'penalty_minutes',
        'faceoff_win_pct',
        'blocks',
        'takeaways',
        'giveaways'
    ]].merge(shot, how='left', on='team').merge(score, how='left', on='team')

    df['winner'] = np.where(df.total_scoring == df.total_scoring.max(), True, False)

    # df['league'] = 'PHF'
    # df['league_id'] = 100

    df = df[['team', 'game_id', 'winner', 'successful_power_plays', 'power_play_opportunities',
       'power_plays', 'penalty_minutes', 'faceoff_win_pct', 'blocks',
       'takeaways', 'giveaways', 'period_1_shots', 'period_2_shots',
       'period_3_shots', 'overtime_shots', 'shootout_made_shots',
       'shootout_missed_shots', 'total_shots', 'period_1_scoring',
       'period_2_scoring', 'period_3_scoring',
       'overtime_scoring', 'shootout_made_scoring', 'shootout_missed_scoring', 'total_scoring']]

    return df