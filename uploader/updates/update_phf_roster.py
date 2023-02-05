import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_team_rosters import phf_roster

def update_phf_roster(season: int):

    teams = get_query(query=f"""select *
                                from phf_standings ps 
                                where true 
                                    and season = {season};""")

    roster_df = pd.DataFrame()

    for team in teams.team_name.tolist():
        roster_df = pd.concat([roster_df, phf_roster(team=team, season=season)[0]])

    execute_command(query="""DELETE FROM phf_roster WHERE season = 2023;""")
    load_data(df=roster_df, table_name='phf_roster')