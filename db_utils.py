import sqlite3
from sqlite3 import Error


class SQLite:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_db_tables()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
        connection = self.create_connection()
        cursor = connection.cursor()
        if connection is not None:
            try:
                cursor.execute(query, *args)
                connection.commit()
                if fetch_option == "fetchone":
                    return cursor.fetchone()
                elif fetch_option == "fetchall":
                    return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")

    def create_year_table(self):
        query = """ CREATE TABLE IF NOT EXISTS years(
                        year_id INTEGER PRIMARY KEY,
                        year INTEGER NOT NULL
                        ); """
        self.execute_sql_query(query)

    def create_month_table(self):
        query = """ CREATE TABLE IF NOT EXISTS months(
                        month_id INTEGER PRIMARY KEY,
                        month INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        FOREIGN KEY (year) REFERENCES years (year_id) ON DELETE PROTECT
                        ); """
        self.execute_sql_query(query)

    def create_day_details_table(self):
        query = """ CREATE TABLE IF NOT EXISTS days(
                        day_id INTEGER PRIMARY KEY,
                        month INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        months_day INTEGER NOT NULL,
                        start_hour TEXT NOT NULL,
                        end_hour TEXT NOT NULL,
                        work_hours TEXT NOT NULL,
                        kilometers INTEGER NOT NULL,
                        liters_refueled INTEGER NOT NULL,
                        fuel_consumption_by_standard INTEGER NOT NULL,
                        status_of_fuel_standard INTEGER NOT NULL,                       
                        FOREIGN KEY (month) REFERENCES months (month_id) ON DELETE PROTECT,
                        FOREIGN KEY (year) REFERENCES years (year_id) ON DELETE PROTECT
                        ); """
        self.execute_sql_query(query)

    def create_db_tables(self):
        self.create_year_table()
        self.create_month_table()
        self.create_day_details_table()
