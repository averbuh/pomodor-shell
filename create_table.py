import sqlite3
from sqlite3 import Error
from settings import dir_path
from create_connection import create_connection as cc


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():

    database=dir_path+"tomato_data.db"

    sql_create_activities_table = """ CREATE TABLE IF NOT EXISTS activities (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL,
                                        status text NOT NULL,
                                        planning_time text DEFAULT 0,
                                        stop_time text DEFAULT '0:0',
                                        completed_time text DEFAULT 0
                                    ); """

    sql_create_archive_table = """CREATE TABLE IF NOT EXISTS archive (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    status text NOT NULL,
                                    planning_time text DEFAULT 0,
                                    stop_time text DEFAULT '0:0',
                                    completed_time text DEFAULT 0
                                );"""

    # create a database connection
    conn=cc(database)
    # create tables
    if conn is not None:
        create_table(conn, sql_create_activities_table)
        create_table(conn, sql_create_archive_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
