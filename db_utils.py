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

    def create_daily_summary_table(self):
        query = """CREATE TABLE IF NOT EXISTS daily_summaries(
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

    def create_monthly_summary_table(self):
        query = """CREATE TABLE IF NOT EXISTS monthly_summaries(
                    month_ID INTEGER PRIMARY KEY,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    working_days INTEGER NOT NULL DEFAULT 0,
                    total_hours VARCHAR NOT NULL DEFAULT '0',
                    average_hours_per_day VARCHAR NOT NULL DEFAULT '0',
                    kilometers INTEGER NOT NULL DEFAULT 0,
                    refuels INTEGER NOT NULL DEFAULT 0,
                    fuel_standard REAL NOT NULL DEFAULT 0,
                    difference INTEGER NOT NULL DEFAULT 0,
                    salary REAL NOT NULL DEFAULT 0,                   
                    FOREIGN KEY (month, year) REFERENCES daily_summaries (month, year) ON DELETE CASCADE
                    );"""
        self.execute_sql_query(query)

    def create_yearly_summary_table(self):
        query = """CREATE TABLE IF NOT EXISTS yearly_summaries(
                    year_ID INTEGER PRIMARY KEY,
                    year INTEGER NOT NULL,
                    working_days INTEGER NOT NULL DEFAULT 0,
                    total_hours VARCHAR NOT NULL DEFAULT '0',
                    average_hours_per_day VARCHAR NOT NULL DEFAULT '0',
                    kilometers INTEGER NOT NULL DEFAULT 0,
                    refuels INTEGER NOT NULL DEFAULT 0,
                    fuel_standard REAL NOT NULL DEFAULT 0,
                    salary INTEGER NOT NULL DEFAULT 0,
                    average_salary_per_month INTEGER NOT NULL DEFAULT '0',
                    FOREIGN KEY (year) REFERENCES monthly_summaries (year) ON DELETE CASCADE
                    );"""
        self.execute_sql_query(query)

    def create_tables(self):
        self.create_daily_summary_table()
        self.create_monthly_summary_table()
        self.create_yearly_summary_table()

    def add_daily_summary(self, day, month, year, start, end, hours, kilometers, refuel,
                          standard_fuel_usage, fuel_difference):
        query = "INSERT INTO daily_summaries (day, month, year, start, end, hours, " \
                "kilometers, refuel, standard_fuel_usage, fuel_difference) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.execute_sql_query(query, (day, month, year, start, end, hours, kilometers, refuel,
                                       standard_fuel_usage, fuel_difference))

    def check_that_monthly_summary_exist(self, month, year):
        check_query = "SELECT * FROM monthly_summaries WHERE month = ? AND year = ?"
        existing_summary = self.execute_sql_query(check_query, (month, year), fetch_option = "fetchone")
        if existing_summary:
            return True
        else:
            return False

    def add_monthly_summary(self, month, year):
        insert_query = "INSERT INTO monthly_summaries (month, year) VALUES (?, ?)"
        self.execute_sql_query(insert_query, (month, year))

    def show_daily_summaries_per_month(self, month, year):
        query = "SELECT * FROM daily_summaries WHERE month = ? AND year = ? ORDER BY day"
        result = self.execute_sql_query(query, (month, year), fetch_option = "fetchall")
        return result

    def update_monthly_summary(self, month, year, working_days, total_hours, average_hours_per_day, kilometers,
                               refuels, fuel_standard, difference, salary):
        query = "UPDATE monthly_summaries SET working_days = ?, total_hours = ?, average_hours_per_day = ?, " \
                "kilometers = ?, refuels = ?, fuel_standard = ?, difference = ?, salary = ? WHERE month = ? AND year = ?"
        self.execute_sql_query(query, (working_days, total_hours, average_hours_per_day, kilometers, refuels, fuel_standard,
                                       difference, salary, month, year))

    def show_monthly_summary(self, month, year):
        query = "SELECT * FROM monthly_summaries WHERE month = ? AND year = ?"
        monthly_summary = self.execute_sql_query(query, (month, year), fetch_option = "fetchone")
        return monthly_summary

