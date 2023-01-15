import pandas as pd
import numpy as np

from database.get_query import get_query
from database.load_data import load_data
from phf.phf_schedule import phf_schedule

def update_phf_schedule(season: int) -> list:
    db_schedule = get_query(f"SELECT game_id, status FROM phf_schedule WHERE TRUE and season = {season};")
    phf = phf_schedule(season=season)

    uploaded_ids = db_schedule.game_id

    ids_to_update = []

    for id in uploaded_ids:
        uploaded_status = db_schedule[db_schedule.game_id == id].status.item()
        new_status = phf[phf.game_id == id].status.item()

        if uploaded_status == new_status:
            next
        elif uploaded_status != new_status:
            ids_to_update.append(str(id))

    game_ids = ', '.join(ids_to_update)
    get_query(f"DELETE FROM phf_schedule WHERE TRUE and game_id in ({game_ids});")
    data_to_upload = phf[phf.game_id.isin(ids_to_update)]
    load_data(df=data_to_upload, table_name='phf_schedule')

    return ids_to_update
