from db_utils import SQLite
from calculate_functions import calculate_salary, calculate_hours, calculate_total_hours, \
    calculate_average_hours, calculate_fuel_difference, calculate_standard_fuel_usage, calculate_total_hours_for_yearly_summary, \
    calculate_average_hours_for_yearly_summary
from config_variables import db_file, hourly_rate, daily_rate, old_hourly_rate, old_daily_rate


class App:
    def __init__(self):
        self.db = SQLite(db_file)
        self.is_running = False
        self.commands = {
            "1": "Add new daily summary",
            "2": "Show monthly summary by days",
            "3": "Show yearly summary by months",
            "4": "Show yearly summaries",
            "5": "Add new invoice (with VAT)",
            "6": "Show invoices (with VAT)",
            "7": "Stop app"
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
        for data in month_details:
            formatted_month = data[1]
            formatted_year = data[2]
            formatted_working_days = data[3]
            formatted_total_hours = data[4]
            formatted_average_hours = data[5]
            formatted_kilometers = data[6]
            formatted_refuel = data[7]
            formatted_fuels_standard = data[8]
            formatted_difference = data[9]
            formatted_salary = data[10]
            print("{:<8} {:<7} {:<15} {:<14} {:<24} {:<13} {:<9} {:<17} {:<13} {:<10}".format(
                formatted_month, formatted_year, formatted_working_days, formatted_total_hours, formatted_average_hours,
                formatted_kilometers, formatted_refuel, formatted_fuels_standard, formatted_difference, formatted_salary
                ))

    def year_table_template(self, year_details):
        print("--------")
        print("{:<7} {:<15} {:<14} {:<26} {:<13} {:<9} {:<17} {:<9} {:<10}".format(
            "YEAR:", "WORKING DAYS:", "TOTAL HOURS:", "AVERAGE HOURS PER MONTH:", "KILOMETERS:", "REFUEL:",
            "FUELS STANDARD:", "SALARY:", "AVERAGE SALARY PER MONTH:"
        ))
        for data in year_details:
            formatted_year = data[1]
            formatted_working_days = data[2]
            formatted_total_hours = data[3]
            formatted_average_hours = data[4]
            formatted_kilometers = data[5]
            formatted_refuel = data[6]
            formatted_fuels_standard = data[7]
            formatted_salary = data[8]
            formatted_average_salary = data[9]
            print("{:<7} {:<15} {:<14} {:<26} {:<13} {:<9} {:<17} {:<9} {:<10}".format(
                formatted_year, formatted_working_days, formatted_total_hours, formatted_average_hours,
                formatted_kilometers, formatted_refuel, formatted_fuels_standard, formatted_salary, formatted_average_salary
                ))

    def check_that_summaries_exists(self, month, year):
        check_that_monthly_summary_exist = self.db.check_that_monthly_summary_exist(month, year)
        if check_that_monthly_summary_exist == False:
            self.db.add_monthly_summary(month, year)
        check_that_yearly_summary_exist = self.db.check_that_yearly_summary_exist(year)
        if check_that_yearly_summary_exist == False:
            self.db.add_yearly_summary(year)

    def add_new_daily_summary(self):
        try:
            day = int(input("DAY: "))
            month = int(input("MONTH: "))
            year = int(input("YEAR: "))
            self.check_that_summaries_exists(month, year)
            start = input("START HOUR (H:M format): ")
            end = input("END HOUR (H:M format): ")
            hours = calculate_hours(start, end)
            kilometers = int(input("KILOMETERS: "))
            refuel = int(input("REFUEL: "))
            standard_fuel_usage = calculate_standard_fuel_usage(kilometers)
            fuel_difference = calculate_fuel_difference(refuel, standard_fuel_usage)
            self.db.add_daily_summary(day, month, year, start, end, hours, kilometers, refuel, standard_fuel_usage, fuel_difference)
        except Exception as e:
            print(e)

    def update_monthly_summary(self, months, year):
        try:
            for month in months:
                daily_summaries = self.db.show_daily_summaries_per_month(month[1], year)
                working_days = len(daily_summaries)
                total_hours = calculate_total_hours(daily_summaries, 6)
                average_hours_per_day = calculate_average_hours(daily_summaries, 6)
                kilometers = sum([i[7] for i in daily_summaries])
                refuels = sum([i[8] for i in daily_summaries])
                fuel_standard = round(refuels * 100 / kilometers, 2)
                difference = sum([i[10] for i in daily_summaries])
                if year <= 2023 and month[1] <= 2:
                    salary = calculate_salary(old_daily_rate, working_days, old_hourly_rate, total_hours)
                elif year >= 2023 and month[1] > 2:
                    salary = calculate_salary(daily_rate, working_days, hourly_rate, total_hours)
                if working_days > 20:
                    bonus = working_days - 20
                    salary += bonus * 100
                self.db.update_monthly_summaries(month[1], year, working_days, str(total_hours), average_hours_per_day,
                                                 kilometers, refuels, fuel_standard, difference, salary)
        except Exception as e:
            print(e)

    def update_yearly_summary(self, years):
        try:
            for year in years:
                months = self.db.get_months_for_update(year[1])
                self.update_monthly_summary(months, year[1])
                monthly_summaries = self.db.show_monthly_summary(year[1])
                working_days = sum([i[3] for i in monthly_summaries])
                total_hours = calculate_total_hours_for_yearly_summary(monthly_summaries, 4)
                average_hours_per_month = calculate_average_hours_for_yearly_summary(monthly_summaries, 4)
                kilometers = sum([i[6] for i in monthly_summaries])
                refuels = sum([i[7] for i in monthly_summaries])
                fuel_standard = round(refuels * 100 / kilometers, 2)
                salary = sum([i[10] for i in monthly_summaries])
                average_salary_per_month = round(salary / len(monthly_summaries), 2)
                self.db.update_yearly_summaries(year[1], working_days, str(total_hours), average_hours_per_month, kilometers,
                                                refuels, fuel_standard, salary, average_salary_per_month)
        except Exception as e:
            print(e)

    def show_daily_summaries_per_month(self):
        try:
            month = int(input("MONTH (number): "))
            year = int(input("YEAR (number): "))
            days_summaries = self.db.show_daily_summaries_per_month(month, year)
            return self.days_table_template(days_summaries)
        except Exception as e:
            print(e)

    def show_monthly_summaries_per_year(self):
        try:
            year = int(input("YEAR (number): "))
            months = self.db.get_months_for_update(year)
            self.update_monthly_summary(months, year)
            monthly_summaries = self.db.show_monthly_summary(year)
            return self.month_table_template(monthly_summaries)
        except Exception as e:
            print(e)

    def show_yearly_summaries(self):
        try:
            years = self.db.get_years_for_update()
            self.update_yearly_summary(years)
            yearly_summaries = self.db.show_yearly_summary()
            return self.year_table_template(yearly_summaries)
        except Exception as e:
            print(e)

    def add_new_invoice(self):
        try:
            month = int(input("MONTH: "))
            year = int(input("YEAR: "))
            value = float(input("VALUE: "))
            self.db.add_invoice(month, year, value)
        except Exception as e:
            print(e)

    def show_invoices(self):
        try:
            year = int(input("YEAR (if you want to see all invoices, tap '0'): "))
            if isinstance(year, int):
                invoices = self.db.get_invoices(year)
            elif year == 0:
                invoices = self.db.get_invoices()
            print("--------")
            invoice_sum = []
            for invoice in invoices:
                print(f"{invoice[1]}.{invoice[2]} --- VALUE: {invoice[3]}")
                invoice_sum.append(invoice[3])
            print("--------")
            print(f"SUM: {round(sum(invoice_sum), 2)}")
        except Exception as e:
            print(e)

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
                    self.show_daily_summaries_per_month()
                elif command_input == "3":
                    self.show_monthly_summaries_per_year()
                elif command_input == "4":
                    self.show_yearly_summaries()
                elif command_input == "5":
                    self.add_new_invoice()
                elif command_input == "6":
                    self.show_invoices()
                elif command_input == "7":
                    print("Bye !")
                    self.is_running = False
                else:
                    print("Unknown command")
            except Exception as e:
                print(e)


app = App()
app.start()
