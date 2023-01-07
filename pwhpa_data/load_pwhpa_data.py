import pandas as pd

from load_data import load_data

load_data(pd.read_csv('pwhpa_data/pwhpa_standings.csv'), table_name='pwhpa_standings')

load_data(pd.read_csv('pwhpa_data/pwhpa_schedule.csv'), table_name='pwhpa_schedule')

load_data(pd.read_csv('pwhpa_data/pwhpa_rosters.csv'), table_name='pwhpa_roster')

load_data(pd.read_csv('pwhpa_data/pwhpa_skaters.csv'), table_name='pwhpa_skaters')

load_data(pd.read_csv('pwhpa_data/pwhpa_goalies.csv'), table_name='pwhpa_goalies')

load_data(pd.read_csv('pwhpa_data/pwhpa_game_box.csv'), table_name='pwhpa_scores')

load_data(pd.read_csv('pwhpa_data/pwhpa_game_skaters.csv'), table_name='pwhpa_game_skaters')

load_data(pd.read_csv('pwhpa_data/pwhpa_game_goalies.csv'), table_name='pwhpa_game_goalies')