import pandas as pd
import numpy as np

from tqdm import tqdm

from database.load_data import load_data
from database.get_query import get_query
from database.execute_command import execute_command

from phf.phf_schedule import phf_schedule
from phf.phf_standings import phf_standings

def reset_phf_schedule():
    try:
        execute_command("DELETE FROM phf_schedule;")
        execute_command("DELETE FROM phf_standings;")
    except TypeError:
        print('Table: phf_schedule has been deleted;')

    lg = pd.DataFrame()
    stand = pd.DataFrame()

    for i in tqdm(np.arange(2016, 2023 + 1)):
        schedule = phf_schedule(season=i)
        current_stand = phf_standings(season=i)
        stand = pd.concat([stand, current_stand])
        lg = pd.concat([lg, schedule])

    load_data(df=lg, table_name='phf_schedule')
    load_data(df=stand, table_name='phf_standings')
