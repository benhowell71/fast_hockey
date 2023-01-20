import pandas as pd
import numpy as np

from database.get_query import get_query
from database.load_data import load_data
from database.execute_command import execute_command
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
            # next
            continue
        elif uploaded_status != new_status:
            ids_to_update.append(str(id))

    game_ids = ', '.join(ids_to_update)
    execute_command(query=f"DELETE FROM phf_schedule WHERE TRUE and game_id in ({game_ids});")

    # np.issubdtype(ids_to_update., int)
    ids_to_update = [int(x) for x in ids_to_update]
    data_to_upload = phf[phf.game_id.isin(ids_to_update)]
    load_data(df=data_to_upload, table_name='phf_schedule')

    return ids_to_update
