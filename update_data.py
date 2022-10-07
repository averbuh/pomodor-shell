import sqlite3

from sqlite3 import Error
from settings import dir_path
from create_connection import create_connection as cc


def update_data_sql(conn, what, value):
    
    sql = ''' UPDATE activities
                 SET '''+what+''' = ?
                WHERE name LIKE ? OR status LIKE ?
                ''' 


    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()

def update_data(key,value,name):

    database = dir_path+"tomato_data.db"
    # create a database connection
    conn = cc(database)
    with conn:
        values = (value, '%'+name+'%', '%'+name+'%') 
        update_data_sql(conn, key, values)


if __name__ == '__main__':
    update_data('completed_time', '5:11', '2') 
