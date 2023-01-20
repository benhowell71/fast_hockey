import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_player_box import phf_player_box
from phf.calculate_game_score import calculate_game_score

def update_phf_box(game_ids: list):

    skaters = pd.DataFrame()
    goalies = pd.DataFrame()

    for i in tqdm(game_ids):
        game_box = phf_player_box(game_id=i)
        skaters = pd.concat([skaters, game_box[0]])
        goalies = pd.concat([goalies, game_box[1]])

    skaters = calculate_game_score(skaters_df=skaters)

    load_data(df=skaters, table_name='phf_game_skaters')
    load_data(df=goalies, table_name='phf_game_goalies')