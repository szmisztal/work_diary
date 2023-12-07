import sqlite3
from sqlite3 import Error


class SQLite:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
        connection = self.create_connection()
        if connection is not None:
            with connection:
                cursor = connection.cursor()
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
        else:
            print("Cannot create the database connection.")

    def create_day_detail_table(self):
        query = """CREATE TABLE IF NOT EXISTS day_details(
                    date_id INTEGER PRIMARY KEY,
                    day INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    start VARCHAR NOT NULL,
                    end VARCHAR NOT NULL,
                    hours VARCHAR NOT NULL,
                    kilometers INTEGER NOT NULL,
                    refuel INTEGER NOT NULL,
                    standard_fuel_usage INTEGER NOT NULL,
                    fuel_difference INTEGER NOT NULL
                    );"""
        self.execute_sql_query(query)

    # def create_salary_table(self):
    #     query = """CREATE TABLE IF NOT EXISTS salaries(
    #                 salary_id INTEGER PRIMARY KEY,
    #                 month INTEGER NOT NULL,
    #                 year INTEGER NOT NULL,
    #                 amount REAL NOT NULL,
    #                 FOREIGN KEY (month) REFERENCES dates (month),
    #                 FOREIGN KEY (year) REFERENCES dates (year)
    #                 );"""
    #     self.execute_sql_query(query)

    def create_tables(self):
        self.create_day_detail_table()
        # self.create_salary_table()

    def add_day_detail(self, day, month, year, start, end, hours, kilometers, refuel,
                       standard_fuel_usage, fuel_difference):
        query = "INSERT INTO day_details (day, month, year, start, end, hours, " \
                "kilometers, refuel, standard_fuel_usage, fuel_difference) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.execute_sql_query(query, (day, month, year, start, end, hours, kilometers, refuel,
                                       standard_fuel_usage, fuel_difference))

    def show_all_days(self):
        query = "SELECT * FROM day_details ORDER BY day, month, year"
        result = self.execute_sql_query(query, fetch_option = "fetchall")
        return result

