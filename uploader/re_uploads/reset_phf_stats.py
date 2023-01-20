import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_team_stats import phf_team_stats

def reset_phf_team_stats():
    try:
        execute_command("DELETE FROM skater_stats;")
        execute_command("DELETE FROM goalie_stats;")
    except:
        print('Tables not deleted.')

    teams = get_query("SELECT team_name, season FROM phf_standings;")
    skaters = pd.DataFrame()
    goalies = pd.DataFrame()

    for index, row in tqdm(teams.iterrows()):
        # print(row)
        stats = phf_team_stats(team=row['team_name'], season=row['season'])
        skaters = pd.concat([skaters, stats[0]])
        goalies = pd.concat([goalies, stats[1]])
    
    load_data(df=skaters, table_name='skater_stats')
    load_data(df=goalies, table_name='goalie_stats')