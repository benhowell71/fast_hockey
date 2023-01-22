import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_team_box import phf_team_box

def update_phf_game_box(game_ids: list):

    games = pd.DataFrame()

    for i in tqdm(game_ids):
        games = pd.concat([games, phf_team_box(game_id=i)])

    load_data(df=games, table_name='phf_games')

    