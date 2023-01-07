"""SQL Database Query functions"""

import mysql.connector
# import MySQLdb
import pandas as pd

from creds.database import PROD_SQL_CREDS

def get_query(query, db="prod", as_dict=False, as_df=True):
    """Common method to connect to db and get data"""
    # connect to db
    if db == "prod":
        connection = mysql.connector.connect(**PROD_SQL_CREDS)
    
    if as_df:
        data = pd.read_sql(query, connection)
    else:
        cursor = connection.cursor(buffered=True, dictionary=as_dict)
        cursor.execute(query)
        data = [x for x in cursor]
        cursor.close()

    # close connection
    connection.close()
    return data