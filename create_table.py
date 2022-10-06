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
                                        planning_time text,
                                        stop_time text,
                                        completed_time text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn=cc(database)
    # create tables
    if conn is not None:
        create_table(conn, sql_create_activities_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
