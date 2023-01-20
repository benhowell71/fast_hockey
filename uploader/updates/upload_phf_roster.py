import pandas as pd
import numpy as np

from tqdm import tqdm

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command

from phf.phf_team_rosters import phf_roster

def update_phf_roster():
    phf_roster(team='Boston Pride', season=2023)