"""SQL Database Query functions"""

import mysql.connector
# import MySQLdb
import pandas as pd

from creds.database import PROD_SQL_CREDS

def execute_command(query, db="prod"):
    """Common method to connect to db and get data"""
    # connect to db
    if db == "prod":
        connection = mysql.connector.connect(**PROD_SQL_CREDS)
    
    cursor = connection.cursor(buffered=True)
    cursor.execute(query)
    # cursor
    # data = [x for x in cursor]
    cursor.close()
    connection.commit()

    # close connection
    connection.close()
    # return data