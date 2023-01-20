import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_team_rosters import phf_roster

def reset_phf_rosters():
    try:
        execute_command("DELETE FROM phf_roster;")
    except:
        print('Table: phf_roster failed to be deleted.')

    teams = get_query("SELECT team_name, season FROM phf_standings;")
    rosters = pd.DataFrame()

    for index, row in tqdm(teams.iterrows()):

        roster_info = phf_roster(team=row['team_name'], season=row['season'])
        rosters = pd.concat([rosters, roster_info[0]])

    load_data(df=rosters, table_name='phf_roster')