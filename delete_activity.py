import sqlite3

from settings import dir_path
from create_connection import create_connection as cc


def delete_activity_sql(conn, activity):
    """
    Delete activity from the activities table.
    :param conn:
    :param activity:
    :return: project id
    """
    sql = ''' DELETE FROM activities
              WHERE name OR status LIKE ?
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
        activity = ('%'+name+'%',);
        delete_activity_sql(conn, activity)


if __name__ == '__main__':
    delete_activity('alex')
