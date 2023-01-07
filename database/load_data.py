"""SQL Database Loading Function"""

import pandas as pd

from sqlalchemy import (
    create_engine
)

from creds.database import SQL_ENGINE

def load_data(df: pd.DataFrame, table_name = str):

    db_con = create_engine(SQL_ENGINE)
    
    conn = db_con.connect()

    df.to_sql(con=conn, name=table_name, if_exists='append', index=False)

    conn.close()