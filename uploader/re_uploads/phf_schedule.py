import pandas as pd
import numpy as np

from tqdm import tqdm

from database.load_data import load_data
from database.get_query import get_query
from phf.phf_schedule import phf_schedule

def reset_phf_schedule():
    try:
        get_query("DELETE FROM phf_schedule;")
    except TypeError:
        print('Table: phf_schedule has been deleted;')

    lg = pd.DataFrame()

    for i in tqdm(np.arange(2016, 2023 + 1)):
        schedule = phf_schedule(season=i)
        lg = pd.concat([lg, schedule])

    load_data(df=lg, table_name='phf_schedule')
