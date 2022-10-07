import sqlite3

import sys
from settings import dir_path
from create_connection import create_connection as cc


database = dir_path+"tomato_data.db"


def create_activity_sql(conn, activity):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO activities(name,status,planning_time)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, activity)
    conn.commit()
    return cur.lastrowid


def create_activity(name, status, planning_time):

    # create a database connection
    conn = cc(database)
    with conn:
        # create a new project
        activity = (name, status, planning_time,);
        create_activity_sql(conn, activity)


def return_for_file():
    sql = ''' SELECT * FROM activities '''
    
    conn = cc(database)
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        rows = cur.fetchall()
    return rows 
    
def get_value(what, status):
    conn=cc(database)
    sql = ''' SELECT '''+what+''' FROM activities
              WHERE status="'''+status+'''" 
              '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql) 
        conn.commit()
        rows = cur.fetchall()
    return rows

def copy_activity(status):
    conn=cc(database)

    sql = ''' INSERT INTO archive SELECT * FROM activities
                WHERE id NOT IN (SELECT id FROM archive) AND status="'''+status+'''"
    '''

    with conn:
        cur = conn.cursor()
        cur.execute(sql) 
        conn.commit()
    


def return_activities(printing = True):
    
    sql = ''' SELECT * FROM activities '''
    
    conn = cc(database)
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        rows = cur.fetchall()
        if printing:
            print('\n\x1b[1;36m \tText | Status | Plan | Process | Completed \x1b[0;0m\n')
        count = 1 
        for row in rows:
            if printing:
                sys.stdout.write('\t   '+str(count) + ':\x1b[1;33m '+row[1]+'\x1b[0;0m | ')
            for word in row[2:6]:
                if printing:
                    sys.stdout.write(str(word) + ' | ')
            count+=1
            if printing:
                print('\n') 
    return count+5 


if __name__ == '__main__':
    get_value()
