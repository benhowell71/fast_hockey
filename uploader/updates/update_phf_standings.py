import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_standings import phf_standings

def update_phf_standings(season):
    standings = phf_standings(season=season)

    execute_command(query="DELETE FROM phf_standings;")

    load_data(df=standings, table_name='phf_standings')