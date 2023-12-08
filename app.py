from datetime import datetime
from db_utils import SQLite
from config_variables import db_file, month, year, daily_rate, hourly_rate, old_daily_rate, old_hourly_rate


class App:
    def __init__(self):
        self.db = SQLite(db_file)
        self.is_running = False
        self.commands = {
            "1": "Add new daily summary",
            "2": "Show monthly summary by days",
            "3": "Show monthly summary",
            "4": "Stop app"
        }

    def read_dict(self, dict):
        print("--------")
        for key, value in dict.items():
            print(f"{key}: {value}")
        print("--------")

    def days_table_template(self, days_details):
        print("--------")
        print("{:<12} {:<16} {:<16} {:<18} {:<14} {:<9} {:<18} {:<12}".format(
            "DATE:", "START HOUR:", "END HOUR:", "HOURS:", "KILOMETERS:", "REFUEL:", "FUELS STANDARD:", "DIFFERENCE:"
        ))
        for data in days_details:
            formatted_data = f"{data[1]}-{data[2]}-{data[3]}"
            formatted_start_hour = data[4]
            formatted_end_hour = data[5]
            formatted_total_hours = data[6]
            formatted_kilometers = data[7]
            formatted_refuel = data[8]
            formatted_fuels_standard = data[9]
            formatted_difference = data[10]
            print("{:<12} {:<16} {:<16} {:<18} {:<14} {:<9} {:<18} {:<12}".format(
                formatted_data, formatted_start_hour, formatted_end_hour, formatted_total_hours, formatted_kilometers,
                formatted_refuel, formatted_fuels_standard, formatted_difference
            ))

    def month_table_template(self, month_details):
        print("--------")
        print("{:<8} {:<7} {:<15} {:<14} {:<24} {:<13} {:<9} {:<17} {:<13} {:<10}".format(
            "MONTH:", "YEAR:", "WORKING DAYS:", "TOTAL HOURS:", "AVERAGE HOURS PER DAY:", "KILOMETERS:", "REFUEL:",
            "FUELS STANDARD:", "DIFFERENCE:", "SALARY:"
        ))
        formatted_month = month_details[1]
        formatted_year = month_details[2]
        formatted_working_days = month_details[3]
        formatted_total_hours = month_details[4]
        formatted_average_hours = month_details[5]
        formatted_kilometers = month_details[6]
        formatted_refuel = month_details[7]
        formatted_fuels_standard = month_details[8]
        formatted_difference = month_details[9]
        formatted_salary = month_details[10]
        print("{:<8} {:<7} {:<15} {:<14} {:<24} {:<13} {:<9} {:<17} {:<13} {:<10}".format(
            formatted_month, formatted_year, formatted_working_days, formatted_total_hours, formatted_average_hours,
            formatted_kilometers, formatted_refuel, formatted_fuels_standard, formatted_difference, formatted_salary
            ))

    def add_new_daily_summary(self):
        try:
            day = int(input("DAY (number): "))
            start = input("START HOUR (H:M format): ")
            end = input("END HOUR (H:M format): ")
            hours = self.calculate_hours(start, end)
            kilometers = int(input("KILOMETERS: "))
            refuel = int(input("REFUEL: "))
            standard_fuel_usage = self.calculate_standard_fuel_usage(kilometers)
            fuel_difference = self.calculate_fuel_difference(refuel, standard_fuel_usage)
            self.db.add_daily_summary(day, month, year, start, end, hours, kilometers, refuel, standard_fuel_usage, fuel_difference)
        except Exception as e:
            print(e)

    def show_all_daily_summaries_per_month(self):
        try:
            month = int(input("MONTH (number): "))
            year = int(input("YEAR (number): "))
            days_details = self.db.show_daily_summaries_per_month(month, year)
            return self.days_table_template(days_details)
        except Exception as e:
            print(e)

    def show_monthly_summary(self):
        try:
            month = int(input("MONTH (number): "))
            year = int(input("YEAR (number): "))
            check_that_summary_exist = self.db.check_that_monthly_summary_exist(month, year)
            if check_that_summary_exist == False:
                self.db.add_monthly_summary(month, year)
            days_details_list = self.db.show_daily_summaries_per_month(month, year)
            working_days = len(days_details_list)
            total_hours = self.calculate_total_hours(days_details_list)
            average_hours_per_day = self.calculate_average_hours_per_day(days_details_list)
            kilometers = sum([i[7] for i in days_details_list])
            refuels = sum([i[8] for i in days_details_list])
            fuel_standard = round(refuels * 100 / kilometers)
            difference = sum([i[10] for i in days_details_list])
            salary = self.calculate_salary(working_days, total_hours)
            self.db.update_monthly_summary(month, year, working_days, total_hours, average_hours_per_day,
                                           kilometers, refuels, fuel_standard, difference, salary)
            monthly_summary = self.db.show_monthly_summary(month, year)
            return self.month_table_template(monthly_summary)
        except Exception as e:
            print(e)

    def calculate_hours(self, start_hour_string, end_hour_string):
        hours_format = "%H:%M"
        start_hour = datetime.strptime(start_hour_string, hours_format)
        end_hour = datetime.strptime(end_hour_string, hours_format)
        difference = end_hour - start_hour
        return str(difference)

    def calculate_total_hours(self, details_list):
        total_seconds_list = [self.time_to_seconds(i[6]) for i in details_list]
        total_seconds = sum(total_seconds_list)
        total_hours = total_seconds / 3600
        return str(total_hours)

    def calculate_average_hours_per_day(self, details_list):
        days = len(details_list)
        total_seconds_list = [self.time_to_seconds(i[6]) for i in details_list]
        total_seconds = sum(total_seconds_list)
        average_hours_per_day = total_seconds / 3600 / days
        return str(average_hours_per_day)

    def time_to_seconds(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def calculate_standard_fuel_usage(self, kilometers):
        standard_usage = kilometers * 0.25
        return round(standard_usage)

    def calculate_fuel_difference(self, refuel, standard_fuel_usage):
        difference = standard_fuel_usage - refuel
        return difference

    def calculate_salary(self, working_days, total_hours):
        salary = (daily_rate * working_days) + (hourly_rate * total_hours)
        return round(salary, 2)

    def start(self):
        self.is_running = True
        print("Hello !")
        while self.is_running == True:
            self.read_dict(self.commands)
            try:
                command_input = input("TYPE: ")
                if command_input == "1":
                    self.add_new_daily_summary()
                elif command_input == "2":
                    self.show_all_daily_summaries_per_month()
                elif command_input == "3":
                    self.show_monthly_summary()
                elif command_input == "4":
                    print("Bye !")
                    self.is_running = False
                else:
                    print("Unknown command")
            except Exception as e:
                print(e)


app = App()
app.start()
