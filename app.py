from datetime import datetime
from db_utils import SQLite
from config_variables import db_file, month, year


class App:
    def __init__(self):
        self.db = SQLite(db_file)
        self.is_running = False
        self.commands = {
            "1": "Add new day details",
            "2": "Show all days",
            "3": "Stop app"
        }

    def read_dict(self, dict):
        print("--------")
        for key, value in dict.items():
            print(f"{key}: {value}")
        print("--------")

    def days_table_template(self, days_details):
        print("--------")
        print("DATE:\t\tSTART HOUR:\t\tEND HOUR:\t\tTOTAL HOURS:\t\tKILOMETERS:\t\tREFUEL:\t\tFUELS STANDARD:\t\tDIFFERENCE:")
        for date in days_details:
            print(f"{date[1]}-{date[2]}-{date[3]}\t{date[4]}\t\t\t{date[5]}\t\t\t{date[6]}\t\t\t\t{date[7]}\t\t\t\t{date[8]}\t\t\t{date[9]}\t\t\t\t\t{date[10]}")

    def add_new_detail(self):
        try:
            day = int(input("DAY (number): "))
            start = input("START HOUR (H:M format): ")
            end = input("END HOUR (H:M format): ")
            hours = self.calculate_hours(start, end)
            kilometers = int(input("KILOMETERS: "))
            refuel = int(input("REFUEL: "))
            standard_fuel_usage = self.calculate_standard_fuel_usage(kilometers)
            fuel_difference = self.calculate_fuel_difference(refuel, standard_fuel_usage)
            self.db.add_day_detail(day, month, year, start, end, hours, kilometers, refuel, standard_fuel_usage, fuel_difference)
        except Exception as e:
            print(e)

    def show_all_days_details(self):
        days_details = self.db.show_all_days()
        return self.days_table_template(days_details)

    def calculate_hours(self, start_hour_string, end_hour_string):
        hours_format = "%H:%M"
        start_hour = datetime.strptime(start_hour_string, hours_format)
        end_hour = datetime.strptime(end_hour_string, hours_format)
        difference = end_hour - start_hour
        return str(difference)

    def calculate_standard_fuel_usage(self, kilometers):
        standard_usage = kilometers * 0.25
        return round(standard_usage)

    def calculate_fuel_difference(self, refuel, standard_fuel_usage):
        difference = standard_fuel_usage - refuel
        return difference

    def start(self):
        self.is_running = True
        print("Hello !")
        while self.is_running == True:
            self.read_dict(self.commands)
            try:
                command_input = input("TYPE: ")
                if command_input == "1":
                    self.add_new_detail()
                elif command_input == "2":
                    self.show_all_days_details()
                elif command_input == "3":
                    print("Bye !")
                    self.is_running = False
                else:
                    print("Unknown command")
            except Exception as e:
                print(e)


app = App()
app.start()
