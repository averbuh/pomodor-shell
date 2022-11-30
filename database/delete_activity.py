import sqlite3

from settings import dir_path
from .create_connection import create_connection as cc


def delete_activity_sql(conn, activity, table):
    """
    Delete activity from the activities table.
    :param conn:
    :param activity:
    :return: project id
    """
    sql = ''' DELETE FROM '''+table+'''
              WHERE name LIKE ? OR status LIKE ?
              '''
    cur = conn.cursor()
    cur.execute(sql, activity)
    conn.commit()
    return cur.lastrowid


def delete_activity(name):
    database = dir_path+"tomato_data.db"

    # create a database connection
    conn = cc(database)
    with conn:
        # create a new project
        activity = ('%'+name+'%', '%'+name+'%');
        delete_activity_sql(conn, activity, 'activities')


def delete_completed_activity(name):
    database = dir_path+"tomato_data.db"

    # create a database connection
    conn = cc(database)
    with conn:
        # create a new project
        activity = ('%'+name+'%', '%'+name+'%');
        delete_activity_sql(conn, activity, 'archive')



if __name__ == '__main__':
    delete_activity('alex')
