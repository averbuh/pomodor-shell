import sqlite3

from sqlite3 import Error
from var import dir_path
from .create_connection import create_connection as cc
from .create_activity import copy_activity as ca
from .delete_activity import delete_activity as da
from .create_activity import get_value


database = dir_path+"tomato_data.db"


def update_data_sql(conn, what, value):
    
    sql = ''' UPDATE activities
                 SET '''+what+''' = ?
                WHERE name LIKE ? OR status LIKE ?
                ''' 


    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()

def update_data(key,value,name):
    
    # create a database connection
    conn = cc(database)
    with conn:
        values = (value, '%'+name+'%', '%'+name+'%') 
        update_data_sql(conn, key, values)
    if key == 'status' and value == 'completed':
        update_data('completed_time',str(get_value('stop_time','completed')[0][0]), str(get_value('name','completed')[0][0])) 
        ca(value)
        da(value)
   

def update_status(value,name):
    update_data('status',value,name) 


def update_name(value,name):
    update_data('name',value,name)


def update_time(value,name):
    update_data('stop_time',value,name)

def update_plan(value,name):
    update_data('planning_time',value,name)

if __name__ == '__main__':
    update_name('Create documentation for hebrew', 'hebrew') 
